"""
migrate.py
==========
Genera la estructura ``docs/CATEGORIA/CARPETA/ARTICULO.md`` a partir de los
artículos de Freshdesk almacenados en SQL Server.

Este script es el único orquestador del pipeline. Cada artículo se convierte
con uno de los dos motores de ``converters.py``:

- ``convert_author``   si el artículo está atribuido a un autor con HTML
  troceado (ver ``AUTHOR_MARKERS``).
- ``convert_standard`` en el resto de casos.

Antes, los artículos de autor se generaban dos veces: ``migrate.py`` los
escribía con el motor estándar y después ``author_articles.py`` los
sobrescribía con el suyo, ya por detrás de la reparación de enlaces. Ahora se
elige el motor una sola vez, antes de escribir, y la reparación de enlaces es
siempre la última fase.

Requiere Python 3.12 o superior.

Uso:
    python migrate.py --product "ERP"
    python migrate.py --categories "Actualizador"
    python migrate.py --all --clean-output
"""

from __future__ import annotations

import argparse
import collections
import html as html_lib
import json
import re
import shutil
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote
from typing import Iterable, Optional

import pyodbc

from pipeline.common import (
    buscar_videos_que_no_se_ven,
    build_article_lookup_keys,
    front_matter,
    contar_enlaces_freshdesk,
    fix_internal_links,
    get_safe_filename,
    resolve_connection_string,
)
from pipeline.converters import convert_author, convert_standard
from pipeline.generation_state import (
    RunState,
    calcular_huella_pipeline,
    finalize_generation_state,
    find_orphan_articles,
    find_relocated_articles,
    get_run_state_path,
    get_state_path,
    load_generation_state,
    pipeline_ha_cambiado,
    should_generate_article,
)
from pipeline.reporting import (
    ARTICULOS_CON_ERROR,
    ENLACES_FRESHDESK,
    ADJUNTOS_NO_PUBLICADOS,
    IMAGENES_HUERFANAS,
    IMAGENES_NO_DESCARGADAS,
    VIDEOS_QUE_NO_SE_VEN,
    RESUMEN,
    TITULOS_DUPLICADOS,
    RunLogs,
)
from pipeline.repair_links import (
    es_portada_generada,
    escribir_portadas_del_arbol,
    run_pipeline,
)

#: Marcas que identifican artículos cuyo HTML necesita el motor de autor.
#: Se comparan en minúsculas sobre el ``Description`` ya des-escapado.
AUTHOR_MARKERS = ('autor: daniel',)

UNKNOWN_CATEGORY = 'Categoria_Desconocida'
UNKNOWN_FOLDER = 'Carpeta_Desconocida'

#: Valor de ``status`` que Freshdesk da a los borradores. Publicado es 2.
#: Solo se filtra por este valor exacto: si algún día la clave del JSON cambia
#: de nombre, el peor caso es no filtrar nada (lo que se hacía hasta ahora),
#: no omitir en silencio los 2.298 artículos.
DRAFT_STATUS = 1
DEFAULT_STATUS = 2

#: Contenido de ``docs/`` que NO es generado y que ``--clean-output`` no puede
#: tocar: son ficheros versionados (tema, estáticos, portadas de idioma).
PRESERVED_IN_DOCS = frozenset({
    'docs_assets', 'javascripts', 'stylesheets',
    'index.md', 'index.es.md', 'index.en.md',
    'cleanup_docs_folders.ps1',
})


def clean_generated_docs(docs_folder: Path) -> int:
    """
    Borra las carpetas de categoría generadas, dejando intacto lo versionado.

    Antes esto era un ``shutil.rmtree(docs)`` que se llevaba por delante el
    tema, los estáticos y las portadas de idioma, todos ellos ficheros del
    repositorio.
    """
    if not docs_folder.exists():
        return 0

    removed = 0
    for entry in docs_folder.iterdir():
        if entry.name in PRESERVED_IN_DOCS:
            continue
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()
        removed += 1
    return removed


def build_run_report(counts: dict[str, int]) -> list[str]:
    """
    Compone el parte de la ejecución: qué ha cambiado respecto a la semana pasada.

    Es lo que se lee de un vistazo para saber si la ejecución ha ido bien, y lo
    que se pega en el mensaje del commit de la documentación. Devuelve solo el
    cuerpo: la cabecera con la fecha la pone ``RunLogs``.
    """
    # Se lee con .get: al final de una ejecución de horas, un contador que falte
    # no puede tirar el informe entero.
    filas = [
        ('Artículos nuevos', counts.get('nuevos', 0)),
        ('Artículos actualizados', counts.get('actualizados', 0)),
        ('Artículos movidos o renombrados', counts.get('movidos', 0)),
        ('Artículos retirados', counts.get('retirados', 0)),
        ('Borradores omitidos', counts.get('borradores', 0)),
        ('Errores de conversión', counts.get('errores', 0)),
        ('Enlaces internos resueltos', counts.get('enlaces', 0)),
        ('URLs de Freshdesk sin traducir', counts.get('freshdesk', 0)),
    ]
    ancho = max(len(nombre) for nombre, _ in filas)

    lineas = [f'{nombre.ljust(ancho)} : {valor}' for nombre, valor in filas]

    if counts.get('pendientes_de_borrar'):
        lineas += [
            '',
            f'{counts.get("pendientes_de_borrar", 0)} ficheros sobran en docs/ y NO se han borrado.',
            'Repite la orden con --prune-orphans para retirarlos.',
        ]
    if counts.get('errores'):
        lineas += ['', 'Los artículos con error se reintentarán en la próxima ejecución.']

    return lineas


def _remove_empty_parents(path: Path, stop_at: Path) -> None:
    """Sube borrando los directorios que hayan quedado vacíos tras un borrado."""
    stop_at = stop_at.resolve()
    parent = path.parent.resolve()
    while stop_at in parent.parents:
        # Si lo único que queda es la portada que escribimos nosotros, la
        # carpeta está vacía a todos los efectos: su index.md solo listaba los
        # artículos que se acaban de borrar. Sin esto, rmdir falla y en el
        # panel de navegación se queda una sección con una página en blanco.
        restos = list(parent.iterdir())
        if (len(restos) == 1 and restos[0].name.lower() == 'index.md'
                and es_portada_generada(restos[0])):
            restos[0].unlink()
        try:
            parent.rmdir()
        except OSError:
            return
        parent = parent.parent


