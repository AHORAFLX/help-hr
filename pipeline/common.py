"""
common.py
=========
Utilidades compartidas por todo el pipeline de migración.

Antes de este módulo, ``migrate.py`` y ``author_articles.py`` mantenían dos
copias divergentes de estas funciones. Cualquier arreglo hay que hacerlo aquí
una sola vez.

Requiere Python 3.12 o superior.
"""

from __future__ import annotations

import collections
import html as html_lib
import os
import re
import sys
import unicodedata
import urllib.parse
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Sesión HTTP global (reutiliza conexiones TCP entre descargas)
# ---------------------------------------------------------------------------

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

#: Dominios cuyas imágenes no se pueden descargar (wiki interna ya apagada).
UNREACHABLE_IMAGE_HOSTS = ("wiki.ahora.es",)


# ---------------------------------------------------------------------------
# Nombres y claves de búsqueda
# ---------------------------------------------------------------------------

def get_safe_filename(name: str, fallback: str, max_length: int = 100) -> str:
    """Genera un nombre de fichero seguro eliminando caracteres problemáticos."""
    if not name or not name.strip():
        return fallback
    safe = re.sub(r'[<>:"/\\|?*\n\r]', '-', name)
    safe = safe[:max_length].strip().rstrip('.')
    return safe if safe.strip() else fallback


#: A partir de aqui una etiqueta no cabe de una pieza en la barra lateral de
#: Material y se parte en cuatro o cinco lineas. El titulo mas largo que hay en
#: la BDD mide 165 caracteres.
NAV_TITLE_MAX = 60

#: Puntos por donde un titulo se puede cortar sin quedar a medias. Se prueban
#: en orden: es mejor cortar por el guion que separa "Tema - Detalle" que por
#: la primera coma que aparezca.
_NAV_CUT_POINTS = (' - ', ': ', ' (', ', ', '. ')


def nav_title(title: str, max_length: int = NAV_TITLE_MAX) -> str:
    """
    Devuelve la etiqueta con la que la pagina aparece en el panel lateral.

    MkDocs usa el H1 como etiqueta del nav, y hay 231 articulos cuyo titulo
    pasa de 60 caracteres —el mayor, 165—: en la barra lateral se parten en
    varias lineas y el arbol se vuelve inservible. Aqui se recorta **solo la
    etiqueta**; el H1 de la pagina sigue llevando el titulo entero, asi que no
    se pierde nada.

    Se corta por un separador natural si lo hay dentro del limite, y si no,
    por la ultima palabra que quepa.
    """
    title = ' '.join((title or '').split())
    if len(title) <= max_length:
        return title

    mejor = ''
    for corte in _NAV_CUT_POINTS:
        trozo = title.split(corte)[0]
        if len(trozo) <= max_length and len(trozo) > len(mejor):
            mejor = trozo
    if len(mejor) >= max_length // 3:
        return mejor.rstrip(' -:,.(')

    # Se descuentan los tres puntos para no volver a pasarse del límite.
    recortado = title[:max_length - 3].rsplit(' ', 1)[0].rstrip(' -:,.(')
    return f'{recortado}...'


def front_matter(title: str) -> str:
    """
    Cabecera YAML con la etiqueta del nav, o cadena vacia si no hace falta.

    Solo se escribe cuando el titulo no cabe: un fichero sin cabecera es mas
    facil de leer, y MkDocs ya usa el H1 cuando no hay nada que decirle.
    """
    corto = nav_title(title)
    if corto == ' '.join((title or '').split()):
        return ''
    # Las comillas dobles evitan que un ':' del titulo rompa el YAML.
    return '---\ntitle: "{}"\n---\n\n'.format(corto.replace('"', "'"))


def normalize_article_key(text: str) -> str:
    """Normaliza un título de artículo para usarlo como clave de búsqueda difusa."""
    if not text or not text.strip():
        return ""
    decoded = html_lib.unescape(text)
    decoded = urllib.parse.unquote(decoded)
    # Eliminar marcas diacríticas (acentos)
    normalized = unicodedata.normalize('NFD', decoded)
    result = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    result = result.lower()
    result = re.sub(r'[^a-z0-9]+', ' ', result)
    result = re.sub(r'\s+', ' ', result).strip()
    return result


def build_article_lookup_keys(title: str) -> list[str]:
    """Genera variantes normalizadas de un título para resolver enlaces internos."""
    if not title or not title.strip():
        return []

    variants: list[str] = []

    def add(value: str) -> None:
        key = normalize_article_key(value)
        if key and key not in variants:
            variants.append(key)

    add(title)
    add(get_safe_filename(title, title))

    separators = [' - ', ' – ', ' — ', ': ', ' | ', ' / ']
    for separator in separators:
        if separator in title:
            parts = [part.strip() for part in title.split(separator) if part.strip()]
            for part in parts:
                add(part)
            if len(parts) >= 2:
                add(parts[-1])
                add(' '.join(parts[-2:]))

    # También registrar el título sin contenido entre paréntesis/corchetes.
    add(re.sub(r'[\(\[\{].*?[\)\]\}]', ' ', title))

    return variants


# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

CONNECTION_ENV_KEYS = (
    'AUTHOR_ARTICLES_CONNECTION_STRING',
    'DB_CONNECTION_STRING',
    'SQLSERVER_CONNECTION_STRING',
)


def load_env_file(env_file: Path) -> None:
    """Carga variables de entorno desde un archivo .env sencillo."""
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]

        os.environ.setdefault(key, value)


def resolve_connection_string(cli_value: Optional[str], env_file: Path) -> str:
    """Resuelve la connection string desde CLI o variables de entorno."""
    if cli_value and cli_value.strip():
        return cli_value.strip()

    load_env_file(env_file)

    for env_key in CONNECTION_ENV_KEYS:
        env_value = os.environ.get(env_key, '').strip()
        if env_value:
            return env_value

    raise RuntimeError(
        'No se ha encontrado la connection string. '
        'Pásala por --connection-string o define AUTHOR_ARTICLES_CONNECTION_STRING '
        'en el archivo .env.'
    )


# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------

def relative_posix(from_dir: Path, to_file: Path) -> str:
    """Devuelve la ruta relativa en formato POSIX (barras /) con espacios %20."""
    try:
        rel = os.path.relpath(str(to_file), str(from_dir))
        return rel.replace('\\', '/').replace(' ', '%20')
    except ValueError:
        # En Windows puede fallar cross-drive; usar ruta absoluta como fallback
        return to_file.as_posix()


def mkdocs_html_image_src(docs_root: Path, md_file_path: Path, local_path: Path) -> str:
    """
    Calcula una ruta relativa para un ``<img src>`` de HTML crudo.

    MkDocs reescribe las rutas de las imágenes en Markdown, pero no las de un
    ``<img>`` embebido, así que aquí hay que compensar a mano el nivel extra que
    introduce ``use_directory_urls=True``.
    """
    md_rel = md_file_path.relative_to(docs_root)
    target_rel = local_path.relative_to(docs_root)

    output_parts = list(md_rel.parts[:-1])
    if md_file_path.stem.lower() != 'index':
        output_parts.append(md_file_path.stem)

    up = '../' * len(output_parts)
    return f'{up}{target_rel.as_posix()}'.replace(' ', '%20')


# ---------------------------------------------------------------------------
# Descarga de imágenes
# ---------------------------------------------------------------------------

#: Acepta espacios tras el paréntesis y un title opcional entre comillas.
#:
#: El texto alternativo se captura con ``[^\]]*``, no con ``.*?``: hay artículos
#: cuyo alt trae un salto de línea ("Captura de pantalla\nDescripción generada
#: automáticamente"), y con ``.`` —que no casa saltos— esas imágenes no las veía
#: nadie: ni se descargaban ni se anotaban como fallidas. Se quedaban apuntando
#: a S3 hasta que la URL caducara.
MD_IMAGE_RX = re.compile(r'!\[([^\]]*)\]\(\s*(https?://[^\s)]+)(?:\s+"[^"]*")?\s*\)')
HTML_IMG_SRC_RX = re.compile(r'(?is)(<img\b[^>]*\bsrc=["\'])(https?://[^"\']+)(["\'][^>]*>)')
TABLE_HTML_RX = re.compile(r'(?is)<table\b[^>]*>.*?</table>')

_IMAGE_EXT_RX = re.compile(r'\.(png|jpg|jpeg|gif|webp|svg)$', re.IGNORECASE)
_CONTENT_TYPE_EXT = {
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/gif': '.gif',
    'image/webp': '.webp',
    'image/svg+xml': '.svg',
}


def _sanitize_image_url(url: str) -> str:
    """Limpia saltos de línea, espacios y caracteres invisibles de una URL."""
    url = re.sub(r'[\r\n\t]', '', url or '').strip()
    url = re.sub('[\u200b\u200c\u200d\ufeff]', '', url)
    return url.replace(' ', '%20')


def _is_unreachable_host(url: str) -> bool:
    host = urllib.parse.urlparse(url).netloc.lower()
    return any(bad in host for bad in UNREACHABLE_IMAGE_HOSTS)


def _download_image(url: str, images_out_dir: Path) -> Path:
    """
    Descarga una imagen y devuelve su ruta local, reutilizándola si ya existe.

    Lanza excepción si la descarga falla, para que el llamante decida qué hacer.
    """
    images_out_dir.mkdir(parents=True, exist_ok=True)

    parsed = urllib.parse.urlparse(url)
    safe_name = get_safe_filename(Path(parsed.path).name or 'image', 'image')

    # Si el nombre ya trae extensión de imagen y el fichero está en disco, reutilizar.
    if _IMAGE_EXT_RX.search(safe_name):
        candidate = images_out_dir / safe_name
        if candidate.exists():
            return candidate

    resp = SESSION.get(url, timeout=30, stream=True)
    resp.raise_for_status()

    if not _IMAGE_EXT_RX.search(safe_name):
        content_type = resp.headers.get('Content-Type', '')
        ext = next((v for k, v in _CONTENT_TYPE_EXT.items() if k in content_type), '.jpg')
        safe_name += ext

    local_path = images_out_dir / safe_name
    if local_path.exists():
        resp.close()
        return local_path

    stem, suffix = Path(safe_name).stem, Path(safe_name).suffix
    index = 1
    while local_path.exists():
        local_path = images_out_dir / f'{stem}_{index}{suffix}'
        index += 1

    with open(local_path, 'wb') as handle:
        for chunk in resp.iter_content(8192):
            handle.write(chunk)

    return local_path


def alt_util(alt: str, origen: str) -> str:
    """
    Descarta el texto alternativo cuando no es más que la URL de origen.

    Al descargar la imagen la ruta cambia, pero el alt se conservaba tal cual y
    quedaban cosas como
    ``![https://s3.amazonaws.com/…png](../../docs_assets/images/x.png)``: un
    lector de pantalla lee la URL entera, y cualquier búsqueda de "freshdesk"
    la encuentra aunque la imagen esté perfectamente descargada. Un alt vacío
    es mejor que un alt inútil.
    """
    # El alt puede venir repartido en varias líneas; en Markdown tiene que
    # quedar en una sola o parte el propio enlace de la imagen.
    limpio = re.sub(r'\s+', ' ', alt or '').strip()
    if not limpio:
        return ''
    if limpio in (origen, urllib.parse.unquote(origen)):
        return ''
    # Cualquier otra URL como alt tampoco describe nada.
    return '' if re.fullmatch(r'https?://\S+', limpio) else limpio


