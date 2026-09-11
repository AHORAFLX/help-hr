"""
repair_links.py
===============
Reparación y validación de los enlaces relativos de la documentación Markdown.

Fases:

1. ``phase_known_link_fixes``  – parches concretos declarados en
   ``article_fixes.LINK_FIXES`` (antes estaban escritos a mano aquí).
2. ``phase_exact_name_repair`` – reapunta enlaces rotos a un fichero cuyo
   nombre normalizado coincide de forma inequívoca.
3. ``phase_overlap_repair``    – último recurso por solape de palabras, con un
   umbral alto y exigiendo un único ganador.
4. ``phase_unwrap_folder_links`` – los enlaces que apuntan a una **carpeta**:
   le da portada ``index.md`` a la categoría y reapunta el enlace a ella, o lo
   deja en texto si esa categoría no está en la ejecución.
5. ``phase_tidy_blank_lines`` – ultimo repaso a las lineas en blanco: las
   fases de arriba dejan huecos al degradar una URL o quitar un enlace, y el
   resultado tiene que ser idempotente.
6. ``phase_validation``        – recorre todo y deja el informe de lo que sigue
   roto.

Las fases 2 y 3 solo **modifican** los ficheros indicados en ``only_files``
(los regenerados en la ejecución). El índice de destinos candidatos siempre es el
árbol completo. Sin ese acotado, una generación incremental de una categoría
reescribía enlaces de ficheros que estaban correctos.

Requiere Python 3.12 o superior.
"""

from __future__ import annotations

import argparse
import os
import re
import unicodedata
from pathlib import Path
from typing import Iterable, NamedTuple, Optional
from urllib.parse import quote, unquote

from .article_fixes import LINK_FIXES
from .common import front_matter
from .converters import limpiar_lineas_en_blanco
from .reporting import ENLACES_A_CATEGORIA, ENLACES_ROTOS, RunLogs

#: El mismo separador que usan los demás informes.
_SEPARADOR = '-' * 70

#: Raíz del repositorio: este módulo vive en ``pipeline/``, un nivel por debajo.
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DOCS_DIR = (BASE_DIR / 'docs').resolve()

#: Palabras compartidas mínimas para aceptar una reasignación por solape.
#: Con 1 (el valor anterior) bastaba una coincidencia trivial como "erp" para
#: reapuntar un enlace a un artículo que no tenía nada que ver.
MIN_WORD_OVERLAP = 3

#: Un enlace Markdown completo: ``[texto](destino)``.
#:
#: El grupo del destino admite UN nivel de paréntesis anidados. Hace falta:
#: hay artículos cuyo nombre de fichero los lleva ("... (common dialog).md"),
#: y la versión anterior —``\(([^)]+)\)``— cortaba en el primer paréntesis,
#: se quedaba con media ruta y daba por roto un enlace que estaba bien.
LINK_RX = re.compile(r'\[([^\]]*)\]\(((?:[^()]|\([^()]*\))*)\)')

#: El título opcional que Markdown admite tras la ruta: ``[t](ruta "título")``.
#: No es parte del destino, así que hay que apartarlo antes de resolverlo y
#: devolverlo en su sitio al reescribir el enlace.
LINK_TITLE_RX = re.compile(r'\s+(?:"[^"]*"|\'[^\']*\')\s*$')

CODE_BLOCK_RX = re.compile(r'```.*?```', re.DOTALL)
INLINE_CODE_RX = re.compile(r'`[^`]+`')

EXTERNAL_PREFIXES = ('http://', 'https://', 'mailto:', 'tel:', 'ftp://', '//', '#')

