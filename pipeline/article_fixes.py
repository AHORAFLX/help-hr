"""
article_fixes.py
================
Parches puntuales para artículos concretos, separados del motor de conversión.

Antes, estos arreglos vivían incrustados a base de ``if article_id == "..."``
dentro de ``migrate.py`` y ``author_articles.py``, y las correcciones de rutas
estaban escritas a mano dentro del pipeline de enlaces. Aquí están todos
juntos, como datos, para que añadir un caso nuevo no obligue a tocar la lógica.

Cómo añadir un parche nuevo:

1. Si es un retoque del Markdown de un artículo, añade un ``ArticleFix`` a
   ``ARTICLE_FIXES`` con su ``article_ids`` (o ``titles``) y sus
   ``substitutions``.
2. Si es un enlace mal escrito en un ``.md`` ya generado, añade una entrada a
   ``LINK_FIXES``.

Requiere Python 3.12 o superior.
"""

from __future__ import annotations

import html as html_lib
import html
import re
from dataclasses import dataclass, field
from typing import Callable, Optional

#: Títulos cuyos fences ``vb`` cortos conviene deshacer: son firmas sueltas,
#: no bloques de código de verdad.
UNWRAP_SHORT_FENCE_TITLES = frozenset({'GeneraApunte', 'Crea Copia Doc'})


# ---------------------------------------------------------------------------
# Transformaciones reutilizables
# ---------------------------------------------------------------------------

def _clean_code_block(block: str) -> str:
    """Deja un bloque de código sin entidades HTML ni fences internos."""
    lines = [html_lib.unescape(line).strip() for line in block.splitlines()]
    return "\n".join(ln for ln in lines if ln and not ln.startswith("```")).strip()


def _wrap_api_reference_sections(md_text: str) -> str:
    """
    Envuelve en fences ``vb`` la firma que sigue a "Implementación:" y el
    bloque que sigue a "Ejemplo de uso:" en los artículos de referencia de API.
    """
    signature_rx = re.compile(
        r"((?:Implementaci\S*n):\n+)(.*?)(\n+(?:Descripci\S*n):)",
        re.IGNORECASE | re.DOTALL,
    )
    usage_rx = re.compile(r"((?:Ejemplo de uso):\n+)(.*)$", re.IGNORECASE | re.DOTALL)

    md_text = signature_rx.sub(
        lambda m: f"{m.group(1)}```vbnet\n{_clean_code_block(m.group(2))}\n```\n\n{m.group(3)}",
        md_text, count=1,
    )
    md_text = usage_rx.sub(
        lambda m: f"{m.group(1)}```vbnet\n{_clean_code_block(m.group(2))}\n```",
        md_text, count=1,
    )
    return re.sub(r"\n{3,}", "\n\n", md_text).strip()


def _move_author_credit_to_end(md_text: str) -> str:
    """
    Mueve la línea de autoría al final del artículo, justo antes del enlace de
    cierre, en lugar de dejarla suelta a mitad del texto.
    """
    credit = '##### Autor: Daniel Ernesto Lutz Llano'
    link_match = re.search(
        r'(\n\[\]\([^)]+DLL%20externa[^)]*\s+"Teclas de acceso [^"]+"\)\s*)$',
        md_text, flags=re.IGNORECASE,
    )
    if not link_match or credit in md_text:
        return md_text
    link_block = link_match.group(1)
    body = md_text[:-len(link_block)].rstrip()
    return f'{body}\n\n{credit}\n\n{link_block.strip()}'


# ---------------------------------------------------------------------------
# Catálogo de parches
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ArticleFix:
    """Un parche aplicable a uno o varios artículos."""

    reason: str
    article_ids: frozenset[str] = frozenset()
    titles: frozenset[str] = frozenset()
    #: Lista de (patrón, reemplazo, flags) aplicados con ``re.sub``.
    substitutions: tuple[tuple[str, str, int], ...] = ()
    #: Reemplazos literales, aplicados con ``str.replace``.
    literals: tuple[tuple[str, str], ...] = ()
    #: Transformación libre, aplicada al final.
    transform: Optional[Callable[[str], str]] = field(default=None)

    def matches(self, article_id: str, title: str) -> bool:
        return article_id in self.article_ids or title in self.titles

    def apply(self, md_text: str) -> str:
        for pattern, replacement, flags in self.substitutions:
            md_text = re.sub(pattern, replacement, md_text, flags=flags)
        for old, new in self.literals:
            md_text = md_text.replace(old, new)
        if self.transform is not None:
            md_text = self.transform(md_text)
        return md_text