def download_images_from_markdown(
    md_content: str,
    md_file_path: Path,
    images_out_dir: Path,
    article_title: str = "",
    broken_images_log: Optional[list] = None,
) -> str:
    """Descarga imágenes remotas y reemplaza sus URLs por rutas relativas locales."""
    if broken_images_log is None:
        broken_images_log = []

    resolved: dict[str, str] = {}

    for m in reversed(list(MD_IMAGE_RX.finditer(md_content))):
        url = _sanitize_image_url(m.group(2))
        alt_text = alt_util(m.group(1), url)
        if not url:
            continue

        if url in resolved:
            md_content = md_content[:m.start()] + f'![{alt_text}]({resolved[url]})' + md_content[m.end():]
            continue

        if _is_unreachable_host(url):
            broken_images_log.append((url, article_title))
            continue

        try:
            local_path = _download_image(url, images_out_dir)
        except Exception as exc:
            # Se anota además de avisar: si solo se escribe en stderr, la imagen
            # se queda apuntando a un servidor remoto y nadie se entera hasta
            # que el enlace caduca.
            print(f'    [WARN] Fallo al descargar imagen: {url} — {exc}', file=sys.stderr)
            broken_images_log.append((url, article_title))
            continue

        rel = relative_posix(md_file_path.parent, local_path)
        resolved[url] = rel
        md_content = md_content[:m.start()] + f'![{alt_text}]({rel})' + md_content[m.end():]

    return md_content


def download_images_in_html_fragment(
    html_fragment: str,
    docs_root: Path,
    md_file_path: Path,
    images_out_dir: Path,
    article_title: str = "",
    broken_images_log: Optional[list] = None,
) -> str:
    """Igual que la anterior, pero sobre ``<img src>`` de HTML crudo preservado."""
    if broken_images_log is None:
        broken_images_log = []

    resolved: dict[str, str] = {}

    for m in reversed(list(HTML_IMG_SRC_RX.finditer(html_fragment))):
        prefix, suffix = m.group(1), m.group(3)
        url = _sanitize_image_url(m.group(2))
        if not url:
            continue

        if url in resolved:
            html_fragment = html_fragment[:m.start()] + f'{prefix}{resolved[url]}{suffix}' + html_fragment[m.end():]
            continue

        if _is_unreachable_host(url):
            broken_images_log.append((url, article_title))
            continue

        try:
            local_path = _download_image(url, images_out_dir)
        except Exception as exc:
            print(f'    [WARN] Fallo al descargar imagen HTML: {url} — {exc}', file=sys.stderr)
            broken_images_log.append((url, article_title))
            continue

        rel = mkdocs_html_image_src(docs_root, md_file_path, local_path)
        resolved[url] = rel
        html_fragment = html_fragment[:m.start()] + f'{prefix}{rel}{suffix}' + html_fragment[m.end():]

    return html_fragment


#: Atributo cuyo valor es una URL. Se compara el nombre aparte para poder
#: respetar los que sí significan algo (``src``, ``href``).
_ATTR_CON_URL_RX = re.compile(
    r'''(?is)\s+([a-zA-Z_:][-\w:.]*)\s*=\s*(["'])\s*(https?://[^"']*)\2'''
)

#: Un encabezado HTML con su contenido, para ver si dentro hay algo que leer.
_ENCABEZADO_HTML_RX = re.compile(r'(?is)<(h[1-6])\b[^>]*>(.*?)</\1>')


def desenvolver_encabezados_html_sin_texto(html_fragment: str) -> str:
    """
    Quita la etiqueta de los encabezados HTML que no tienen texto que mostrar.

    El editor de Freshdesk deja dentro de las tablas conservadas encabezados
    vacios: ``<h2><br/></h2>``. Publicados son un hueco en el indice lateral y
    un ancla sin destino visible, y el lector no ve nada donde el indice le
    promete una seccion. Eran 8 en 3 articulos.

    Se **desenvuelve**, no se borra: uno de ellos es un ``<h1>`` cuyo unico
    contenido es una captura, y la captura si se ve. Lo que sobra es que eso
    sea un encabezado, no la imagen.
    """
    def desenvolver(match):
        interior = match.group(2)
        visible = re.sub(r'(?is)<[^>]+>|&nbsp;|\s', '', interior)
        return interior if not visible else match.group(0)

    return _ENCABEZADO_HTML_RX.sub(desenvolver, html_fragment or '')


#: Fondo del contenido en modo claro (``--fh-color-section`` del tema) y en
#: modo oscuro. El color de letra que se escribe a mano en el HTML del
#: artículo no cambia con el tema, así que hay que juzgarlo contra estos dos.
_FONDO_CLARO = (0xf5, 0xf7, 0xf8)
_FONDO_OSCURO = (0x29, 0x29, 0x29)

#: Color de letra del tema en cada modo.
_TEXTO_CLARO = (0x1a, 0x1a, 0x1a)

#: Contraste por debajo del cual el texto deja de leerse. WCAG pide 4.5 para
#: texto normal; se corta en 3 para tocar solo lo que no hay por dónde coger.
_CONTRASTE_MINIMO = 3.0

_COLORES_CON_NOMBRE = {
    'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (255, 0, 0),
    'blue': (0, 0, 255), 'green': (0, 128, 0), 'gray': (128, 128, 128),
    'grey': (128, 128, 128), 'yellow': (255, 255, 0), 'lime': (0, 255, 0),
    'aqua': (0, 255, 255), 'cyan': (0, 255, 255), 'silver': (192, 192, 192),
    'navy': (0, 0, 128), 'teal': (0, 128, 128), 'olive': (128, 128, 0),
}

_DECLARACION_DE_COLOR_RX = re.compile(r'(?i)(?<![-\w])color\s*:\s*([^;]+);?')
_FONDO_RX = re.compile(r'(?i)(?<![-\w])background(?:-color)?\s*:\s*([^;]+)')