def delete_generated_md(rel_path: str, output_dir: Path, docs_folder: Path) -> bool:
    """Borra un ``.md`` generado y limpia su carpeta si se queda vacía."""
    target = output_dir / str(rel_path or '')
    if target.suffix.lower() != '.md' or not target.exists():
        return False
    target.unlink()
    _remove_empty_parents(target, docs_folder)
    return True


# ---------------------------------------------------------------------------
# Modelo
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class Article:
    """Un artículo de Freshdesk ya normalizado desde su JSON."""

    article_id: str
    title: str
    description: str
    category_id: str
    folder_id: str
    updated_at: str
    #: Estado en Freshdesk. Lleva valor por defecto porque hay tests que
    #: construyen ``Article`` a mano.
    status: int = DEFAULT_STATUS
    #: Ficheros colgados del artículo en Freshdesk. No se publican —su URL es
    #: un enlace firmado de S3 que caduca a los 5 minutos—, así que lo único
    #: que se puede hacer con ellos es dejarlos anotados.
    attachments: tuple = ()

    @property
    def is_draft(self) -> bool:
        return self.status == DRAFT_STATUS

    @property
    def uses_author_engine(self) -> bool:
        if not self.description:
            return False
        lowered = html_lib.unescape(self.description).lower()
        return any(marker in lowered for marker in AUTHOR_MARKERS)




def _tamano_legible(bytes_) -> str:
    """El tamaño de un fichero, con la coma decimal y el punto de los miles."""
    try:
        n = int(bytes_ or 0)
    except (TypeError, ValueError):
        return 'tamaño desconocido'
    if n >= 1024 * 1024:
        cifra, unidad = n / (1024 * 1024), 'MB'
    else:
        cifra, unidad = n / 1024, 'KB'
    return f'{cifra:,.1f}'.translate(str.maketrans(',.', '.,')) + f' {unidad}'



#: Cualquier mención a un fichero de ``docs_assets/images``, venga de donde
#: venga: un ``![](...)``, un ``<img src>``, un enlace a la imagen, el logo de
#: ``mkdocs.yml`` o un ``url()`` de una hoja de estilos. Se queda con la parte
#: que va DESPUÉS de la carpeta, que es lo único estable entre ficheros: la
#: parte de delante son los ``../..`` que dependen de dónde esté el artículo.
_MENCION_DE_IMAGEN_RX = re.compile(
    r'(?i)docs_assets/images/([^\s"\'()<>\]]+)')

#: Dónde se puede mencionar una imagen sin que sea un artículo. Sin mirar aquí,
#: el logo y el favicon del tema saldrían huérfanos en la primera ejecución.
_FUERA_DE_DOCS = ('mkdocs.yml', 'overrides/**/*.html', 'docs/**/*.css',
                  'docs/**/*.js')


def buscar_imagenes_huerfanas(docs_folder: Path, images_folder: Path) -> list[Path]:
    """
    Las imágenes descargadas que ya no menciona nadie.

    Cada ejecución descarga las imágenes de los artículos que publica, pero
    nunca retiraba las de los que dejaron de publicarse —un artículo pasado a
    borrador, una captura sustituida por otra—. Medido sobre el corpus: 789
    ficheros y 54 MB, el 14 % de la carpeta.

    Se busca la mención en **todo** lo que puede apuntar a una imagen, no solo
    en los ``.md``: ``mkdocs.yml`` declara el logo y el favicon, y una hoja de
    estilos puede traer un ``url()``. Sin eso, la primera ejecución se llevaría
    por delante el logo del tema.

    Devuelve las rutas; no borra nada. Quien decide es ``--prune-orphans``.
    """
    if not images_folder.is_dir():
        return []

    raiz = Path('.')
    mencionadas: set[str] = set()

    def apuntar(texto: str) -> None:
        for m in _MENCION_DE_IMAGEN_RX.finditer(texto):
            ruta = m.group(1).split('#')[0].split('?')[0]
            if ruta:
                mencionadas.add(unquote(ruta).replace('\\', '/').lower())

    for md in docs_folder.rglob('*.md'):
        try:
            apuntar(md.read_text(encoding='utf-8'))
        except OSError:
            continue
    for patron in _FUERA_DE_DOCS:
        for otro in raiz.glob(patron):
            if otro.is_file():
                try:
                    apuntar(otro.read_text(encoding='utf-8', errors='replace'))
                except OSError:
                    continue

    huerfanas = []
    for fichero in sorted(images_folder.rglob('*')):
        if not fichero.is_file():
            continue
        rel = fichero.relative_to(images_folder).as_posix().lower()
        if rel not in mencionadas:
            huerfanas.append(fichero)
    return huerfanas


def _tamano_de_imagenes(ficheros: list[Path]) -> int:
    total = 0
    for f in ficheros:
        try:
            total += f.stat().st_size
        except OSError:
            pass
    return total


def lineas_de_imagenes_huerfanas(huerfanas: list[Path], images_folder: Path,
                                 borradas: bool) -> list[str]:
    """El informe de las imágenes que ya no usa ningún artículo."""
    if not huerfanas:
        return []
    peso = _tamano_de_imagenes(huerfanas)
    if borradas:
        cabecera = [f'Se han retirado {len(huerfanas)} imágenes que ya no menciona '
                    f'ningún artículo ({_tamano_legible(peso)}).', '']
    else:
        cabecera = [
            f'{len(huerfanas)} imágenes de docs_assets/images ya no las menciona '
            f'ningún artículo ({_tamano_legible(peso)}).',
            '',
            'Son de artículos que pasaron a borrador o se retiraron, y de capturas',
            'que el autor sustituyó por otras. No se han borrado.',
            '',
            'Repite la orden con --prune-orphans para retirarlas.',
            '',
        ]
    return cabecera + [f'  {f.relative_to(images_folder).as_posix()}'
                       for f in huerfanas]