#: La ficha de un parametro en "ERP - Parámetros de la aplicación": el nombre
#: en un encabezado y, debajo, la descripción, el módulo y los metadatos. Los
#: dos últimos llegan aquí como ``######`` —el paso que los pasa a negrita va
#: después— pero se admite también la forma en negrita, para poder aplicar
#: esto sobre un .md ya generado.
_FICHA_PARAMETRO_RX = re.compile(
    r'(?ms)^#####[ \t]+\**(?P<nombre>[^*\n]+?)\**[ \t]*$'
    r'(?P<cuerpo>.*?)'
    r'(?=^#####[ \t]|\Z)'
)
_FICHA_META_RX = re.compile(r'(?m)^(?:######[ \t]+|\*\*)(?P<txt>.+?)(?:\*\*)?[ \t]*$')
_FICHA_TIPO_RX = re.compile(
    r'(?i)tipo\s*valor\s*:\s*(?P<tipo>\S+)\s+valor\s+por\s+defecto\s*:\s*(?P<def>.*)')

#: La marca de un bloque de código. Aparte, para no llenar de acentos
#: graves las expresiones regulares de aquí abajo.
BACKTICKS = '```'

#: Por debajo de esto no compensa: tres párrafos sueltos se leen igual de bien.
_FICHAS_MINIMAS = 20

def _es_nombre_de_parametro(nombre: str) -> bool:
    """
    ¿Este encabezado es el nombre de un parámetro o una frase?

    No vale pedir mayúsculas y guiones bajos: los nombres reales llevan Ñ
    (``OFERTAS_DISEÑO``), equis minúscula por "por" (``PEDIDOSxPLANTA``),
    ampersands (``FACTURAS_GASTOS_ &_ACREEDOR_GRUPO_6``) y hasta minúsculas
    sueltas (``Empleados_Presencia_AnticiposAB``). Lo que de verdad los separa
    de una frase es que **no llevan espacios**.
    """
    nombre = nombre.strip()
    return (
        bool(nombre)
        and len(nombre) <= 60
        and nombre.count(' ') <= 1
        and any(c.isalpha() for c in nombre)
    )


def _limpio(texto: str) -> str:
    """
    Junta el texto en una línea y le quita las entidades HTML.

    Sin el ``unescape`` el valor por defecto de ``OFERTAS_CLI_SELECTUNIONART``
    se publicaba como ``&#x20;`` dentro de un código: el lector veía la
    entidad, no el espacio que representa.
    """
    return ' '.join(html.unescape(texto).split())


#: Un bloque de código que llegó aplastado en una sola línea, con la marca de
#: apertura y la de cierre pegadas al contenido. Markdown no lo reconoce como
#: bloque —la marca de apertura no admite acentos graves en su etiqueta—, así
#: que se publicaba como código en línea con el ``sql`` pegado delante:
#: ``sql Select Articulos.IdArticulo...``.
_BLOQUE_APLASTADO_RX = re.compile(
    r'^' + BACKTICKS + r'(?P<lang>[A-Za-z0-9_+-]*)[ \t]+(?P<codigo>.+?)[ \t]*'
    + BACKTICKS + r'$'
)


def _saca_codigo(cuerpo: str) -> tuple[list[str], list[list[str]]]:
    """
    Separa el cuerpo de una ficha en (líneas de prosa, bloques de código).

    Hace falta porque la prosa se junta en una sola línea y el código no se
    puede juntar: aplastarlo era lo que dejaba la consulta SQL de
    ``OFERTAS_CLI_SELECTUNIONART`` en una línea inmensa y sin resaltar.
    """
    prosa: list[str] = []
    bloques: list[list[str]] = []
    actual: list[str] = []
    dentro = False

    for cruda in cuerpo.splitlines():
        linea = cruda.strip()

        if not dentro:
            aplastado = _BLOQUE_APLASTADO_RX.match(linea)
            if aplastado:
                bloques.append([BACKTICKS + aplastado.group('lang'),
                                aplastado.group('codigo'), BACKTICKS])
                continue

        if linea.startswith(BACKTICKS):
            if dentro:
                actual.append(BACKTICKS)
                bloques.append(actual)
                actual, dentro = [], False
            else:
                actual, dentro = [linea], True
            continue

        if dentro:
            actual.append(cruda.rstrip())
        elif linea:
            prosa.append(linea)

    # Un bloque que no cierra no se tira: se devuelve cerrado a mano, que es
    # mejor que perder el código o dejar el resto del artículo dentro de él.
    if actual:
        actual.append(BACKTICKS)
        bloques.append(actual)

    return prosa, bloques


