"""
test_ejecucion_completa.py
========================
Ensayo de una ejecución entera de ``migrate.main()``, con la base de datos
falseada. Se ejecuta con

    python tests/test_ejecucion_completa.py

``test_pipeline.py`` prueba las piezas por separado; esto prueba el flujo que
se ejecuta de verdad cada semana: qué se genera, qué se deja en paz, qué se
limpia y qué pasa cuando algo falla. Sin BDD ni red: se sustituyen las tres
funciones de lectura y la reparación de enlaces.

Requiere Python 3.12 o superior.
"""

from __future__ import annotations

import contextlib
import json
import sys
import tempfile
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import migrate  # noqa: E402
from pipeline import generation_state, reporting  # noqa: E402

#: Artículos que devuelve la BDD falsa en cada momento.
ORIGEN: list = []


class _FakeConn:
    def cursor(self): return self
    def close(self): pass
    def __enter__(self): return self
    def __exit__(self, *a): return False


def _instalar_bdd_falsa() -> None:
    migrate.pyodbc.connect = lambda *a, **k: _FakeConn()
    migrate.resolve_connection_string = lambda *a, **k: 'fake'
    migrate.load_categories = lambda cur: (
        {'10': 'CatA', '11': 'CatB'}, {'10': 'CatA', '11': 'CatB'}, {'10': 'ERP', '11': 'ERP'},
    )
    migrate.load_folders = lambda cur, docs, cats: ({'20': 'Carp'}, {})
    migrate.load_articles = lambda cur: list(ORIGEN)
    # La reparación de enlaces tiene sus propios tests; aquí solo estorba.
    migrate.run_pipeline = lambda *a, **k: None


def art(article_id, title, category_id='10', updated_at='2026-01-01T00:00:00Z',
        status=2, description='<p>hola</p>'):
    return migrate.Article(
        article_id=article_id, title=title, description=description,
        category_id=category_id, folder_id='20', updated_at=updated_at, status=status,
    )


def correr(output_dir: Path, *flags) -> tuple[int, str]:
    """Ejecuta una ejecución completa y devuelve (código de salida, consola)."""
    args = migrate.build_parser().parse_args(['--all', '--output-dir', str(output_dir), *flags])
    trozos: list[str] = []

    class _Captura:
        def write(self, texto): trozos.append(texto)
        def flush(self): pass

    with contextlib.redirect_stdout(_Captura()):
        codigo = migrate.main(args)
    return codigo, ''.join(trozos)


def generados(output_dir: Path) -> list[str]:
    """Los artículos generados. Las portadas de carpeta van aparte, en portadas()."""
    return sorted(p.relative_to(output_dir / 'docs').as_posix()
                  for p in (output_dir / 'docs').rglob('*.md')
                  if p.name.lower() != 'index.md')


def portadas(output_dir: Path) -> list[str]:
    """Los index.md que el pipeline escribe para dar URL a cada carpeta."""
    return sorted(p.relative_to(output_dir / 'docs').as_posix()
                  for p in (output_dir / 'docs').rglob('index.md'))


# ---------------------------------------------------------------------------
# Los tests
# ---------------------------------------------------------------------------

def test_borradores_no_se_publican():
    global ORIGEN
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        ORIGEN = [
            art('1', 'Uno'), art('2', 'Dos'),
            art('3', 'Borrador', status=1),
        ]
        codigo, salida = correr(out)

        assert codigo == 0, salida
        assert generados(out) == ['CatA/Carp/Dos.md', 'CatA/Carp/Uno.md'], generados(out)
        assert 'Omitidos 1 borradores' in salida


def test_lo_no_modificado_no_se_reescribe():
    """Es la premisa de la ejecución semanal."""
    global ORIGEN
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        ORIGEN = [art('1', 'Uno'), art('2', 'Dos')]
        correr(out)

        marcas = {p: p.stat().st_mtime_ns for p in (out / 'docs').rglob('*.md')}
        _, salida = correr(out)

        assert all(p.stat().st_mtime_ns == m for p, m in marcas.items()), \
            'se ha reescrito un .md que no había cambiado'
        assert 'Artículos a generar: 0' in salida