def lineas_de_videos(docs_folder) -> list[str]:
    """
    Anota los vídeos enlazados que ya no se pueden ver.

    Un vídeo roto no se nota: el hueco del reproductor sale en blanco y el
    enlace parece bueno hasta que alguien lo pulsa. Y no hay forma de saberlo
    sin preguntar, porque el problema está fuera de esta documentación.

    Se pregunta por cada uno: a YouTube por su ``oembed``, que responde 404 si
    el vídeo ya no existe y 401/403 si es privado, y al resto de servidores
    por HTTP. Un servidor que no contesta se prueba **una vez** y su veredicto
    vale para todos sus enlaces: si no, los 44 de ``videos.ahora.es`` harían
    esperar seis segundos cada uno.
    """
    rotos, se_ven = buscar_videos_que_no_se_ven(Path(docs_folder))
    if not rotos:
        return []

    articulos = {a for _, _, arts in rotos for a in arts}
    lineas = [
        f'{len(rotos)} de los {len(rotos) + se_ven} vídeos enlazados ya no se ven,',
        f'y aparecen en {len(articulos)} artículos.',
        '',
        'Esto no se puede arreglar desde aquí: o se sustituye el vídeo en el',
        'artículo de Freshdesk, o se quita el enlace.',
        '',
    ]
    motivo_previo = None
    for url, motivo, arts in rotos:
        if motivo != motivo_previo:
            lineas += [motivo.upper(), '-' * 70]
            motivo_previo = motivo
        lineas.append(url)
        for art in arts:
            lineas.append(f'    {art}')
        lineas.append('')
    return lineas


def lineas_de_adjuntos(articulos) -> list[str]:
    """
    Anota los ficheros colgados de un artículo, que no se pueden publicar.

    Freshdesk sirve los adjuntos con un **enlace firmado de S3 que caduca a
    los 5 minutos** (``X-Amz-Expires=300``). El de la base de datos lleva
    caducado desde el momento en que se guardó: comprobado, responde 403 con
    firma y sin ella. Las imágenes del cuerpo sí son públicas, y por eso esas
    sí se descargan.

    Así que aquí no hay nada que descargar y publicar un enlace sería publicar
    un 404. Lo único honesto es dejar constancia: son 41 ficheros en 17
    artículos, y varios son contenido de verdad —``sacar usuarios SQL.sql``,
    dos fuentes ``.ttf``, 13 PDF—.

    El arreglo de verdad no cabe en este repositorio: tiene que hacerlo el
    proceso que rellena ``freshdesk_articles``, bajándose el fichero mientras
    la URL sigue viva.
    """
    con_adjuntos = [a for a in articulos if a.attachments]
    if not con_adjuntos:
        return []

    total = sum(len(a.attachments) for a in con_adjuntos)
    plural = 'artículo' if len(con_adjuntos) == 1 else 'artículos'
    lineas = [
        'Freshdesk sirve los adjuntos con un enlace firmado que caduca a los 5',
        'minutos, así que el que hay en la base de datos ya no vale (403) y no',
        'se pueden descargar desde aquí. Para publicarlos, el proceso que carga',
        'freshdesk_articles tiene que bajárselos mientras la URL sigue viva.',
        '',
        f'{total} ficheros en {len(con_adjuntos)} {plural}.',
        '',
    ]
    for articulo in sorted(con_adjuntos, key=lambda a: a.title.lower()):
        lineas.append(f'Artículo: {articulo.title}  ({articulo.article_id})')
        for adjunto in articulo.attachments:
            nombre = adjunto.get('name') or '(sin nombre)'
            lineas.append(f'  {nombre}  ({_tamano_legible(adjunto.get("size"))})')
        lineas.append('')
    return lineas


def _parse_article(raw: str) -> Optional[Article]:
    """Convierte una fila JSONDATA en un ``Article``; devuelve None si no vale."""
    if not raw or not raw.strip():
        return None
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None

    article_id = data.get('Id') or data.get('id')
    if article_id is None:
        return None

    # El resto del JSON viene en PascalCase (``Id``, ``Title``, ``CategoryId``),
    # así que se tantea ese primero. Ante cualquier duda, "publicado".
    try:
        status = int(data.get('Status') or data.get('status') or DEFAULT_STATUS)
    except (TypeError, ValueError):
        status = DEFAULT_STATUS

    return Article(
        article_id=str(article_id).strip(),
        title=data.get('Title') or data.get('title') or '',
        description=str(data.get('Description') or data.get('description') or ''),
        category_id=str(data.get('CategoryId') or data.get('category_id') or ''),
        folder_id=str(data.get('FolderId') or data.get('folder_id') or ''),
        updated_at=str(data.get('updated_at') or data.get('UpdatedAt') or ''),
        status=status,
        attachments=tuple(data.get('attachments') or data.get('Attachments') or ()),
    )


# ---------------------------------------------------------------------------
# Lectura de la BDD
# ---------------------------------------------------------------------------

def load_categories(cursor) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """Devuelve (nombre_seguro, nombre_original, producto) indexados por id."""
    safe_names: dict[str, str] = {}
    raw_names: dict[str, str] = {}
    products: dict[str, str] = {}

    cursor.execute('SELECT JSONDATA, Product FROM [dbo].[freshdesk_categories] WHERE JSONDATA IS NOT NULL')
    for row in cursor.fetchall():
        try:
            data = json.loads(row[0])
        except (json.JSONDecodeError, TypeError):
            continue
        cid = str(data.get('Id') or data.get('id') or '')
        if not cid:
            continue
        name = data.get('Name') or data.get('name') or ''
        safe_names[cid] = get_safe_filename(name, f'Categoria_{cid}')
        raw_names[cid] = str(name)
        products[cid] = str(row[1] or '').strip() if len(row) > 1 else ''

    return safe_names, raw_names, products