def _fichas_a_lista(md_text: str) -> str:
    """
    Reescribe la ristra de fichas de parámetro como una lista de definición.

    El artículo trae **602 parámetros**, cada uno con su encabezado y tres
    párrafos: 6.000 líneas de pared que hay que recorrer a ojo para comparar
    dos valores.

    Se probó primero con una tabla de cinco columnas y quedó peor: en el ancho
    de contenido de Material el nombre del parámetro se parte letra a letra
    —``ACTIVAR_C`` / ``ALCULO_DE`` / ``SFASE_HOR``— y la columna de la
    descripción se sale de la pantalla. Una lista de definición pone el nombre
    en su propia línea, a ancho completo, y deja toda la anchura para la
    descripción:

        `ACTIVAR_CALCULO_DESFASE_HORAS_CONTRATO`
        :   **BOOL**, por defecto `ON` — ALQUILER (CONTRATOS) - Contratos.
            Parámetro para facturar los posibles desfases.

    La extensión ``def_list`` ya está activada en ``mkdocs.yml``.
    """
    # El artículo abre con un "##### **A continuación, detallamos la utilidad
    # de los parámetros...**", que también es un h5 y se colaba como si fuera
    # un parámetro, con su definición vacía.
    todas = list(_FICHA_PARAMETRO_RX.finditer(md_text))
    fichas = [m for m in todas if _es_nombre_de_parametro(m.group('nombre'))]
    if len(fichas) < _FICHAS_MINIMAS:
        return md_text

    bloques = []
    for m in todas:
        # Lo que no es un parámetro se copia TAL CUAL. Antes se filtraba la
        # lista y se sustituía del primero al último de una tacada, así que
        # las fichas descartadas que caían en medio —27 parámetros con Ñ, con
        # equis minúscula o con &— desaparecían del artículo.
        if m not in fichas:
            bloques.append(md_text[m.start():m.end()].rstrip())
            bloques.append('')
            continue
        modulo = tipo = defecto = ''
        descripcion: list[str] = []
        prosa, codigo = _saca_codigo(m.group('cuerpo'))
        for linea in prosa:
            meta = _FICHA_META_RX.match(linea)
            if not meta:
                descripcion.append(linea)
                continue
            texto = meta.group('txt').strip().strip('*')
            encontrado = _FICHA_TIPO_RX.search(texto)
            if encontrado:
                tipo = encontrado.group('tipo').strip()
                defecto = encontrado.group('def').strip().strip('*')
            elif not modulo:
                modulo = texto

        ficha = []
        if tipo:
            ficha.append(f'**{_limpio(tipo)}**')
        # Un valor por defecto que al deshacer las entidades se queda en nada
        # —``&#x20;`` es un espacio— no se anuncia: dejaba un código vacío.
        if _limpio(defecto):
            ficha.append(f'por defecto `{_limpio(defecto)}`')
        cabeza = ', '.join(ficha)
        if modulo:
            cabeza = f'{cabeza} — {_limpio(modulo)}' if cabeza else _limpio(modulo)

        bloques.append(f'`{_limpio(m.group("nombre"))}`')
        bloques.append(f':   {cabeza}' if cabeza else ':   ')
        if descripcion:
            bloques.append(f'    {_limpio(" ".join(descripcion))}')
        # El código va con su sangría, en su propio bloque: dentro de una
        # lista de definición, cuatro espacios lo mantienen en la definición.
        for bloque in codigo:
            bloques.append('')
            bloques.extend(f'    {linea}' if linea else '' for linea in bloque)
        bloques.append('')

    return md_text[:fichas[0].start()] + '\n'.join(bloques) + '\n' + md_text[fichas[-1].end():]