#: Prefijos de producto que no aportan nada al comparar nombres de artículo.
_PRODUCT_PREFIX_RX = re.compile(
    r'^(erp|ventas|compras|logistica|contabilidad|configuracion|facturacion'
    r'|gestion|sga|reporting)\b',
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def normalize_name(text: str) -> str:
    """Normaliza un nombre de fichero para compararlo sin acentos ni símbolos."""
    if not text:
        return ""
    text = unquote(text).lower()
    if text.endswith('.md'):
        text = text[:-3]
    normalized = unicodedata.normalize('NFD', text)
    result = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', ' ', result).strip()


def link_words(text: str) -> set[str]:
    """Extrae el conjunto de palabras significativas de un nombre de artículo."""
    text = unquote(text or '')
    if text.lower().endswith('.md'):
        text = text[:-3]
    text = _PRODUCT_PREFIX_RX.sub('', text)
    return set(re.findall(r'[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ]{3,}', text.lower()))


def get_relative_posix(from_dir: Path, to_file: Path) -> str:
    return os.path.relpath(str(to_file), str(from_dir)).replace('\\', '/').replace(' ', '%20')


def _is_external(url: str) -> bool:
    return url.startswith(EXTERNAL_PREFIXES)


def _split_anchor(url: str) -> tuple[str, str]:
    path_part, _, anchor = url.partition('#')
    return path_part.split('?', 1)[0], anchor


def split_link_target(raw: str) -> tuple[str, str]:
    """
    Parte el interior de un enlace en (destino, título).

    ``ruta.md "Teclas de acceso rápido"`` -> ``('ruta.md', '"Teclas de acceso rápido"')``

    El título se devuelve con sus comillas, tal cual, para poder recomponer el
    enlace sin perder nada.
    """
    raw = raw.strip()
    match = LINK_TITLE_RX.search(raw)
    if not match:
        return raw, ''
    return raw[:match.start()].strip(), match.group(0).strip()


def build_link(text: str, url: str, title: str = '') -> str:
    """Recompone un enlace Markdown conservando su título, si lo tenía."""
    if title:
        return f'[{text}]({url} {title})'
    return f'[{text}]({url})'


def _resolve_targets(docs_dir: Path, only_files: Optional[Iterable[Path]]) -> list[Path]:
    """Ficheros que se pueden modificar en esta ejecución."""
    if only_files is None:
        return sorted(docs_dir.rglob('*.md'))
    resolved = docs_dir.resolve()
    out: list[Path] = []
    for path in only_files:
        candidate = Path(path).resolve()
        if candidate.suffix.lower() == '.md' and candidate.exists() and candidate.is_relative_to(resolved):
            out.append(candidate)
    return sorted(set(out))


# ---------------------------------------------------------------------------
# Fase 1: parches conocidos
# ---------------------------------------------------------------------------

def phase_known_link_fixes(docs_dir: Path) -> int:
    """Aplica los ``LINK_FIXES`` declarados en article_fixes.py."""
    print('[*] Fase 1: parches de enlaces conocidos...')
    applied = 0

    for fix in LINK_FIXES:
        file_path = docs_dir / fix.path
        if not file_path.exists():
            continue

        content = file_path.read_text(encoding='utf-8')
        original = content

        for pattern, replacement, flags in fix.substitutions:
            content = re.sub(pattern, replacement, content, flags=flags)

        for old, new in fix.replacements:
            if old in content:
                content = content.replace(old, new)
            else:
                # Tolerar que los espacios estén como %20 o como espacios.
                tolerant = re.escape(old).replace(r'\%20', r'(?:%20|\s)').replace(r'\ ', r'(?:%20|\s)')
                if re.search(tolerant, content):
                    content = re.sub(tolerant, new.replace('\\', r'\\'), content)

        if content != original:
            file_path.write_text(content, encoding='utf-8')
            applied += 1

    print(f'    Ficheros parcheados: {applied}')
    return applied


# ---------------------------------------------------------------------------
# Fases 2 y 3: reparación de enlaces rotos
# ---------------------------------------------------------------------------

def _build_file_index(docs_dir: Path) -> tuple[dict[str, list[Path]], list[tuple[Path, set[str], str]]]:
    """Construye los índices por nombre normalizado y por palabras."""
    by_name: dict[str, list[Path]] = {}
    by_words: list[tuple[Path, set[str], str]] = []

    for path in docs_dir.rglob('*.md'):
        by_name.setdefault(normalize_name(path.name), []).append(path)
        words = link_words(path.stem)
        if words:
            by_words.append((path, words, path.stem.lower()))

    return by_name, by_words


def _code_spans(content: str) -> list[tuple[int, int]]:
    """
    Tramos de código del documento: fences ``` y código en línea.

    Se devuelven como posiciones, no sustituyendo el texto por un marcador,
    porque las fases 2 y 3 reescriben sobre el contenido original y cualquier
    cambio de longitud les descuadraría los desplazamientos.
    """
    spans = [m.span() for m in CODE_BLOCK_RX.finditer(content)]

    # Hay que buscar el código en línea sobre el texto con los fences ya
    # tapados: si no, las comillas de cierre de un fence emparejan con las de
    # apertura del siguiente trozo y los tramos salen corridos.
    masked = list(content)
    for start, end in spans:
        masked[start:end] = ' ' * (end - start)   # misma longitud: no mueve nada

    spans += [m.span() for m in INLINE_CODE_RX.finditer(''.join(masked))]
    return spans


def _is_inside(spans: list[tuple[int, int]], position: int) -> bool:
    return any(start <= position < end for start, end in spans)


class UnrepairedLink(NamedTuple):
    """Un enlace que las fases 2 o 3 no supieron reasignar, y por qué."""

    file: str      #: fichero donde está el enlace, relativo a docs/
    url: str       #: el destino tal cual está escrito
    cause: str     #: por qué no se pudo arreglar solo


class BrokenLink(NamedTuple):
    """Un enlace relativo que no resuelve a un fichero de disco."""

    match: re.Match          #: la coincidencia entera, para poder sustituirla
    url: str                 #: el destino tal cual estaba escrito, sin título
    path: str                #: solo la ruta: sin título, sin ancla y sin %20
    anchor: str              #: el ancla, si la había
    title: str               #: el título Markdown con sus comillas, si lo había


def _iter_broken_links(content: str, md_file: Path):
    """
    Recorre los enlaces relativos del fichero que no resuelven a disco.

    El SQL de la documentación está lleno de cosas que parecen un enlace
    —``[Descrip] [varchar](50) NULL``— y que no lo son. Si no se excluye el
    código, las fases de reparación acaban reescribiendo el interior de un
    bloque SQL.
    """
    code_spans = _code_spans(content)

    for match in reversed(list(LINK_RX.finditer(content))):
        if _is_inside(code_spans, match.start()):
            continue

        url, title = split_link_target(match.group(2))
        if not url or _is_external(url) or 'docs_assets' in url:
            continue

        path_part, anchor = _split_anchor(url)
        clean = unquote(path_part)
        if not clean:
            continue

        target = (md_file.parent / clean).resolve()
        if target.exists() and target.is_file():
            continue

        yield BrokenLink(match, url, clean, anchor, title)


class EnlaceACategoria(NamedTuple):
    """Un enlace que apuntaba a una carpeta y se dejó en texto."""

    file: str        #: el artículo, relativo a docs/
    text: str        #: el texto visible que se conserva
    target: str      #: la carpeta a la que apuntaba, tal cual estaba escrita
    folder: str      #: la carpeta resuelta, relativa a docs/, o '(no existe)'


#: Marca que identifica una portada escrita por este pipeline.
#:
#: Sirve para poder **rehacerla en cada ejecución** sin pisar una que haya
#: escrito alguien a mano: si la marca está, el listado se regenera —los
#: artículos de la categoría cambian—; si no está, la portada es de su autor y
#: no se toca.
MARCA_PORTADA_GENERADA = '<!-- portada de categoría generada automáticamente -->'


def es_portada_generada(index_md: Path) -> bool:
    """¿Esta portada la escribió el pipeline, o alguien a mano?"""
    try:
        with index_md.open(encoding='utf-8', errors='replace') as fh:
            # La marca va detras del H1, no en la primera linea: con el
            # comentario delante MkDocs titula la pagina "Index".
            cabeza = [next(fh, '') for _ in range(5)]
        return any(MARCA_PORTADA_GENERADA in linea for linea in cabeza)
    except OSError:
        return False


def _titulo_de_categoria(carpeta: Path) -> str:
    """El nombre de la carpeta, tal cual, como título de su portada."""
    return carpeta.name


def _cuenta_articulos(carpeta: Path) -> int:
    """Cuántos artículos cuelgan de una carpeta, contando los de dentro."""
    return sum(1 for p in carpeta.rglob('*.md') if p.stem.lower() != 'index')


#: Iconos de las tarjetas. Son los de Material —``pymdownx.emoji`` con el
#: índice de twemoji, ya configurado en ``mkdocs.yml``—, así que se escriben
#: en el propio Markdown y el tema los resuelve a un SVG. Los modificadores
#: ``{ .lg .middle }`` también son del tema: tamaño y alineación con el texto.
_ICONO_CARPETA = ':material-folder-outline:{ .lg .middle }'
_ICONO_ARTICULO = ':material-file-document-outline:{ .lg .middle }'


def _rejilla(tarjetas: list[list[str]]) -> list[str]:
    """
    Envuelve las tarjetas en la rejilla de Material.

    ``grid cards`` es un componente del propio tema: la lista de dentro se
    pinta como tarjetas y **no hace falta CSS ninguno**. El ``markdown`` del
    ``<div>`` es de ``md_in_html``, y es lo que hace que lo de dentro se
    siga tratando como Markdown —incluidos los enlaces, que MkDocs reescribe
    como en cualquier otra página—.
    """
    lineas = ['<div class="grid cards" markdown>', '']
    for tarjeta in tarjetas:
        lineas += tarjeta + ['']
    lineas.append('</div>')
    return lineas


def _enlace(destino: Path, desde: Path) -> str:
    """
    La ruta con la que se enlaza a ``destino`` desde una portada.

    Siempre al ``.md``, nunca a la carpeta: MkDocs solo reescribe los enlaces
    que reconoce como documento, y con ``use_directory_urls`` la página vive
    un nivel más abajo que el fichero. Escrito ``FAQ/`` se queda corto y da
    404; escrito ``FAQ/index.md``, MkDocs lo publica como ``FAQ/``, que sí
    resuelve.

    Se codifica la ruta entera, no solo los espacios: hay artículos con ``#``
    en el nombre —que Markdown lee como ancla— y otros con paréntesis, que
    cierran el enlace antes de tiempo.
    """
    if destino.is_dir():
        destino = destino / 'index.md'
    return quote(destino.relative_to(desde).as_posix(), safe='/')


def _reparto(carpeta: Path) -> tuple[list[Path], list[Path]]:
    """
    Reparte lo que hay dentro en (carpetas, artículos sueltos).

    La subcarpeta que repite el nombre de su madre no es una carpeta de
    verdad: es la propia categoría doblada en el origen
    —``docs/Actualizador/Actualizador/``—. Sus artículos se listan con los
    sueltos, que es donde estarían si el origen estuviera bien.

    Una carpeta sin artículos no sale: no tendría portada a la que llevar.
    """
    carpetas: list[Path] = []
    sueltos = sorted(p for p in carpeta.glob('*.md') if p.stem.lower() != 'index')

    for sub in sorted(d for d in carpeta.iterdir() if d.is_dir()):
        if not _cuenta_articulos(sub):
            continue
        if sub.name == carpeta.name:
            sueltos += sorted(p for p in sub.rglob('*.md') if p.stem.lower() != 'index')
        else:
            carpetas.append(sub)

    return carpetas, sueltos


def _titulo_de_articulo(md_file: Path) -> str:
    """El H1 del artículo, o su nombre de fichero si no lo tuviera."""
    try:
        for linea in md_file.read_text(encoding='utf-8', errors='replace').splitlines():
            if linea.startswith('# '):
                return linea[2:].strip()
    except OSError:
        pass
    return md_file.stem


def _escribir_portada(carpeta: Path) -> tuple[Path, bool]:
    """
    Escribe la portada ``index.md`` de una carpeta, con su listado.

    Hace falta porque MkDocs publica **páginas, no directorios**: una carpeta
    solo tiene URL si lleva un ``index.md``. Sin ella, ``[AHORA API](../../API/)``
    no lleva a ninguna parte.

    Vale igual para una categoría —``docs/API/``— que para una carpeta de
    Freshdesk —``docs/API/Instalación/``—, que es lo mismo un nivel más abajo.
    Lo que cambia es lo que tiene dentro: la categoría lista sus carpetas y la
    carpeta lista sus artículos.

    Se escribe en Markdown, con la rejilla de tarjetas que trae Material de
    serie. Ni una línea de CSS propio: ``grid cards``, los iconos
    ``:material-...:`` y los modificadores ``{ .lg .middle }`` son del tema, y
    las extensiones que hacen falta —``attr_list``, ``md_in_html`` y
    ``pymdownx.emoji``— ya estaban en ``mkdocs.yml``.

    Devuelve ``(ruta, ha_escrito)``.
    """
    titulo = _titulo_de_categoria(carpeta)
    carpetas, sueltos = _reparto(carpeta)

    # El H1 va PRIMERO, y la marca detrás. Con el comentario delante, MkDocs no
    # detecta el H1 y titula la página "Index": así salía en el panel izquierdo,
    # en la pestaña del navegador y en los resultados de búsqueda.
    #
    # La cabecera YAML lleva, si hace falta, la versión corta del nombre: hay
    # carpetas de Freshdesk con nombres larguísimos, y en el panel izquierdo
    # la portada es la etiqueta de toda la sección.
    lineas = [f'{front_matter(titulo)}# {titulo}', '', MARCA_PORTADA_GENERADA, '']

    # Los dos encabezados solo se ponen cuando hay las dos cosas. En una
    # carpeta hoja —solo artículos— un "## Artículos" sobre la única lista de
    # la página no dice nada y encima ensucia la tabla de contenidos.
    con_ambos = bool(carpetas and sueltos)

    if carpetas:
        if con_ambos:
            lineas += ['## Carpetas', '']
        # Solo el nombre. La tarjeta no lleva raya ni recuento: cuántos
        # artículos hay dentro no es lo que se viene a leer, y la raya con
        # una línea suelta debajo hacía la tarjeta el doble de alta.
        lineas += _rejilla([
            [f'-   {_ICONO_CARPETA} **[{sub.name}]({_enlace(sub, carpeta)})**']
            for sub in carpetas
        ])
        lineas.append('')

    if sueltos:
        if con_ambos:
            lineas += ['## Artículos', '']
        # La del artículo, igual: solo el título.
        lineas += _rejilla([
            [f'-   {_ICONO_ARTICULO} '
             f'[{_titulo_de_articulo(md_file)}]({_enlace(md_file, carpeta)})']
            for md_file in sueltos
        ])
        lineas.append('')

    destino = carpeta / 'index.md'
    texto = '\n'.join(lineas).rstrip() + '\n'
    # Solo se escribe si ha cambiado algo. La portada se rehace en cada ejecución
    # —el listado depende de los artículos, que van y vienen—, pero reescribir
    # un fichero idéntico le cambia la fecha y lo saca en el 'git status' de
    # las 156 carpetas todas las semanas.
    try:
        if destino.read_text(encoding='utf-8') == texto:
            return destino, False
    except OSError:
        pass
    destino.write_text(texto, encoding='utf-8')
    return destino, True


def escribir_portada(carpeta: Path) -> Path:
    """Escribe la portada de ``carpeta`` y devuelve su ruta."""
    destino, _ = _escribir_portada(carpeta)
    return destino


#: Nombre viejo de :func:`escribir_portada`, de cuando solo se hacían portadas
#: de categoría.
escribir_indice_de_categoria = escribir_portada


def escribir_portadas_del_arbol(raices: Iterable[Path]) -> tuple[int, int]:
    """
    Da portada a **todas** las carpetas que cuelgan de ``raices``, y a ellas.

    Hasta ahora la portada se escribía solo cuando un enlace roto apuntaba a
    esa carpeta, así que de 15 categorías y 141 carpetas había dos portadas.
    El resultado era que un enlace de Freshdesk a una carpeta —que
    ``fix_internal_links`` sí sabe traducir a su ruta local— llegaba a un
    directorio sin página y acababa degradado a texto plano.

    Se hace en cada ejecución y para todo el árbol seleccionado, no solo para lo
    regenerado: el listado de una carpeta cambia en cuanto se le añade, se le
    quita o se le renombra un artículo, y eso pasa en artículos que no son la
    portada.

    Una carpeta sin artículos no lleva portada: sería una página vacía en el
    panel de navegación. Una portada escrita a mano —sin la marca— se respeta.

    Devuelve ``(escritas, respetadas)``, donde ``escritas`` son las que de
    verdad han cambiado en disco: decir "151 escritas" cuando no ha cambiado
    ninguna es mentir en el parte de la ejecución.
    """
    escritas = respetadas = 0

    for raiz in raices:
        raiz = Path(raiz)
        if not raiz.is_dir():
            continue
        for carpeta in [raiz, *sorted(d for d in raiz.rglob('*') if d.is_dir())]:
            if not _cuenta_articulos(carpeta):
                continue
            existente = carpeta / 'index.md'
            if existente.is_file() and not es_portada_generada(existente):
                respetadas += 1
                continue
            _, ha_escrito = _escribir_portada(carpeta)
            escritas += ha_escrito

    return escritas, respetadas



def phase_unwrap_dead_links(
    docs_dir: Path,
    only_files: Optional[Iterable[Path]] = None,
) -> int:
    """
    Deja en texto los enlaces que, tras todo, siguen sin destino.

    Son los que apuntan a artículos de otro producto: al generar solo el ERP,
    89 enlaces a `TPV`, `SGA` o `_ahoraSCO` se publicaban **como enlaces**, y
    el lector que los pulsaba llegaba a un 404. El texto se conserva entero,
    así que no se pierde nada de lo que el autor escribió: solo deja de ser
    pulsable algo que no lleva a ninguna parte.

    Va **después** de ``phase_validation``, y ese orden importa: el informe
    ``enlaces-rotos.txt`` tiene que decir qué había —artículo de origen, texto
    y destino— porque una vez en texto ya no se ve. Con el informe delante, la
    decisión de generar ese producto sigue siendo posible.

    Si más adelante se genera el producto que falta, el enlace se resuelve solo
    en la ejecución siguiente y deja de pasar por aquí.
    """
    quitados = 0

    for md_file in _resolve_targets(docs_dir, only_files):
        content = md_file.read_text(encoding='utf-8', errors='replace')
        original = content

        for roto in _iter_broken_links(content, md_file):
            texto = roto.match.group(1)
            if not texto.strip():
                continue
            content = content[:roto.match.start()] + texto + content[roto.match.end():]
            quitados += 1

        content, n = _desenvolver_anclas_sin_destino(content, md_file)
        quitados += n

        if content != original:
            md_file.write_text(content, encoding='utf-8')

    if quitados:
        print(f'[*] Enlaces sin destino dejados en texto: {quitados}')
    return quitados


#: Un ancla HTML cruda con su contenido. Las tablas que se conservan traen sus
#: enlaces así, no como enlace Markdown, y ``LINK_RX`` no las ve.
#: El destino se cierra con la **misma** comilla que lo abre, no con cualquiera
#: de las dos: 4 artículos enlazan a ``ERP - Modelos 300, 320, 320 y 390
#: Gipuzkoa 'Ventanilla única'.md``, y un ``[^"']*`` cortaba el destino en el
#: apóstrofo del título.
_ANCLA_HTML_RX = re.compile(
    r'''(?is)<a\b[^>]*\bhref\s*=\s*(["'])(?P<url>(?:(?!\1)[^>])*)\1[^>]*>(?P<texto>.*?)</a>''')


def _tiene_destino(ruta: str, md_file: Path) -> bool:
    """
    Dice si el destino de un ancla HTML existe, en cualquiera de sus dos formas.

    Un ancla puede venir apuntando al fichero fuente —``Modelo 111.md``— o ya
    en la forma con la que se publica —``../Modelo%20111/``—, que es la que le
    deja ``phase_publish_html_links``. Comprobar solo la primera hacía que las
    ya traducidas parecieran muertas, y la fase de degradar se comía justo los
    87 enlaces que la de traducir acababa de arreglar.

    La forma publicada se resuelve desde la **carpeta de la página**, que con
    ``use_directory_urls`` es un nivel más abajo que el fichero.
    """
    ruta = unquote(ruta)

    if (md_file.parent / ruta).resolve().exists():
        return True

    if ruta.endswith('/'):
        desde = md_file.parent / md_file.stem
        destino = (desde / ruta).resolve()
        # El ``.md`` se **añade**, no se sustituye: ``with_suffix`` se lleva por
        # delante lo que hay tras el último punto, y estos títulos van llenos
        # —``ERP - Modelo 369. Declaraciones de IVA…``, ``AHORA Install
        # 4.4.2400 - …``—, así que 5 destinos buenos parecían no existir.
        return destino.is_dir() or destino.with_name(destino.name + '.md').exists()

    return False


def _desenvolver_anclas_sin_destino(content: str, md_file: Path) -> tuple[str, int]:
    """
    Deja en texto las anclas HTML cuyo destino relativo no existe.

    Las 31 que quedaban tras degradar los enlaces Markdown venían **dentro de
    una tabla conservada**: los artículos de Hotfix escriben sus enlaces como
    ``<a href="...">`` y ``LINK_RX``, que solo entiende Markdown, no las veía.

    Se conserva el contenido del ancla tal cual —puede llevar su ``<strong>``
    o su ``<img>``—, así que lo único que se pierde es un enlace que llevaba a
    un 404.
    """
    spans = _code_spans(content)
    quitados = 0

    for m in reversed(list(_ANCLA_HTML_RX.finditer(content))):
        if _is_inside(spans, m.start()):
            continue
        url = (m.group('url') or '').strip()
        if not url or _is_external(url):
            continue
        ruta, _ = _split_anchor(url)
        if not ruta:
            continue
        if _tiene_destino(ruta, md_file):
            continue
        interior = m.group('texto')
        if not re.sub(r'(?is)<[^>]+>|\s|&nbsp;', '', interior):
            continue          # sin nada visible dentro: de eso se encargan otras reglas
        content = content[:m.start()] + interior + content[m.end():]
        quitados += 1

    return content, quitados


def phase_publish_html_links(
    docs_dir: Path,
    only_files: Optional[Iterable[Path]] = None,
) -> int:
    """
    Traduce a URL publicada las anclas HTML que apuntan a un ``.md`` que existe.

    MkDocs reescribe los enlaces Markdown, pero **no los de las tablas que se
    conservan en crudo**: el HTML en bruto lo aparta antes de recorrer el
    documento, así que un ``<a href="ERP - Modelo 111.md">`` sale publicado
    con el ``.md`` puesto y da un 404 aunque el artículo esté ahí al lado.

    Eran 87 enlaces buenos rotos en la publicación, y ninguno salía en el
    informe de enlaces rotos: el destino existe, el fallo estaba solo en la
    forma. Tampoco los avisa ``mkdocs build``, por el mismo motivo por el que
    no los reescribe.

    La traducción es la que hace MkDocs con ``use_directory_urls``: la página
    se publica en su propia carpeta, así que hay un nivel más que subir y el
    destino pierde la extensión::

        ERP - Modelo 111.md   ->   ../ERP%20-%20Modelo%20111/

    Va después de degradar los enlaces muertos, así que aquí solo quedan
    anclas con destino de verdad.
    """
    arreglados = 0

    for md_file in _resolve_targets(docs_dir, only_files):
        content = md_file.read_text(encoding='utf-8', errors='replace')
        content, n = _anclas_html_a_url_publicada(content, md_file)
        arreglados += n
        if n:
            md_file.write_text(content, encoding='utf-8')

    if arreglados:
        print(f'[*] Enlaces HTML traducidos a URL publicada: {arreglados}')
    return arreglados


def _anclas_html_a_url_publicada(content: str, md_file: Path) -> tuple[str, int]:
    """Reescribe el ``href`` de las anclas HTML que llevan a un ``.md`` real."""
    spans = _code_spans(content)
    arreglados = 0

    for m in reversed(list(_ANCLA_HTML_RX.finditer(content))):
        if _is_inside(spans, m.start()):
            continue
        url = (m.group('url') or '').strip()
        if not url or _is_external(url):
            continue
        ruta, fragmento = _split_anchor(url)
        ruta = unquote(ruta)
        if not ruta.lower().endswith('.md'):
            continue
        if not (md_file.parent / ruta).resolve().exists():
            continue          # sin destino: lo degrada _desenvolver_anclas_sin_destino
        publicada = '../' + quote(ruta[:-len('.md')], safe='/') + '/'
        if fragmento:
            publicada += '#' + fragmento
        inicio, fin = m.span('url')
        content = (content[:inicio] + publicada + content[fin:])
        arreglados += 1

    return content, arreglados


def phase_tidy_blank_lines(
    docs_dir: Path,
    only_files: Optional[Iterable[Path]] = None,
) -> int:
    """
    Último repaso a las líneas en blanco, cuando ya nadie va a tocar el texto.

    El conversor ya las ordena, pero las fases de enlaces corren **después**:
    al degradar una URL o quitar un enlace queda la línea vacía detrás, y el
    fichero acaba con rachas de tres y cuatro saltos, o con una línea de un
    solo espacio.

    Lo que se busca no es cosmética: es que el resultado sea **idempotente**.
    Si al acabar la ejecución las reglas de limpieza aún tendrían trabajo, el
    fichero no está en su forma final y no hay manera de comprobar de un
    vistazo que una ejecución está completa. Eran 5 artículos.
    """
    arreglados = 0

    for md_file in _resolve_targets(docs_dir, only_files):
        contenido = md_file.read_text(encoding='utf-8', errors='replace')
        limpio = _limpiar_fuera_de_fences(contenido)
        if limpio != contenido:
            md_file.write_text(limpio, encoding='utf-8')
            arreglados += 1

    if arreglados:
        print(f'[*] Ficheros con líneas en blanco ordenadas: {arreglados}')
    return arreglados


def _limpiar_fuera_de_fences(contenido: str) -> str:
    """Aplica la limpieza solo fuera de los bloques de código."""
    return ''.join(
        trozo if trozo.startswith('```') else limpiar_lineas_en_blanco(trozo)
        for trozo in re.split(r'(?s)(```.*?```)', contenido)
    )


def phase_unwrap_folder_links(
    docs_dir: Path,
    only_files: Optional[Iterable[Path]] = None,
) -> list[EnlaceACategoria]:
    """
    Deja en texto los enlaces que apuntan a una carpeta sin página índice.

    El origen escribe cosas como ``[AHORA TPV](../../TPV/)`` o
    ``[Sección Actualizador](../../Actualizador/)``: un enlace a la categoría,
    no a un artículo. Con ``use_directory_urls`` una carpeta solo tiene URL si
    lleva un ``index.md``, y ninguna de las categorías lo lleva, así que eran
    **6 enlaces que daban 404**. Lo detectó ``mkdocs build``, que avisa de
    ellos uno por uno.

    Ninguna de las fases de reparación puede con esto —no hay artículo al que
    reapuntar—, así que la única salida honrada es quitar el enlace y dejar su
    texto, que ya dice lo que hay que decir.

    Si algún día se generan índices de categoría, la carpeta tendrá su página
    y estos enlaces dejarán de entrar aquí solos.

    Respeta ``only_files`` como las demás fases: en una ejecución incremental
    solo se toca lo que se ha vuelto a generar.

    Devuelve lo que ha quitado, para que quede en el informe
    ``enlaces-a-categoria.txt``: quitar un enlace es perder información, y el
    lector del log tiene que poder decidir si esa categoría merece una página
    índice o si el enlace estaba de más.
    """
    quitados: list[EnlaceACategoria] = []
    indices: dict[Path, Path] = {}
    creadas: set[Path] = set()
    reapuntados = 0
    raiz = docs_dir.resolve()

    for md_file in _resolve_targets(docs_dir, only_files):
        content = md_file.read_text(encoding='utf-8', errors='replace')
        original = content

        for roto in _iter_broken_links(content, md_file):
            destino = (md_file.parent / roto.path).resolve()
            es_carpeta = roto.path.endswith('/') or destino.is_dir()
            if not es_carpeta:
                continue

            texto = roto.match.group(1)
            if not texto.strip():
                continue

            if destino.is_dir() and destino.is_relative_to(raiz):
                # La categoría existe: se le da portada —si no la tiene ya— y
                # el enlace se reapunta a ella.
                #
                # Ojo: hay que reapuntarlo **aunque la portada ya exista**. Un
                # enlace a carpeta MkDocs no lo reescribe, y con
                # ``use_directory_urls`` la página vive un nivel más abajo que
                # el fichero, así que ``../../API/`` se queda corto y da 404
                # con portada y sin ella. Solo resuelve escrito al ``.md``.
                if destino not in indices:
                    existente = destino / 'index.md'
                    # Una portada escrita a mano se respeta; la nuestra se
                    # rehace, porque los articulos de la categoria cambian.
                    if existente.is_file() and not es_portada_generada(existente):
                        indices[destino] = existente
                    else:
                        indices[destino] = escribir_portada(destino)
                        creadas.add(destino)
                ruta = get_relative_posix(md_file.parent, indices[destino])
                if roto.anchor:
                    ruta += '#' + roto.anchor
                content = (content[:roto.match.start()]
                           + build_link(texto, ruta, roto.title)
                           + content[roto.match.end():])
                reapuntados += 1
                continue

            # La categoría no está en esta ejecución: no hay página que crear,
            # así que el enlace se queda en texto para no publicar un 404.
            content = content[:roto.match.start()] + texto + content[roto.match.end():]
            quitados.append(EnlaceACategoria(
                file=_relativo(md_file, raiz),
                text=' '.join(texto.split()),
                target=roto.url,
                folder='(la carpeta no está en esta ejecución)',
            ))

        if content != original:
            md_file.write_text(content, encoding='utf-8')

    if indices:
        print(f'[*] Enlaces a categoría reapuntados: {reapuntados} '
              f'({len(creadas)} portada(s) nueva(s))')
        for carpeta in sorted(indices):
            marca = 'creada ' if carpeta in creadas else 'ya había'
            print(f'    [{marca}] {_relativo(carpeta, raiz)}/index.md')
    if quitados:
        print(f'[*] Enlaces a carpetas que no están en esta ejecución, '
              f'dejados en texto: {len(quitados)}')
    return quitados


def _relativo(ruta: Path, raiz: Path) -> str:
    """La ruta relativa a ``docs/``, o absoluta si cae fuera."""
    try:
        return ruta.resolve().relative_to(raiz).as_posix()
    except ValueError:
        return str(ruta)


def build_category_links_report(enlaces: Iterable[EnlaceACategoria]) -> list[str]:
    """
    Compone el informe de enlaces a categoría, agrupado por carpeta de destino.

    Va por destino y no por fichero de origen porque la decisión se toma por
    categoría: o esa carpeta merece una página índice —y entonces se arreglan
    todos sus enlaces de una vez— o no la merece y no hay nada que hacer.
    """
    enlaces = list(enlaces)
    if not enlaces:
        return []

    grupos: dict[str, list[EnlaceACategoria]] = {}
    for enlace in enlaces:
        grupos.setdefault(enlace.folder, []).append(enlace)

    lineas = [
        f'{len(enlaces)} enlace(s) apuntaban a una carpeta de categoría, que no tiene',
        'página propia: con use_directory_urls una carpeta solo se publica si lleva',
        'un index.md. Se ha quitado el enlace y se ha conservado su texto, para no',
        'publicar un 404.',
        '',
        'Estas categorías no están en esta ejecución: para recuperar sus enlaces hay',
        'que generar también ese producto. En cuanto la carpeta exista, la ejecución le',
        'escribe su portada y reapunta los enlaces sola.',
        '',
    ]

    for carpeta in sorted(grupos):
        del_grupo = grupos[carpeta]
        lineas.append(_SEPARADOR)
        lineas.append(f'CARPETA: {carpeta}   ({len(del_grupo)} enlace(s))')
        lineas.append('')
        for enlace in sorted(del_grupo, key=lambda e: (e.file, e.text)):
            lineas.append(f'  {enlace.file}')
            lineas.append(f'      texto conservado : {enlace.text}')
            lineas.append(f'      destino que tenía: {enlace.target}')
        lineas.append('')

    return lineas


def phase_exact_name_repair(
    docs_dir: Path,
    targets: list[Path],
    by_name: dict[str, list[Path]],
    unfixable: list[UnrepairedLink],
) -> tuple[int, int]:
    """Reapunta enlaces rotos cuando hay un único fichero con ese nombre."""
    print('[*] Fase 2: reparación por nombre de fichero...')
    broken = 0
    fixed = 0

    for md_file in targets:
        content = md_file.read_text(encoding='utf-8')
        new_content = content
        changed = False

        for link in _iter_broken_links(content, md_file):
            broken += 1
            norm = normalize_name(Path(link.path).name)
            # Copia: extender la lista del índice lo corrompería para el resto.
            candidates = list(by_name.get(norm, ()))

            if not candidates and len(norm) >= 10:
                for key, paths in by_name.items():
                    if key.startswith(norm) or norm.startswith(key):
                        candidates.extend(paths)

            rel_file = md_file.relative_to(docs_dir)
            if len(candidates) == 1:
                new_rel = get_relative_posix(md_file.parent, candidates[0])
                if link.anchor:
                    new_rel += '#' + link.anchor
                nuevo = build_link(link.match.group(1), new_rel, link.title)
                new_content = (new_content[:link.match.start()] + nuevo
                               + new_content[link.match.end():])
                fixed += 1
                changed = True
            elif len(candidates) > 1:
                names = ', '.join(str(c.relative_to(docs_dir)) for c in candidates)
                unfixable.append(UnrepairedLink(
                    str(rel_file), link.url, f'ambiguo, varios candidatos: {names}'))

        if changed:
            md_file.write_text(new_content, encoding='utf-8')

    print(f'    Enlaces rotos detectados: {broken} · reparados: {fixed}')
    return broken, fixed


def phase_overlap_repair(
    docs_dir: Path,
    targets: list[Path],
    by_words: list[tuple[Path, set[str], str]],
    unfixable: list[UnrepairedLink],
) -> int:
    """
    Último recurso: reasigna por solape de palabras, exigiendo
    ``MIN_WORD_OVERLAP`` coincidencias y un único ganador claro.
    """
    print('[*] Fase 3: reparación por solape de palabras...')
    fixed = 0

    for md_file in targets:
        content = md_file.read_text(encoding='utf-8')
        new_content = content
        changed = False

        for link in _iter_broken_links(content, md_file):
            search_words = link_words(Path(link.path).name) | link_words(link.match.group(1))
            if len(search_words) < MIN_WORD_OVERLAP:
                continue

            lower_find = Path(link.path).name.lower()
            scored: list[tuple[float, Path]] = []
            for path, words, lower_name in by_words:
                score = float(len(search_words & words))
                if score < MIN_WORD_OVERLAP:
                    continue
                if lower_find and (lower_find in lower_name or lower_name in lower_find):
                    score += 3.0
                scored.append((score, path))

            if not scored:
                unfixable.append(UnrepairedLink(
                    str(md_file.relative_to(docs_dir)), link.url,
                    f'sin candidato con al menos {MIN_WORD_OVERLAP} palabras en común',
                ))
                continue

            best_score = max(score for score, _ in scored)
            best = [path for score, path in scored if score == best_score]
            if len(best) != 1:
                unfixable.append(UnrepairedLink(
                    str(md_file.relative_to(docs_dir)), link.url,
                    f'empate entre {len(best)} candidatos con la misma puntuación',
                ))
                continue

            new_rel = get_relative_posix(md_file.parent, best[0])
            if link.anchor:
                new_rel += '#' + link.anchor
            if new_rel == link.url:
                continue
            nuevo = build_link(link.match.group(1), new_rel, link.title)
            new_content = (new_content[:link.match.start()] + nuevo
                           + new_content[link.match.end():])
            fixed += 1
            changed = True

        if changed:
            md_file.write_text(new_content, encoding='utf-8')

    print(f'    Enlaces reasignados por solape: {fixed}')
    return fixed


# ---------------------------------------------------------------------------
# Fase 4: validación
# ---------------------------------------------------------------------------

def phase_validation(docs_dir: Path) -> list[dict[str, str]]:
    """
    Recorre toda la documentación y devuelve los enlaces que siguen rotos.

    Solo mira; ni repara ni escribe. Componer el informe es de
    ``build_broken_links_report`` y guardarlo, de ``RunLogs``.
    """
    print('[*] Fase 4: validación final...')

    # Absoluta siempre: los destinos se resuelven con .resolve() y hay que
    # poder compararlos con esta raíz para saber a qué categoría apuntan.
    docs_dir = Path(docs_dir).resolve()
    broken_links: list[dict[str, str]] = []

    for md_file in docs_dir.rglob('*.md'):
        content = md_file.read_text(encoding='utf-8')
        clean_content = CODE_BLOCK_RX.sub('CODE_BLOCK_PLACEHOLDER', content)
        clean_content = INLINE_CODE_RX.sub('INLINE_CODE_PLACEHOLDER', clean_content)

        for match in LINK_RX.finditer(clean_content):
            url, _title = split_link_target(match.group(2))
            if not url or _is_external(url):
                continue

            path_part, _ = _split_anchor(url)
            if not path_part:
                continue

            target = (md_file.parent / unquote(path_part)).resolve()
            if target.exists():
                continue
            if not target.suffix:
                continue  # ruta de carpeta: MkDocs la resuelve en el build

            # El primer tramo del destino es su categoría, que es como se
            # agrupa el informe: los enlaces a un mismo producto se sustituyen
            # todos por la misma URL base, así que van juntos.
            try:
                destino = target.relative_to(docs_dir).parts[0]
            except ValueError:
                destino = '(fuera de docs/)'

            broken_links.append({
                'file': str(md_file.relative_to(docs_dir)),
                'link': url,
                'text': match.group(1).strip(),
                'target': destino,
            })

    print(f'    Enlaces rotos que quedan: {len(broken_links)}')
    return broken_links


def build_broken_links_report(
    broken_links: list[dict[str, str]],
    unfixable: Iterable[UnrepairedLink] = (),
) -> list[str]:
    """
    Compone el informe de enlaces rotos, agrupado por destino.

    Estos enlaces se arreglan **a mano**, cambiando el destino por la URL del
    sitio del producto correspondiente. Por eso van agrupados por categoría de
    destino y no por fichero de origen: todos los de un mismo producto llevan
    la misma URL base, así que se sustituyen de una sentada.

    ``unfixable`` aporta el motivo por el que la reparación automática no pudo
    con cada uno, cuando ese enlace estaba entre los ficheros de la ejecución.
    """
    if not broken_links:
        return []

    motivos = {(item.file, item.url): item.cause for item in unfixable}

    grupos: dict[str, list[dict[str, str]]] = {}
    for item in broken_links:
        grupos.setdefault(item['target'], []).append(item)

    lineas = [
        f'{len(broken_links)} enlaces apuntan a un .md que no existe en docs/.',
        '',
        'Se corrigen a mano: hay que sustituir el destino por la URL del sitio',
        'de ese producto, por ejemplo',
        '    https://ayuda.ahora.es/Flexygo/9.x/Installation/CreatingProduct/',
        '',
        'Van agrupados por destino porque todos los de un mismo grupo llevan la',
        'misma URL base. Un destino que aún no se ha generado no es un error del',
        'artículo: es documentación que todavía no está publicada.',
        '',
    ]

    for destino in sorted(grupos, key=lambda k: (-len(grupos[k]), k)):
        items = grupos[destino]
        lineas += ['-' * 70, f'DESTINO: {destino}   ({len(items)} enlaces)', '-' * 70, '']

        for item in sorted(items, key=lambda i: i['file']):
            lineas.append(item['file'])
            if item['text']:
                lineas.append(f"    texto  : {item['text']}")
            lineas.append(f"    destino: {item['link']}")
            motivo = motivos.get((item['file'], item['link']))
            if motivo:
                lineas.append(f'    motivo : {motivo}')
            lineas.append('')

    return lineas


# ---------------------------------------------------------------------------
# Orquestación
# ---------------------------------------------------------------------------

def run_pipeline(
    docs_dir: Path,
    only_files: Optional[Iterable[Path]] = None,
    *,
    skip_fuzzy: bool = False,
    skip_validation: bool = False,
    logs: Optional[RunLogs] = None,
) -> dict[str, int]:
    """
    Ejecuta el pipeline completo y devuelve un resumen numérico.

    ``logs`` son los informes de la ejecución. ``migrate.py`` pasa los suyos para
    que todo acabe en la misma carpeta; lanzado a mano se usan los del
    repositorio.
    """
    docs_dir = Path(docs_dir).resolve()
    if not docs_dir.exists():
        raise FileNotFoundError(f'El directorio {docs_dir} no existe.')

    if logs is None:
        logs = RunLogs(BASE_DIR)

    summary = {'patched': 0, 'broken': 0, 'fixed_exact': 0, 'fixed_overlap': 0, 'still_broken': 0}
    summary['patched'] = phase_known_link_fixes(docs_dir)

    #: Motivos por los que las fases 2 y 3 no pudieron con un enlace. Se
    #: guardan para anotarlos en el informe final, que es uno solo.
    unfixable: list[UnrepairedLink] = []

    if not skip_fuzzy:
        targets = _resolve_targets(docs_dir, only_files)
        print(f'[*] Ficheros a revisar: {len(targets)}')
        if targets:
            by_name, by_words = _build_file_index(docs_dir)
            broken, fixed_exact = phase_exact_name_repair(docs_dir, targets, by_name, unfixable)
            fixed_overlap = phase_overlap_repair(docs_dir, targets, by_words, unfixable)
            summary.update(broken=broken, fixed_exact=fixed_exact, fixed_overlap=fixed_overlap)

    # Después de intentar repararlos: lo que apunta a una carpeta no tiene
    # artículo al que reapuntar, así que se queda en texto en vez de publicar
    # un 404.
    a_categoria = phase_unwrap_folder_links(docs_dir, only_files)
    summary['folders_unwrapped'] = len(a_categoria)
    escrito = logs.write(
        ENLACES_A_CATEGORIA,
        'ENLACES A UNA CARPETA DE CATEGORÍA, DEJADOS EN TEXTO',
        build_category_links_report(a_categoria),
    )
    if escrito:
        print(f'[*] Informe de enlaces a categoría en: {escrito}')

    if not skip_validation:
        broken_links = phase_validation(docs_dir)
        summary['still_broken'] = len(broken_links)
        escrito = logs.write(
            ENLACES_ROTOS,
            'ENLACES QUE APUNTABAN A DOCUMENTACIÓN QUE NO ESTÁ EN docs/',
            build_broken_links_report(broken_links, unfixable),
        )
        if escrito:
            print(f'[*] Informe de enlaces rotos en: {escrito}')

        # Se anotan primero y se degradan después: el informe tiene que decir
        # qué había, porque una vez en texto ya no se ve.
        summary['dead_unwrapped'] = phase_unwrap_dead_links(docs_dir, only_files)

    # Después de degradar las muertas, las anclas HTML que quedan sí tienen
    # destino: hay que darles la forma con la que se publican.
    summary['html_links_published'] = phase_publish_html_links(docs_dir, only_files)

    # Lo último de todo, y tiene que ser lo último: cada fase de arriba deja
    # una línea vacía detrás al degradar una URL o quitar un enlace. Así el
    # resultado es idempotente.
    summary['blank_lines_tidied'] = phase_tidy_blank_lines(docs_dir, only_files)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description='Pipeline de reparación y validación de enlaces.')
    parser.add_argument('--docs-dir', default=str(DEFAULT_DOCS_DIR), help='Directorio de documentación')
    parser.add_argument('--skip-fuzzy', action='store_true', help='Saltar la reparación de enlaces rotos')
    parser.add_argument('--skip-validation', action='store_true', help='Saltar la validación final')
    args = parser.parse_args()

    # Ejecutado a mano, siempre revisa toda la documentación.

    summary = run_pipeline(
        Path(args.docs_dir),
        only_files=None,
        skip_fuzzy=args.skip_fuzzy,
        skip_validation=args.skip_validation,
    )

    print('\n[OK] Pipeline finalizado.')
    print(f'    Ficheros parcheados:        {summary["patched"]}')
    print(f'    Enlaces rotos detectados:   {summary["broken"]}')
    print(f'    Reparados por nombre:       {summary["fixed_exact"]}')
    print(f'    Reparados por solape:       {summary["fixed_overlap"]}')
    print(f'    Siguen rotos:               {summary["still_broken"]}')


if __name__ == '__main__':
    main()