def load_folders(cursor, docs_folder: Path, categories: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    """Devuelve (nombre_seguro por id, ruta absoluta de la carpeta por id)."""
    names: dict[str, str] = {}
    paths: dict[str, str] = {}

    cursor.execute('SELECT JSONDATA FROM [dbo].[freshdesk_folders] WHERE JSONDATA IS NOT NULL')
    for row in cursor.fetchall():
        try:
            data = json.loads(row[0])
        except (json.JSONDecodeError, TypeError):
            continue
        fid = str(data.get('Id') or data.get('id') or '')
        if not fid:
            continue
        safe_name = get_safe_filename(data.get('Name') or data.get('name') or '', f'Carpeta_{fid}')
        names[fid] = safe_name
        cat_id = str(data.get('CategoryId') or data.get('category_id') or '')
        if cat_id in categories:
            paths[fid] = str((docs_folder / categories[cat_id] / safe_name).resolve())

    return names, paths


def load_articles(cursor) -> list[Article]:
    cursor.execute('SELECT JSONDATA FROM [dbo].[freshdesk_articles] WHERE JSONDATA IS NOT NULL')
    articles = [_parse_article(row[0]) for row in cursor.fetchall()]
    return [a for a in articles if a is not None]


# ---------------------------------------------------------------------------
# Selección de categorías
# ---------------------------------------------------------------------------

def select_categories(
    args: argparse.Namespace,
    raw_names: dict[str, str],
    products: dict[str, str],
) -> tuple[list[str], list[str]]:
    """Resuelve el filtro del usuario a una lista de ids y nombres de categoría."""
    selected_ids: list[str] = []

    if args.product:
        for cid, product in products.items():
            match = (args.product.lower() in product.lower()) if args.product_contains \
                else (product.lower() == args.product.lower())
            if match and cid not in selected_ids:
                selected_ids.append(cid)
        if not selected_ids:
            raise SystemExit(f'No se encontraron categorías para el producto: {args.product}')

    elif args.categories:
        for wanted in args.categories:
            for cid, name in raw_names.items():
                match = (wanted.lower() in name.lower()) if args.category_contains \
                    else (name.lower() == wanted.lower())
                if match and cid not in selected_ids:
                    selected_ids.append(cid)
        if not selected_ids:
            raise SystemExit(
                f'No se encontró ninguna categoría que coincida con: {", ".join(args.categories)}'
            )

    else:
        # --all: todas las categorías. selected_ids vacío significa "sin filtro",
        # así que aquí lo llenamos explícitamente para poder acotar los huérfanos.
        selected_ids = list(raw_names.keys())

    return selected_ids, [raw_names[cid] for cid in selected_ids]


def resolve_filters(args: argparse.Namespace) -> None:
    """
    Valida que haya un filtro. Solo pregunta por consola si hay terminal:
    en una ejecución desatendida, un ``input()`` colgaría el proceso.
    """
    if args.product or args.categories or args.all:
        return

    if sys.stdin is not None and sys.stdin.isatty():
        answer = input('Producto a generar (vacío = todas las categorías): ').strip()
        if answer:
            args.product = answer
            return
        args.all = True
        return

    raise SystemExit(
        'Hay que indicar qué generar: usa --product, --categories o --all.\n'
        'Sin terminal interactiva no se puede preguntar.'
    )


# ---------------------------------------------------------------------------
# Rutas de salida
# ---------------------------------------------------------------------------

def categoria_que_no_hace_carpeta(
    args: argparse.Namespace,
    selected_ids: list[str],
) -> str:
    """
    La categoría cuyo nivel NO se crea, o ``''`` si se crean todos.

    Cuando se genera **un solo producto** y ese producto tiene **una sola
    categoría**, la carpeta de la categoría no aporta nada: todo el sitio es
    ese producto, y el lector se come un nivel de más para llegar a cualquier
    artículo. En ese caso las carpetas suben a la raíz de ``docs/``.

    Se mira el ámbito de la ejecución, no solo la BDD, porque hay nombres de
    carpeta que se repiten entre productos —``Versiones`` está en Sebastian
    HR, en Bruno GMAO y en Flexygo, y ``¿Sabías que...`` en SAT, CRM y
    Flexygo—. Quitando el nivel siempre, generar dos de esos productos en el
    mismo ``docs/`` los mezclaría en una única carpeta.

    Cambiar el ámbito mueve los ficheros de sitio, pero eso ya está resuelto:
    ``find_relocated_articles`` los detecta como reubicados y
    ``--prune-orphans`` retira los que quedaron atrás.
    """
    if not getattr(args, 'product', None):
        return ''
    return selected_ids[0] if len(selected_ids) == 1 else ''


def _naive_output_path(
    article: Article,
    docs_folder: Path,
    categories: dict[str, str],
    folders: dict[str, str],
    sin_carpeta: str = '',
) -> Path:
    """Ruta que le tocaría al artículo si su título fuese único."""
    cat_name = categories.get(article.category_id, UNKNOWN_CATEGORY)
    folder_name = folders.get(article.folder_id, UNKNOWN_FOLDER)
    clean_title = get_safe_filename(article.title, f'Articulo_{article.article_id}')
    if sin_carpeta and article.category_id == sin_carpeta:
        return docs_folder / folder_name / f'{clean_title}.md'
    return docs_folder / cat_name / folder_name / f'{clean_title}.md'


def assign_output_paths(
    articles: Iterable[Article],
    docs_folder: Path,
    categories: dict[str, str],
    folders: dict[str, str],
    sin_carpeta: str = '',
) -> tuple[dict[str, Path], list[list[Article]]]:
    """
    Asigna a cada artículo una ruta de salida ÚNICA.

    Hay artículos distintos que comparten título dentro de la misma carpeta (y
    hay títulos que colisionan porque dos carpetas distintas se llaman igual).
    Antes se escribían todos sobre el mismo ``.md`` y solo sobrevivía el
    último: contenido perdido en silencio.

    Ahora, dentro de un grupo en conflicto, el artículo de id más bajo conserva
    el nombre limpio —para no renombrar lo ya publicado— y al resto se les
    añade su ``ArticleId``. El reparto se hace sobre TODOS los artículos, no
    solo sobre los del filtro, para que sea estable entre ejecuciones.

    Devuelve (rutas por id, grupos en conflicto).
    """
    grouped: dict[Path, list[Article]] = {}
    for article in articles:
        grouped.setdefault(
            _naive_output_path(article, docs_folder, categories, folders, sin_carpeta),
            [],
        ).append(article)

    paths: dict[str, Path] = {}
    collisions: list[list[Article]] = []

    for path, group in grouped.items():
        if len(group) == 1:
            paths[group[0].article_id] = path
            continue

        ordered = sorted(group, key=lambda a: a.article_id)
        collisions.append(ordered)
        for position, article in enumerate(ordered):
            if position == 0:
                paths[article.article_id] = path
            else:
                paths[article.article_id] = path.with_name(f'{path.stem} ({article.article_id}).md')

    return paths, collisions


def build_link_indexes(
    articles: Iterable[Article],
    paths: dict[str, Path],
) -> tuple[dict[str, str], dict[str, str]]:
    """Precalcula las rutas de destino para poder resolver enlaces internos."""
    by_id: dict[str, str] = {}
    by_title: dict[str, str] = {}

    for article in articles:
        target = paths.get(article.article_id)
        if target is None:
            continue
        path_abs = str(target.resolve())
        by_id[article.article_id] = path_abs
        for key in build_article_lookup_keys(article.title):
            by_title.setdefault(key, path_abs)

    return by_id, by_title


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Genera la estructura MkDocs docs/CATEGORIA/CARPETA/ARTICULO.md desde SQL Server.'
    )
    parser.add_argument('--connection-string', help='ODBC connection string de SQL Server')
    parser.add_argument('--env-file', default='.env', help='Archivo .env con la connection string')
    parser.add_argument('--output-dir', default='.', help='Directorio base donde se generará docs/')
    parser.add_argument('--categories', nargs='*', default=[], help='Filtrar por nombre de categoría')
    parser.add_argument('--category-contains', action='store_true', help='Coincidencia parcial de categoría')
    parser.add_argument('--product', default='', help='Filtrar por producto de la categoría')
    parser.add_argument('--product-contains', action='store_true', help='Coincidencia parcial de producto')
    parser.add_argument('--all', action='store_true', help='Generar todas las categorías')
    parser.add_argument('--clean-output', action='store_true', help='Borrar docs/ antes de generar')
    parser.add_argument('--force', action='store_true', help='Ignorar el estado incremental y regenerar todo')
    parser.add_argument(
        '--only-author', action='store_true',
        help='Generar solo los artículos que usan el motor de autor',
    )
    parser.add_argument(
        '--skip-author', action='store_true',
        help='Saltar los artículos que usan el motor de autor',
    )
    parser.add_argument(
        '--include-drafts', action='store_true',
        help='Generar también los borradores (status=1). Por defecto se omiten.',
    )
    parser.add_argument(
        '--sin-comprobar-videos', action='store_true',
        help='No preguntar a YouTube ni a videos.ahora.es si los vídeos siguen ahí',
    )
    parser.add_argument(
        '--prune-orphans', action='store_true',
        help='Borrar los .md que sobran: artículos eliminados en origen, movidos o renombrados',
    )
    parser.add_argument('--skip-link-repair', action='store_true', help='No ejecutar la reparación de enlaces')
    parser.add_argument(
        '--list-products', action='store_true',
        help='Listar los productos disponibles y salir (lo usa run.ps1 para su menú)',
    )
    return parser