ARTICLE_FIXES: tuple[ArticleFix, ...] = (
    ArticleFix(
        reason='602 fichas de parámetro seguidas: en lista de definición se leen mejor.',
        article_ids=frozenset({'154000129239'}),
        transform=_fichas_a_lista,
    ),
    ArticleFix(
        reason='Referencia de API cuya firma y ejemplo quedan como texto plano.',
        article_ids=frozenset({'154000130036', '154000130021'}),
        transform=_wrap_api_reference_sections,
    ),
    ArticleFix(
        reason='Código pegado a la prosa y crédito de autor mal colocado.',
        article_ids=frozenset({'154000128795'}),
        substitutions=(
            (r'\n##### Autor: Daniel Ernesto Lutz Llano\n', '\n', re.IGNORECASE),
            (
                r'(-\s*Llamarla desde el ERP de una forma similar a la expuesta:\n+)'
                r'(Set lObj = CreateObject \("[^"]*"\)\n+\s*lObj\.)',
                r'\1\n```vbnet\n\2\n```\n',
                re.IGNORECASE,
            ),
            (
                r'(Para llamarla desde el ERP se realizaría de la siguiente forma:\n)'
                r'(Set lObj = CreateObject \("Prueba_ExternoNet\.Procesos"\)\n'
                r'lObj\.mensaje\s*\nlObj\.crearPedido gcn, "00001", "0", 25)',
                r'\1\n```vbnet\n\2\n```',
                re.IGNORECASE,
            ),
            (r'\n{3,}', '\n\n', 0),
        ),
        literals=(
            (
                'End ClassPara llamarla desde el ERP se realizaría de la siguiente forma:',
                'End Class\n```\n\nPara llamarla desde el ERP se realizaría de la siguiente forma:',
            ),
            (
                'lObj.crearPedido gcn, "00001", "0", 25En este ejemplo se mostraría '
                'un mensaje y se crearía un pedido.',
                'lObj.crearPedido gcn, "00001", "0", 25\n```\n\nEn este ejemplo se '
                'mostraría un mensaje y se crearía un pedido.',
            ),
        ),
        transform=_move_author_credit_to_end,
    ),
)


def apply_article_fixes(article_id: str, article_title: str, md_text: str) -> str:
    """Aplica todos los parches que correspondan a este artículo."""
    if not md_text:
        return md_text

    aid = str(article_id or '').strip()
    title = str(article_title or '').strip()

    for fix in ARTICLE_FIXES:
        if fix.matches(aid, title):
            md_text = fix.apply(md_text)

    return md_text


# ---------------------------------------------------------------------------
# Correcciones de enlaces sobre ficheros ya generados
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LinkFix:
    """Corrección de un enlace concreto dentro de un ``.md`` concreto."""

    reason: str
    #: Ruta del fichero, relativa a ``docs/``.
    path: str
    #: Reemplazos literales tolerantes al encoding de espacios (%20 o espacio).
    replacements: tuple[tuple[str, str], ...] = ()
    #: Reemplazos por expresión regular.
    substitutions: tuple[tuple[str, str, int], ...] = ()


LINK_FIXES: tuple[LinkFix, ...] = (
    LinkFix(
        reason='Enlace a ICONOS truncado y con sufijos ".md)" repetidos.',
        path='Producto - Versiones/Versión 5.0/'
             'Principales Novedades AHORA ERP 5 (HighLights).md',
        replacements=(
            (
                '../../ERP - Configuración ADMON/Admon/Admon - Gestión de ICONOS (v.5',
                '../../ERP - Configuración ADMON/Admon/Admon - Gestión de ICONOS (v.5).md',
            ),
        ),
        substitutions=(
            (
                r'\[aquí\]\(\.\./\.\./ERP - Configuración ADMON/Admon/'
                r'Admon - Gestión de ICONOS \(v\.5\)\.md\)(?:\.md\)\.?)+',
                r'[aquí](../../ERP - Configuración ADMON/Admon/'
                r'Admon - Gestión de ICONOS (v.5).md)',
                0,
            ),
        ),
    ),
    LinkFix(
        reason='Enlace a "Precios de Transporte con intervalos" truncado.',
        path='ERP_ahoraSCO/Ventas_ahoraSCO/ERP. Precios de Transporte.md',
        replacements=(
            (
                'ERP. Precios de Transporte con intervalos de Unidades, Pesos o Bultos (EN PROCESO',
                'ERP. Precios de Transporte con intervalos de Unidades, Pesos o Bultos '
                '(EN PROCESO).md',
            ),
        ),
    ),
    LinkFix(
        reason='Enlace a DevExpress Reports truncado en la extensión ".rpt".',
        path='ERP/Ley Antifraude/'
             'ERP - Añadir componente QR Veri-Factu al listado factura.md',
        replacements=(
            (
                '../Reporting/DevExpress Reports - Conversión de informes desde '
                'Crystal Reports (.rpt',
                '../Reporting/DevExpress Reports - Conversión de informes desde '
                'Crystal Reports (.rpt).md',
            ),
        ),
    ),
    LinkFix(
        reason='URL de la Agencia Tributaria con un "?" y el esquema escapado.',
        path='ERP/Ley Antifraude/'
             'FAQ - Ley Antifraude - ¿Puedo emitir una factura con fecha de '
             'expedición distinta a la actual-.md',
        replacements=(
            ('?https%3A//sede.agenciatributaria.gob.es', 'https://sede.agenciatributaria.gob.es'),
        ),
    ),
)
