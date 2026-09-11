"""
reporting.py
============
Los informes de una ejecución: un único sitio que sabe dónde se escriben, cómo
se llaman y qué hacer cuando no hay nada que contar.

Antes cada módulo se buscaba la vida. ``migrate.py`` escribía en
``<output_dir>/logs`` y ``repair_links.py`` en la carpeta del repositorio, así
que al generar con ``--output-dir`` los informes de una misma ejecución acababan
repartidos en dos sitios. Y, sobre todo, un informe de la ejecución anterior
sobrevivía a una ejecución limpia: mirabas ``conversion_errors_log.txt``, veías
errores y no había forma de saber que eran de la semana pasada. Un log que
miente sin avisar es peor que no tenerlo.

Las dos reglas de aquí:

1. **Todos los informes de una ejecución van juntos**, en ``<output_dir>/logs``.
2. **Lo que está en la carpeta es de esta ejecución.** Si algo no tiene nada que
   contar, su fichero no se escribe, y si quedaba uno viejo con ese nombre, se
   retira.

Requiere Python 3.12 o superior.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

#: Carpeta, colgando del directorio de salida.
LOGS_DIRNAME = 'logs'

RESUMEN = 'resumen.txt'
ARTICULOS_CON_ERROR = 'articulos-con-error.txt'
TITULOS_DUPLICADOS = 'titulos-duplicados.txt'
IMAGENES_NO_DESCARGADAS = 'imagenes-no-descargadas.txt'
ENLACES_ROTOS = 'enlaces-rotos.txt'
ENLACES_FRESHDESK = 'enlaces-freshdesk.txt'
ENLACES_A_CATEGORIA = 'enlaces-a-categoria.txt'
ADJUNTOS_NO_PUBLICADOS = 'adjuntos-no-publicados.txt'
VIDEOS_QUE_NO_SE_VEN = 'videos-que-no-se-ven.txt'
IMAGENES_HUERFANAS = 'imagenes-huerfanas.txt'

#: Qué hay en cada informe. Se usa para el índice del resumen, así que el orden
#: es el que se quiere leer: primero lo que exige actuar.
DESCRIPCIONES: dict[str, str] = {
    RESUMEN: 'Qué ha cambiado en esta ejecución.',
    ARTICULOS_CON_ERROR: 'Artículos que no se pudieron convertir. Se reintentan solos.',
    ENLACES_ROTOS: 'Enlaces a documentación que no está en docs/. Se corrigen a mano.',
    ENLACES_FRESHDESK: 'URLs de Freshdesk que quedaron sin traducir. Falta una regla.',
    ENLACES_A_CATEGORIA: 'Enlaces a una carpeta de categoría. Se dejaron en texto: no tienen página.',
    TITULOS_DUPLICADOS: 'Títulos que colisionan y qué nombre le tocó a cada uno.',
    IMAGENES_NO_DESCARGADAS: 'Imágenes que no se pudieron descargar.',
    ADJUNTOS_NO_PUBLICADOS: 'Ficheros adjuntos del artículo que no se publican. Su URL caduca.',
    VIDEOS_QUE_NO_SE_VEN: 'Vídeos enlazados que ya no se pueden ver. El problema está fuera de aquí.',
    IMAGENES_HUERFANAS: 'Imágenes descargadas que ya no menciona ningún artículo.',
}

NOMBRES: tuple[str, ...] = tuple(DESCRIPCIONES)

#: Nombres de la organización anterior. Se retiran al empezar para que no
#: queden dos generaciones de informes mezcladas en la misma carpeta.
NOMBRES_ANTIGUOS: tuple[str, ...] = (
    'enlaces-sin-reparar.txt',
    'last_run_report.txt',
    'conversion_errors_log.txt',
    'duplicated_titles_log.txt',
    'wiki_ahora_images_log.txt',
    'docs_validation_log.txt',
    'unfixable_links_log.txt',
)

_SEPARADOR = '=' * 70


class RunLogs:
    """
    Los informes de una ejecución concreta.

    Uso típico desde ``migrate.py``::

        logs = RunLogs(output_dir, executed_at)
        logs.clear()                      # al empezar
        logs.write(ARTICULOS_CON_ERROR, 'ARTÍCULOS CON ERROR', lineas)
    """

    def __init__(self, output_dir: Path, executed_at: str = '') -> None:
        self.folder = Path(output_dir) / LOGS_DIRNAME
        self.executed_at = executed_at
        self._written: dict[str, Path] = {}

    # -- rutas ----------------------------------------------------------

    def path(self, name: str) -> Path:
        return self.folder / name

    # -- escritura ------------------------------------------------------

    def clear(self) -> None:
        """
        Retira los informes de la ejecución anterior.

        Solo toca los ficheros que conoce: la carpeta puede tener cosas que ha
        dejado alguien a mano y no es asunto nuestro borrarlas.
        """
        for name in NOMBRES + NOMBRES_ANTIGUOS:
            self.discard(name)

    def discard(self, name: str) -> None:
        """Quita un informe que ya no tiene sentido, si existía."""
        self._written.pop(name, None)
        target = self.path(name)
        if target.exists():
            target.unlink()

    def write(self, name: str, title: str, lines: Iterable[str]) -> Optional[Path]:
        """
        Escribe un informe, o lo retira si no hay nada que contar.

        Devuelve la ruta escrita, o ``None`` si no había contenido.
        """
        body = [str(line).rstrip() for line in lines]
        if not body:
            self.discard(name)
            return None

        self.folder.mkdir(parents=True, exist_ok=True)
        target = self.path(name)

        cabecera = [title, _SEPARADOR]
        if self.executed_at:
            cabecera.append(f'Ejecución del {self.executed_at}')
        cabecera.append('')

        target.write_text('\n'.join(cabecera + body) + '\n', encoding='utf-8')
        self._written[name] = target
        return target

    # -- consulta -------------------------------------------------------

    def written(self) -> list[tuple[str, Path]]:
        """Informes escritos en esta ejecución, en el orden de ``DESCRIPCIONES``."""
        return [(name, self._written[name]) for name in NOMBRES if name in self._written]

    def index_lines(self) -> list[str]:
        """El índice que se pega al final del resumen."""
        otros = [(name, path) for name, path in self.written() if name != RESUMEN]
        if not otros:
            return ['Sin incidencias: no hay más informes que este.']

        ancho = max(len(name) for name, _ in otros)
        lineas = ['Informes de esta ejecución, en la carpeta logs/:']
        lineas += [f'  {name.ljust(ancho)}  {DESCRIPCIONES[name]}' for name, _ in otros]
        return lineas