def list_products(connection_string: str) -> int:
    """
    Escribe la lista de productos, uno por línea: ``producto|categorías|artículos``.

    Formato pensado para que ``run.ps1`` lo parta y monte su menú, pero legible
    también a ojo desde la consola.
    """
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        categories, _, products = load_categories(cursor)
        articles = [a for a in load_articles(cursor) if not a.is_draft]
        cursor.close()

    por_producto: dict[str, list[str]] = {}
    for category_id, product in products.items():
        por_producto.setdefault(product or '(sin producto)', []).append(category_id)

    for product, category_ids in sorted(por_producto.items()):
        ids = set(category_ids)
        total = sum(1 for a in articles if a.category_id in ids)
        print(f'{product}|{len(ids)}|{total}')

    return 0


def main(args: Optional[argparse.Namespace] = None) -> int:
    if args is None:
        args = build_parser().parse_args()

    if args.list_products:
        return list_products(resolve_connection_string(args.connection_string, Path(args.env_file)))

    resolve_filters(args)

    if args.only_author and args.skip_author:
        raise SystemExit('--only-author y --skip-author son incompatibles.')

    print('=====================================================')
    print(' Generando estructura MkDocs (Categoría > Carpeta) ')
    print('=====================================================')

    env_file = Path(args.env_file)
    connection_string = resolve_connection_string(args.connection_string, env_file)
    output_dir = Path(args.output_dir)
    docs_folder = output_dir / 'docs'
    images_folder = docs_folder / 'docs_assets' / 'images'

    # Los informes de la ejecución anterior se retiran ya: lo que quede en
    # logs/ al terminar es de esta ejecución y solo de esta.
    logs = RunLogs(output_dir)
    logs.clear()

    generation_state = load_generation_state(output_dir)
    incremental_mode = get_state_path(output_dir).exists() and not args.force

    if args.clean_output:
        removed = clean_generated_docs(docs_folder)
        print(f'[*] Limpiadas {removed} entradas generadas de {docs_folder} '
              f'(se conservan {", ".join(sorted(PRESERVED_IN_DOCS))}).')
        incremental_mode = False
    docs_folder.mkdir(parents=True, exist_ok=True)

    # El estado incremental solo miraba el updated_at del artículo, así que un
    # arreglo del conversor o de los enlaces únicamente alcanzaba a los
    # artículos que por casualidad cambiaran en Freshdesk. La huella del código
    # cierra ese agujero: si el pipeline cambió, lo de disco ya no vale.
    huella = calcular_huella_pipeline()
    if incremental_mode and pipeline_ha_cambiado(generation_state, huella):
        print('[*] El pipeline ha cambiado desde la última ejecución: se regenera todo')
        print(f'    (huella {generation_state.get("meta", {}).get("pipeline_fingerprint") or "ninguna"}'
              f' → {huella})')
        incremental_mode = False

    if incremental_mode:
        last = generation_state.get('meta', {}).get('last_generated_at', '')
        print(f'[*] Modo incremental activo desde {last or "(sin fecha válida)"}')
    else:
        print('[*] Modo completo: se generará todo lo que encaje con el filtro.')

    # Si la ejecución anterior murió a medias (Ctrl-C, caída, corte de red al
    # descargar imágenes), su avance quedó en .generation_run_state.json. Se
    # reanuda en lugar de rehacer lo que ya estaba escrito en disco.
    aborted = get_run_state_path(output_dir).exists() and not args.force
    run_state = RunState(output_dir, resume=aborted)
    already_done: set[str] = set(run_state.articles()) if aborted else set()
    if already_done:
        print(f'[*] Se reanuda una ejecución interrumpida: {len(already_done)} artículos '
              f'ya generados que no se repiten.')
        print('    (usa --force para empezar de cero)')

    link_counter = [0]
    wiki_broken_images: list[tuple[str, str]] = []
    conversion_errors: list[tuple[str, str, str]] = []

    # ------------------------------------------------------------------
    # 1. Leer la BDD
    # ------------------------------------------------------------------
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()

        print('[*] Leyendo categorías...')
        categories, raw_names, products = load_categories(cursor)
        selected_ids, selected_names = select_categories(args, raw_names, products)
        print(f'[*] Categorías seleccionadas ({len(selected_ids)}): {", ".join(selected_names[:8])}'
              + (' ...' if len(selected_names) > 8 else ''))

        print('[*] Leyendo carpetas...')
        folders, folder_paths = load_folders(cursor, docs_folder, categories)

        # Una URL /support/solutions/<id> de Freshdesk es una CATEGORÍA, y su
        # equivalente local es la carpeta de esa categoría.
        category_paths = {
            cid: str((docs_folder / name).resolve()) for cid, name in categories.items()
        }

        print('[*] Leyendo artículos...')
        all_articles = load_articles(cursor)
        cursor.close()

    selected_id_set = set(selected_ids)
    # Un solo producto con una sola categoría: su carpeta no aporta nada y las
    # de dentro suben a la raíz de docs/.
    sin_carpeta = categoria_que_no_hace_carpeta(args, selected_ids)
    if sin_carpeta:
        print(f'[*] «{raw_names.get(sin_carpeta, sin_carpeta)}» es la única categoría de '
              f'este producto: sus carpetas van directas a docs/.')

    # ------------------------------------------------------------------
    # 1.b Borradores
    # ------------------------------------------------------------------
    # Un borrador de Freshdesk no es documentación publicable. Se apartan aquí
    # y NO en el SQL: el reparto de rutas necesita ver todos los artículos para
    # que los nombres sean estables entre ejecuciones (ver assign_output_paths).
    drafts = [a for a in all_articles if a.is_draft]
    if args.include_drafts:
        publishable = all_articles
        if drafts:
            print(f'[*] {len(drafts)} borradores INCLUIDOS por --include-drafts.')
    else:
        publishable = [a for a in all_articles if not a.is_draft]
        if drafts:
            print(f'[*] Omitidos {len(drafts)} borradores (status={DRAFT_STATUS}). '
                  f'Usa --include-drafts para incluirlos.')

    scoped_articles = [a for a in publishable if a.category_id in selected_id_set]

    if args.only_author:
        scoped_articles = [a for a in scoped_articles if a.uses_author_engine]
    elif args.skip_author:
        scoped_articles = [a for a in scoped_articles if not a.uses_author_engine]

    # ------------------------------------------------------------------
    # 2. Precalcular rutas para los enlaces internos
    # ------------------------------------------------------------------
    # El reparto de rutas se hace sobre TODOS los artículos —borradores
    # incluidos— para que el desempate de títulos duplicados no cambie según lo
    # que se genere en cada ejecución.
    #
    # El índice de enlaces, en cambio, solo lleva los publicables: incluye
    # artículos de categorías no seleccionadas (para que un enlace cruzado
    # resuelva), pero no borradores, porque su .md no existe en disco y el
    # enlace quedaría apuntando a la nada. Sin resolver, se conserva la URL
    # original y la fase de validación lo reporta.
    print('[*] Pre-calculando rutas para enlaces internos...')
    output_paths, collisions = assign_output_paths(
        all_articles, docs_folder, categories, folders, sin_carpeta)

    if sin_carpeta:
        # Su categoría ya no tiene página, así que un enlace a ella no tiene
        # a dónde ir. Se le manda a la primera carpeta del producto —la
        # primera por nombre, para que no dependa del orden de la BDD—, que
        # es lo más cerca que se puede llegar de "el principio de esto".
        primeras = sorted(
            p.parent.name for aid, p in output_paths.items()
            if p.parent.parent == docs_folder and p.parent != docs_folder
        )
        if primeras:
            category_paths[sin_carpeta] = str((docs_folder / primeras[0]).resolve())
            print(f'    Los enlaces a la categoría llevan a «{primeras[0]}».')
    paths_by_id, paths_by_title = build_link_indexes(publishable, output_paths)

    if collisions:
        afectados = sum(len(g) - 1 for g in collisions)
        print(f'[*] {len(collisions)} títulos duplicados; {afectados} artículos llevan su Id en el nombre.')
        for group in collisions[:5]:
            print(f'    - "{group[0].title}" → {", ".join(a.article_id for a in group)}')
        if len(collisions) > 5:
            print(f'    ... y {len(collisions) - 5} grupos más (ver logs/titulos-duplicados.txt)')

    # ------------------------------------------------------------------
    # 3. Decidir qué hay que regenerar
    # ------------------------------------------------------------------
    known_ids = set(generation_state.get('articles') or {})
    pending: list[tuple[Article, Path]] = []

    for article in scoped_articles:
        md_path = output_paths[article.article_id]
        if article.article_id in already_done:
            continue
        if incremental_mode and not should_generate_article(
            generation_state, article.article_id, article.updated_at, md_path
        ):
            continue
        pending.append((article, md_path))

    total = len(pending)
    author_count = sum(1 for article, _ in pending if article.uses_author_engine)
    nuevos = sum(1 for article, _ in pending if article.article_id not in known_ids)
    print(f'[*] Artículos a generar: {total} '
          f'({nuevos} nuevos, {total - nuevos} modificados, {author_count} con el motor de autor)')

    # ------------------------------------------------------------------
    # 4. Generar
    # ------------------------------------------------------------------
    generated_files: list[Path] = []
    count_ok = 0
    count_nuevos = 0
    enlaces_freshdesk: collections.Counter = collections.Counter()
    ejemplos_freshdesk: dict[str, tuple[str, str]] = {}

    for index, (article, md_path) in enumerate(pending, start=1):
        try:
            md_path.parent.mkdir(parents=True, exist_ok=True)
            convert = convert_author if article.uses_author_engine else convert_standard

            md_content = convert(
                article.description,
                docs_folder,
                md_path,
                images_folder,
                article.title,
                article.article_id,
                wiki_broken_images,
            )
            md_content = fix_internal_links(
                md_content, md_path, paths_by_id, paths_by_title, folder_paths, link_counter,
                category_paths,
            )

            # Una URL de Freshdesk que llega hasta aquí es una forma que
            # ninguna regla contempla. Se cuenta para que salga en el informe
            # en lugar de colarse en la documentación sin que nadie lo note.
            for forma, veces in contar_enlaces_freshdesk(md_content).items():
                enlaces_freshdesk[forma] += veces
                ejemplos_freshdesk.setdefault(forma, (article.article_id, article.title))

            # El H1 lleva el titulo entero; la cabecera YAML, si hace falta,
            # lleva la version corta con la que la pagina sale en el panel.
            md_path.write_text(
                f'{front_matter(article.title)}# {article.title}\n\n{md_content}',
                encoding='utf-8',
            )
            generated_files.append(md_path)

            run_state.record(
                article.article_id,
                title=article.title,
                product=products.get(article.category_id, ''),
                category_id=article.category_id,
                category_name=categories.get(article.category_id, UNKNOWN_CATEGORY),
                folder_id=article.folder_id,
                folder_name=folders.get(article.folder_id, UNKNOWN_FOLDER),
                path=md_path.relative_to(output_dir).as_posix(),
                source_updated_at=article.updated_at,
            )
            count_ok += 1
            if article.article_id not in known_ids:
                count_nuevos += 1

        except Exception as exc:
            conversion_errors.append((article.article_id, article.title, f'{exc.__class__.__name__}: {exc}'))
            print(f'    [ERROR] {article.article_id} — {article.title}: {exc}', file=sys.stderr)

        if index % 100 == 0 or index == total:
            print(f'    -> [{index}/{total}] {count_ok} generados, {len(conversion_errors)} con error', flush=True)

    run_state.flush()

    # ------------------------------------------------------------------
    # 5. Ficheros que sobran: huérfanos y reubicados
    # ------------------------------------------------------------------
    # Un artículo omitido por ser borrador NO cuenta como vivo: así su .md, si
    # se generó en una ejecución anterior, se puede limpiar como huérfano.
    live_ids = {a.article_id for a in publishable}
    orphans = find_orphan_articles(generation_state, live_ids, selected_id_set)
    removed_ids: list[str] = []

    if orphans:
        print(f'\n[*] {len(orphans)} artículos del estado ya no se publican '
              f'(eliminados en origen o pasados a borrador).')
        if args.prune_orphans:
            for article_id, entry in orphans.items():
                if delete_generated_md(entry.get('path') or '', output_dir, docs_folder):
                    print(f'    [BORRADO] {entry.get("path")}')
                removed_ids.append(article_id)
        else:
            for entry in list(orphans.values())[:20]:
                print(f'    - {entry.get("title") or "(sin título)"} → {entry.get("path")}')
            print('    Usa --prune-orphans para borrar sus .md.')

    # Un artículo movido de categoría/carpeta, o al que le cambian el título,
    # sigue vivo en origen: no es huérfano. Lo que queda atrás es su fichero
    # anterior, que sin esto se quedaría en docs/ para siempre.
    scoped_ids = {a.article_id for a in scoped_articles}
    relocated = find_relocated_articles(generation_state, output_paths, output_dir, scoped_ids)

    if relocated:
        print(f'\n[*] {len(relocated)} artículos han cambiado de ruta (movidos o renombrados).')
        if args.prune_orphans:
            for old_rel, new_rel in relocated.values():
                if delete_generated_md(old_rel, output_dir, docs_folder):
                    print(f'    [BORRADO] {old_rel}')
                    print(f'       ahora en {new_rel}')
        else:
            for old_rel, new_rel in list(relocated.values())[:20]:
                print(f'    - {old_rel}')
                print(f'      → {new_rel}')
            print('    Usa --prune-orphans para borrar los .md que quedaron atrás.')

    # Las imágenes que ya no menciona nadie. Solo en una ejecución COMPLETA:
    # si está filtrada por categorías, las imágenes de las que no se han
    # generado parecerían huérfanas y se irían por delante.
    huerfanas: list[Path] = []
    if selected_id_set:
        print('\n[*] Ejecución filtrada por categorías: no se buscan imágenes huérfanas.')
    else:
        huerfanas = buscar_imagenes_huerfanas(docs_folder, images_folder)
        if huerfanas:
            peso = _tamano_legible(_tamano_de_imagenes(huerfanas))
            print(f'\n[*] {len(huerfanas)} imágenes ya no las menciona ningún '
                  f'artículo ({peso}).')
            if args.prune_orphans:
                for fichero in huerfanas:
                    try:
                        fichero.unlink()
                    except OSError as error:
                        print(f'    [ERROR] {fichero.name}: {error}')
                print(f'    [BORRADAS] {len(huerfanas)} imágenes, {peso} liberados.')
            else:
                print('    Usa --prune-orphans para borrarlas. '
                      'El detalle, en logs/imagenes-huerfanas.txt')

    # ------------------------------------------------------------------
    # 6. Informes
    # ------------------------------------------------------------------
    errores_lineas: list[str] = []
    for article_id, title, error in conversion_errors:
        errores_lineas += [f'ArticleId: {article_id}', f'Título: {title}', f'Error: {error}', '']
    logs.write(ARTICULOS_CON_ERROR, 'ARTÍCULOS QUE NO SE PUDIERON CONVERTIR', errores_lineas)

    duplicados_lineas: list[str] = []
    if collisions:
        duplicados_lineas = [
            'El artículo con el ArticleId más bajo conserva el nombre limpio;',
            'el resto llevan su ArticleId en el nombre del fichero.',
            '',
        ]
        for group in collisions:
            duplicados_lineas.append(f'Título: {group[0].title}')
            for article in group:
                duplicados_lineas.append(
                    f'  {article.article_id} → {output_paths[article.article_id].name}')
            duplicados_lineas.append('')
    logs.write(TITULOS_DUPLICADOS, 'TÍTULOS DUPLICADOS', duplicados_lineas)

    imagenes_lineas: list[str] = []
    for url, title in wiki_broken_images:
        imagenes_lineas += [f'Artículo: {title}', f'URL: {url}', '']
    logs.write(IMAGENES_NO_DESCARGADAS, 'IMÁGENES QUE NO SE PUDIERON DESCARGAR', imagenes_lineas)

    logs.write(
        ADJUNTOS_NO_PUBLICADOS,
        'FICHEROS ADJUNTOS QUE NO SE PUBLICAN',
        lineas_de_adjuntos(scoped_articles),
    )

    logs.write(
        IMAGENES_HUERFANAS,
        'IMÁGENES QUE YA NO USA NINGÚN ARTÍCULO',
        lineas_de_imagenes_huerfanas(huerfanas, images_folder, args.prune_orphans),
    )

    if not args.sin_comprobar_videos:
        logs.write(
            VIDEOS_QUE_NO_SE_VEN,
            'VÍDEOS ENLAZADOS QUE YA NO SE PUEDEN VER',
            lineas_de_videos(docs_folder),
        )

    freshdesk_lineas: list[str] = []
    if enlaces_freshdesk:
        freshdesk_lineas += [
            'Estas URLs apuntan todavía a Freshdesk. Cada forma que aparezca aquí',
            'es un patrón de enlace que ninguna regla de fix_internal_links cubre.',
            '',
        ]
        for forma, veces in enlaces_freshdesk.most_common():
            art_id, titulo = ejemplos_freshdesk.get(forma, ('', ''))
            freshdesk_lineas.append(f'{forma}: {veces}')
            freshdesk_lineas.append(f'  ejemplo: {art_id} · {titulo}')
            freshdesk_lineas.append('')
    logs.write(ENLACES_FRESHDESK, 'URLS DE FRESHDESK SIN TRADUCIR', freshdesk_lineas)

    # ------------------------------------------------------------------
    # 6.b Portadas de categoría y de carpeta
    # ------------------------------------------------------------------
    # MkDocs publica páginas, no directorios: sin un index.md, una carpeta no
    # tiene URL. Los enlaces de Freshdesk a una carpeta —que fix_internal_links
    # sí traduce a su ruta local— llegaban a un directorio sin página y la
    # reparación no tenía más remedio que degradarlos a texto.
    #
    # Va ANTES de la reparación de enlaces a propósito: así phase_unwrap_folder_links
    # se encuentra la portada ya escrita y reapunta el enlace en lugar de quitarlo.
    raices_portada = [
        docs_folder / categories[cid]
        for cid in selected_ids if cid in categories and cid != sin_carpeta
    ]
    if sin_carpeta:
        # Su categoría no tiene carpeta, así que las raíces son las carpetas
        # que han subido: cada una necesita su portada igual que antes.
        raices_portada += sorted(
            {p.parent for aid, p in output_paths.items()
             if p.parent != docs_folder and p.parent.parent == docs_folder}
        )
    escritas, respetadas = escribir_portadas_del_arbol(raices_portada)
    print()
    print(f'[*] Portadas de carpeta: {escritas} escritas'
          + (f', {respetadas} escritas a mano respetadas' if respetadas else ''))

    # ------------------------------------------------------------------
    # 7. Reparación de enlaces — siempre la última fase
    # ------------------------------------------------------------------
    links_ok = True

    if args.skip_link_repair:
        print('[*] Reparación de enlaces omitida por --skip-link-repair.')
    elif generated_files or removed_ids:
        try:
            print('\n[*] Ejecutando reparación de enlaces...')
            run_pipeline(docs_folder, only_files=generated_files, logs=logs)
        except Exception as exc:
            links_ok = False
            print(f'[WARN] Falló la reparación de enlaces: {exc}', file=sys.stderr)
            traceback.print_exc()

    # ------------------------------------------------------------------
    # 8. Consolidar el estado incremental
    # ------------------------------------------------------------------
    # Se consolida SIEMPRE lo que se ha generado bien. Los artículos que
    # fallaron no llegaron a ``run_state``, así que su entrada en el estado se
    # queda con el ``updated_at`` viejo (o no existe) y la próxima ejecución los
    # reintenta sola.
    #
    # Antes, un único error de conversión abortaba la consolidación entera: la
    # ejecución siguiente daba por no generados los 2.298 artículos y volvía a
    # sobrescribir todos los .md sin modificar. En una tarea semanal, eso
    # convierte cualquier artículo defectuoso en una regeneración completa.
    executed_at = finalize_generation_state(
        output_dir, run_state, removed_article_ids=removed_ids, pipeline_fingerprint=huella,
    )
    print(f'\n[*] generation_state.json actualizado a {executed_at}')

    if not links_ok:
        print('[WARN] La reparación de enlaces falló. Los .md están generados y el estado')
        print('       consolidado; relánzala aparte con: python -m pipeline.repair_links')

    # ------------------------------------------------------------------
    # 9. Parte de la ejecución
    # ------------------------------------------------------------------
    logs.executed_at = executed_at
    sin_borrar = (0 if args.prune_orphans
                  else len(orphans) + len(relocated) + len(huerfanas))
    report = build_run_report(
        {
            'nuevos': count_nuevos,
            'actualizados': count_ok - count_nuevos,
            'movidos': len(relocated),
            'retirados': len(removed_ids),
            'borradores': 0 if args.include_drafts else len(drafts),
            'errores': len(conversion_errors),
            'enlaces': link_counter[0],
            'freshdesk': sum(enlaces_freshdesk.values()),
            'pendientes_de_borrar': sin_borrar,
        }
    )

    report_path = logs.write(RESUMEN, 'RESUMEN DE LA EJECUCIÓN', report + [''] + logs.index_lines())

    print()
    print(f' Resumen de la ejecución — {executed_at}')
    print(' ' + '-' * 53)
    for linea in report:
        print(' ' + linea)
    print()
    for linea in logs.index_lines():
        print(' ' + linea)
    print(f'\n[*] Informes en {report_path.parent}')

    return 1 if (conversion_errors or not links_ok) else 0


if __name__ == '__main__':
    sys.exit(main())