def test_un_cambio_en_el_pipeline_regenera_todo():
    """
    El estado solo miraba el updated_at del artículo, así que un arreglo del
    conversor o de los enlaces no llegaba a lo ya generado: se quedaba con la
    salida antigua para siempre y sin ningún aviso. La huella lo detecta.
    """
    global ORIGEN
    import json
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        ORIGEN = [art('1', 'Uno'), art('2', 'Dos')]
        correr(out)

        _, salida = correr(out)
        assert 'Artículos a generar: 0' in salida, 'sin cambios no debería regenerar'

        # Simula que se ha tocado el pipeline.
        estado_path = out / 'generation_state.json'
        estado = json.loads(estado_path.read_text(encoding='utf-8'))
        estado['meta']['pipeline_fingerprint'] = 'huella-vieja'
        estado_path.write_text(json.dumps(estado), encoding='utf-8')

        _, salida = correr(out)
        assert 'El pipeline ha cambiado' in salida, salida
        assert 'Artículos a generar: 2' in salida, salida

        # Y una vez regenerado, vuelve a estarse quieto.
        _, salida = correr(out)
        assert 'Artículos a generar: 0' in salida, salida


def test_mover_y_renombrar_no_deja_duplicados():
    global ORIGEN
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        ORIGEN = [art('1', 'Uno'), art('2', 'Dos')]
        correr(out)

        # Cambio de categoría.
        ORIGEN[0] = art('1', 'Uno', category_id='11', updated_at='2026-02-01T00:00:00Z')
        _, salida = correr(out, '--prune-orphans')
        assert generados(out) == ['CatA/Carp/Dos.md', 'CatB/Carp/Uno.md'], generados(out)
        assert 'han cambiado de ruta' in salida

        # Cambio de título.
        ORIGEN[1] = art('2', 'Dos Renombrado', updated_at='2026-03-01T00:00:00Z')
        correr(out, '--prune-orphans')
        assert generados(out) == ['CatA/Carp/Dos Renombrado.md', 'CatB/Carp/Uno.md'], generados(out)


def test_pasar_a_borrador_retira_el_fichero():
    global ORIGEN
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        ORIGEN = [art('1', 'Uno'), art('2', 'Dos')]
        correr(out)

        ORIGEN[1] = art('2', 'Dos', status=1)
        correr(out, '--prune-orphans')
        assert generados(out) == ['CatA/Carp/Uno.md'], generados(out)


def test_bug_un_error_de_conversion_no_tira_el_estado():
    """
    Antes, un solo artículo defectuoso impedía consolidar el estado entero: a
    la semana siguiente se regeneraban los más de 2.000 artículos y se
    sobrescribían todos los .md sin modificar.
    """
    global ORIGEN
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        ORIGEN = [art('1', 'Bueno'), art('2', 'Malo', description='EXPLOTA')]

        original = migrate.convert_standard
        migrate.convert_standard = (
            lambda html, *a, **k: (_ for _ in ()).throw(RuntimeError('boom'))
            if html == 'EXPLOTA' else original(html, *a, **k)
        )
        try:
            codigo, salida = correr(out)
        finally:
            migrate.convert_standard = original

        estado = json.loads((out / 'generation_state.json').read_text(encoding='utf-8'))
        assert codigo == 1, 'tiene que avisar del fallo'
        assert '1' in estado['articles'], 'el que sí salió bien debe quedar registrado'
        assert '2' not in estado['articles'], 'el que falló no se registra: se reintenta'
        assert 'se reintentarán en la próxima ejecución' in salida

        # Y a la semana siguiente solo se reintenta ese.
        #
        # Las portadas quedan fuera a propósito: al entrar el artículo que
        # había fallado, el listado de su carpeta cambia y la portada tiene
        # que reescribirse. Lo que no puede tocarse es el artículo que ya
        # estaba bien.
        marcas = {p: p.stat().st_mtime_ns for p in (out / 'docs').rglob('*.md')
                  if p.name.lower() != 'index.md'}
        codigo, salida = correr(out)
        assert 'Artículos a generar: 1' in salida, salida
        assert all(p.stat().st_mtime_ns == m for p, m in marcas.items()), \
            'no se puede tocar lo que ya estaba bien'
        assert codigo == 0