def _a_rgb(valor: str) -> Optional[tuple]:
    """Pasa a (r, g, b) los formatos de color que usa el editor de Freshdesk."""
    if not valor:
        return None
    v = valor.strip().lower()
    m = re.match(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?', v)
    if m:
        # ``rgba(0, 0, 0, 0)`` es transparente, no negro: el editor lo escribe
        # a punta pala para decir "sin fondo". Tomarlo por negro hacia creer
        # que habia texto oscuro sobre negro donde no hay fondo ninguno.
        alfa = m.group(4)
        if alfa is not None and float(alfa) == 0:
            return None
        return tuple(int(x) for x in m.groups()[:3])
    m = re.match(r'#([0-9a-f]{6})$', v)
    if m:
        return tuple(int(m.group(1)[i:i + 2], 16) for i in (0, 2, 4))
    m = re.match(r'#([0-9a-f]{3})$', v)
    if m:
        return tuple(int(c * 2, 16) for c in m.group(1))
    return _COLORES_CON_NOMBRE.get(v)


def _luminancia(c: tuple) -> float:
    def canal(x: float) -> float:
        x /= 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contraste(a: tuple, b: tuple) -> float:
    la, lb = _luminancia(a), _luminancia(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def quitar_colores_ilegibles(html_fragment: str) -> str:
    """
    Quita el color de letra escrito a mano cuando no se lee sobre el tema.

    El editor de Freshdesk pinta los colores dentro del HTML del artículo, y
    un color en línea **no cambia con el tema**. Hay verdes y naranjas claros
    que sobre el fondo claro del sitio dan un contraste de 1.9: el lector ve
    el texto lavado o directamente no lo ve. Son 20 trozos en 11 artículos,
    entre ellos los ``1.-``, ``2.-``… que numeran los pasos de Techfun y los
    ``NOTA:`` de dos Hotfix.

    Se quita **solo la declaración de color**, no el resto del estilo, y solo
    cuando el texto va sobre el fondo del tema: si el HTML fija también el
    fondo, el par lo decidió el autor y se respeta. Sin color propio, el tema
    pone el suyo, que se lee en claro y en oscuro.

    No se oscurece el color para conservar el tono a propósito: un tono que
    cumple sobre el fondo claro deja de cumplir sobre el oscuro, así que
    arreglar un modo estropearía el otro.
    """
    if not html_fragment or 'color' not in html_fragment.lower():
        return html_fragment

    sopa = BeautifulSoup(html_fragment, 'html.parser')
    sospechosos: dict[str, bool] = {}
    #: Estilos de un ancestro cuyo negro hay que soltar para poder soltar el
    #: color de dentro. Se comprueban aparte porque el propio ancestro, mirado
    #: por su cuenta, se lee perfectamente sobre el fondo claro.
    forzados: set = set()

    for el in sopa.find_all(style=True):
        estilo = el.get('style') or ''
        m = _DECLARACION_DE_COLOR_RX.search(estilo)
        if not m:
            continue
        color = _a_rgb(m.group(1))
        if color is None:
            continue
        # El fondo lo puede fijar el propio elemento o cualquiera que lo
        # envuelva: una celda de color con letra oscura dentro es cosa del
        # autor y no se toca.
        fondo = None
        for pad in [el] + list(el.parents):
            if getattr(pad, 'get', None) is None:
                continue
            f = _FONDO_RX.search(pad.get('style') or '')
            if f:
                fondo = _a_rgb(f.group(1))
                if fondo is not None:
                    break
        # Quitar el color solo sirve si detras manda el tema. Si lo fija un
        # ancestro, el texto hereda ESE, y hay que mirar si se lee: en
        # ``Cierres de Inventario`` la celda pone ``color: black``, asi que
        # quitar el verde de dentro dejaba negro sobre negro en modo oscuro.
        heredado = None
        for pad in el.parents:
            if getattr(pad, 'get', None) is None:
                continue
            h = _DECLARACION_DE_COLOR_RX.search(pad.get('style') or '')
            if h:
                heredado = _a_rgb(h.group(1))
                if heredado is not None:
                    break
        if heredado is None:
            releva_bien = True            # manda el tema, que se lee en los dos modos
        else:
            releva_bien = (_contraste(heredado, _FONDO_CLARO) >= 4.5
                           and _contraste(heredado, _FONDO_OSCURO) >= _CONTRASTE_MINIMO)

        ilegible = (fondo is None and releva_bien
                    and _contraste(color, _FONDO_CLARO) < _CONTRASTE_MINIMO)
        # El mismo texto de estilo puede repetirse en sitios distintos. Solo
        # se cambia si TODAS sus apariciones son ilegibles.
        sospechosos[estilo] = sospechosos.get(estilo, True) and ilegible

        # Si lo que estorba es el negro heredado, se quita también: sobre el
        # fondo claro el negro no aporta nada —es el color que ya pone el
        # tema— y sobre el oscuro es justo lo que no deja leer. Así el verde
        # de debajo sí puede soltarse. Son las cifras de "Cierres de
        # Inventario", en una celda con ``color: black``.
        if (fondo is None and not releva_bien and heredado is not None
                and _luminancia(heredado) < 0.05
                and _contraste(color, _FONDO_CLARO) < _CONTRASTE_MINIMO):
            for pad in el.parents:
                if getattr(pad, 'get', None) is None:
                    continue
                e_pad = pad.get('style') or ''
                if not _DECLARACION_DE_COLOR_RX.search(e_pad):
                    continue
                if not _FONDO_RX.search(e_pad):
                    forzados.add(e_pad)
                    sospechosos[estilo] = True
                break

    # Un fondo escrito a mano SIN color de letra: en modo claro le cae encima
    # el texto oscuro del tema, y si el fondo es oscuro no se lee. Se le pone
    # una letra explícita, elegida por el fondo, que vale en los dos modos.
    letras: dict[str, str] = {}
    for el in sopa.find_all(style=True):
        estilo = el.get('style') or ''
        f = _FONDO_RX.search(estilo)
        if not f or _DECLARACION_DE_COLOR_RX.search(estilo):
            continue
        fondo = _a_rgb(f.group(1))
        if fondo is None:
            continue
        if any(_DECLARACION_DE_COLOR_RX.search(pad.get('style') or '')
               for pad in el.parents if getattr(pad, 'get', None) is not None):
            continue
        if _contraste(_TEXTO_CLARO, fondo) >= _CONTRASTE_MINIMO:
            continue
        letras[estilo] = '#ffffff' if _luminancia(fondo) < 0.35 else '#1a1a1a'

    # Un estilo forzado se suelta solo si NINGUNA de sus apariciones cuelga de
    # un fondo escrito a mano: ahi el negro puede ser lo unico que hace legible
    # la celda.
    for estilo in forzados:
        seguro = True
        for el in sopa.find_all(style=estilo):
            if any(_FONDO_RX.search(pad.get('style') or '')
                   for pad in el.parents if getattr(pad, 'get', None) is not None):
                seguro = False
                break
        if seguro:
            sospechosos[estilo] = True

    limpio = html_fragment
    for estilo, letra in letras.items():
        for comilla in ('"', "'"):
            viejo_attr = f'style={comilla}{estilo}{comilla}'
            if viejo_attr in limpio:
                nuevo = estilo.rstrip().rstrip(';') + f'; color: {letra};'
                limpio = limpio.replace(viejo_attr, f'style={comilla}{nuevo}{comilla}')
    for estilo, ilegible in sospechosos.items():
        if not ilegible:
            continue
        nuevo = _DECLARACION_DE_COLOR_RX.sub('', estilo).strip()
        nuevo = re.sub(r'\s*;\s*;+', ';', nuevo).strip(' ;')
        for comilla in ('"', "'"):
            viejo_attr = f'style={comilla}{estilo}{comilla}'
            if viejo_attr not in limpio:
                continue
            if nuevo:
                limpio = limpio.replace(viejo_attr, f'style={comilla}{nuevo}{comilla}')
            else:
                # Sin nada que declarar, el atributo entero sobra. Se lleva por
                # delante el espacio de delante para no dejar ``<span >``.
                limpio = limpio.replace(' ' + viejo_attr, '').replace(viejo_attr, '')

    return limpio


#: Una tabla completa, para mirarle la primera fila.
_TABLA_ENTERA_RX = re.compile(r'(?is)<table\b.*?</table>')


def ascender_cabecera_de_tabla(html_fragment: str) -> str:
    """
    Pasa a ``<th>`` la primera fila cuando ya hace de cabecera con ``<td>``.

    El editor de Freshdesk no distingue cabecera de dato: escribe todas las
    celdas como ``<td>`` y marca la primera fila poniéndola en negrita o
    dándole un fondo gris. Publicado, el tema no tiene forma de saber que eso
    es una cabecera, así que no la destaca, no la separa del cuerpo y no la
    deja fija al desplazar la tabla a lo ancho.

    Solo se toca la tabla que **de verdad** es de datos, y el listón es alto a
    propósito: sin ningún ``<th>`` ya puesto, al menos tres filas, la primera
    con dos celdas o más, **todas** en negrita o con fondo, y tantas celdas
    como la fila más ancha de la tabla. Son 41 tablas en 25 artículos; las
    otras 970 sin cabecera son tablas de maquetado, que no la necesitan.
    """
    if not html_fragment or '<table' not in html_fragment.lower():
        return html_fragment

    def convertir(m):
        bruto = m.group(0)
        sopa = BeautifulSoup(bruto, 'html.parser')
        tabla = sopa.find('table')
        if tabla is None or tabla.find('th'):
            return bruto
        filas = tabla.find_all('tr')
        if len(filas) < 3:
            return bruto
        cabecera = filas[0].find_all('td', recursive=False)
        if len(cabecera) < 2:
            return bruto
        if any(len(f.find_all('td', recursive=False)) > len(cabecera) for f in filas):
            return bruto
        marcada = all(c.find(['strong', 'b']) or 'background' in (c.get('style') or '')
                      for c in cabecera)
        if not marcada:
            return bruto
        for celda in cabecera:
            celda.name = 'th'
        return str(sopa)

    return _TABLA_ENTERA_RX.sub(convertir, html_fragment)


#: Lo que hace que una tabla tenga algo dentro aunque no lleve una letra.
_ALGO_VISIBLE_EN_LA_TABLA_RX = re.compile(r'(?i)<(?:img|a|iframe|input|hr|video)\b')

#: La apertura y el cierre de una tabla, para recorrerlas contando anidadas.
_LIMITE_DE_TABLA_RX = re.compile(r'(?i)<(/?)table\b[^>]*>')


def _no_se_ve_nada(trozo: str) -> bool:
    if _ALGO_VISIBLE_EN_LA_TABLA_RX.search(trozo):
        return False
    return not html_lib.unescape(_HTML_TAG_RX.sub(' ', trozo)).strip()


def _todas_las_tablas(html_fragment: str) -> list:
    """Los limites de cada tabla, a cualquier profundidad, de fuera adentro."""
    pila, trozos = [], []
    for m in _LIMITE_DE_TABLA_RX.finditer(html_fragment):
        if not m.group(1):
            pila.append(m.start())
        elif pila:
            trozos.append((pila.pop(), m.end()))
    return sorted(trozos, key=lambda t: (t[0], -t[1]))


def quitar_tablas_vacias(html_fragment: str) -> str:
    """
    Tira la tabla que se publicaria sin nada dentro.

    El editor de Freshdesk maqueta con tablas y quedan restos: una tabla de
    una fila con celdas que solo llevan un ``<br>`` o un espacio duro. En el
    sitio eso no es invisible —Material le pinta su borde y su margen—, asi
    que sale un recuadro vacio en mitad del articulo. Los hotfixes de la
    version 4.4.2100 los llevaban a pares.

    Cuenta como vacia solo si ademas no tiene imagen, enlace ni nada que se
    vea sin texto: una tabla de capturas no lleva una letra y no hay que
    tocarla.

    **Se miran todas, no solo las de fuera.** En *ERP - Declaracion
    INTRASTAT* la tabla vacia cuelga de la misma celda que la captura: la de
    fuera tiene la imagen y se queda, la de dentro no tiene nada y sobra.

    Se recorre el texto crudo en vez de reconstruirlo con BeautifulSoup: la
    ida y vuelta normaliza el HTML de todo el articulo —``&nbsp;`` se vuelve
    el caracter, las etiquetas sueltas se cierran— y aqui solo queremos
    quitar un trozo, no reescribir el resto.
    """
    if not html_fragment or '<table' not in html_fragment.lower():
        return html_fragment

    sobran = []
    for a, b in _todas_las_tablas(html_fragment):
        if sobran and a >= sobran[-1][0] and b <= sobran[-1][1]:
            continue                     # ya cae dentro de una que se va entera
        if _no_se_ve_nada(html_fragment[a:b]):
            sobran.append((a, b))
    if not sobran:
        return html_fragment

    limpio, ultimo = [], 0
    for a, b in sobran:
        limpio.append(html_fragment[ultimo:a])
        ultimo = b
    limpio.append(html_fragment[ultimo:])
    return ''.join(limpio)


#: Una linea que es una sentencia de codigo VB, no una frase. El criterio es
#: estrecho a proposito: sin el, una descripcion de parametro del tipo
#: ``Campo (STRING): nombre del campo`` pasaba por codigo.
_SENTENCIA_VB_RX = re.compile(
    r'(?i)^(?:Set\s+\w|Dim\s+\w|Sub\s+\w|Function\s+\w|End\s+(?:Sub|Function|If)'
    r'|If\s+.+\bThen\b|MsgBox\b|g?[Cc]n\.[\w.]+|\w+\.[\w.]+\s*(?:\(|=))')

#: Una sentencia de T-SQL, que en esta casa aparece tanto como el VB. La forma
#: mas comun es la lista de parametros de un procedimiento, cada uno con su
#: comentario detras: ``@Tabla NVARCHAR(1000), -- Tabla en la que...``.
_SENTENCIA_SQL_RX = re.compile(
    r'(?i)^(?:@\w+\s+(?:N?VARCHAR|N?CHAR|INT|BIGINT|SMALLINT|TINYINT|BIT|DECIMAL|NUMERIC'
    r'|FLOAT|REAL|MONEY|DATE|DATETIME2?|UNIQUEIDENTIFIER|XML|TABLE)\b'
    r'|DECLARE\s+@|SELECT\s+|INSERT\s+INTO\b|UPDATE\s+\w|DELETE\s+FROM\b|EXEC(?:UTE)?\s+\w'
    r'|CREATE\s+(?:TABLE|PROC|PROCEDURE|VIEW|FUNCTION|INDEX)\b'
    r'|ALTER\s+(?:TABLE|PROC|PROCEDURE|VIEW|FUNCTION)\b|DROP\s+(?:TABLE|PROC|VIEW)\b)')

#: Palabras que delatan que la linea es prosa castellana, aunque empiece como
#: una sentencia.
_PROSA_EN_LA_LINEA_RX = re.compile(
    r'(?i)\b(?:para|pero|cuando|porque|debe|permite|muestra|siguiente)\b')


#: Una linea que no empieza una instruccion pero pertenece al mismo codigo:
#: la continuacion de VB —que acaba en ``_``— y el comentario, que empieza
#: por comilla simple o por ``--``. Sin contarlas, un ejemplo de webservice
#: parecia mitad codigo y mitad prosa, y al partirlo se perdia la peticion.
_CONTINUACION_DE_LINEA_RX = re.compile(r'(?:&amp;|&)?\s*_\s*$')
_COMENTARIO_DE_LINEA_RX = re.compile(r"^(?:'|--\s)")


def _acompana_al_codigo(linea: str) -> bool:
    """No abre una instruccion, pero va con la de al lado."""
    linea = (linea or '').strip()
    if not linea:
        return False
    return bool(_CONTINUACION_DE_LINEA_RX.search(linea)
                or _COMENTARIO_DE_LINEA_RX.match(linea))


def _es_sentencia(linea: str, con_comentario: bool = True) -> bool:
    """
    ¿Esta linea es una instruccion, o una frase que lo parece?

    El T-SQL no pasa por el filtro de prosa: la lista de parametros lleva el
    comentario en castellano **dentro** de la propia linea —``@CadenaDefault
    NVARCHAR(1000) = N'', -- Valor por defecto para el nuevo campo``— y una
    palabra como "para" no la convierte en prosa. El VB si lo pasa, porque su
    patron es mas laxo y sin el se colaban descripciones de parametro.
    """
    if len(linea) <= 8:
        return False
    if _SENTENCIA_SQL_RX.match(linea):
        # ``con_comentario`` distingue los dos sitios donde se usa esto. En la
        # lista de parametros de un procedimiento el comentario en castellano
        # va DENTRO de la linea y hay que admitirlo. Cuando lo que se mira es
        # un elemento entero, no: ``INSERT INTO: se usa para anadir uno o
        # varios registros`` es una frase que explica el INSERT, no un INSERT.
        return con_comentario or not _PROSA_EN_LA_LINEA_RX.search(linea)
    return (bool(_SENTENCIA_VB_RX.match(linea))
            and not _PROSA_EN_LA_LINEA_RX.search(linea))



#: Las etiquetas de formato que el editor mete alrededor del codigo y que hay
#: que quitar para leerlo. Cualquier otra cosa entre angulos se deja: en los
#: ejemplos de webservice el codigo lleva XML literal —``<soap:Envelope
#: xmlns:soap=...>``— y quitar "toda etiqueta" se llevaba la peticion entera.
_FORMATO_ALREDEDOR_DEL_CODIGO_RX = re.compile(
    r'(?i)</?(?:span|font|strong|b|em|i|u|small|code|a|p|div)\b[^>]*>')


def _solo_texto_del_trozo(html_trozo: str) -> str:
    """El texto de un trozo de parrafo, sin el formato pero con su contenido."""
    limpio = _FORMATO_ALREDEDOR_DEL_CODIGO_RX.sub('', html_trozo or '')
    return html_lib.unescape(limpio).replace(' ', ' ').strip()


def codigo_suelto_en_parrafo_a_pre(html_fragment: str) -> str:
    """
    Saca a un ``<pre>`` el codigo que viene metido en un parrafo de prosa.

    El origen escribe la explicacion y la instruccion en el **mismo** parrafo,
    separadas por ``<br>``::

        <p>Instruccion para cambiar el puntero del raton.<br><br>
        gCn.Obj.HourglassAll(true)<br><br>gCn.Obj.HourglassAll(False)</p>

    Publicado, las dos llamadas salian como prosa: sin monoespaciado, sin
    resaltado y sin distinguirse de la frase que las explica. Son 537 lineas
    en 107 articulos, casi todos de personalizacion.

    Solo se saca lo que **es** una sentencia —``Set``, ``Dim``, ``Sub``, una
    llamada con punto, un ``If ... Then``— y solo cuando en el mismo parrafo
    queda prosa: un parrafo entero de codigo ya lo recoge otra regla.
    """
    if not html_fragment or '<br' not in html_fragment.lower():
        return html_fragment

    def partir(m: re.Match) -> str:
        interior = m.group(2)
        if '<br' not in interior.lower():
            return m.group(0)
        crudos = re.split(r'(?i)<br\s*/?>', interior)
        limpios = [_solo_texto_del_trozo(x) for x in crudos]
        sentencias = [_es_sentencia(x) for x in limpios]
        if not any(sentencias):
            return m.group(0)
        # Una continuacion o un comentario van con el codigo, aunque por si
        # solos no sean una instruccion. Y lo que sigue a una continuacion la
        # termina, sea lo que sea.
        marcas: list[bool] = []
        venia_a_medias = False
        for texto, es in zip(limpios, sentencias):
            marcas.append(bool(es or venia_a_medias or _acompana_al_codigo(texto)))
            if texto.strip():
                venia_a_medias = bool(_CONTINUACION_DE_LINEA_RX.search(texto.strip()))
        if all(marcas or [False]):
            return m.group(0)
        if not any(x and not c for x, c in zip(limpios, marcas)):
            return m.group(0)           # lo que no es codigo esta vacio: nada que separar

        piezas: list[str] = []
        buffer_codigo: list[str] = []

        def cerrar_codigo():
            if buffer_codigo:
                texto = '\n'.join(buffer_codigo)
                piezas.append(f'<pre><code>{html_lib.escape(texto, quote=False)}</code></pre>')
                buffer_codigo.clear()

        buffer_prosa: list[str] = []

        def cerrar_prosa():
            if buffer_prosa:
                piezas.append('<p>' + '<br>'.join(buffer_prosa) + '</p>')
                buffer_prosa.clear()

        for crudo, limpio, es_codigo in zip(crudos, limpios, marcas):
            if not limpio:
                continue
            if es_codigo:
                cerrar_prosa()
                buffer_codigo.append(limpio)
            else:
                cerrar_codigo()
                buffer_prosa.append(crudo.strip())
        cerrar_codigo()
        cerrar_prosa()
        return ''.join(piezas)

    return re.sub(r'(?is)<p([^>]*)>(.*?)</p>', partir, html_fragment)


def quitar_anclas_vacias_repetidas(html_fragment: str) -> str:
    """
    Borra el ancla vacia cuyo destino ya tiene otro enlace con texto.

    El editor de Freshdesk deja anclas sin nada dentro, y la regla que las
    etiqueta con su URL las convertia en un enlace mas. Cuando el mismo
    destino ya estaba enlazado con un texto legible, el resultado era la misma
    direccion repetida dos y tres veces seguidas::

        [https://we.tl/t-h0aLXCuCFw](...)[https://we.tl/t-h0aLXCuCFw](...)[Descarga documentación](...)

    Son 62 anclas en 39 articulos. El ancla vacia que **no** tiene pareja no
    se toca: ahi la URL es lo unico que se puede enseñar.
    """
    if not html_fragment or '<a' not in html_fragment.lower():
        return html_fragment

    sopa = BeautifulSoup(html_fragment, 'html.parser')
    con_texto = {a.get('href') for a in sopa.find_all('a', href=True)
                 if a.get_text(' ', strip=True) or a.find('img')}
    #: Destinos ya enlazados por un ancla vacía anterior.
    ya_vistas: set = set()

    def borrar(m: re.Match) -> str:
        etiqueta = m.group(0)
        # Una imagen dentro SÍ es contenido: el ancla se ve y se pulsa. Sin
        # esta salvedad el ancla de un banner se borraba a sí misma, porque su
        # propio destino figuraba en la lista de los que tienen contenido.
        if re.search(r'(?i)<img\b', m.group(2) or ''):
            return etiqueta
        if re.sub(r'(?is)<[^>]+>|&nbsp;|\s', '', m.group(2)):
            return etiqueta             # tiene contenido
        href = re.search(r'(?is)\bhref\s*=\s*(["\'])(.*?)\1', m.group(1))
        if not href:
            return etiqueta
        destino = html_lib.unescape(href.group(2))
        if destino in con_texto:
            return ''
        # Dos anclas vacías al mismo sitio publican la misma URL dos veces
        # seguidas. Se queda la primera, que es la que lleva el enlace.
        if destino in ya_vistas:
            return ''
        ya_vistas.add(destino)
        return etiqueta

    return re.sub(r'(?is)<a([^>]*)>(.*?)</a>', borrar, html_fragment)


#: De dónde puede colgar un vídeo en esta documentación.
_VIDEOS_ENLAZADOS_RX = (
    re.compile(r'(?i)https?://(?:www\.)?youtube(?:-nocookie)?\.com/embed/([\w-]+)[^"\'<>)\s]*'),
    re.compile(r'(?i)https?://(?:www\.)?youtube\.com/watch\?[^"\'<>)\s]*v=([\w-]+)[^"\'<>)\s]*'),
    re.compile(r'(?i)https?://youtu\.be/([\w-]+)[^"\'<>)\s]*'),
    re.compile(r'(?i)https?://(?:www\.)?youtube\.com/playlist\?[^"\'<>)\s]*list=([\w-]+)[^"\'<>)\s]*'),
    re.compile(r'(?i)https?://videos\.ahora\.es/[^"\'<>)\s\]]*'),
)

#: Lo que se espera de un servidor que está vivo. Más de esto y la ejecución se
#: alarga por nada: los 44 enlaces a un servidor caído tardarían lo mismo cada
#: uno, así que el servidor se prueba **una vez** y su veredicto vale para
#: todos sus enlaces.
_ESPERA_DE_VIDEO = 6


def _responde(url: str, metodo: str = 'HEAD') -> tuple:
    """(codigo, motivo). ``codigo`` es None si no hubo respuesta."""
    try:
        r = SESSION.request(metodo, url, timeout=_ESPERA_DE_VIDEO, allow_redirects=True)
        return r.status_code, ''
    except requests.exceptions.RequestException as e:
        return None, type(e).__name__


def _se_ve_el_video(url: str, hosts_caidos: set) -> tuple:
    """(se_ve, explicación). ``se_ve`` None si no se ha podido comprobar."""
    host = urllib.parse.urlparse(url).netloc.lower()
    if host in hosts_caidos:
        return False, 'el servidor no responde'

    if 'youtube.com/playlist' in url:
        codigo, _ = _responde(url, 'GET')
        if codigo == 200:
            return True, ''
        if codigo is None:
            return None, 'no se pudo comprobar'
        return False, f'la lista de reproducción responde {codigo}'

    vid = None
    for rx in _VIDEOS_ENLAZADOS_RX[:3]:
        m = rx.search(url)
        if m:
            vid = m.group(1)
            break
    if vid:
        # oEmbed responde 200 si el vídeo existe y es público, y 401/403/404
        # si lo han quitado, es privado o no admite incrustarse.
        consulta = ('https://www.youtube.com/oembed?format=json&url='
                    + urllib.parse.quote(f'https://www.youtube.com/watch?v={vid}', safe=''))
        codigo, _ = _responde(consulta, 'GET')
        if codigo == 200:
            return True, ''
        if codigo in (401, 403):
            return False, f'privado o no se puede incrustar (YouTube responde {codigo})'
        if codigo == 404:
            return False, 'el vídeo ya no existe (YouTube responde 404)'
        if codigo is None:
            return None, 'no se pudo comprobar'
        return False, f'YouTube responde {codigo}'

    codigo, motivo = _responde(url)
    if codigo and 200 <= codigo < 400:
        return True, ''
    if codigo is None:
        hosts_caidos.add(host)
        return False, 'el servidor no responde'
    return False, f'responde {codigo}'


def buscar_videos_que_no_se_ven(docs_folder: Path) -> tuple:
    """
    Comprueba uno a uno los vídeos enlazados y devuelve los que no se ven.

    Un vídeo roto no se nota: el hueco del reproductor sale en blanco y el
    enlace parece bueno hasta que alguien lo pulsa. Y no hay forma de saberlo
    sin preguntar, porque el problema está fuera de esta documentación.

    Devuelve ``(rotos, cuantos_se_ven)``, donde ``rotos`` es una lista de
    ``(url, motivo, [artículos])`` ordenada por motivo.
    """
    por_url: dict = {}
    for md_file in sorted(docs_folder.rglob('*.md')):
        texto = md_file.read_text(encoding='utf-8', errors='replace')
        if 'youtu' not in texto and 'videos.ahora.es' not in texto:
            continue
        rel = md_file.relative_to(docs_folder).as_posix()
        for rx in _VIDEOS_ENLAZADOS_RX:
            for m in rx.finditer(texto):
                por_url.setdefault(m.group(0).rstrip('.,);'), set()).add(rel)

    hosts_caidos: set = set()
    rotos = []
    se_ven = 0
    for url in sorted(por_url):
        ok, motivo = _se_ve_el_video(url, hosts_caidos)
        if ok:
            se_ven += 1
        elif ok is False:
            rotos.append((url, motivo, sorted(por_url[url])))
    rotos.sort(key=lambda x: (x[1], x[0]))
    return rotos, se_ven


#: Los huecos donde puede aparecer una sentencia suelta.
_HUECOS_DE_CODIGO = ('p', 'td', 'li', 'em', 'strong', 'i', 'b')

#: Lo que descarta que el hueco sea una sentencia suelta: si dentro hay otro
#: bloque, un salto, una imagen o ya hay código, esto no es el caso simple.
_HAY_ALGO_MAS_RX = re.compile(r'(?i)<(?:p|td|li|table|ul|ol|pre|code|img|br)\b')


def _texto_de_hueco(el) -> str:
    return (el.get_text(' ', strip=True) or '').replace('\xa0', ' ').strip()


#: Una sentencia que se queda a medias: la siguiente linea la continua, asi
#: que esto es un bloque, no una instruccion suelta.
_SENTENCIA_A_MEDIAS_RX = re.compile(r'(?i)(?:[(,+&_]|\bthen|\bas)\s*$')

#: Una linea que CONTINUA la sentencia anterior en vez de empezar una nueva.
#: Son clausulas sueltas de SQL, que no chocan con la prosa castellana. Sin
#: esto, en una consulta partida en varios parrafos solo se marcaba el trozo
#: del medio -el unico que empieza por algo con pinta de sentencia- y quedaba
#: una linea monoespaciada suelta dentro de una consulta en texto plano.
_CONTINUACION_DE_SENTENCIA_RX = re.compile(
    r'(?i)^(?:from|where|on|and|or|values|set|having|union(?:\s+all)?'
    r'|(?:inner|left|right|full|cross)(?:\s+outer)?\s+join|join'
    r'|order\s+by|group\s+by)\b')


def _continua_una_sentencia(el) -> bool:
    """Es este hueco la continuacion de la sentencia del hueco anterior?"""
    texto = _texto_de_hueco(el)
    return (len(texto) > 8
            and bool(_CONTINUACION_DE_SENTENCIA_RX.match(texto))
            and not _PROSA_EN_LA_LINEA_RX.search(texto))


def _la_tirada_entera(el) -> list:
    """Los huecos seguidos que forman una misma sentencia, con el de dentro."""
    tirada = [el]
    # Hacia atras: el de antes entra si tiene forma de sentencia o si se
    # quedaba a medias, porque entonces era este el que lo terminaba.
    v, previo = el.find_previous_sibling(), el
    while v is not None and (_es_de_la_tirada(v) or _se_queda_a_medias(v)):
        tirada.append(v)
        v, previo = v.find_previous_sibling(), v
    # Hacia delante: el de despues entra si tiene forma de sentencia o si el
    # anterior se quedaba a medias. Asi entra la lista de columnas pelada que
    # sigue a un ``INSERT INTO Tabla (IdOferta, Revision,``.
    previo, v = el, el.find_next_sibling()
    while v is not None and (_es_de_la_tirada(v) or _se_queda_a_medias(previo)):
        tirada.append(v)
        previo, v = v, v.find_next_sibling()
    return tirada


def _es_hueco_de_sentencia(el, entera: bool = True) -> bool:
    """
    Con ``entera``, la que se queda a medias no cuenta: la siguiente linea la
    continua, asi que es un bloque. Sin ``entera`` solo se pregunta si la
    linea tiene forma de sentencia, que es lo que hace falta para reconocer
    la primera de una tirada.
    """
    if el.find(['p', 'td', 'li', 'table', 'ul', 'ol', 'pre', 'code', 'img', 'br']):
        return False
    texto = _texto_de_hueco(el)
    if entera and _SENTENCIA_A_MEDIAS_RX.search(texto):
        return False
    return _es_sentencia(texto, con_comentario=False)


def _se_queda_a_medias(el) -> bool:
    """La linea acaba en ``(``, ``,``, ``Then``...: la siguiente la termina."""
    return (getattr(el, 'name', None) in _HUECOS_DE_CODIGO
            and bool(_SENTENCIA_A_MEDIAS_RX.search(_texto_de_hueco(el))))


def _es_de_la_tirada(el) -> bool:
    return (getattr(el, 'name', None) in _HUECOS_DE_CODIGO
            and (_es_hueco_de_sentencia(el, entera=False) or _continua_una_sentencia(el)))


def sentencia_suelta_a_codigo(html_fragment: str) -> str:
    """
    Marca como código la sentencia que va **sola** en su hueco.

    El origen deja instrucciones sueltas en su propio párrafo, en una celda o
    en un punto de lista, sin nada que las distinga de la prosa::

        <p><em>SELECT * FROM Conta_Apuntes_Bloqueos_Tipos</em></p>
        <li>UPDATE Ceesi_configuracion SET Valor = 'ON' WHERE Parametro = 'SII'</li>
        <td>gform.ControlesDDA("NombreControl").Text</td>

    Se envuelve en ``<code>``, no en un bloque: una sentencia dentro de una
    celda o de un punto de lista no puede ser un bloque sin romper la tabla o
    la lista, y en un párrafo el código en línea ya la distingue.

    **Sola de verdad.** Si el hueco de al lado también es una sentencia, esto
    no es una instrucción suelta sino una línea de un bloque, y ese bloque lo
    reconstruye después ``repair_vb_reference_markdown`` en un fence con su
    lenguaje. Marcando la primera línea por su cuenta se rompía esa
    reconstrucción: un ``CREATE TABLE [dbo].[Tab_PruebasA](`` se llevaba el
    fence entero, y las columnas de debajo acababan de prosa —con
    ``[Descrip] [varchar](50) NULL`` publicado como un **enlace roto**,
    porque en Markdown eso es la sintaxis de un enlace—.

    La énfasis desaparece al marcar el código: una consulta en cursiva *y*
    monoespaciada es peor que cualquiera de las dos cosas por separado.

    Y una frase que habla de código no es código: ``INSERT INTO: se usa para
    añadir uno o varios registros`` explica el ``INSERT``, no lo ejecuta.
    """
    if not html_fragment:
        return html_fragment
    if not re.search(r'(?i)<(?:' + '|'.join(_HUECOS_DE_CODIGO) + r')\b', html_fragment):
        return html_fragment

    sopa = BeautifulSoup(html_fragment, 'html.parser')
    a_marcar = []
    for el in sopa.find_all(_HUECOS_DE_CODIGO):
        if not _es_hueco_de_sentencia(el, entera=False):
            continue
        antes, despues = el.find_previous_sibling(), el.find_next_sibling()
        del_bloque = ((antes is not None and (_es_de_la_tirada(antes)
                                              or _se_queda_a_medias(antes)))
                      or (despues is not None and (_es_de_la_tirada(despues)
                                                   or _se_queda_a_medias(el))))
        if not del_bloque:
            # Sola: solo se marca si es una sentencia entera. La que se queda
            # a medias sin nadie al lado no es una instruccion, es un resto.
            if _es_hueco_de_sentencia(el):
                a_marcar.append(str(el))
            continue
        if el.find_parent('td') is None:
            continue                     # es una línea de un bloque, no una suelta
        # Dentro de una celda no hay fence que reconstruir: la tabla se
        # conserva en HTML tal cual. Asi que la consulta partida en varios
        # <p> se marca ENTERA, linea a linea, en vez de dejarla de prosa.
        for hermano in _la_tirada_entera(el):
            a_marcar.append(str(hermano))

    limpio = html_fragment
    for viejo in dict.fromkeys(a_marcar):
        m = re.match(r'(?is)<(\w+)([^>]*)>(.*)</\1\s*>$', viejo)
        if not m:
            continue
        interior = _FORMATO_ALREDEDOR_DEL_CODIGO_RX.sub('', m.group(3)).strip()
        if m.group(1).lower() in ('em', 'strong', 'i', 'b'):
            nuevo = f'<code>{interior}</code>'
        else:
            nuevo = f'<{m.group(1)}{m.group(2)}><code>{interior}</code></{m.group(1)}>'
        limpio = limpio.replace(viejo, nuevo)
    return limpio


def limpiar_atributos_de_freshdesk(html_fragment: str) -> str:
    """
    Quita de una tabla en crudo los atributos que arrastran URLs de Freshdesk.

    El editor de Freshdesk deja en cada ``<img>`` un rastro de atributos suyos
    —``data-filelink``, ``data-fileid``, ``data-linked-resource-*``— y uno de
    ellos guarda la URL original en S3. La imagen se descarga bien y el ``src``
    queda apuntando a local, pero esa URL se publicaba igualmente dentro del
    HTML: no se ve en la página, pero está en el fichero y caduca como
    cualquier otro enlace a Freshdesk.

    ``src`` y ``href`` no se tocan: de esos se encargan la descarga de imágenes
    y la corrección de enlaces.
    """
    def limpiar_etiqueta(match: re.Match) -> str:
        etiqueta = match.group(0)

        def quitar(attr: re.Match) -> str:
            nombre, valor = attr.group(1).lower(), attr.group(3)
            if nombre in ('src', 'href'):
                return attr.group(0)
            if re.search(_FRESHDESK_HOST, valor, re.IGNORECASE):
                return ''
            return attr.group(0)

        return _ATTR_CON_URL_RX.sub(quitar, etiqueta)

    limpio = _HTML_TAG_RX.sub(limpiar_etiqueta, html_fragment or '')
    limpio = desenvolver_encabezados_html_sin_texto(limpio)
    limpio = ascender_cabecera_de_tabla(limpio)
    return quitar_clases_de_tabla(quitar_clases_del_editor(limpio))


#: Las clases que deja Froala, el editor de Freshdesk. Todas empiezan por
#: ``fr-``: ``fr-no-borders``, ``fr-alternate-rows``, ``fr-dashed-borders``…
_CLASE_DE_FROALA_RX = re.compile(r'(?i)\bfr-[\w-]+')

#: El atributo ``class`` de una etiqueta.
_ATTR_CLASS_RX = re.compile(r'''(?is)\s+class\s*=\s*(["'])(.*?)\1''')


def quitar_clases_del_editor(html_fragment: str) -> str:
    """
    Quita de las tablas conservadas las clases del editor de Freshdesk.

    No es limpieza estética: **bloquean el estilo del tema**. Material aplica
    todo lo suyo con el selector ``.md-typeset table:not([class])`` —bordes,
    relleno, cabecera, hover— y envuelve la tabla en un
    ``md-typeset__scrollwrap`` con el mismo criterio, para que las anchas se
    puedan desplazar en vez de desbordarse.

    Una tabla con ``class="fr-no-borders"`` deja de cumplir ese selector, así
    que se publicaba **sin ningún estilo y sin scroll**. Y no hay nada que la
    estilice en su lugar: en el CSS del tema no existe una sola regla ``fr-``.
    Eran **1.147 de 2.381 tablas**, casi la mitad, y entre ellas una de 29
    columnas que se salía de la pantalla.

    Solo se quitan las clases ``fr-*``; si la etiqueta tuviera alguna otra, se
    conserva y el atributo se queda.
    """
    def limpiar(m: re.Match) -> str:
        clases = [c for c in m.group(2).split() if not _CLASE_DE_FROALA_RX.fullmatch(c)]
        if not clases:
            return ''
        return f' class={m.group(1)}{" ".join(clases)}{m.group(1)}'

    return _ATTR_CLASS_RX.sub(limpiar, html_fragment or '')


#: La etiqueta de apertura de una tabla o de una de sus partes, con su
#: ``class``. Acotado por etiqueta a propósito: así no se toca el
#: ``<div class="grid cards">`` de Material que lleva la portada a mano.
_TABLA_CON_CLASE_RX = re.compile(
    r'''(?is)(<(?:table|thead|tbody|tfoot|tr|td|th|col|colgroup)\b[^>]*?)'''
    r'''\s+class\s*=\s*(["']).*?\2'''
)


def quitar_clases_de_tabla(html_fragment: str) -> str:
    """
    Quita **todas** las clases de una tabla conservada en crudo.

    Las de Froala eran la mayoría, pero al limpiarlas quedaron 6 tablas con
    clases de otras procedencias: ``MsoNormalTable`` (Word), un puñado de
    Tailwind (``min-w-full border-collapse text-sm``, seguramente contenido
    pegado desde otra herramienta), ``ticket-editor-apply-border``,
    ``table table-sm``…

    Ninguna está definida en ninguna hoja de estilo del sitio —comprobado
    contra ``extra_css`` y ``overrides/``— así que no pintan nada y sí
    estorban: con el atributo puesto, la tabla deja de cumplir
    ``.md-typeset table:not([class])`` y pierde todo el estilo del tema y el
    contenedor con scroll.

    Se aplica solo a las etiquetas de tabla, y solo dentro del fragmento que
    viene de Freshdesk: el ``<div class="grid cards">`` de la portada no pasa
    por aquí, y aunque pasara, no es una etiqueta de tabla.
    """
    return _TABLA_CON_CLASE_RX.sub(r'\1', html_fragment or '')


#: Apertura o cierre de tabla, para poder contar la profundidad.
_TABLE_TAG_RX = re.compile(r'(?is)<(/)?table\b[^>]*?(/)?>')


#: Lo que hace que una tabla merezca conservarse: texto, una imagen o un
#: enlace. Las que solo llevan imágenes son legítimas —el origen las usa para
#: maquetar galerías— y por eso ``<img>`` cuenta como contenido.
_TABLA_CON_CONTENIDO_RX = re.compile(r'(?i)<(?:img|a)\b')


def _tabla_vacia(tabla: str) -> bool:
    """
    ¿Esta tabla no enseña absolutamente nada?

    El editor del origen deja cascarones como
    ``<table><tbody><tr><td style="width: 50%"></td><td></td></tr></tbody></table>``:
    sin texto, sin imágenes y sin enlaces. En la página son un hueco en blanco.
    """
    if _TABLA_CON_CONTENIDO_RX.search(tabla):
        return False
    sin_marcado = re.sub(r'(?is)<[^>]+>', '', tabla)
    return not sin_marcado.replace('&nbsp;', '').strip()


def protect_html_tables(html: str) -> tuple[str, dict[str, str]]:
    """
    Sustituye tablas HTML por tokens para preservar su estructura real durante
    la conversión a Markdown.

    Las tablas **se anidan**, y eso no lo puede resolver una expresión regular.
    Con ``<table>.*?</table>`` una tabla dentro de otra casaba desde la
    apertura de la exterior hasta el cierre de la **interior**, y el cierre de
    la exterior se quedaba huérfano. El artículo acababa con una tabla sin
    cerrar y, a partir de ahí, **Python-Markdown deja de procesar Markdown**:
    encabezados, negritas, listas y enlaces salían en crudo hasta el final del
    documento.

    Por eso se recorre contando profundidad y se extraen solo las tablas de
    primer nivel, con su contenido anidado dentro.
    """
    html = html or ''
    table_map: dict[str, str] = {}
    piezas: list[str] = []
    counter = 1
    profundidad = 0
    inicio = 0        # dónde empezó la tabla exterior en curso
    ultimo_corte = 0  # hasta dónde se ha volcado ya texto normal

    for m in _TABLE_TAG_RX.finditer(html):
        es_cierre, autocerrada = m.group(1), m.group(2)
        if autocerrada:               # <table/>, rarísimo pero no abre nada
            continue

        if not es_cierre:
            if profundidad == 0:
                piezas.append(html[ultimo_corte:m.start()])
                inicio = m.start()
            profundidad += 1
            continue

        if profundidad == 0:
            # Cierre suelto sin apertura: se descarta, o dejaría el HTML
            # descompensado igual que antes.
            piezas.append(html[ultimo_corte:m.start()])
            ultimo_corte = m.end()
            continue

        profundidad -= 1
        if profundidad == 0:
            tabla = html[inicio:m.end()]
            if _tabla_vacia(tabla):
                # Cascarón del editor del origen: filas y celdas con anchos,
                # y nada dentro. En la página ocupa hueco y no enseña nada.
                ultimo_corte = m.end()
                continue

            token = f'%%HTMLTABLE_{counter}%%'
            counter += 1
            table_map[token] = tabla
            piezas.append(f'\n\n{token}\n\n')
            ultimo_corte = m.end()

    if profundidad > 0:
        # Tabla sin cerrar en el origen: se protege hasta el final para no
        # dejar la etiqueta abierta suelta en el Markdown.
        token = f'%%HTMLTABLE_{counter}%%'
        table_map[token] = html[inicio:] + '</table>' * profundidad
        piezas.append(f'\n\n{token}\n\n')
    else:
        piezas.append(html[ultimo_corte:])

    return ''.join(piezas), table_map


# ---------------------------------------------------------------------------
# Corrección de enlaces internos de Freshdesk
# ---------------------------------------------------------------------------

#: Solape mínimo de palabras para aceptar una resolución difusa de título.
#: Con 1 bastaba una única palabra compartida y se producían enlaces erróneos.
MIN_FUZZY_TOKEN_OVERLAP = 2

#: Cualquier etiqueta HTML del Markdown. Las tablas se conservan como HTML
#: crudo a propósito, así que el texto lleva atributos dentro.
#:
#: El nombre de etiqueta se exige de verdad (letra y luego letras, dígitos o
#: guiones) para no tragarse un autolink de Markdown: ``<https://…>`` empieza
#: por ``<h`` y con un patrón laxo pasaba por etiqueta, así que las reglas lo
#: daban por HTML y no lo tocaban nunca.
_HTML_TAG_RX = re.compile(r'(?s)</?[a-zA-Z][a-zA-Z0-9-]*(?:\s[^>]*)?/?>')

#: Autolink de Markdown: una URL entre ángulos.
_AUTOLINK_RX = re.compile(r'<(https?://[^\s<>]+)>')

#: Ancla HTML completa, con su texto.
_HTML_ANCHOR_RX = re.compile(
    r'(?is)<a\b[^>]*?\bhref\s*=\s*(["\'])(?P<url>.*?)\1[^>]*>(?P<texto>.*?)</a>'
)

#: Dominio de Freshdesk, en cualquiera de sus dos formas.
_FRESHDESK_HOST = r'freshdesk\.(?:com|es)'

#: Cualquier URL de Freshdesk que haya sobrevivido a las reglas anteriores.
#: Los corchetes quedan fuera de la clase a propósito: sin eso, en un
#: ``![<url>](destino.png)`` la expresión se comía también el ``]`` de cierre y
#: rompía la imagen.
#: El esquema es opcional: el HTML de origen trae también enlaces sin él
#: (``//ahora.freshdesk.com``), y sin contemplarlos se colaban enteros.
#:
#: El ``(?<![:/\w])`` de delante no es adorno: sin él, en ``https://x`` la
#: expresión podía empezar a casar en el ``//`` de dentro del propio esquema.
#: Al borrar la URL dejaba un ``![foto](https:)`` y se cargaba la imagen.
_URL_CHAR = r'[^\s()<>\[\]"\'`]'
_ESQUEMA = r'(?<![:/\w])(?:https?:)?//'
_FRESHDESK_URL_RX = re.compile(rf'(?i){_ESQUEMA}{_URL_CHAR}*{_FRESHDESK_HOST}{_URL_CHAR}*')


#: Lo que un nombre de servidor no puede contener nunca. Un espacio —o su
#: forma codificada— delata que ahí hay prosa, no una dirección.
_HOST_IMPOSIBLE_RX = re.compile(r'(?i)\s|%20|,|;|"')

#: Ninguna URL de esta documentación se acerca de lejos a este tamaño.
_LARGO_MAXIMO_DE_URL = 300


def url_es_plausible(url: str) -> bool:
    """
    Dice si eso puede ser una dirección de verdad.

    En Freshdesk hay artículos donde alguien pegó un párrafo entero en el
    campo del enlace: queda un ``href`` de mil caracteres con la prosa del
    propio artículo codificada y un ``http://`` delante. Tratarla como una URL
    normal la sacaba a la página como texto visible.

    El listón es deliberadamente bajo: solo se descarta lo que **no puede** ser
    un servidor. Un ``http://servidor:puerto/api`` es un marcador de posición
    de la documentación, perfectamente intencionado, y tiene que sobrevivir.
    """
    url = (url or '').strip()
    if not url or len(url) > _LARGO_MAXIMO_DE_URL:
        return False
    host = urllib.parse.urlparse(url).netloc
    if not host or len(host) > 80:
        return False
    return not _HOST_IMPOSIBLE_RX.search(host)


def _html_tag_spans(text: str) -> list[tuple[int, int]]:
    """Posiciones de las etiquetas HTML, para no sustituir dentro de ellas."""
    return [(m.start(), m.end()) for m in _HTML_TAG_RX.finditer(text)]


def _sub_outside_html(pattern: re.Pattern, repl, text: str) -> str:
    """
    Como ``pattern.sub`` pero saltándose lo que caiga dentro de una etiqueta.

    Una URL dentro de ``href="..."`` no es una URL suelta: al borrarla, la
    expresión se llevaba por delante también la comilla de cierre y dejaba el
    atributo partido (``<a href=" rel="noopener">``). Se comparan **posiciones**,
    sin tocar el texto, para que los desplazamientos no se descuadren.
    """
    spans = _html_tag_spans(text)
    if not spans:
        return pattern.sub(repl, text)

    for m in reversed(list(pattern.finditer(text))):
        if any(a <= m.start() < b for a, b in spans):
            continue
        nuevo = repl(m) if callable(repl) else m.expand(repl)
        text = text[:m.start()] + nuevo + text[m.end():]
    return text


def destinos_ya_enlazados(md_content: str) -> set[str]:
    """
    Destinos que ya tienen en el artículo un enlace **con texto**.

    El editor de Freshdesk deja detrás de un enlace bueno una ristra de ``<a>``
    vacíos al mismo sitio. Invisibles no molestaban; al ponerles el nombre del
    fichero se convertían en duplicados a la vista — cuatro veces el mismo
    enlace al final del artículo.

    Se calcula de una vez, **antes** de tocar nada: durante la sustitución el
    documento todavía lleva las URLs de origen, así que comparar contra el
    destino ya resuelto no encontraría nada. Y así tampoco importa que el
    enlace bueno vaya antes o después de los restos.
    """
    destinos: set[str] = set()
    for m in re.finditer(r'\[([^\]]+)\]\(([^)\s]+)', md_content):
        # Un enlace metido dentro del título de otro —``[](A.md "[x](A.md)")``,
        # que el origen genera mal formado— no cuenta: si contara, el enlace
        # de fuera se daría por duplicado y se perdería.
        if md_content[m.start() - 1:m.start()] == '"':
            continue
        if m.group(1).strip():
            destinos.add(m.group(2))
    for m in _HTML_ANCHOR_RX.finditer(md_content):
        if _texto_visible(m.group('texto')):
            destinos.add(html_lib.unescape(m.group('url') or '').strip())
    return destinos


def _etiqueta_para_destino(url: str) -> str:
    """
    Texto visible para un enlace que se quedó sin él.

    Si apunta a un artículo, su nombre de fichero es justo el título que le
    falta. Si es una dirección de fuera, la propia URL. Y si no es ni una cosa
    ni otra, cadena vacía: el enlace sobra.
    """
    destino = (url or '').strip()
    if destino.lower().endswith('.md'):
        nombre = urllib.parse.unquote(destino.rsplit('/', 1)[-1])[:-3]
        return nombre.strip()
    if re.match(r'(?i)^(?:https?:)?//', destino) and url_es_plausible(destino):
        return destino
    return ''


def _texto_visible(html_fragment: str) -> str:
    """Texto de un fragmento HTML, sin etiquetas ni entidades."""
    limpio = _HTML_TAG_RX.sub('', html_fragment or '')
    return re.sub(r'\s+', ' ', html_lib.unescape(limpio)).strip()


def _parece_url(texto: str) -> bool:
    """¿El texto visible de un enlace es, en realidad, una URL?"""
    return bool(re.match(r'(?i)\s*<?https?://', texto or ''))


def _texto_del_slug(url: str) -> str:
    """
    Saca un texto legible del slug de una URL de Freshdesk.

    ``/articles/44001761035-portal-gestion-de-licencias`` da
    *Portal gestion de licencias*. Sirve para no dejar la frase coja cuando el
    enlace no se puede traducir a un artículo local.
    """
    slug = re.search(r'/articles/\d+-([^/?#)]+)', url or '', re.IGNORECASE)
    if not slug:
        return ''
    legible = urllib.parse.unquote(slug.group(1)).replace('-', ' ').strip()
    return f'_{legible[:1].upper()}{legible[1:]}_' if legible else ''


def fix_internal_links(
    md_content: str,
    current_file_path: Path,
    article_paths: dict[str, str],
    article_paths_by_title: dict[str, str],
    folder_paths: Optional[dict[str, str]],
    counter: list[int],
    category_paths: Optional[dict[str, str]] = None,
) -> str:
    """Repara enlaces internos de Freshdesk apuntando a ficheros .md locales."""
    # El código se aparta ANTES que nada. Dentro de un ejemplo, un `<a href>`
    # es texto del ejemplo, no un enlace que reparar: la regla de anclas lo
    # desenvolvía a su texto visible y, si el ancla solo envolvía una imagen,
    # ese texto era vacío y **se borraba el trozo entero**. Así desaparecía la
    # línea del `<img>` de un ejemplo de HTML.
    md_content, _codigo = _apartar_codigo(md_content)

    # Una imagen envuelta en un enlace a Freshdesk se queda **solo en la
    # imagen**, y esto va antes que todo lo demás. Si no, cada regla ve un
    # ``[![](img)](url-de-freshdesk)`` y toma el ``![`` de la imagen como si
    # fuera el texto del enlace: la imagen acababa apuntando a la URL del
    # enlace, o partida en un ``[![]()``.
    md_content = _IMAGEN_ENVUELTA_EN_FRESHDESK_RX.sub(r'\1', md_content)

    # Qué destinos tienen ya un enlace con texto. Se mira ANTES de tocar nada:
    # durante la sustitución el documento aún lleva las URLs de origen.
    _con_texto = destinos_ya_enlazados(md_content)
    # Un autolink de Markdown (``<url>``) es una URL con dos ángulos alrededor.
    # Se le quitan de entrada para que le lleguen todas las reglas de abajo:
    # así se traduce al artículo local si lo conocemos, en vez de quedarse
    # publicado por no encajar en ninguna forma prevista.
    md_content = _AUTOLINK_RX.sub(
        lambda m: m.group(1) if re.search(_FRESHDESK_HOST, m.group(1), re.IGNORECASE) else m.group(0),
        md_content,
    )
    if folder_paths is None:
        folder_paths = {}
    if category_paths is None:
        category_paths = {}

    def get_relative_local_path(target_abs: str) -> str:
        return relative_posix(current_file_path.parent, Path(target_abs))

    def resolve_target_path(article_id: str, link_text: str, url: str) -> Optional[str]:
        if article_id and article_id in article_paths:
            return article_paths[article_id]

        candidates: list[str] = []
        if link_text:
            candidates.extend(build_article_lookup_keys(link_text))
        if url:
            slug_m = re.search(r'/articles/\d+-([^/?#)]+)', url, re.IGNORECASE)
            if slug_m:
                candidates.extend(build_article_lookup_keys(slug_m.group(1)))

        for ck in dict.fromkeys(c for c in candidates if c):
            if ck in article_paths_by_title:
                return article_paths_by_title[ck]

            tokens = [t for t in ck.split(' ') if len(t) >= 3]
            if not tokens:
                continue

            # Coincidencia exacta por subcadena: solo vale si es inequívoca.
            hits = [k for k in article_paths_by_title if all(t in k for t in tokens)]
            if len(hits) == 1:
                return article_paths_by_title[hits[0]]

            # Fallback por solape de palabras, exigiendo un mínimo real de
            # coincidencias y un único ganador.
            if len(tokens) < MIN_FUZZY_TOKEN_OVERLAP:
                continue
            token_set = set(tokens)
            ranked: list[tuple[int, int, str]] = []
            for key in article_paths_by_title:
                overlap = len(token_set & set(key.split(' ')))
                if overlap >= MIN_FUZZY_TOKEN_OVERLAP:
                    ranked.append((overlap, -len(key), key))
            if not ranked:
                continue
            ranked.sort(reverse=True)
            best_overlap = ranked[0][0]
            best = [key for overlap, _neg_len, key in ranked if overlap == best_overlap]
            if len(best) == 1:
                return article_paths_by_title[best[0]]
        return None

    # 1. Enlaces Markdown con /articles/ID
    md_rx = re.compile(r'(?is)\[([^\]]*)\]\(([^)\s]*?/articles/(\d+)[^)\s]*?)(?:\s+"([^"]*)")?\)')
    for m in reversed(list(md_rx.finditer(md_content))):
        alt = m.group(1)
        url = m.group(2)
        art_id = m.group(3).strip()
        title = html_lib.unescape(m.group(4) or '').strip()
        target = resolve_target_path(art_id, alt, url)
        if not target:
            continue
        rel = get_relative_local_path(target)
        # El origen escribe autoenlaces, con la URL entera de texto visible. Si
        # se deja, el lector ve un pegote de 120 caracteres en vez del nombre
        # del artículo; y peor, otras reglas la toman por una URL suelta.
        if _parece_url(alt):
            alt = Path(target).stem
        if title:
            safe_title = title.replace('"', "'")
            new_link = f'[{alt}]({rel} "{safe_title}")'
        else:
            new_link = f'[{alt}]({rel})'
        md_content = md_content[:m.start()] + new_link + md_content[m.end():]
        counter[0] += 1

    # 2. URLs crudas que no están ya en Markdown.
    #    Una URL dentro de href="..." no es una URL suelta: si se sustituye por
    #    un enlace Markdown, el atributo queda hecho un nudo. Esas se tratan
    #    como anclas en la regla 11.
    # El ``(?<!\[)`` es tan necesario como el ``(?<!\]\()``: cuando el texto del
    # enlace es la propia URL —``[https://.../articles/123](...)``, que es como
    # viene un autoenlace del origen— sin él esta regla envolvía esa URL en OTRO
    # enlace y dejaba ``[[Enlace Interno](destino)](destino)``, que se renderiza
    # enseñando el Markdown en crudo.
    raw_rx = re.compile(r'(?i)(?<!\]\()(?<!\[)(\bhttps?://[^\s()]*?/articles/(\d+)[^\s()]*)\b')
    tag_spans = _html_tag_spans(md_content)
    for m in reversed(list(raw_rx.finditer(md_content))):
        if any(a <= m.start() < b for a, b in tag_spans):
            continue
        target = resolve_target_path(m.group(2).strip(), '', m.group(1))
        if not target:
            continue
        rel = get_relative_local_path(target)
        # La etiqueta es el TÍTULO del artículo de destino, que ya conocemos
        # porque acabamos de resolverlo. Antes se ponía "Enlace Interno", que
        # no le dice nada al lector: en ``Mensaje 'Element PaymentDetails'``
        # quedaba "Enlace: [Enlace Interno](...)" donde el origen traía la URL
        # con su slug —``asignar-el-tipo-de-efecto-de-la-efactura-...``—, así
        # que la información estaba y se tiraba.
        md_content = (md_content[:m.start()]
                      + f'[{_titulo_del_destino(target)}]({rel})'
                      + md_content[m.end():])
        counter[0] += 1

    # Limpiar artefactos del tipo [](freshdesk)[Titulo](local.md)
    md_content = re.sub(
        r'\[\]\((https?://[^)\s]*?/articles/[^)\s]*)(?:\s+"[^"]*")?\)\s*\[([^\]]+)\]\(([^)]+?\.md)\)',
        r'[\2](\3)', md_content, flags=re.IGNORECASE
    )
    md_content = re.sub(
        r'\[\]\(([^)\s]+?\.md)(?:\s+"[^"]*")?\)\s*\[([^\]]+)\]\(([^)]+?\.md)\)',
        r'[\2](\3)', md_content, flags=re.IGNORECASE
    )

    # 3. [](freshdesk) seguido del texto que hace de título
    empty_rx = re.compile(
        r'\[\]\(([^)\s]*?/articles/(\d+)[^)\s]*?)(?:\s+"[^"]*")?\)'
        r'((?:[^\s\[\]\(\),.;:!?][^,\n\r\)\]]{0,120}))'
    )
    for m in reversed(list(empty_rx.finditer(md_content))):
        candidate = re.sub(r'\s+', ' ', m.group(3)).strip()
        if not candidate or len([w for w in candidate.split(' ') if w]) > 8:
            continue
        target = resolve_target_path(m.group(2).strip(), candidate, m.group(1))
        if not target:
            continue
        rel = get_relative_local_path(target)
        md_content = md_content[:m.start()] + f'[{candidate}]({rel})' + md_content[m.end():]
        counter[0] += 1

    # 4. Enlaces a carpetas de Freshdesk cuyo destino local conocemos
    folder_rx = re.compile(r'(?is)\[([^\]]*)\]\(([^)]*?/support/solutions/folders/(\d+)[^)]*?)\)')
    for m in reversed(list(folder_rx.finditer(md_content))):
        fid = m.group(3).strip()
        if fid not in folder_paths:
            continue
        rel = get_relative_local_path(folder_paths[fid])
        if not rel.endswith('/'):
            rel += '/'
        md_content = md_content[:m.start()] + f'[{m.group(1)}]({rel})' + md_content[m.end():]
        counter[0] += 1

    raw_folder_rx = re.compile(r'(?i)(?<!\]\()(\bhttps?://[^\s()]*?/support/solutions/folders/(\d+)[^\s()]*)\b')
    tag_spans = _html_tag_spans(md_content)
    for m in reversed(list(raw_folder_rx.finditer(md_content))):
        if any(a <= m.start() < b for a, b in tag_spans):
            continue
        fid = m.group(2).strip()
        if fid not in folder_paths:
            continue
        rel = get_relative_local_path(folder_paths[fid])
        if not rel.endswith('/'):
            rel += '/'
        md_content = md_content[:m.start()] + f'[Ver Carpeta]({rel})' + md_content[m.end():]
        counter[0] += 1

    # 5. Degradar a texto plano los enlaces de Freshdesk que no se han resuelto
    #
    #    Uno sin texto no se puede borrar sin más: la frase que lo introducía se
    #    queda colgando ("Versión 4.4.2100 o anterior:" y detrás, nada). El
    #    propio enlace lleva el título en su slug —``/articles/123-portal-de-
    #    licencias``—, así que se rescata de ahí y al menos queda dicho a qué
    #    se refería.
    md_content = re.sub(
        r'\[\]\((https?://[^)\s]*?(?:freshdesk\.com|freshdesk\.es)[^)\s]*?/articles/[^)\s]*)(?:\s+"[^"]*")?\)',
        lambda m: _texto_del_slug(m.group(1)), md_content, flags=re.IGNORECASE
    )
    def _degradar_con_texto(match: re.Match) -> str:
        # Si el texto visible era la propia URL, dejarlo tal cual solo sirve
        # para que la regla siguiente —la que borra URLs sueltas— se lo lleve y
        # la frase se quede coja. Se rescata el nombre del slug.
        if _parece_url(match.group(1)):
            return _texto_del_slug(match.group(2))
        return match.group(1)

    md_content = re.sub(
        r'\[([^\]]+)\]\((https?://[^)]*?(?:freshdesk\.com|freshdesk\.es)[^)]*?/articles/[^)]*)\)',
        _degradar_con_texto, md_content, flags=re.IGNORECASE
    )
    md_content = _sub_outside_html(
        re.compile(rf'(?i)https?://[^\s]*?{_FRESHDESK_HOST}[^\s]*?/articles/[^\s)]+'),
        '', md_content,
    )

    # 6. Carpetas de Freshdesk sin destino local conocido → nuevo dominio
    md_content = _sub_outside_html(
        re.compile(
            rf'(?i)https?://[^\s)]*?{_FRESHDESK_HOST}[^\s)]*?'
            r'/(?:support/solutions|a/forums)/folders/(\d+)[^\s)]*'
        ),
        r'https://ayuda.ahora.es/{{producto}}/\1',
        md_content,
    )

    # 7. Enlaces externos que se quedaron sin texto. En el HTML original son
    #    <a href="...">&nbsp;</a>: sin etiqueta se renderizan como un <a>
    #    vacío, invisible, y el lector pierde el enlace (los tutoriales en
    #    vídeo eran el caso habitual). Se les pone la propia URL como texto.
    #
    #    Salvo que la URL no sea una URL. Hay artículos donde alguien pegó un
    #    párrafo entero en el campo del enlace, y queda un href de mil y pico
    #    caracteres con la prosa del propio artículo codificada. Poner eso
    #    como texto visible convertía un enlace invisible en un muro de 2.264
    #    caracteres en mitad de la página.
    md_content = re.sub(
        r'(?<!!)\[[ \t\r\n]*\]\((https?://[^)\s]+)\)',
        lambda m: f'[{m.group(1)}]({m.group(1)})' if url_es_plausible(m.group(1)) else '',
        md_content,
    )

    #    Y si el enlace disparatado sí traía texto, se conserva el texto y se
    #    tira el enlace, que no lleva a ninguna parte.
    md_content = re.sub(
        r'(?<!!)\[([^\]]+)\]\((https?://[^)\s]+)\)',
        lambda m: m.group(1) if not url_es_plausible(m.group(2)) else m.group(0),
        md_content,
    )

    # 8. Categorías de Freshdesk cuyo destino local conocemos.
    #    /support/solutions/<id> es una categoría, no un artículo.
    category_rx = re.compile(
        r'(?is)\[([^\]]*)\]\(([^)]*?/support/solutions/(\d+)/?[^)]*?)\)')
    for m in reversed(list(category_rx.finditer(md_content))):
        target = category_paths.get(m.group(3).strip())
        if not target:
            continue
        rel = get_relative_local_path(target)
        if not rel.endswith('/'):
            rel += '/'
        texto = m.group(1) or 'Ver categoría'
        md_content = md_content[:m.start()] + f'[{texto}]({rel})' + md_content[m.end():]
        counter[0] += 1

    # 9. Enlaces a la interfaz de agente de Freshdesk.
    #
    #    /a/solutions/... y /a/tickets/... son la trastienda de Freshdesk: piden
    #    login de agente, así que para quien lee la documentación no llevan a
    #    ninguna parte. Y sus identificadores son de otra cuenta, no están en la
    #    BDD, con lo que tampoco se pueden traducir a un artículo nuestro. Se
    #    quedan en texto plano: se pierde el enlace, que no servía, y se
    #    conserva la frase, que sí.
    md_content = re.sub(
        rf'(?i)\[([^\]]*)\]\(https?://[^)\s]*?{_FRESHDESK_HOST}/a/[^)]*\)',
        lambda m: m.group(1),
        md_content,
    )
    md_content = _sub_outside_html(
        re.compile(rf'(?i)(?<!\]\()\bhttps?://[^\s()]*?{_FRESHDESK_HOST}/a/[^\s()]*'),
        '', md_content,
    )

    # 10. Enlaces locales sin texto visible.
    #
    #     Un ``[](destino.md)`` no se ve en la página: el lector no tiene dónde
    #     pulsar. Si apunta a un artículo, su nombre de fichero es justo el
    #     título que le falta. Si apunta a otra cosa —restos de un <a> que
    #     envolvía una imagen— sobra del todo.
    def _texto_para_enlace_vacio(match: re.Match) -> str:
        destino = match.group(1)
        if not destino.lower().endswith('.md'):
            return ''
        # Si ese destino ya está enlazado con texto en el artículo, esto es
        # un resto del editor —Freshdesk deja cuatro <a> vacíos seguidos al
        # mismo sitio— y ponerle nombre lo convierte en un duplicado visible.
        if destino in _con_texto:
            return ''
        nombre = urllib.parse.unquote(destino.rsplit('/', 1)[-1])[:-3]
        if not nombre.strip():
            return ''
        counter[0] += 1
        return f'[{nombre}]({destino})'

    #     El título es opcional y se descarta: cuando existe, en estos casos es
    #     un duplicado mal formado del propio enlace —``"[Enlace Interno](...)"``—
    #     que no aporta nada.
    md_content = re.sub(
        r'(?<!!)\[[ \t\r\n]*\]\(([^)\s]+)(?:[ \t]+"[^"]*")?\)',
        _texto_para_enlace_vacio,
        md_content,
    )

    # 11. Anclas HTML dentro de las tablas que se conservan en crudo.
    #
    #     Las reglas anteriores solo entienden sintaxis Markdown, así que un
    #     <a href="...freshdesk..."> de una tabla se les escapaba entero. Aquí
    #     se traduce si sabemos a dónde va, y si no se deshace el ancla
    #     dejando su texto: un enlace que pide login de agente no le sirve a
    #     nadie, pero la frase sí.
    def _arreglar_ancla(match: re.Match) -> str:
        url = html_lib.unescape(match.group('url') or '').strip()
        texto = match.group('texto') or ''

        if not re.search(_FRESHDESK_HOST, url, re.IGNORECASE):
            # Un ancla sin texto no se ve: el lector no tiene dónde pulsar.
            # Las reglas de Markdown no llegan aquí, porque esto vive dentro
            # de una tabla que se conserva en crudo.
            #
            # Salvo que lo que lleve dentro sea una **imagen**: entonces sí se
            # ve, y es justo lo que se pulsa. Poniendo la URL de etiqueta se
            # perdía el banner y quedaba la dirección a pelo. Son 7 anclas en
            # 7 artículos, y una de ellas es el banner del canal de YouTube en
            # los Hotfix.
            if _texto_visible(texto) or re.search(r'(?i)<img\b', texto):
                return match.group(0)
            etiqueta = _etiqueta_para_destino(url)
            return f'<a href="{url}">{etiqueta}</a>' if etiqueta else ''

        destino = None
        art = re.search(r'/(?:solution/)?articles/(\d+)', url, re.IGNORECASE)
        if art:
            destino = resolve_target_path(art.group(1), _texto_visible(texto), url)
        if destino is None:
            carpeta = re.search(r'/support/solutions/folders/(\d+)', url, re.IGNORECASE)
            if carpeta:
                destino = folder_paths.get(carpeta.group(1))
        if destino is None:
            categoria = re.search(r'/support/solutions/(\d+)/?(?:$|[?#])', url, re.IGNORECASE)
            if categoria:
                destino = (category_paths or {}).get(categoria.group(1))

        if destino:
            rel = get_relative_local_path(destino)
            # La etiqueta se saca del destino YA resuelto, no de la URL de
            # Freshdesk. Poniendo la URL original, la red de seguridad de la
            # regla 12 la borraba después del texto visible y el ancla se
            # quedaba vacía: un enlace que existe pero no se ve.
            if not _texto_visible(texto):
                if url in _con_texto:
                    return ''      # resto del editor: ya hay un enlace bueno
                texto = _etiqueta_para_destino(rel)
            counter[0] += 1
            return f'<a href="{rel}">{texto}</a>'

        # Sin destino conocido: se queda el texto y se pierde el enlace.
        return texto

    md_content = _HTML_ANCHOR_RX.sub(_arreglar_ancla, md_content)

    # 12. Red de seguridad. Cualquier URL de Freshdesk que siga en pie a estas
    #     alturas es una forma que no habíamos previsto. Degradarla es siempre
    #     mejor que publicarla: lleva a una página que pide login, o a la
    #     cuenta de Freshdesk de otro. Si aparece mucho en el informe
    #     `enlaces-freshdesk.txt`, es que falta una regla específica arriba.
    #     Las imágenes quedan fuera (el ``(?<!!)`` y el ``(?<!\]\()``): si una
    #     no se pudo descargar, sigue apuntando al servidor remoto y ahí se
    #     queda. Una imagen remota se ve; una imagen borrada, no. Las fallidas
    #     se anotan en `imagenes-no-descargadas.txt`.
    #     El ``(?!!\[)`` es la otra mitad de esa protección, y hace falta: el
    #     ``(?<!!)`` cuida de que el patrón no empiece en la imagen, pero no de
    #     que empiece en el corchete que la **envuelve**. Con
    #     ``[![](S3-de-freshdesk)](otra-url)`` el patrón casaba
    #     ``[![](S3…)`` y devolvía como texto solo ``![``, que pegado al resto
    #     daba ``![](otra-url)``: la imagen se quedaba apuntando al enlace de
    #     fuera y desaparecía.
    md_content = re.sub(
        rf'(?i)(?<!!)\[(?!!\[)([^\]]*)\]\({_ESQUEMA}[^)\s]*?{_FRESHDESK_HOST}[^)\s]*(?:[ \t]+"[^"]*")?\)',
        lambda m: m.group(1),
        md_content,
    )
    md_content = _sub_outside_html(
        re.compile(rf'(?i)(?<!\]\(){_ESQUEMA}{_URL_CHAR}*{_FRESHDESK_HOST}{_URL_CHAR}*'),
        '', md_content,
    )

    return _restaurar_codigo(md_content, _codigo)


#: Un bloque ``` con su contenido, o un trozo de código en línea con acentos
#: graves. Es lo que hay que apartar antes de tocar los enlaces.
_CODIGO_RX = re.compile(r'(?s)```.*?```|`[^`\n]+`')


#: Una imagen envuelta en un enlace cuyo destino es de Freshdesk.
#:
#: El editor enlaza la miniatura a la imagen grande, o a la propia ficha del
#: artículo. Ese enlace no lleva a ninguna parte útil una vez publicado, y
#: mientras está ahí desordena todas las reglas de enlaces: ven un
#: ``[![](img)](url)`` y toman el ``![`` de la imagen por el texto del enlace.
_IMAGEN_ENVUELTA_EN_FRESHDESK_RX = re.compile(
    rf'(?i)\[(!\[[^\]]*\]\([^)\s]+(?:[ \t]+"[^"]*")?\))\]'
    rf'\({_ESQUEMA}[^)\s]*?{_FRESHDESK_HOST}[^)\s]*(?:[ \t]+"[^"]*")?\)'
)


def _titulo_del_destino(target_abs: str) -> str:
    """
    El título del artículo de destino, para usarlo como texto del enlace.

    Se saca del nombre del fichero, que es el título con el que se generó, y
    se le quita el sufijo ``(ArticleId)`` que llevan los títulos que colisionan
    —en el texto de un enlace ese número no aporta nada—.

    Si por lo que sea no queda nada legible, se cae a ``Enlace interno``, que
    es lo que se ponía siempre antes.
    """
    nombre = Path(target_abs).stem
    nombre = re.sub(r'\s*\(\d{6,}\)\s*$', '', nombre).strip()
    return nombre or 'Enlace interno'


def _apartar_codigo(md_content: str) -> tuple[str, dict[str, str]]:
    """
    Cambia por un token cada bloque o trozo de código.

    Dentro de un ejemplo, un ``<a href>`` o un ``[texto](destino)`` son texto
    del ejemplo, no enlaces que reparar. ``repair_links.py`` ya lo tenía en
    cuenta —su docstring explica que el SQL está lleno de cosas que parecen un
    enlace—, pero ``fix_internal_links`` no, y eso borraba contenido: la regla
    de anclas desenvolvía el ``<a>`` a su texto visible y, cuando el ancla solo
    envolvía una imagen, ese texto era vacío y desaparecía la línea entera.
    """
    guardado: dict[str, str] = {}

    def apartar(m: re.Match) -> str:
        token = f'%%CODIGOENLACES_{len(guardado)}%%'
        guardado[token] = m.group(0)
        return token

    return _CODIGO_RX.sub(apartar, md_content), guardado


def _restaurar_codigo(md_content: str, guardado: dict[str, str]) -> str:
    """Devuelve a su sitio el código apartado."""
    for token, original in guardado.items():
        md_content = md_content.replace(token, original)
    return md_content


def contar_enlaces_freshdesk(md_content: str) -> collections.Counter:
    """
    Cuenta las URLs de Freshdesk que quedan, agrupadas por forma.

    Sirve para el informe: una cifra que sube avisa de que el HTML de origen
    trae una forma de enlace que ninguna regla contempla.
    """
    formas: collections.Counter = collections.Counter()
    for m in _FRESHDESK_URL_RX.finditer(md_content):
        ruta = re.sub(r'^https?://[^/]+', '', m.group(0))
        for patron, nombre in (
            (r'^/a/solutions/', '/a/solutions/'),
            (r'^/a/tickets/', '/a/tickets/'),
            (r'^/a/forums/', '/a/forums/'),
            (r'^/a/', '/a/ (otro)'),
            (r'^/support/solutions/folders/', '/support/solutions/folders/'),
            (r'^/support/solutions/articles/', '/support/solutions/articles/'),
            (r'^/support/solutions/', '/support/solutions/ (categoría)'),
            (r'^/solution/articles/', '/solution/articles/'),
        ):
            if re.search(patron, ruta, re.IGNORECASE):
                formas[nombre] += 1
                break
        else:
            formas['otra forma'] += 1
    return formas