def test_ejecución_cortada_se_reanuda():
    global ORIGEN
    flush_original = generation_state.FLUSH_EVERY
    generation_state.FLUSH_EVERY = 2      # el real es 200: aquí no caben tantos

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        ORIGEN = [art(str(i), f'Art {i}') for i in range(1, 6)]

        hechos: list[Path] = []
        original = migrate.convert_standard

        def convert_que_muere(html, docs, md_path, *a, **k):
            if len(hechos) >= 3:
                raise KeyboardInterrupt('corte simulado')
            hechos.append(md_path)
            return original(html, docs, md_path, *a, **k)

        migrate.convert_standard = convert_que_muere
        try:
            correr(out)
        except KeyboardInterrupt:
            pass
        finally:
            migrate.convert_standard = original
            generation_state.FLUSH_EVERY = flush_original

        assert generation_state.get_run_state_path(out).exists(), \
            'el avance de la ejecución cortada tiene que quedar en disco'
        assert not (out / 'generation_state.json').exists()

        _, salida = correr(out)
        assert 'Se reanuda una ejecución interrumpida' in salida
        assert 'Artículos a generar: 3' in salida, salida
        assert len(generados(out)) == 5
        assert not generation_state.get_run_state_path(out).exists(), \
            'el temporal desaparece al consolidar'


def test_parte_de_la_ejecución_se_escribe():
    global ORIGEN
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        ORIGEN = [art('1', 'Uno')]
        correr(out)

        ORIGEN = [
            art('1', 'Uno'),
            art('2', 'Nuevo'),
            art('3', 'Borrador', status=1),
        ]
        correr(out)

        parte = (out / 'logs' / reporting.RESUMEN).read_text(encoding='utf-8')
        assert 'Artículos nuevos' in parte
        assert 'Borradores omitidos             : 1' in parte, parte
        # Sin incidencias, el resumen es el único informe de la carpeta.
        assert sorted(p.name for p in (out / 'logs').iterdir()) == [reporting.RESUMEN]


def test_los_informes_viejos_no_sobreviven_a_una_ejecución_limpia():
    """
    Un informe de la ejecución anterior en una ejecución limpia es la peor clase
    de log: dice que hay errores y no hay forma de saber que son de la semana
    pasada.
    """
    global ORIGEN
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        ORIGEN = [art('1', 'Bueno'), art('2', 'Malo', description='EXPLOTA')]

        original = migrate.convert_standard
        migrate.convert_standard = (
            lambda html, *a, **k: (_ for _ in ()).throw(RuntimeError('boom'))
            if html == 'EXPLOTA' else original(html, *a, **k)
        )
        try:
            correr(out)
        finally:
            migrate.convert_standard = original

        errores = out / 'logs' / reporting.ARTICULOS_CON_ERROR
        assert errores.exists(), 'la ejecución con error deja su informe'

        # Segunda ejecución, ya sin el artículo que fallaba.
        ORIGEN = [art('1', 'Bueno')]
        correr(out)
        assert not errores.exists(), 'el informe viejo tiene que desaparecer'


# ---------------------------------------------------------------------------

def test_un_producto_de_una_sola_categoria_no_crea_su_carpeta():
    """
    Si toda la ejecucion es un producto y ese producto tiene una sola
    categoria, su carpeta no aporta nada: el lector se come un nivel de mas
    para llegar a cualquier articulo. Las carpetas de dentro suben a docs/.
    """
    global ORIGEN
    with tempfile.TemporaryDirectory() as tmp:
        salida = Path(tmp)
        # Un unico producto, "SOLO", con una sola categoria.
        migrate.load_categories = lambda cur: (
            {'10': 'CatUnica'}, {'10': 'CatUnica'}, {'10': 'SOLO'},
        )
        ORIGEN = [art('1', 'Uno'), art('2', 'Dos')]
        args = migrate.build_parser().parse_args(
            ['--product', 'SOLO', '--output-dir', str(salida)])
        trozos: list[str] = []

        class _Captura:
            def write(self, texto): trozos.append(texto)
            def flush(self): pass

        with contextlib.redirect_stdout(_Captura()):
            codigo = migrate.main(args)
        assert codigo == 0, ''.join(trozos)

        hechos = generados(salida)
        assert hechos == ['Carp/Dos.md', 'Carp/Uno.md'], hechos
        # Y la carpeta que ha subido tiene su portada, como cualquier otra.
        assert (salida / 'docs' / 'Carp' / 'index.md').exists()
        assert 'CatUnica' not in ' '.join(hechos)

    _instalar_bdd_falsa()


def test_con_varios_productos_la_categoria_se_conserva():
    """
    Hay nombres de carpeta que se repiten entre productos —``Versiones`` esta
    en tres—. Quitando el nivel siempre, generar dos de esos productos en el
    mismo docs/ los mezclaria en una sola carpeta. Asi que solo se quita
    cuando la ejecucion es de un unico producto.
    """
    global ORIGEN
    with tempfile.TemporaryDirectory() as tmp:
        salida = Path(tmp)
        migrate.load_categories = lambda cur: (
            {'10': 'CatUna', '11': 'CatOtra'},
            {'10': 'CatUna', '11': 'CatOtra'},
            {'10': 'UNO', '11': 'OTRO'},
        )
        ORIGEN = [art('1', 'Uno', category_id='10'), art('2', 'Dos', category_id='11')]
        codigo, salida_txt = correr(salida)
        assert codigo == 0, salida_txt
        hechos = generados(salida)
        assert hechos == ['CatOtra/Carp/Dos.md', 'CatUna/Carp/Uno.md'], hechos

    _instalar_bdd_falsa()


def test_un_producto_con_varias_categorias_conserva_sus_carpetas():
    """Lo que se quita es el nivel redundante, no el nivel de categoria."""
    global ORIGEN
    with tempfile.TemporaryDirectory() as tmp:
        salida = Path(tmp)
        migrate.load_categories = lambda cur: (
            {'10': 'CatA', '11': 'CatB'},
            {'10': 'CatA', '11': 'CatB'},
            {'10': 'MISMO', '11': 'MISMO'},
        )
        ORIGEN = [art('1', 'Uno', category_id='10'), art('2', 'Dos', category_id='11')]
        args = migrate.build_parser().parse_args(
            ['--product', 'MISMO', '--output-dir', str(salida)])
        trozos: list[str] = []

        class _Captura:
            def write(self, texto): trozos.append(texto)
            def flush(self): pass

        with contextlib.redirect_stdout(_Captura()):
            codigo = migrate.main(args)
        assert codigo == 0, ''.join(trozos)
        hechos = generados(salida)
        assert hechos == ['CatA/Carp/Uno.md', 'CatB/Carp/Dos.md'], hechos

    _instalar_bdd_falsa()

def main() -> int:
    _instalar_bdd_falsa()

    tests = [(nombre, obj) for nombre, obj in sorted(globals().items())
             if nombre.startswith('test_') and callable(obj)]

    correctos = 0
    fallos: list[tuple[str, str]] = []

    for nombre, test in tests:
        try:
            test()
        except Exception:
            fallos.append((nombre, traceback.format_exc()))
            print(f'FALLA  {nombre}')
        else:
            correctos += 1
            print(f'ok     {nombre}')

    print(f'\n{correctos}/{len(tests)} tests correctos.')
    for nombre, tb in fallos:
        print(f'\n===== {nombre} =====\n{tb}')

    return 1 if fallos else 0


if __name__ == '__main__':
    sys.exit(main())
