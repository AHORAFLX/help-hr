"""
converters.py
=============
Los dos motores de conversión HTML → Markdown del pipeline.

- ``convert_standard``: motor por defecto, basado en html2text. Preserva las
  tablas como HTML crudo y aplica heurísticas para el SQL suelto y las listas
  ordenadas que Freshdesk parte en varios ``<li>``.
- ``convert_author``: motor para artículos con HTML especialmente troceado
  (párrafos de una línea de código cada uno). Basado en markdownify, con un
  saneado previo agresivo.

Requiere Python 3.12 o superior.
"""

from __future__ import annotations

import html as html_lib
import collections
import re
import unicodedata
from pathlib import Path
from typing import Optional

import html2text
from bs4 import BeautifulSoup
from markdownify import markdownify as markdownify_html
from pygments.lexers import guess_lexer

from .article_fixes import UNWRAP_SHORT_FENCE_TITLES, apply_article_fixes
import markdown

from .common import (
    download_images_from_markdown,
    download_images_in_html_fragment,
    codigo_suelto_en_parrafo_a_pre,
    limpiar_atributos_de_freshdesk,
    sentencia_suelta_a_codigo,
    protect_html_tables,
    desenvolver_encabezados_html_sin_texto,
    quitar_anclas_vacias_repetidas,
    quitar_tablas_vacias,
    quitar_colores_ilegibles,
    _FORMATO_ALREDEDOR_DEL_CODIGO_RX,
)

# ---------------------------------------------------------------------------
# Detección de SQL suelto en texto plano
# ---------------------------------------------------------------------------

_SQL_START = re.compile(
    r'^\s*(IF\s+NOT\s+EXISTS|SELECT\s+|UPDATE\s+[\[\w]|INSERT\s+INTO|DELETE\s+FROM'
    r'|DECLARE\s+@|BEGIN\b|CREATE\s+(?:TABLE|PROC|VIEW|FUNCTION)|ALTER\s+(?:TABLE|PROC|VIEW|FUNCTION)'
    r'|USE\s+\[|EXEC\s+\w|SET\s+(?:ANSI|NOCOUNT|@)|\bDim\s+\w+\s+As\b|\bSet\s+\w+\s*='
    # Constante de tabla (CTE). Era el arranque que faltaba: sin él la cabecera
    # del WITH se quedaba fuera del bloque y el código empezaba a media
    # sentencia. Se admite la lista de columnas —";WITH LosEfectos(Id,Otro)"—
    # y el "AS" en la línea siguiente, y también los ** que el autor mete para
    # poner el nombre en negrita. El "AS" o el "(" o el fin de línea son
    # obligatorios: si no, "With mucho gusto le atendemos" pasaría por SQL.
    r'|;?\s*WITH\s+[\w\[*][\w\]*.]*\s*(?:\([^)]*\))?\s*(?:AS\b|$))',
    re.IGNORECASE
)
_SQL_CONTINUE = re.compile(
    r'^\s*(--|@@|@\w+|AND\b|OR\b|WHERE\b|FROM\b|JOIN\b|ON\b|LEFT\b|RIGHT\b|INNER\b'
    r'|GROUP\b|ORDER\b|HAVING\b|VALUES\b|SET\b|END\b|IF\b|ELSE\b|CASE\b|WHEN\b|THEN\b'
    r'|AS\b|GO\b|INSERT\s+INTO\b|UPDATE\b|DELETE\s+FROM\b|SELECT\b'
    r'|\s*\[\w+\]\s*|PRINT\b|EXEC\b|DECLARE\b|\(|\)|\w+\s*=|\'\'|\bWith\b'
    r'|\bEnd\s+With\b|\.\w+)',
    re.IGNORECASE
)


# ---------------------------------------------------------------------------
# Detección de lenguaje para los fences
# ---------------------------------------------------------------------------

#: Hint de lenguaje para Visual Basic. Tiene que ser un alias que Pygments
#: reconozca: "vb" NO lo es, y todo bloque etiquetado así se pintaba en gris,
#: sin resaltar nada. "vbnet" sí, y cubre bien el VB6/VBScript de estos
#: artículos (Dim ... As, Optional, continuaciones con "_").
VB_LANG = 'vbnet'

_LANG_ALIASES = {
    'c#': 'csharp', 'csharp': 'csharp', 'cs': 'csharp',
    'vb.net': VB_LANG, 'vbnet': VB_LANG, 'vb': VB_LANG, 'visualbasic': VB_LANG,
    'vbscript': VB_LANG, 'vba': VB_LANG,
    't-sql': 'sql', 'tsql': 'sql', 'transact-sql': 'sql', 'sql': 'sql',
    'js': 'javascript', 'javascript': 'javascript',
    'json': 'json', 'html': 'html', 'xml': 'xml',
    'powershell': 'powershell', 'pwsh': 'powershell', 'ps1': 'powershell',
    'bash': 'bash', 'sh': 'bash', 'shell': 'bash',
}


def _normalize_detected_lang(lang: str) -> str:
    """Normaliza aliases de detectores externos a nombres útiles para fences."""
    return _LANG_ALIASES.get((lang or '').strip().lower(), '')


def _detect_lang_with_pygments(code: str) -> str:
    """Usa Pygments como último recurso para inferir el lenguaje del bloque."""
    if not code or len(code.strip()) < 12:
        return ''
    try:
        lexer = guess_lexer(code)
    except Exception:  # ClassNotFound y cualquier otro fallo del detector
        return ''

    for alias in (getattr(lexer, 'aliases', None) or []):
        lang = _normalize_detected_lang(alias)
        if lang:
            return lang

    return _normalize_detected_lang(getattr(lexer, 'name', ''))


#: VB inequívoco: palabras clave que no existen en C#.
_STRONG_VB_RX = re.compile(
    r'(?im)^\s*(?:(?:Public|Private|Friend)\s+)?(?:Sub|Function|Property)\s+\w+\s*\(?'
    r'|^\s*End\s+(?:Sub|Function|Property|Class|With|Get|Set|If)\b'
    r'|^\s*Dim\s+\w+|^\s*Set\s+\.?\w+\s*=|^\s*MsgBox\b|^\s*(?:Public|Private)\s+Class\b'
    r'|^\s*\.[A-Za-z_]\w*(?:\s*\([^)\n]*\))?(?:\.\w+(?:\s*\([^)\n]*\))?)*\s*='
    r'|^\s*With\s+\w'
    # La sintaxis de tipos de VB ("As Long", "As String") no existe en C#.
    r'|\bAs\s+(?:Long|String|Boolean|Variant|Double|Integer|Object|Date|Byte'
    r'|Single|Currency|Decimal)\b'
)
#: C# inequívoco. Se comprueba ANTES del VB flojo: un "obj.Prop = true;" de C#
#: encajaba en el patrón laxo de VB y los ejemplos C# salían etiquetados vb.
_STRONG_CSHARP_RX = re.compile(
    r'(?im)^\s*(?:using\s+System|namespace\s+\w+|public\s+(?:void|static|class|string|int|bool)\b'
    r'|private\s+(?:void|static|class|string|int|bool)\b|protected\s+\w+|internal\s+\w+'
    r'|//|/\*)'
)

#: El punto y coma al final y la llave sola en su linea NO son marcadores
#: de C#: los usan igual JavaScript, Java, C y PowerShell. Contarlos con
#: los demas hacia que un script de PowerShell saliera etiquetado csharp.
#: Valen solo como ultimo recurso, cuando nadie tiene marcadores propios.
_PUNTUACION_DE_LLAVES_RX = re.compile(r'(?im);\s*$|^\s*[{}]\s*$')
#: VB flojo: sirve de desempate, no de primera opción. Una asignación sin ";"
#: al final (p. ej. "gForm.grdLineas.ActivarScripts = True") es VB, no C#.
#: La asignación admite llamadas e índices por medio —``gForm.Controls("x").Tab
#: Index = 0`` es lo más común de esta documentación— y el comentario de VB,
#: que empieza por apóstrofo. Sin eso, un bloque entero de VB6 se quedaba sin
#: lenguaje y salía en gris.
_LOOSE_VB_RX = re.compile(
    r"(?im)^\s*(?:"
    r"[A-Za-z_][\w.]*(?:\([^)\n]*\)|\[[^\]\n]*\])?(?:\.[\w.]+(?:\([^)\n]*\))?)*\s*=(?!=)[^;\n]*$"
    r"|Return\b|Get\b|Set\s*\(|If\b.*\bThen\b|'"
    r")"
)


#: SQL inequívoco. Anclado a principio de línea a propósito: así un
#: gCn.DameValorCampo("Select ... From ...") de VB no se etiqueta como sql.
_STRONG_SQL_RX = re.compile(
    r'(?im)^\s*(?:SELECT\s|UPDATE\s+[\[\w]|INSERT\s+INTO|DELETE\s+FROM|DECLARE\s+@'
    r'|CREATE\s+(?:TABLE|PROC|PROCEDURE|VIEW|FUNCTION|INDEX)|ALTER\s+(?:TABLE|PROC|PROCEDURE|VIEW|FUNCTION)'
    r'|EXEC\s+\w|MERGE\s+|BEGIN\s+TRAN|SET\s+@|FROM\s+[\[\w]|WHERE\s+|GROUP\s+BY|ORDER\s+BY'
    r'|DELETE\s+[\[\w]|GRANT\s+\w|DENY\s+\w|REVOKE\s+\w|TRUNCATE\s+TABLE'
    r'|INNER\s+JOIN|LEFT\s+JOIN|IF\s+(?:NOT\s+)?EXISTS\s*[(]|VALUES\s*[(]'
    r'|USE\s+[\[\w]|^GO\s*$|ALTER\s+DATABASE)'
)
#: JavaScript inequívoco. "function" a secas no vale: también es VB.
_STRONG_JS_RX = re.compile(
    r'=>|console\.log|document\.\w|window\.\w|\b(?:var|let|const)\s+\w+\s*='
    r'|\bfunction\s*\w*\s*\([^)]*\)\s*\{',
    re.IGNORECASE,
)
#: PowerShell tiene marcadores propios de sobra —un verbo con guion, una
#: variable con $, un parametro con guion—. Sin contarlos aqui, el bloque
#: caia en 'csharp' porque _STRONG_CSHARP_RX cuenta la llave suelta ``}``
#: como marcador inequivoco, y una llave la usan los dos.
_STRONG_POWERSHELL_RX = re.compile(
    r'(?im)^\s*(?:Get|Set|New|Start|Stop|Write|Test|Invoke|Remove|Add)-\w+'
    r'|^\s*\$\w+\s*=|\s-(?:ErrorAction|Name|Path|Force|Recurse|Filter)\b'
)

_MARKUP_RX = re.compile(
    r'(?im)^\s*<(?:html|head|body|div|span|table|tr|td|th|ul|ol|li|img|script|style|form|input)\b'
)


def detect_code_lang(code: str) -> str:
    """
    Detecta el lenguaje de un bloque de código para el hint de la valla.

    VB, C# y T-SQL comparten demasiada sintaxis para decidir con el primer
    patrón que encaje (así es como los ejemplos de C# acababan etiquetados
    ``vb``): se cuentan los marcadores inequívocos de cada uno y gana el que
    más tenga.
    """
    stripped = (code or '').strip()
    if not stripped:
        return ''

    # El marcado sí es inequívoco: nada más empieza por <html> o <table>.
    if _MARKUP_RX.search(stripped):
        return 'html'

    # Todo lo demás compite por recuento. JavaScript NO puede cortocircuitar:
    # un ``window.o`` suelto dentro de un script de 66 sentencias T-SQL
    # bastaba para publicar el bloque entero como JavaScript.
    scores = {
        VB_LANG: len(_STRONG_VB_RX.findall(stripped)),
        'csharp': len(_STRONG_CSHARP_RX.findall(stripped)),
        'sql': len(_STRONG_SQL_RX.findall(stripped)),
        'javascript': len(_STRONG_JS_RX.findall(stripped)),
        'powershell': len(_STRONG_POWERSHELL_RX.findall(stripped)),
    }
    # El punto y coma final y la llave sola valen MEDIO punto: rompen el
    # empate entre C# y VB —VB no tiene ni una cosa ni la otra— pero no
    # pueden ganar a un marcador de verdad de otro lenguaje.
    # El punto y coma final y la llave sola SI distinguen C# de VB —VB no
    # tiene ninguno de los dos—, asi que cuentan para C#.
    reales_de_csharp = scores['csharp']
    scores['csharp'] += len(_PUNTUACION_DE_LLAVES_RX.findall(stripped))
    best = max(scores, key=lambda k: scores[k])
    # Si C# gana solo por la puntuacion, cualquier otro que use llaves y
    # tenga marcadores PROPIOS le pasa por delante: un script de PowerShell
    # o de T-SQL no es C# por acabar sus lineas en punto y coma.
    if best == 'csharp' and not reales_de_csharp:
        otros = {k: v for k, v in scores.items()
                 if k in ('javascript', 'powershell', 'sql') and v}
        if otros:
            return max(otros, key=lambda k: otros[k])
    if scores[best]:
        # Empate entre VB y C#: se queda en VB, que es el caso mayoritario.
        if scores[VB_LANG] == scores[best]:
            return VB_LANG
        return best


    if _LOOSE_VB_RX.search(stripped):
        return VB_LANG
    if re.search(
        r'\b(using\s+System|public\s+class|private|protected|internal|void|string|int'
        r'|namespace\s+\w+|public\s+static)\b',
        stripped, re.IGNORECASE,
    ):
        return 'csharp'
    if re.search(r'(?m)^\s*<\?xml\b|^\s*<[\w:-]+(?:\s|>)', stripped, re.IGNORECASE):
        return 'xml'
    if re.search(r'(?m)^\s*\{[\s\S]*\}\s*$|^\s*\[[\s\S]*\]\s*$', stripped) and re.search(r'"\s*:\s*', stripped):
        return 'json'
    if re.search(r'(?m)^\s*(Get-|Set-|New-Object|Write-Host|Write-Output|\$[A-Za-z_]\w*\s*=)', stripped):
        return 'powershell'
    if re.search(r'(?m)^\s*(#!/bin/(?:ba)?sh|echo\s+|export\s+\w+=|if\s+\[|fi$)', stripped):
        return 'bash'

    return _detect_lang_with_pygments(stripped)


def _add_missing_lang_hints(md_text: str) -> str:
    """Añade hint de lenguaje a los fences ``` que no lo traen."""
    def repl(m: re.Match) -> str:
        if m.group(1).strip():
            return m.group(0)
        return f'```{detect_code_lang(m.group(2))}\n{m.group(2)}```'

    return re.sub(r'```(\w*)\n(.*?)```', repl, md_text, flags=re.DOTALL)


#: Una línea que por sí sola ya es Markdown —un enlace o imagen suelta, una
#: línea entera en negrita, un encabezado, una viñeta— es prosa, no código.
#: Corta la racha de SQL aunque sea corta y no termine en punto.
#:
#: Sin esto, el enlace al vídeo y el "**Ver código ejemplo**" que separan dos
#: ejemplos se quedaban DENTRO del bloque de código, y el fence acababa
#: cerrándose muchas líneas más abajo.
_MD_PROSE_LINE_RX = re.compile(
    r'^(?:'
    # Uno o varios enlaces solos en la línea. Varios, porque el pie de estos
    # artículos es "[<< Artículo anterior](a.md) [Siguiente >>](b.md)" y con un
    # solo enlace admitido esa línea no cortaba: la navegación acababa dentro
    # del bloque de código.
    r'(?:!?\[[^\]]*\]\([^)]*\)[.,;:]?\s*)+'
    r'|\*\*[^*]+\*\*[.,;:]?'              # una línea entera en negrita
    # Una línea que ABRE en negrita y sigue con texto: "**Ejemplo** de WITH
    # recursivo para...". Es el pie de foto o el rótulo con que el autor
    # separa dos ejemplos, y sin esto la racha de SQL se lo tragaba y seguía
    # hasta el final del artículo, enlaces de navegación incluidos.
    r'|\*\*[^*\n]+\*\*\s+\S.*'
    # El ".*" de estas dos no es adorno: con el "$" del final, "#{1,6}\s"
    # solo casaba un "###" vacío, así que un encabezado CON texto nunca
    # cortaba la racha y acababa dentro del bloque de código.
    r'|#{1,6}\s.*'                         # un encabezado
    r'|[-*+]\s+\S.*'                       # una viñeta
    r')$'
)


def _extract_loose_sql_blocks(md_text: str) -> str:
    """
    Envuelve en fences las rachas de SQL/VB que quedaron como texto plano.

    Solo mira líneas que estén fuera de un fence ya existente.
    """
    lines = md_text.split('\n')
    out: list[str] = []
    block: list[str] = []
    sql_map: dict[str, str] = {}
    counter = 1
    in_sql = False
    in_fence = False

    def flush() -> None:
        nonlocal in_sql, counter
        content = '\n'.join(block).strip()
        if content:
            token = f'%%SQLBLK_{counter}%%'
            sql_map[token] = content
            counter += 1
            out.extend(['', token, ''])
        in_sql = False
        block.clear()

    for line in lines:
        trimmed = line.strip()

        if trimmed.startswith('```'):
            in_fence = not in_fence
            if in_sql and not in_fence:
                flush()
            out.append(line)
            continue

        if in_fence:
            out.append(line)
            continue

        if not in_sql:
            if _SQL_START.match(trimmed):
                in_sql = True
                block.clear()
                block.append(line)
            else:
                out.append(line)
            continue

        if trimmed == '':
            block.append(line)
            continue

        # Un token protegido corta la racha de SQL.
        if trimmed.startswith('%%') and trimmed.endswith('%%'):
            flush()
            out.append(line)
            continue

        # Prosa escrita en Markdown: corta sin más, no hace falta que parezca
        # una frase larga acabada en punto.
        if _MD_PROSE_LINE_RX.match(trimmed) and not _SQL_CONTINUE.match(trimmed):
            flush()
            out.append(line)
            continue

        is_normal_text = (
            bool(re.match(r'^[A-ZÁÉÍÓÚ¿¡][^\n]{15,}?[.!?]$', trimmed))
            and not _SQL_CONTINUE.match(trimmed)
        )
        long_non_sql = (
            len(trimmed) > 80
            and not _SQL_CONTINUE.match(trimmed)
            and not re.search(r'[=><+\-*]', trimmed)
        )
        if is_normal_text or long_non_sql:
            flush()
            out.append(line)
        else:
            block.append(line)

    if in_sql:
        flush()

    md_text = '\n'.join(out)
    for token, content in sql_map.items():
        md_text = md_text.replace(token, f'\n\n```{detect_code_lang(content)}\n{content}\n```\n\n')
    return md_text


#: Separador horizontal tal y como lo escribe html2text para un <hr>: "* * *".
#: Hay que normalizarlo ANTES de tocar el énfasis, o la limpieza de cursivas
#: vacías se come dos de sus tres asteriscos y deja un " *" suelto.
_THEMATIC_BREAK_RX = re.compile(r'(?m)^[ \t]*\*(?:[ \t]*\*){2,}[ \t]*$')

#: Ítem de lista sin contenido: Freshdesk usa <li><br></li> como separador y
#: al convertirlo quedaba una viñeta suelta en mitad de la lista.
_EMPTY_LIST_ITEM_RX = re.compile(r'(?m)^[ \t]*[*+-][ \t]*$\n?')

#: html2text escapa por precaución el guion inicial de línea, y deja cosas
#: como "\--- Los valores disponibles son:" a la vista de quien lee el .md.
#: Solo se quita el escape cuando hay DOS O MÁS guiones seguidos de texto: esa
#: línea no puede ser ni un separador (serían solo guiones) ni un ítem de
#: lista (sería un único guion), así que devolverla a "---" es inocuo.
#: El escape de un guion suelto o el de "8\." sí hacen falta y se respetan.
#:
#: El espacio tras los guiones es opcional: un comentario SQL se escribe pegado
#: —"\--familias hijas"— y también hay que desescaparlo. Pero lo que siga NO
#: puede ser otro guion: en una línea de solo guiones, "-{2,}" se los comería
#: todos menos el último y tomaría ese por el texto, robándole la línea a la
#: regla de separación de más abajo.
_ESCAPED_DASH_RUN_RX = re.compile(r'(?m)^([ \t]*)\\(-{2,}[ \t]*[^\s\-])')

#: Línea que el autor escribió como viñeta ("- _Param_ : algo") y que
#: html2text dejó escapada como "\- ...".
_ESCAPED_DASH_ITEM_RX = re.compile(r'^([ \t]*)\\-([ \t]+\S.*)$')

#: Línea de solo guiones ("\-------------"), usada como separador visual.
_ESCAPED_RULE_RX = re.compile(r'^[ \t]*\\-{2,}[ \t]*$')


def _promote_escaped_dashes(chunk: str) -> str:
    """
    Devuelve su sentido a los guiones que html2text dejó escapados.

    En el HTML original son líneas sueltas separadas por ``<br>``: unas son
    viñetas que el autor escribió a mano (``- _Param_ : algo``) y otras son
    reglas de separación (``-----------``). html2text las escapa a ``\\-`` por
    precaución, y el resultado es una barra invertida a la vista y una lista
    que no se ve como lista.

    En los dos casos hay que abrir una línea en blanco por delante: sin ella
    Python-Markdown deja la lista dentro del párrafo, y una regla pegada a un
    texto convierte ese texto en encabezado (sintaxis setext).
    """
    lines = chunk.split('\n')
    out: list[str] = []
    i = 0

    def abrir_hueco() -> None:
        if out and out[-1].strip():
            out[-1] = out[-1].rstrip()   # fuera el salto de línea duro
            out.append('')

    def cerrar_hueco() -> None:
        if i < len(lines) and lines[i].strip():
            out.append('')

    while i < len(lines):
        if _ESCAPED_RULE_RX.match(lines[i]):
            i += 1
            abrir_hueco()
            out.append('---')
            cerrar_hueco()
            continue

        if not _ESCAPED_DASH_ITEM_RX.match(lines[i]):
            # Un guion escapado a mitad de línea ("\-----> Enumeración") no
            # tiene ningún significado de bloque: la barra solo estorba.
            line = lines[i]
            stripped = line.lstrip()
            if stripped.startswith('\\-'):
                head = line[:len(line) - len(stripped)]
                line = head + stripped[:2] + stripped[2:].replace('\\-', '-')
            else:
                line = line.replace('\\-', '-')
            out.append(line)
            i += 1
            continue

        run: list[str] = []
        while i < len(lines) and (m := _ESCAPED_DASH_ITEM_RX.match(lines[i])):
            run.append(f'{m.group(1)}-{m.group(2)}'.rstrip())
            i += 1

        abrir_hueco()
        out.extend(run)
        cerrar_hueco()

    return '\n'.join(out)

#: Negrita vacía: "****" o "**   **".
#: Negrita vacía. Se admite un salto de línea entre los dos marcadores: el
#: origen los parte con un salto duro ("**  \n**") y, exigiéndolos en la misma
#: línea, quedaban 301 líneas sueltas con un "**" a la vista en la página.
_EMPTY_BOLD_RX = re.compile(r'(\*\*|__)[ \t]*\n?[ \t]*\1')

#: Una línea que es SOLO un marcador de negrita, sin nada más. Es un resto de
#: la conversión: no puede significar nada. Va aparte de la regla de arriba
#: porque su pareja puede estar a una línea en blanco de distancia, y ampliar
#: aquella para cruzar párrafos fusionaba negritas legítimas ("**a**" y
#: "**b**" en párrafos distintos acababan como un solo "**ab**").
_MARCADOR_HUERFANO_RX = re.compile(r'(?m)^[ \t]*(?:\*\*|__)[ \t]*$\n?')
#: Cursiva vacía: "* *". Exige un espacio de verdad entre los dos asteriscos y
#: que no formen parte de un "**". La regla anterior era ``\*\s*\*``, que casa
#: con el "**" de CUALQUIER negrita: borraba el marcado de todos los artículos
#: y el texto en negrita salía plano.
_EMPTY_ITALIC_RX = re.compile(r'(?<!\*)\*[ \t]+\*(?!\*)')


#: Un par de marcadores de énfasis con espacio pegado por dentro. El cuerpo no
#: puede contener el propio marcador ni cruzar un párrafo en blanco.
_ENFASIS_CON_ESPACIO_RX = re.compile(
    r'(?P<marca>\*\*|__)'
    r'(?P<pre>[ \t]+)?'
    r'(?P<cuerpo>(?!\s)(?:(?!(?P=marca))[^\n])*?)'
    r'(?P<post>[ \t]+)?'
    r'(?P=marca)'
)


def _sacar_espacios_del_enfasis(chunk: str) -> str:
    """
    Mueve fuera de los marcadores los espacios que quedaron dentro.

    En Markdown, ``** Ejemplo**`` **no es negrita**: el marcador de apertura
    tiene que ir pegado al texto. Se renderizan los asteriscos tal cual y el
    lector ve ``** Ejemplo**`` en mitad de la página. Salía de HTML como
    ``<b><u>texto</u></b>``, que html2text convierte en ``** _texto_**``.

    Solo se tocan los pares equilibrados: mover el espacio afuera no cambia
    nada de lo que se lee, pero un ``**`` suelto sin pareja es otro problema y
    aquí no se toca, que sería adivinar dónde quería cerrar el autor.
    """
    def mover(m: re.Match) -> str:
        cuerpo = m.group('cuerpo').strip()
        # Un cuerpo que solo son marcadores es un resto de la conversión, no
        # texto: "** __**" no quiere decir nada.
        if not cuerpo.strip('*_ \t'):
            return ''

        marca = m.group('marca')
        # El espacio se saca fuera, pero sin duplicar el que ya hubiera.
        anterior = m.string[m.start() - 1] if m.start() else '\n'
        siguiente = m.string[m.end()] if m.end() < len(m.string) else '\n'
        pre = '' if (not m.group('pre') or anterior.isspace()) else ' '
        post = '' if (not m.group('post') or siguiente.isspace()) else ' '
        return f'{pre}{marca}{cuerpo}{marca}{post}'

    return _ENFASIS_CON_ESPACIO_RX.sub(mover, chunk)


#: Encabezado cuyo texto entero va en negrita, cursiva, o las dos. El origen
#: los escribe así muy a menudo; un encabezado ya destaca por sí solo.
_ENCABEZADO_RX = re.compile(r'(?m)^(#{1,6})[ \t]+(.+?)[ \t]*$')

#: Marcadores de énfasis, de más largo a más corto: ``**`` tiene que probarse
#: antes que ``*``, o se le quita un solo asterisco y queda descuadrado.
_MARCADORES = ('**', '__', '*', '_')


def _pelar_enfasis(texto: str) -> str:
    """
    Quita capa a capa el énfasis que envuelve un texto entero.

    Se hace en bucle porque vienen anidados —``**_Plataforma externa_**``— y
    con marcadores huérfanos pegados detrás. Una sola pasada de regex no
    llegaba: el 40 % de los casos lleva además un ``_`` dentro del texto
    (``Ahora_Impresion``), que hacía fallar cualquier patrón que prohibiera
    el marcador por medio.
    """
    previo = None
    while texto != previo:
        previo = texto
        texto = texto.strip()
        for marca in _MARCADORES:
            # Par equilibrado que abarca todo: se pela.
            if (texto.startswith(marca) and texto.endswith(marca)
                    and len(texto) > 2 * len(marca)
                    and marca not in texto[len(marca):-len(marca)]):
                texto = texto[len(marca):-len(marca)]
                break
            # Marcador sin pareja, al principio o al final. El origen los deja
            # sueltos y se imprimen tal cual: "## **Módulo eFactura:".
            if texto.startswith(marca) and marca not in texto[len(marca):]:
                texto = texto[len(marca):]
                break
            if texto.endswith(marca) and marca not in texto[:-len(marca)]:
                texto = texto[:-len(marca)]
                break
    return texto


def _quitar_enfasis_de_encabezados(md_text: str) -> str:
    """
    Quita la negrita o cursiva que envuelve un encabezado entero.

    ``## **Token (JWT)**`` se renderiza como un ``<h2>`` con un ``<strong>``
    dentro: redundante, porque el encabezado ya destaca. En el ``.md`` además
    se lee mal. Son el 20 % de los encabezados.

    Solo se toca cuando el énfasis abarca **todo** el texto: un encabezado con
    una parte resaltada conserva su marcado.
    """
    def limpiar(m: re.Match) -> str:
        # Se pela otra vez despues de quitar los dos puntos: en
        # ``**Cuentas** :`` el ``:`` de en medio impedía ver el par de
        # negritas, y la negrita se quedaba puesta.
        limpio = _pelar_enfasis(_quitar_dos_puntos_finales(_pelar_enfasis(m.group(2))))
        return f'{m.group(1)} {limpio}' if limpio else m.group(0)

    return _ENCABEZADO_RX.sub(limpiar, md_text)


#: Un encabezado que acaba en ``#`` **pegado a la palabra**: ``C#``, ``F#``.
#:
#: El espacio es lo que distingue este caso del cierre ATX legítimo
#: (``## Título ##``), que sí debe seguir desapareciendo. En el corpus hay 301
#: pegadas y ni un solo cierre, pero el corte se hace igual: es la diferencia
#: entre proteger un nombre de lenguaje y convertir un cierre en basura visible.
_ALMOHADILLA_FINAL_RX = re.compile(r'(?m)^(#{1,6} .*[^\s\\#])(#)[ \t]*$')


def normalizar_encabezados_al_final(md_text: str) -> str:
    """
    Último repaso a los encabezados, cuando ya nadie va a crear más.

    Hace dos cosas, y las dos tienen que ir **aquí**:

    - Quita los dos puntos finales. La limpieza de encabezados ya lo hace,
      pero corre antes que ``_etiquetas_sueltas_a_encabezados`` y
      ``promover_negritas_sueltas``, que crean encabezados nuevos después. Han
      hecho falta tres ejecuciones para aprender que ese arreglo no puede depender
      del orden.
    - Escapa la ``#`` final pegada a la palabra. ``## Código C#`` se renderiza
      como «Código C», porque Markdown la interpreta como el cierre opcional
      del encabezado ATX. Eran 301 encabezados, y lo introdujo esta misma casa
      al quitar los dos puntos, que sin saberlo hacían de escudo.
    """
    md_text = _degradar_encabezados_imposibles(md_text)
    # Después de la degradación: los de navegación se van a párrafo con su
    # enlace entero, y aquí solo quedan los que de verdad son un título.
    md_text = _encabezados_que_son_un_enlace(md_text)
    md_text = _DOS_PUNTOS_EN_ENCABEZADO_RX.sub(r'\1', md_text)
    return _ALMOHADILLA_FINAL_RX.sub(lambda m: f'{m.group(1)}{chr(92)}#', md_text)


#: Un enlace sin texto pegado al que sí lo tiene, ocupando la línea entera.
#:
#: El origen escribe ``<h2><a href="url"></a>Permisos</h2>``: el ancla se
#: quedó sin texto y la etiqueta de verdad quedó fuera, pegada detrás. Si no se
#: junta aquí, la regla que etiqueta enlaces vacíos le mete la URL como texto y
#: el encabezado pasa de 157 a 299 caracteres con la URL a la vista.
#:
#: Se exige que ocupe **toda la línea** —opcionalmente tras las almohadillas de
#: un encabezado— y que la etiqueta sea corta. Si no, en un párrafo se
#: enlazaría la frase entera.
_ENLACE_VACIO_PEGADO_RX = re.compile(
    r'(?m)^(?P<pre>#{1,6} |[ \t]*)\[\](?P<url>\([^)\s]+\))(?P<etq>[^\s\[<*_][^\n\[]{0,79})[ \t]*$'
)


def juntar_enlace_vacio_con_su_texto(md_text: str) -> str:
    """Devuelve al enlace sin texto la etiqueta que se quedó fuera."""
    return _ENLACE_VACIO_PEGADO_RX.sub(
        lambda m: f'{m.group("pre")}[{m.group("etq").strip()}]{m.group("url")}', md_text,
    )


#: Cualquier forma de enlace: Markdown, autolink o URL desnuda.
_CUALQUIER_ENLACE_RX = re.compile(r'!?\[[^\]]*\]\([^)]*\)|<https?://[^>]+>|https?://\S+')

#: Más allá de esto no hay títulos. El más largo legítimo del corpus tiene 117
#: caracteres; por encima de 160 son bloques de prosa que el origen envolvió en
#: un encabezado —hay uno de 1.052—.
_MAX_LARGO_DE_ENCABEZADO = 160

#: Lo que tiene que quedar de texto propio al quitarle los enlaces para que
#: siga siendo un título. Por debajo, el encabezado *es* el enlace.
_MIN_TEXTO_PROPIO = 4

#: La flecha de «anterior / siguiente». Es lo que distingue un enlace de
#: navegación de un título que además enlaza a algún sitio.
#:
#: Sin este corte se degradaban también las secciones de
#: ``Usar el Asistente para planes de mantenimiento``, donde cada título
#: (``Permisos``, ``Requisitos previos``) enlaza a su apartado en la
#: documentación de Microsoft. Esas **sí** son secciones.
_FLECHA_DE_NAVEGACION_RX = re.compile(r'^\s*[<«]|[>»]\s*$')


#: Un encabezado cuyo texto entero es un enlace, con etiqueta de verdad.
_ENCABEZADO_QUE_ES_UN_ENLACE_RX = re.compile(
    r'(?m)^(?P<almohadillas>#{2,6}) \[(?P<texto>[^\]]+)\]\([^)\s]+(?:[ \t]+"[^"]*")?\)[ \t]*$'
)


def _encabezados_que_son_un_enlace(md_text: str) -> str:
    """
    Deja en texto los encabezados cuyo título entero es un enlace.

    Un encabezado es un título, y en toda la documentación se ve como un
    título. Estos catorce se veían en azul y se podían pulsar, porque el
    origen —una copia de una página de Microsoft Learn— traía cada sección
    enlazada a su ancla en el original:

        ## [Limitaciones y restricciones](https://learn.microsoft.com/...#Restrictions)

    No se degradan a párrafo, que es lo que hace ``_degradar_encabezados_
    imposibles`` con los de navegación: aquí el texto **sí** es un título de
    sección y el panel derecho lo necesita. Lo que sobra es el enlace.

    Lo que se pierde son catorce anclas a secciones de una misma página
    externa, cuyo contenido está ya en el propio artículo. Alcance medido:
    14 encabezados en 1 artículo de 1.500.
    """
    return _ENCABEZADO_QUE_ES_UN_ENLACE_RX.sub(
        lambda m: f'{m.group("almohadillas")} {m.group("texto").strip()}', md_text)


def _degradar_encabezados_imposibles(md_text: str) -> str:
    """
    Pasa a párrafo los encabezados que no pueden ser un título.

    Dos casos, los dos medidos:

    - **Es un enlace.** Son los 8 enlaces de navegación del tipo
      ``## [< Codificación: Manipulación de grids en frmPedidos](...)``. Un
      encabezado que es un enlace es un enlace, el mismo criterio que ya usa
      ``promover_negritas_a_encabezados()``.
    - **Es demasiado largo.** 15 encabezados pasan de 160 caracteres, y ahí no
      hay títulos: el origen envolvió bloques de prosa en un ``<h3>``/``<h4>``
      y uno llega a 1.052 caracteres.

    Se hace sobre el Markdown, al final, y eso es deliberado: así vale para
    los **dos** motores. ``convert_author`` no pasa por
    ``preprocess_reference_html``, donde vive la degradación por
    ``_parece_prosa()``, y el encabezado de 1.052 caracteres era justo de un
    artículo de autor.
    """
    def degradar(m: re.Match) -> str:
        texto = m.group(2)
        # El largo se mide sobre lo que SE VE, no sobre la línea: en
        # ``## [Limitaciones y restricciones](https://learn.microsoft.com/...)``
        # el panel lee 28 caracteres y la línea tiene 190. Midiendo la línea se
        # degradaban las secciones de un artículo entero por lo larga que era
        # la URL.
        visible = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', texto)
        propio = re.sub(r'[*_`<>\[\]() \t.,;:#-]', '', _CUALQUIER_ENLACE_RX.sub('', texto))
        es_solo_enlace = (bool(_CUALQUIER_ENLACE_RX.search(texto))
                          and len(propio) <= _MIN_TEXTO_PROPIO)
        etiqueta = re.match(r'\s*!?\[([^\]]*)\]', texto)
        es_navegacion = es_solo_enlace and bool(
            _FLECHA_DE_NAVEGACION_RX.search(etiqueta.group(1)) if etiqueta else False
        )
        # Un enlace SIN etiqueta tampoco es un título: no se ve nada.
        sin_etiqueta = es_solo_enlace and not (etiqueta and etiqueta.group(1).strip())
        if es_navegacion or sin_etiqueta or len(visible) > _MAX_LARGO_DE_ENCABEZADO:
            return texto
        return m.group(0)

    return re.compile(r'(?m)^(#{2,6}) (.+)$').sub(degradar, md_text)


#: Los dos puntos con los que acaba un encabezado. Se exige algo delante, para
#: no dejar un encabezado vacío.
_DOS_PUNTOS_EN_ENCABEZADO_RX = re.compile(r'(?m)^(#{1,6} .*[^\s:;])[ \t]*[:;]+[ \t]*$')


def _quitar_dos_puntos_finales(texto: str) -> str:
    """
    Quita los dos puntos con los que acaban muchos encabezados.

    Un encabezado es un título, no el arranque de una frase, y en el panel
    derecho ``Descripción:`` o ``Modo automático:`` se leen mal. Eran 987, y
    además incoherentes: unos los llevan y otros no. De ellos, 732 son las
    etiquetas de referencia que promueve este mismo pipeline, así que buena
    parte de la incoherencia era propia.

    Solo se quita si detrás queda algo: ``##  :`` se deja como está.
    """
    limpio = texto.rstrip().rstrip(':;').rstrip()
    return limpio if limpio else texto


#: La misma lista cerrada que ``_ETIQUETA_DE_REFERENCIA_RX``, aplicada ya sobre
#: el Markdown. Hace falta porque no todas las etiquetas vienen en un ``<p>``
#: limpio: algunas cuelgan de un ``<div>`` o llevan un ``<br>`` dentro de la
#: negrita, y ahi la regla del HTML no las alcanza.
_ETIQUETA_SUELTA_RX = re.compile(
    r'(?im)(?<=\n)([ \t]*\r?\n)[ \t]*(?:\*\*|__)?[ \t]*'
    r'(C\S*digo(?:\s+en)?\s+[^*_:\n]{1,12}|Implementaci\S*n|Descripci\S*n'
    r'|Ejemplo(?:\s+de\s+uso)?|Par\S*metros|Sintaxis)[ \t]*:?[ \t]*'
    r'(?:\*\*|__)?[ \t]*(?=\r?\n[ \t]*\r?\n|\r?\n[ \t]*$)'
)


#: Una viñeta escrita a mano al principio de la línea.
#:
#: El autor no usó la lista del editor: tecleó el carácter. Llegan 62 líneas
#: así, con ``•`` (39) y ``·`` (23), y también el ``\uf0b7`` que mete Word con
#: la fuente Symbol. Markdown no las reconoce, así que se publican como un
#: párrafo que empieza con un punto gordo en vez de como una lista.
#:
#: Además arregla de paso un daño colateral: ``• **OFERTAS_OCULTA_EMBALAJE**``
#: solo en su párrafo lo veía ``promover_negritas_sueltas`` como una negrita
#: suelta y lo ascendía a ``## • OFERTAS_OCULTA_EMBALAJE``, con la viñeta
#: dentro del encabezado. Convertida antes en item de lista, ya no es
#: candidata a encabezado.
#:
#: Se exige que haya algo detrás: una viñeta sola es un artefacto, no una
#: lista, y de esa ya se encarga ``_EMPTY_LIST_ITEM_RX``.
_VINETA_LITERAL_RX = re.compile(
    r'(?m)^([ \t]*)[\u2022\u00b7\u25aa\u25e6\u2023\u2043\uf0b7][ \t]*(?=\S)'
)


#: La misma viñeta, pero dentro de un encabezado.
#:
#: Cuando el origen ya traía la línea como ``<h5>• OFERTAS_OCULTA_EMBALAJE</h5>``
#: no hay lista que crear —es un encabezado de verdad— pero el símbolo sobra:
#: se publicaba como "## • OFERTAS_OCULTA_EMBALAJE", con la viñeta dentro del
#: título y, de ahí, dentro de la tabla de contenidos.
_VINETA_EN_ENCABEZADO_RX = re.compile(
    r'(?m)^(#{1,6}[ \t]+)[\u2022\u00b7\u25aa\u25e6\u2023\u2043\uf0b7][ \t]*(?=\S)'
)


def vinetas_literales_a_lista(md_text: str) -> str:
    """Convierte en lista las viñetas que el autor escribió a mano."""
    md_text = _VINETA_EN_ENCABEZADO_RX.sub(r'\1', md_text)
    return _VINETA_LITERAL_RX.sub(r'\1- ', md_text)


#: Un elemento de lista sin numerar. El espacio tras el marcador es lo que lo
#: distingue de un ``*énfasis*`` o de un ``---`` separador.
#: Markdown admite de uno a cuatro espacios entre la vineta y el texto.
#: Exigiendo solo uno, una vineta escrita con dos —``-  Incobrable``— no se
#: contaba ni se cambiaba, y dos articulos seguian mezclando marcadores.
_ITEM_DE_LISTA_RX = re.compile(r'(?m)^([ \t]{0,6})([-*+])[ \t]{1,4}(?=\S)')


#: Un parrafo que es un paso numerado a mano. El numero puede venir dentro de
#: la negrita —``**2.** El banco...``, ``**1.IBAN** correctamente...``— o
#: suelto, y el separador puede ser punto, parentesis o guion.
#: El separador puede venir doblado —``**1.-** En la primera opción``—, y si
#: solo se consume uno, el que queda se publica como si fuera el texto del
#: paso: ``1. **-** En la primera opción``.
_PASO_EN_NEGRITA_RX = re.compile(r'^\*\*(\d{1,2})\s*[.)\-]+\s*(.*?)\*\*\s*(.*)$', re.S)
_PASO_SUELTO_RX = re.compile(r'^(\d{1,2})\s*[.)\-]+\s+(\S.*)$', re.S)

#: A partir de tres seguidos ya es una lista. Con dos puede ser casualidad.
_MINIMO_DE_PASOS = 3


def _numero_del_paso(parrafo: str) -> Optional[tuple[int, str]]:
    """Devuelve (numero, texto ya sin el numero) si el parrafo es un paso."""
    if '\n' in parrafo.strip():
        return None                     # de una sola linea: si no, no es un paso
    m = _PASO_EN_NEGRITA_RX.match(parrafo.strip())
    if m:
        dentro, fuera = m.group(2).strip(), m.group(3).strip()
        # La negrita puede envolver solo el numero —"**2.** El banco"— o
        # tambien la primera palabra —"**1.IBAN** correctamente"—, y esa
        # palabra hay que devolverla en negrita.
        texto = f'**{dentro}** {fuera}'.strip() if dentro else fuera
        return int(m.group(1)), texto
    m = _PASO_SUELTO_RX.match(parrafo.strip())
    if m:
        return int(m.group(1)), m.group(2).strip()
    return None


def pasos_numerados_a_lista(md_text: str) -> str:
    """
    Convierte en lista ordenada los pasos que el autor numero a mano.

    En vez de una lista, el origen trae parrafos sueltos que empiezan por un
    numero, casi siempre en negrita::

        **1.IBAN** correctamente informado.

        **2.** El banco debe tener informado **el codigo SWIFT/BIC**.

        **3.** Domiciliacion marcada como **activa**.

    La negrita impide que Markdown los reconozca, asi que se publican como
    parrafos independientes: con el espaciado de parrafo, sin sangria colgante
    y sin que se vea que son los pasos de un mismo procedimiento. Son 172
    parrafos en 41 rachas de 28 articulos.

    Se exige que la racha sea de **tres o mas** y que los numeros vayan de uno
    en uno: dos seguidos pueden ser casualidad, y una numeracion que salta
    seguramente no es una lista. La racha puede empezar donde quiera —hay
    procedimientos partidos por una captura, que siguen en el 12— y
    Python-Markdown respeta ese primer numero.
    """
    trozos = re.split(r'(?s)(```.*?```)', md_text)
    for i, trozo in enumerate(trozos):
        if trozo.startswith('```'):
            continue
        bloques = trozo.split('\n\n')
        pasos = [_numero_del_paso(b) for b in bloques]
        salida = list(bloques)
        j = 0
        while j < len(bloques):
            if pasos[j] is None:
                j += 1
                continue
            k = j
            while (k + 1 < len(bloques) and pasos[k + 1] is not None
                   and pasos[k + 1][0] == pasos[k][0] + 1):
                k += 1
            # Solo las rachas que arrancan en 1: Python-Markdown no emite
            # ``start``, así que una que empieza en el 12 saldría renumerada
            # desde el 1 y diría otra cosa. Esas 7 se quedan como están.
            if k - j + 1 >= _MINIMO_DE_PASOS and pasos[j][0] == 1:
                items = [f'{pasos[x][0]}. {pasos[x][1]}' for x in range(j, k + 1)]
                # Apretada, no suelta: con una línea en blanco entre items,
                # Python-Markdown envuelve cada uno en un ``<p>`` y la lista
                # sale con el mismo aire suelto que tenían los párrafos, que
                # es justo lo que se quería quitar.
                salida[j] = '\n'.join(items)
                for x in range(j + 1, k + 1):
                    salida[x] = None
            j = k + 1
        trozos[i] = '\n\n'.join(b for b in salida if b is not None)
    return ''.join(trozos)


#: Los nombres con los que esta documentacion encabeza su indice.
_TITULOS_DE_INDICE = ('tabla de contenidos', 'indice', 'índice', 'contenido', 'contenidos')
_ENCABEZADO_DE_INDICE_RX = re.compile(
    r'(?im)^#{2,6}\s+\**\s*(?:' + '|'.join(_TITULOS_DE_INDICE) + r')\s*:?\s*\**\s*$')

#: Un punto de lista, con su sangria y su marcador.
_PUNTO_DE_LISTA_RX = re.compile(r'^(\s*)([-*+]|\d+\.)\s+(.*)$')


def _texto_llano(s: str) -> str:
    """El texto de un encabezado sin el marcado que Markdown se come."""
    s = re.sub(r'`([^`]*)`', r'\1', s or '')
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'[*_]{1,3}', '', s)
    s = s.replace('\\', '')
    return re.sub(r'\s+', ' ', s).strip()


def _clave(s: str) -> str:
    """Para comparar un punto del indice con un encabezado."""
    s = unicodedata.normalize('NFKD', _texto_llano(s))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^0-9a-z]+', ' ', s.lower()).strip()


def desangrar_el_indice(md_text: str) -> str:
    """
    Quita la sangria de mas al indice escrito a mano.

    90 articulos traen los puntos de su indice sangrados con cuatro espacios o
    mas. En Markdown eso no es una lista: es un **bloque de codigo**, y se
    publican en gris y monoespaciados, con los asteriscos a la vista::

        * Introduccion
        * Plazo de presentacion
        * Generar la declaracion INTRASTAT en AHORA ERP

    Son 920 puntos. Se le resta a todo el bloque la sangria del punto menos
    sangrado, con lo que el primer nivel queda pegado al margen y los
    subniveles conservan su distancia relativa: la lista sale como lista y con
    su jerarquia intacta.
    """
    if not _ENCABEZADO_DE_INDICE_RX.search(md_text or ''):
        return md_text

    lineas = md_text.split('\n')
    ini = None
    for i, linea in enumerate(lineas):
        if _ENCABEZADO_DE_INDICE_RX.match(linea):
            ini = i + 1
            break
    if ini is None:
        return md_text

    fin = len(lineas)
    for i in range(ini, len(lineas)):
        if re.match(r'^#{1,6}\s', lineas[i]):
            fin = i
            break

    puntos = [i for i in range(ini, fin) if _PUNTO_DE_LISTA_RX.match(lineas[i])]
    if not puntos:
        return md_text

    # Manda la sangría del **primer** punto, no la menor: Markdown lee de
    # arriba abajo, así que si el primero ya entra en el bloque de código, lo
    # que venga después con menos sangría no lo rescata.
    sangria = len(_PUNTO_DE_LISTA_RX.match(lineas[puntos[0]]).group(1))
    if sangria < 4:
        return md_text                  # ya es una lista de verdad

    for i in range(ini, fin):
        sobra = len(lineas[i]) - len(lineas[i].lstrip(' '))
        lineas[i] = lineas[i][min(sangria, sobra):]
    return '\n'.join(lineas)


def _secciones_del_documento(md_text: str) -> dict:
    """
    Las secciones y su ancla, tal y como las va a numerar la pagina.

    No se calculan a mano: se le pide el indice a la propia extension ``toc``
    de Python-Markdown, que es quien pone los ``id``. Aproximar el texto del
    encabezado quitando asteriscos y guiones bajos fallaba con la puntuacion
    rara del origen —``## _Configuracion de_ **_ _ERP_**`` acaba siendo
    ``configuracion-de-_erp``, no ``configuracion-de-erp``— y dejaba 6
    enlaces apuntando a un ancla que no existe.
    """
    md = markdown.Markdown(extensions=['toc'])
    md.convert(md_text)
    secciones: dict = {}

    def recorrer(tokens):
        for t in tokens:
            # El nivel 1 es el título de la página, y un índice enlaza a las
            # secciones, no a la cabecera del propio artículo. Además el
            # conversor no ve ese título —se añade después—, así que sin esta
            # salvedad la regla se comporta distinto según cuándo se aplique.
            if t.get('level') != 1:
                secciones.setdefault(_clave(t.get('name') or ''), t.get('id'))
            recorrer(t.get('children') or [])

    recorrer(getattr(md, 'toc_tokens', []) or [])
    return secciones


def enlazar_indice_a_las_secciones(md_text: str) -> str:
    """
    Convierte en enlaces los puntos del indice que el autor escribio a mano.

    136 articulos abren con un "Indice" o una "Tabla de contenidos" hecha a
    mano, y **ninguno** de los 136 tiene un solo enlace: son listas de texto
    plano que enumeran las secciones y no llevan a ninguna parte. El lector
    las lee, intenta pulsarlas y no pasa nada.

    Se enlaza cada punto que case con una seccion del propio articulo. El
    punto que no case se queda como texto: puede referirse a algo que no es un
    encabezado, y un enlace a ninguna parte es peor que ningun enlace.

    De los 136, en 42 casan todos los puntos y en 91 casan algunos.
    """
    if not _ENCABEZADO_DE_INDICE_RX.search(md_text or ''):
        return md_text

    secciones = _secciones_del_documento(md_text)
    if not secciones:
        return md_text

    lineas = md_text.split('\n')
    dentro = False
    for i, linea in enumerate(lineas):
        if _ENCABEZADO_DE_INDICE_RX.match(linea):
            dentro = True
            continue
        if not dentro:
            continue
        punto = _PUNTO_DE_LISTA_RX.match(linea)
        if not punto:
            # El indice acaba en la primera linea que no es un punto ni esta
            # en blanco. Cortar solo al llegar al siguiente encabezado dejaba
            # la regla suelta por el resto del articulo, y llego a enlazar un
            # ``* ## TBAI`` que estaba veinte parrafos mas abajo.
            if linea.strip():
                break
            continue
        sangria, marca, texto = punto.groups()
        if '](' in texto:
            continue                    # ya es un enlace
        # Un punto que empieza por otro marcador de lista o por almohadillas
        # los traia como adorno: Markdown se los comia al pintarlo, y metidos
        # dentro de un enlace se verian. Es el caso de los encabezados que el
        # autor escribio como ``### - Ampliacion de validaciones AEAT``.
        texto = re.sub(r'^\s*(?:[-*+]\s+|#{1,6}\s+)', '', texto).strip()
        ancla = secciones.get(_clave(texto))
        if not ancla:
            continue
        # Un asterisco suelto —``Veri*Factu``— se lee como apertura de enfasis
        # en cuanto el texto entra en un enlace, y desaparece. Fuera del
        # enlace nadie lo tocaba.
        if texto.count('*') % 2:
            texto = texto.replace('*', chr(92) + '*')
        # El texto del punto se envuelve TAL CUAL. Limpiarlo se llevaba por
        # delante los guiones bajos de nombres como ``Ahora_Impresion``, que
        # no son énfasis sino parte del nombre.
        lineas[i] = f'{sangria}{marca} [{texto}](#{ancla})'

    return '\n'.join(lineas)


def unificar_marcadores_de_lista(md_text: str) -> str:
    """
    Deja un solo marcador de viñeta por documento.

    Mezclar ``*`` y ``-`` no es solo desorden en el ``.md``: **cambia lo que se
    ve**. Al cambiar de marcador, Python-Markdown funde las dos listas en una
    sola *suelta* y envuelve algunos ``<li>`` en ``<p>``, así que unos items
    salen espaciados y otros apretados en la misma lista. Había 10 listas así,
    una de 14 items con 4 espaciados y 10 apretados.

    La mezcla la produce la propia casa: html2text emite ``*`` y
    ``vinetas_literales_a_lista()`` emite ``-``.

    Se unifica al marcador **que ya predomina en ese fichero**, no a uno fijo:
    así solo cambian los documentos que mezclan, en vez de reescribir las 6.895
    viñetas del corpus por una cuestión de estilo.

    Ojo: el marcador dominante se cuenta sobre el documento **entero**, y por
    eso esta función se ocupa ella misma de saltarse los fences en vez de ir
    envuelta en ``_outside_fences``. Envuelta, cada trozo entre bloques de
    código elegía *su* dominante y ocho ficheros seguían mezclando.
    """
    trozos = re.split(r'(?s)(```.*?```)', md_text)
    marcas: collections.Counter = collections.Counter()
    for trozo in trozos:
        if not trozo.startswith('```'):
            marcas.update(m.group(2) for m in _ITEM_DE_LISTA_RX.finditer(trozo))
    if len(marcas) < 2:
        return md_text

    dominante = marcas.most_common(1)[0][0]
    return ''.join(
        trozo if trozo.startswith('```')
        else _ITEM_DE_LISTA_RX.sub(lambda m: f'{m.group(1)}{dominante} ', trozo)
        for trozo in trozos
    )


def _etiquetas_sueltas_a_encabezados(md_text: str) -> str:
    """
    Convierte en ``##`` las etiquetas de seccion que llegaron al Markdown.

    Se exige que la etiqueta este **sola en su parrafo** —linea en blanco
    antes y despues—. Sin eso se partiria un parrafo por la mitad: hay
    articulos donde ``parámetros:`` es la segunda linea de un bloque que
    empieza con el nombre del procedimiento, y ahi la etiqueta no es una
    seccion sino parte de la frase.
    """
    # Sin los dos puntos: un encabezado es un título. Emitirlos aquí dejaba
    # seis "## Parámetros:" a la vista, porque la limpieza de encabezados corre
    # ANTES que esta regla y ya no los veía. Mejor no crear la dependencia.
    return _ETIQUETA_SUELTA_RX.sub(lambda m: f'{m.group(1)}## {m.group(2).strip()}', md_text)


CALLOUT_WORDS = frozenset({
    'nota', 'notas', 'importante', 'recuerda', 'recuerde', 'ejemplo', 'ejemplos',
    'aviso', 'atencion', 'atención', 'ojo', 'consejo', 'truco', 'advertencia',
    'observacion', 'observación', 'observaciones', 'dato', 'datos de interes',
    'datos de interés', 'a tener en cuenta',
    # Estas cuatro salieron al revisar las cajas hechas con reglas ``---``.
    # Ningún encabezado del corpus se llama así, así que añadirlas no cambia
    # nada en ``demote_callout_headings``.
    'tip', 'recomendacion', 'recomendación', 'sugerencia', 'comprobar',
})

#: Tipo de admonition de Material para cada palabra de aviso. La lista de
#: palabras es ``CALLOUT_WORDS``, que ya la usa ``demote_callout_headings``:
#: una sola fuente de verdad, o las dos reglas se pelean por el mismo texto.
#: Lo que no esté aquí cae en ``note``.
_TIPO_DE_AVISO = {
    'importante': 'warning', 'aviso': 'warning', 'advertencia': 'warning',
    'atencion': 'warning', 'atención': 'warning', 'ojo': 'warning',
    'recuerda': 'tip', 'recuerde': 'tip', 'consejo': 'tip', 'truco': 'tip',
    'tip': 'tip', 'sugerencia': 'tip',
    'recomendacion': 'tip', 'recomendación': 'tip', 'comprobar': 'question',
    'ejemplo': 'example', 'ejemplos': 'example',
    'dato': 'info', 'datos de interes': 'info', 'datos de interés': 'info',
    'a tener en cuenta': 'info',
}

#: Un enlace cuyo destino es ``//host`` o ``//host:puerto``, sin ruta. El
#: editor de Freshdesk enlaza así lo que le parece un dominio, y aquí lo que
#: hay es el valor de un parámetro: ``SERVIDOR_CORREO`` =
#: ``smtp.office365.com:587``. Publicado queda un enlace muerto a un servidor
#: de correo.
_ENLACE_A_HOST_RX = re.compile(r'(?<!!)\[([^\]]+)\]\(//[\w.-]+(?::\d+)?/?\)')


def quitar_enlaces_a_un_host(md_text: str) -> str:
    """Deja en texto los enlaces que apuntan a un host, no a una página."""
    return _ENLACE_A_HOST_RX.sub(r'\1', md_text)


#: Una caja de aviso dibujada con dos reglas horizontales, con la palabra y su
#: texto en la MISMA línea: ``---`` / ``**NOTA:** El fichero tiene que...`` /
#: ``---``. Las reglas prueban la intención, así que aquí no hay que adivinar
#: dónde acaba el aviso: acaba en la regla de cierre.
_AVISO_ENTRE_REGLAS_RX = re.compile(
    r'(?m)^---[ \t]*$\n(?:[ \t]*\n)*'
    r'[ \t]*(?:\*\*|__)[ \t]*(' +
    '|'.join(re.escape(w) for w in sorted(CALLOUT_WORDS, key=len, reverse=True)) +
    r')[ \t]*:?[ \t]*(?:\*\*|__)[ \t]*:?[ \t]*'
    r'(?P<cuerpo>.*?)'
    r'\n(?:[ \t]*\n)*^---[ \t]*$',
    re.IGNORECASE | re.DOTALL,
)


def avisos_entre_reglas_a_admonitions(md_text: str) -> str:
    """
    Convierte en admonition las cajas de aviso hechas con reglas ``---``.

    El origen dibuja el recuadro con una regla horizontal arriba y otra
    abajo, y mete la palabra y el texto en la misma línea. Publicado quedan
    dos líneas separadoras y una negrita suelta en medio, que es justo lo que
    una admonition hace bien. Son 65 en el corpus, y las dos reglas dicen sin
    ambigüedad dónde empieza y dónde acaba.
    """
    def convertir(m: re.Match) -> str:
        palabra = m.group(1).strip()
        tipo = _TIPO_DE_AVISO.get(palabra.lower(), 'note')
        cuerpo = '\n'.join(
            '    ' + ln.strip() if ln.strip() else ''
            for ln in m.group('cuerpo').strip().splitlines()
        )
        if not cuerpo.strip():
            return m.group(0)
        return f'!!! {tipo} "{palabra}"\n\n{cuerpo}'

    return _AVISO_ENTRE_REGLAS_RX.sub(convertir, md_text)


#: La palabra de aviso, sola en su párrafo y en negrita.
_AVISO_RX = re.compile(
    r'^[ \t]*(?:\*\*|__)[ \t]*(' +
    '|'.join(re.escape(w) for w in sorted(CALLOUT_WORDS, key=len, reverse=True)) +
    r')[ \t]*:?[ \t]*(?:\*\*|__)[ \t]*$',
    re.IGNORECASE,
)

#: Una viñeta o un número: el comienzo de un elemento de lista.
_VINETA_RX = re.compile(r'[ \t]*(?:[-*+]|\d+[.)])[ \t]+\S')

#: Lo que no puede abrir el cuerpo de un aviso: un encabezado es la sección
#: siguiente, y una tabla en crudo no cabe en la caja —comprobado: indentada
#: dentro de una admonition, Python-Markdown la deja como ``<p><table>``, que
#: es HTML inválido y el navegador saca la tabla del párrafo—.
_NO_ES_CUERPO_RX = re.compile(r'[ \t]*(?:#|<|\||>)')

#: Un bloque de código o una imagen sola: **sí** caben en la caja. Comprobado
#: con la configuración real del tema: el fence indentado sale con su
#: resaltado y la imagen se ve. Son los 6 avisos que quedaban con un
#: ``**Ejemplo**`` suelto y su bloque justo debajo.
_ABRE_UN_BLOQUE_RX = re.compile(r'[ \t]*(?:```|!\[)')

#: Cuántas líneas de párrafo se admiten como cuerpo. Más allá, lo que hay
#: detrás del aviso ya no es el aviso.
_MAX_LINEAS_DE_AVISO = 6


def _cuerpo_del_aviso(lineas: list[str], i: int) -> int:
    """
    Devuelve dónde acaba el cuerpo del aviso que empieza en ``lineas[i]``.

    Son dos formas: una lista —que se toma entera, hasta la primera línea en
    blanco seguida de algo que ya no es lista— o un párrafo corrido. Si lo que
    viene detrás no es ni una cosa ni otra, devuelve ``i`` y no se toca nada.
    """
    if i >= len(lineas):
        return i
    if _VINETA_RX.match(lineas[i]):
        fin = i
        for j in range(i, len(lineas)):
            if lineas[j].strip():
                fin = j + 1
            elif not _hay_mas_lista(lineas, j + 1):
                break
        return fin
    if _ABRE_UN_BLOQUE_RX.match(lineas[i]):
        return _fin_del_bloque(lineas, i)
    if _NO_ES_CUERPO_RX.match(lineas[i]):
        return i
    fin = i
    while fin < len(lineas) and lineas[fin].strip() and fin - i < _MAX_LINEAS_DE_AVISO:
        if _NO_ES_CUERPO_RX.match(lineas[fin]) or _ABRE_UN_BLOQUE_RX.match(lineas[fin]):
            break
        fin += 1
    return fin


def _fin_del_bloque(lineas: list[str], i: int) -> int:
    """
    Dónde acaba el bloque que abre el cuerpo del aviso.

    Una imagen sola ocupa su línea. Un fence llega hasta su cierre; si no
    estuviera cerrado, se deja como está en vez de arrastrar el resto del
    artículo dentro de la caja.
    """
    if lineas[i].lstrip().startswith('!['):
        return i + 1
    for j in range(i + 1, len(lineas)):
        if lineas[j].lstrip().startswith('```'):
            return j + 1
    return i


def _hay_mas_lista(lineas: list[str], j: int) -> bool:
    """Tras una línea en blanco, ¿sigue la misma lista?"""
    while j < len(lineas) and not lineas[j].strip():
        j += 1
    return j < len(lineas) and bool(_VINETA_RX.match(lineas[j]))


#: Un aviso con la palabra y su texto en la MISMA línea, solo en su párrafo:
#: ``**NOTA:** Si la intercalación de la instancia...``.
#:
#: Es la forma en que salen las cajas ``fd-callout`` de Freshdesk una vez
#: dejan de tratarse como código, y también la que escribe el autor a mano.
_AVISO_EN_LINEA_RX = re.compile(
    r'(?im)^[ \t]*(?:\*\*|__)[ \t]*(' +
    '|'.join(re.escape(w) for w in sorted(CALLOUT_WORDS, key=len, reverse=True)) +
    r')[ \t]*:?[ \t]*(?:\*\*|__)[ \t]*:?[ \t]+(?P<resto>\S.*)$'
)


def avisos_en_linea_a_admonitions(md_text: str) -> str:
    """
    Convierte en admonition el aviso que lleva su texto en la misma línea.

    Son **264 párrafos en 166 artículos**: ``nota`` 167, ``importante`` 59,
    ``dato`` 16, ``ejemplo`` 13… Publicados quedaban como una negrita suelta a
    principio de párrafo, indistinguible del texto que la rodea.

    El criterio es el mismo que en las otras dos reglas de avisos: el párrafo
    tiene que **empezar** por la palabra en negrita, y el cuerpo se toma hasta
    la primera línea en blanco. Si detrás viene una lista, un encabezado, una
    tabla o un fence, no se toca —meterlo en la caja obligaría a re-indentarlo
    y es mucho suponer—.
    """
    lineas = md_text.split('\n')
    salida: list[str] = []
    i = 0
    while i < len(lineas):
        m = _AVISO_EN_LINEA_RX.match(lineas[i])
        if not m:
            salida.append(lineas[i])
            i += 1
            continue

        # El cuerpo es el resto de la línea más lo que siga hasta el blanco.
        cuerpo = [m.group('resto').strip()]
        j = i + 1
        while (j < len(lineas) and lineas[j].strip()
               and not _NO_ES_CUERPO_RX.match(lineas[j])
               and j - i < _MAX_LINEAS_DE_AVISO):
            cuerpo.append(lineas[j].strip())
            j += 1

        palabra = m.group(1).strip()
        tipo = _TIPO_DE_AVISO.get(palabra.lower(), 'note')
        salida.append(f'!!! {tipo} "{palabra}"')
        salida.append('')
        salida.extend('    ' + ln for ln in cuerpo)
        i = j
    return '\n'.join(salida)


def avisos_a_admonitions(md_text: str) -> str:
    """
    Convierte ``**NOTA:**`` y compañía en una admonition de Material.

    El origen marca los avisos poniendo la palabra en negrita en su propio
    párrafo. Promoverlos a ``##`` —que es lo que haría la regla de secciones—
    llenaría el panel derecho de entradas "NOTA, NOTA, Aviso" que no sirven
    para navegar. Una admonition dice lo mismo, se ve como caja de color y no
    entra en el índice. El tema ya trae la extensión activada.

    Va **después** de ``demote_callout_headings()``, que es donde nace la
    negrita que se convierte aquí. Puesta antes, cada ejecución promovía y
    degradaba y no llegaba ni una caja a la salida.
    """
    lineas = md_text.split('\n')
    salida: list[str] = []
    i = 0
    while i < len(lineas):
        m = _AVISO_RX.match(lineas[i])
        if not m:
            salida.append(lineas[i])
            i += 1
            continue
        # Saltar las líneas en blanco que separan la palabra de su texto.
        j = i + 1
        while j < len(lineas) and not lineas[j].strip():
            j += 1
        fin = _cuerpo_del_aviso(lineas, j)
        if fin == j:
            salida.append(lineas[i])
            i += 1
            continue
        palabra = m.group(1).strip()
        tipo = _TIPO_DE_AVISO.get(palabra.lower(), 'note')
        salida.append(f'!!! {tipo} "{palabra}"')
        salida.append('')
        salida.extend(
            '    ' + ln.strip() if ln.strip() else ''
            for ln in lineas[j:fin]
        )
        i = fin
    return '\n'.join(salida)


#: Una negrita sola en su párrafo, candidata a sección. Mismo criterio que la
#: regla del lado HTML: hasta 70 caracteres, sin punto final y sin enlace.
_NEGRITA_SUELTA_RX = re.compile(
    r'(?m)(?<=\n)([ \t]*\r?\n)[ \t]*(?:\*\*|__)([^*_\n]{3,70})(?:\*\*|__)[ \t]*'
    r'(?=\r?\n[ \t]*\r?\n)'
)


def promover_negritas_sueltas(md_text: str) -> str:
    """
    Pasa a ``##`` las negritas que quedaron sueltas en el Markdown.

    ``promover_negritas_a_encabezados()`` hace esto mismo sobre el HTML, pero
    solo alcanza las que vienen en un ``<p>`` limpio. Las que cuelgan de un
    ``<div>`` o llevan un ``<br>`` dentro llegaban hasta aquí sin tocar, y con
    ellas 51 artículos se quedaban sin panel derecho.

    Se aplica **después** de los avisos: para entonces los ``**NOTA:**`` ya no
    están, así que no acaban en el índice.
    """
    def convertir(m: re.Match) -> str:
        texto = m.group(2).strip()
        if texto.endswith('.') or '](' in texto or '<a ' in texto:
            return m.group(0)
        if texto.rstrip(':;.').strip().lower() in CALLOUT_WORDS:
            return m.group(0)
        return f'{m.group(1)}## {texto}'

    return _NEGRITA_SUELTA_RX.sub(convertir, md_text)


def _outside_fences(md_text: str, transform) -> str:
    """Aplica ``transform`` solo al texto que está fuera de un bloque ```."""
    parts = re.split(r'(?s)(```.*?```)', md_text)
    return ''.join(p if p.startswith('```') else transform(p) for p in parts)


def _clean_freshdesk_artifacts(md_text: str) -> str:
    """Limpia los artefactos típicos que deja el HTML de Freshdesk."""
    # Imagen rota del tipo [* ](url) → imagen Markdown normal.
    # Ojo: sin espacio tras el paréntesis, o la descarga de imágenes no la ve.
    md_text = re.sub(r'\[\s*\*\s*\]\((https?://[^\s)]+)\)', r'![](\1)', md_text)
    # Imagen envuelta en un enlace a Freshdesk/S3 → quitar el enlace exterior.
    md_text = re.sub(
        r'\[(!\[[^\]]*\]\([^)]+\)(?:\s+"[^"]*")?)\]\((https?://[^\s)]*?(?:amazonaws|freshdesk)[^\s)]*)\)',
        r'\1', md_text
    )

    # Énfasis vacío que deja html2text/markdownify. Nunca dentro de un fence:
    # ahí un asterisco es código, no marcado.
    def drop_empty_emphasis(chunk: str) -> str:
        # El separador va primero: si no, la limpieza de cursivas se come dos
        # de sus tres asteriscos.
        chunk = _THEMATIC_BREAK_RX.sub('---', chunk)
        chunk = _EMPTY_LIST_ITEM_RX.sub('', chunk)
        chunk = _ESCAPED_DASH_RUN_RX.sub(r'\1\2', chunk)
        chunk = _promote_escaped_dashes(chunk)
        chunk = _EMPTY_BOLD_RX.sub('', chunk)
        chunk = _MARCADOR_HUERFANO_RX.sub('', chunk)
        chunk = _EMPTY_ITALIC_RX.sub('', chunk)
        return _sacar_espacios_del_enfasis(chunk)

    md_text = _outside_fences(md_text, drop_empty_emphasis)
    md_text = _outside_fences(md_text, _quitar_enfasis_de_encabezados)
    # Antes de las dos reglas que crean encabezados: una viñeta convertida en
    # item de lista ya no puede acabar ascendida a ``##``.
    md_text = _outside_fences(md_text, vinetas_literales_a_lista)
    md_text = _outside_fences(md_text, _etiquetas_sueltas_a_encabezados)
    md_text = _outside_fences(md_text, quitar_enlaces_a_un_host)
    return re.sub(r'\n{3,}', '\n\n', md_text)


#: Etiquetas HTML reales. Todo lo demás entre < y > dentro de un bloque de
#: código es contenido (p. ej. el marcador <NombreLibreria.NombreClase>) y no
#: se debe borrar.
_HTML_TAG_NAMES = (
    'a|abbr|address|area|article|aside|audio|b|base|bdi|bdo|blockquote|body|br|button'
    '|canvas|caption|cite|code|col|colgroup|data|datalist|dd|del|details|dfn|dialog|div'
    '|dl|dt|em|embed|fieldset|figcaption|figure|footer|form|h1|h2|h3|h4|h5|h6|head'
    '|header|hgroup|hr|html|i|iframe|img|input|ins|kbd|label|legend|li|link|main|map'
    '|mark|menu|meta|meter|nav|noscript|object|ol|optgroup|option|output|p|param'
    '|picture|pre|progress|q|rp|rt|ruby|s|samp|script|section|select|small|source|span'
    '|strong|style|sub|summary|sup|table|tbody|td|template|textarea|tfoot|th|thead'
    '|time|title|tr|track|u|ul|var|video|wbr'
)
_REAL_HTML_TAG_RX = re.compile(rf'(?is)</?(?:{_HTML_TAG_NAMES})\b[^>]*>')

#: Algo entre ángulos que ni es etiqueta HTML ni autolink: un marcador del
#: texto, como ``<identity impersonate>`` o ``<Tipo>``.
_MARCADOR_ENTRE_ANGULOS_RX = re.compile(
    rf'(?is)<(?!/?(?:{_HTML_TAG_NAMES})\b)(?!https?:|mailto:|ftp:)([^<>\n]{{1,80}})>'
)


def escapar_marcadores_entre_angulos(md_text: str) -> str:
    """
    Escapa lo que va entre ángulos y no es ni etiqueta ni enlace.

    En el origen viene como ``&lt;identity impersonate&gt;``; html2text lo
    des-escapa a ``<identity impersonate>`` y el navegador, al no conocer esa
    etiqueta, **no pinta nada**: el lector se queda sin saber qué subclave
    buscar. Escapando el ``<`` vuelve a verse como texto.

    Los autolinks (``<https://…>``) y las etiquetas de verdad quedan fuera.
    """
    return _MARCADOR_ENTRE_ANGULOS_RX.sub(r'&lt;\1&gt;', md_text)

#: Dos fences consecutivos sin nada entre medias: hay que unirlos.
_ADJACENT_FENCES_RX = re.compile(r'```[ \t]*\n[ \t]*```[A-Za-z0-9_-]*[ \t]*\n')


def _collapse_adjacent_fences(md_text: str) -> str:
    """
    Une los bloques de código que quedaron partidos en dos fences seguidos.

    Cerrar y volver a abrir sin contenido entre medias siempre es un artefacto
    de la conversión, nunca una intención del autor.
    """
    previous = None
    while previous != md_text:
        previous = md_text
        md_text = _ADJACENT_FENCES_RX.sub('', md_text)
    return md_text


#: Encabezado sin texto real: <h4><br></h4>, <h3><small></small></h3>, etc.
#: El "relleno" incluye el espacio duro tanto escapado (&nbsp;) como ya
#: convertido a carácter (\xa0): Freshdesk usa las dos formas y con solo la
#: primera seguían saliendo encabezados vacíos.
_HEADING_RX = re.compile(r'(?is)<h([1-6])([^>]*)>(.*?)</h\1>')
_BR_AL_BORDE_RX = re.compile(r'(?is)^(?:\s|&nbsp;|<br\b[^>]*>)+|(?:\s|&nbsp;|<br\b[^>]*>)+$')


def drop_empty_headings(html: str) -> str:
    """
    Normaliza los encabezados: quita los vacíos y los ``<br>`` de los extremos.

    Dos problemas distintos, los dos muy frecuentes en el HTML de Freshdesk:

    - ``<h4><br></h4>`` o ``<h2><font>&nbsp;</font></h2>``, usados como
      separador visual. Quedan como un ``####`` suelto, que MkDocs pinta como
      encabezado vacío y además mete en la tabla de contenidos.
    - ``<h3><br>TEXTO</h3>``: el ``<br>`` inicial empuja el texto a la línea
      siguiente, así que el ``###`` se queda sin nada y el título acaba
      convertido en un párrafo cualquiera. El encabezado se pierde dos veces.

    Se decide por el **texto visible**, no por una lista de etiquetas de
    relleno: enumerarlas siempre deja fuera alguna, y ``<font>`` fue la última.
    """
    def visible(fragmento: str) -> str:
        limpio = html_lib.unescape(re.sub(r'<[^>]+>', '', fragmento))
        return limpio.replace(' ', ' ').strip()

    def normalizar(m: re.Match) -> str:
        nivel, atributos, interior = m.group(1), m.group(2), m.group(3)
        if not visible(interior):
            # Sin texto pero CON imagen no está vacío: hay artículos que meten
            # cada captura en su propio <h2>. Tratarlo como vacío borraba el
            # encabezado con la imagen dentro — 19 capturas en un solo
            # artículo. Se desenvuelve y la imagen se queda.
            if re.search(r'(?i)<img\b', interior):
                return interior
            return ''

        # Se quita el <br> que no tenga texto por delante (o por detras), sin
        # importar cuantas etiquetas lo envuelvan: el caso real venia metido
        # en un <span>, asi que mirar solo el borde literal no bastaba.
        def sin_br_de_borde(br: re.Match) -> str:
            rodeado = visible(interior[:br.start()]) and visible(interior[br.end():])
            return br.group(0) if rodeado else ''

        limpio = re.sub(r'(?is)<br\b[^>]*>', sin_br_de_borde, interior)
        return f'<h{nivel}{atributos}>{limpio}</h{nivel}>'

    return _HEADING_RX.sub(normalizar, html)


#: Un título escrito a mano no pasa de esto. Más largo ya es un párrafo que
#: alguien puso en negrita para darle énfasis.
_LARGO_DE_TITULO = 70

_PARRAFO_RX = re.compile(r'(?is)<p[^>]*>(.*?)</p>')
_NEGRITA_RX = re.compile(r'(?is)<(strong|b)\b[^>]*>.*?</\1>')


def promover_negritas_a_encabezados(html: str) -> str:
    """
    Convierte en ``<h2>`` los párrafos que son solo un título en negrita.

    Muchos artículos escriben las secciones a mano —``<p><strong>1.
    Comprobaciones previas</strong></p>``— en vez de usar un encabezado. El
    resultado se lee igual, pero MkDocs construye el panel derecho con los
    ``##``, así que esos artículos se quedaban sin tabla de contenidos y sin
    forma de navegarlos. Eran 529 artículos.

    El criterio es deliberadamente estrecho, porque aquí se está inventando
    estructura y una falsa alarma acaba en el índice de la página:

    - **todo** el texto visible del párrafo tiene que ir dentro de la negrita;
    - corto, hasta ``_LARGO_DE_TITULO`` caracteres;
    - y sin punto final, que delata una frase.

    Los dos puntos sí valen: "Modo automático:" es un título de sección.
    """
    def convertir(m: re.Match) -> str:
        interior = m.group(1)
        # Un párrafo que es un enlace en negrita es un enlace, no un título.
        # Sin este corte acababan en el índice encabezados de 200 caracteres
        # con la URL entera dentro.
        if re.search(r'(?is)<a\b[^>]*\bhref', interior):
            return m.group(0)

        texto = html_lib.unescape(re.sub(r'<[^>]+>', '', interior)).replace('\xa0', ' ').strip()
        if not texto or len(texto) > _LARGO_DE_TITULO or texto.endswith('.'):
            return m.group(0)

        # Si al quitar las negritas queda texto, es un párrafo con una parte
        # resaltada, no un título.
        fuera = re.sub(r'<[^>]+>', '', _NEGRITA_RX.sub('', interior))
        if html_lib.unescape(fuera).replace('\xa0', ' ').strip():
            return m.group(0)
        if not _NEGRITA_RX.search(interior):
            return m.group(0)

        # La imagen del párrafo no se pierde: el rótulo sube a encabezado y la
        # captura queda debajo, que es donde va.
        #
        # Es la misma trampa que en ``drop_empty_headings()``: una imagen no
        # aporta texto visible, así que ``<p><strong>3. Accedemos a
        # UTILIDADES:</strong><br><img src="..."></p>`` cumplía el criterio de
        # "todo el texto está en la negrita" y se ascendía **descartando la
        # captura**. Eran 5 imágenes en 4 artículos.
        imagenes = re.findall(r'(?is)<img\b[^>]*>', interior)
        if imagenes:
            return f'<h2>{texto}</h2><p>{"".join(imagenes)}</p>'
        return f'<h2>{texto}</h2>'

    return _PARRAFO_RX.sub(convertir, html)


def protect_code_blocks(html: str, counters: dict[str, int]) -> tuple[str, dict[str, tuple[str, bool]]]:
    """
    Sustituye cada ``<pre>``/``<code>`` por un token y devuelve su contenido.

    Se hace ANTES de convertir y antes de des-escapar nada, por dos razones:

    - Dentro de un ``<pre>``, un ``&lt;style&gt;`` es texto del ejemplo, no
      marcado: des-escapar el documento entero primero lo destruía.
    - El conversor deja de ver el código, así que no lo puede trocear ni
      reindentar. html2text, en particular, convertía cada ``<pre>`` en texto
      indentado con 4 espacios y sin lenguaje, y el postproceso lo partía
      después en varios fences dejando fuera las líneas que no parecían código.

    Devuelve (html con tokens, mapa token → (código, es_bloque)).
    """
    code_map: dict[str, tuple[str, bool]] = {}

    html = re.sub(r'(?is)<pre[^>]*>\s*<code[^>]*>', '<pre>', html)
    html = re.sub(r'(?is)</code>\s*</pre>', '</pre>', html)

    # Unir bloques pre/code fragmentados aunque haya relleno por medio.
    join_rx = (r'(?is)</(?:pre|code)>\s*'
               r'(?:<br\b[^>]*>|</?p[^>]*>|</?div[^>]*>|</?span[^>]*>|&nbsp;)*\s*<(?:pre|code)[^>]*>')
    html = re.sub(join_rx, '\n', html)
    html = re.sub(join_rx, '\n', html)

    def extract(m: re.Match) -> str:
        code = m.group(1)
        is_pre = bool(re.match(r'(?is)<pre', m.group(0)[:5]))
        code = re.sub(r'(?is)<br\b[^>]*>', '\n', code)
        code = re.sub(r'(?is)</?(?:p|div)[^>]*>', '\n', code)
        # Solo se borran etiquetas HTML de verdad: un marcador del ejemplo como
        # <NombreLibreria.NombreClase> tiene que sobrevivir.
        code = _REAL_HTML_TAG_RX.sub('', code)
        code = html_lib.unescape(code).replace('\xa0', ' ').replace('\r\n', '\n').strip()
        if not code:
            return ''

        is_block = '\n' in code or is_pre
        token = f'%%{"CBLK" if is_block else "CILN"}_{counters["code"]}%%'
        counters['code'] += 1
        code_map[token] = (code, is_block)
        return f'\n\n{token}\n\n' if is_block else f' {token} '

    html = re.sub(r'(?is)<(?:pre|code)[^>]*>(.*?)</(?:pre|code)>', extract, html)
    return html, code_map


#: "&lt;algo&gt;" cuyo nombre no es una etiqueta HTML real.
_ESCAPED_PSEUDO_TAG_RX = re.compile(r'&lt;\s*(/?)\s*([^&<>\s][^&<>]{0,80}?)\s*&gt;')

#: Etiquetas cuyo contenido **desaparece** si se convierten en marcado real.
#:
#: No es que se pierda la etiqueta: el conversor se lleva por delante todo lo
#: que hay dentro. El caso que lo destapó: un artículo documenta una cabecera
#: CSS escrita como ``&lt;style&gt;.BlockBody{width:380px;}...&lt;/style&gt;``
#: en un párrafo. Al des-escapar quedaba un ``<style>`` de verdad, markdownify
#: lo eliminaba con su contenido, y el lector se quedaba con un "Cabecera:"
#: colgando y sin el CSS.
#:
#: Y restaurarlas sin escapar tampoco vale: un ``<style>`` en el Markdown lo
#: **aplica** el navegador como CSS de la página en vez de mostrarlo. Así que
#: se devuelven escapadas, que es como se ven.
_TAGS_QUE_SE_COMEN_SU_CONTENIDO = (
    'style', 'script', 'title', 'textarea', 'template', 'iframe', 'noscript', 'head',
)
_TAG_QUE_COME_RX = re.compile(
    r'(?i)^(?:' + '|'.join(_TAGS_QUE_SE_COMEN_SU_CONTENIDO) + r')\b'
)


#: El ``<iframe>`` de YouTube tal y como lo deja el editor de Freshdesk.
#:
#: Son los 106 videos del corpus, todos de YouTube y todos con la misma forma:
#: ``<iframe width="640" height="360" src="https://www.youtube.com/embed/ID?
#: &amp;wmode=opaque" frameborder="0" allowfullscreen class="fr-draggable">``.
_VIDEO_DE_YOUTUBE_RX = re.compile(
    r'(?is)<iframe\b[^>]*\bsrc\s*=\s*(["\'])'
    r'(?P<url>[^"\']*youtube(?:-nocookie)?\.com/embed/[^"\']*)'
    r'\1[^>]*>\s*(?:</iframe\s*>)?'
)

#: De la URL del video solo se conservan los parametros que significan algo.
#: El editor arrastra ``wmode=opaque`` y ``feature=youtu.be``, que no pintan
#: nada, y ``&amp;`` sin des-escapar, que rompe el enlace.
_PARAMETROS_DE_VIDEO = ('list', 'start', 't', 'index')


def apartar_videos_de_youtube(html: str, counters: dict) -> tuple[str, dict]:
    """
    Aparta los videos de YouTube antes de convertir, y deja una marca.

    Ni html2text ni markdownify saben que hacer con un ``<iframe>``: lo borran
    con todo lo que lleva dentro. En 57 articulos eso dejaba la pagina sin el
    video **y sin rastro de que existiera** —ni un enlace, ni un hueco—, asi
    que el lector no podia ni echarlo en falta.

    La marca es texto plano y en su propio parrafo: sobrevive a cualquiera de
    los dos motores, y al restaurarla el bloque queda a nivel de documento,
    que es donde Python-Markdown respeta el HTML en crudo.
    """
    videos: dict[str, str] = {}

    def apartar(m: re.Match) -> str:
        url = html_lib.unescape(m.group('url'))
        camino, _, consulta = url.partition('?')
        idv = camino.rsplit('/', 1)[-1]
        if not idv:
            return m.group(0)
        extras = [t for t in consulta.split('&')
                  if t and t.split('=')[0] in _PARAMETROS_DE_VIDEO]
        limpia = 'https://www.youtube.com/embed/' + idv
        if extras:
            limpia += '?' + '&'.join(extras)
        token = f'%%VIDEO_{counters.get("video", 1)}%%'
        counters['video'] = counters.get('video', 1) + 1
        videos[token] = limpia
        return f'<p>{token}</p>'

    return _VIDEO_DE_YOUTUBE_RX.sub(apartar, html or ''), videos


def restaurar_videos_de_youtube(md_text: str, videos: dict) -> str:
    """
    Devuelve cada video como reproductor incrustado y responsive.

    Los estilos van **en linea** a proposito: asi el bloque no depende de que
    nadie anada una hoja de estilos, y una regeneracion que rehaga ``docs/``
    no puede dejarlo sin ellos. El ``padding-bottom: 56.25%`` es la proporcion
    16:9, que es la unica forma de que un iframe se estire con el ancho sin
    dejar franjas negras ni salirse en el movil.

    El envoltorio es un ``<span display:block`` y no un ``<div>``: 3 de los
    videos vienen dentro de una tabla conservada, y ahi el bloque acababa
    metido en un ``<p>`` y en un ``<span>`` ajenos, que es HTML invalido. Un
    span vale en cualquiera de los tres sitios y se comporta igual.
    """
    for token, url in videos.items():
        bloque = (
            '<span style="display: block; position: relative; padding-bottom: 56.25%; '
            'height: 0; overflow: hidden; max-width: 100%; margin: 1.2em 0;">'
            f'<iframe src="{url}" '
            'style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" '
            'title="Vídeo de YouTube" loading="lazy" allowfullscreen '
            'allow="accelerometer; clipboard-write; encrypted-media; gyroscope; '
            'picture-in-picture"></iframe></span>'
        )
        # El ``<p>`` de la marca sobra cuando el video venia dentro de una
        # tabla conservada: ahi el parrafo sigue en el HTML en crudo y quedaba
        # un bloque metido dentro de un ``<p>``.
        md_text = md_text.replace(f'<p>{token}</p>', bloque).replace(token, bloque)
    return md_text


def protect_escaped_pseudo_tags(html: str, counters: dict[str, int]) -> tuple[str, dict[str, str]]:
    """
    Aparta los ``&lt;marcador&gt;`` que NO son etiquetas HTML.

    Los artículos escriben huecos con esa forma —
    ``Set lObj = CreateObject("&lt;NombreLibreria.NombreClase&gt;")`` — y al
    des-escapar el documento se convertían en ``<NombreLibreria.NombreClase>``,
    que el conversor eliminaba como si fuera marcado. El marcador desaparecía y
    el lector se quedaba sin saber qué poner ahí.
    """
    pseudo_map: dict[str, str] = {}

    def repl(m: re.Match) -> str:
        name = m.group(2)
        token = f'%%PSEUDOTAG_{counters["pseudo"]}%%'
        if _TAG_QUE_COME_RX.match(name):
            # Etiqueta real, pero de las que se llevan su contenido. Se aparta
            # igual y se devuelve ESCAPADA: así el lector la ve como texto y el
            # navegador no la ejecuta.
            counters['pseudo'] += 1
            pseudo_map[token] = f'&lt;{m.group(1)}{name}&gt;'
            return token
        if re.match(rf'(?i)^(?:{_HTML_TAG_NAMES})\b', name):
            return m.group(0)          # etiqueta HTML de verdad: no se toca
        counters['pseudo'] += 1
        pseudo_map[token] = f'<{m.group(1)}{name}>'
        return token

    return _ESCAPED_PSEUDO_TAG_RX.sub(repl, html), pseudo_map


def restore_code_blocks(md_text: str, code_map: dict[str, tuple[str, bool]]) -> str:
    """Devuelve el código protegido al Markdown, ya como fence con lenguaje."""
    for token, (content, is_block) in code_map.items():
        if is_block:
            replacement = f'\n\n```{detect_code_lang(content)}\n{content}\n```\n\n'
        else:
            replacement = f'`{content}`'
        md_text = md_text.replace(token, replacement)
    return md_text


def _normalize_markdown_fences(md_text: str) -> str:
    """Deja los fences siempre en su propia línea y sin saltos sobrantes."""
    if not md_text:
        return md_text
    md_text = re.sub(r'([^\n])(```[A-Za-z0-9_-]*)', r'\1\n\2', md_text)
    md_text = re.sub(r'(```[A-Za-z0-9_-]*)[ \t]*\n?', r'\1\n', md_text)
    md_text = re.sub(r'([^\n])\n?```', r'\1\n```', md_text)
    md_text = re.sub(r'(?m)^[ \t]*(```[A-Za-z0-9_-]*)[ \t]*$', r'\1', md_text)
    md_text = re.sub(r'(?m)^[ \t]*```[ \t]*$', '```', md_text)
    md_text = re.sub(r'\n{3,}```', '\n\n```', md_text)
    return re.sub(r'```\n{3,}', '```\n\n', md_text)


# ---------------------------------------------------------------------------
# Motor estándar (html2text)
# ---------------------------------------------------------------------------

def _html_to_text_lines(block: str) -> str:
    """Extrae el texto plano de una serie de ``<p>``, respetando los ``<br>``."""
    lines: list[str] = []
    for part in re.findall(r"(?is)<p[^>]*>(.*?)</p>", block):
        part = re.sub(r"(?is)<br\b[^>]*>", "\n", part)
        part = re.sub(r"<[^>]+>", "", part)
        part = html_lib.unescape(part).replace("\xa0", " ")
        lines.extend(line.strip() for line in part.splitlines() if line.strip())
    return "\n".join(lines).strip()


_VB_LINE_RX = re.compile(
    r"^(Public|Private|Friend)?\s*(Function|Sub|Property)\b|^Dim\b|^Set\b|^If\b|^End\b"
    r"|^\w+\s*=|^\w+\.|^'.*|^MsgBox\b",
    re.IGNORECASE,
)
_VB_SIGNATURE_RX = re.compile(r"^(Public|Private|Friend)?\s*(Function|Sub|Property)\b", re.IGNORECASE)

def _wrap_code_runs(text: str, min_run: int = 2) -> str:
    """
    Envuelve en ``<pre>`` solo las rachas de líneas que parecen código.

    Antes esto era todo-o-nada: si en la sección había tres líneas con pinta de
    código, se metía la sección **entera** en un ``<pre>``, párrafos de prosa
    incluidos, y MkDocs los pintaba dentro de la caja de código.
    """
    out: list[str] = []
    run: list[str] = []
    prose: list[str] = []

    def flush_run() -> None:
        if not run:
            return
        if len(run) >= min_run:
            out.append('<pre>' + '\n'.join(run) + '</pre>')
        else:
            prose.extend(run)
        run.clear()

    def flush_prose() -> None:
        if prose:
            out.append('<p>' + '<br>'.join(prose) + '</p>')
            prose.clear()

    for line in text.splitlines():
        if not line.strip():
            continue
        if _VB_LINE_RX.search(line.strip()):
            flush_prose()
            run.append(line)
        else:
            flush_run()
            prose.append(line)

    flush_run()
    flush_prose()
    return ''.join(out)


#: Si una sección ya trae el código marcado con <pre>/<code>, las heurísticas
#: de "rescatar código escrito como párrafos" no tienen nada que hacer ahí y
#: solo pueden estropearlo. Su único cometido es el código sin marcar.
_ALREADY_MARKED_CODE_RX = re.compile(r'(?is)<(?:pre|code)\b')


#: A partir de aquí un encabezado ya no es un título, es un párrafo.
_LARGO_DE_PROSA = 100
#: Y si además termina en punto, con bastante menos basta.
_LARGO_DE_FRASE = 60


def _parece_prosa(texto: str) -> bool:
    """
    Decide si un encabezado del origen es en realidad una frase.

    Antes bastaba con que terminase en ``.`` **o en ``:``** para degradarlo a
    párrafo. Los dos puntos al final de un título son de lo más normal en
    castellano —"Procedimiento almacenado:", "Crear auto numéricos:"— y esa
    regla se llevaba por delante 205 encabezados de sección perfectamente
    válidos. Sin ellos el artículo se queda sin tabla de contenidos y el panel
    derecho de MkDocs no tiene nada por donde navegar.

    El punto final sí delata una frase, pero solo cuando el texto da para una:
    "F.A.Q." es un título; una línea de noventa caracteres acabada en punto, no.
    """
    texto = (texto or '').strip()
    if len(texto) > _LARGO_DE_PROSA:
        return True
    if texto.endswith('.') and len(texto) > _LARGO_DE_FRASE:
        return True
    # Un título con dos puntos es corto por naturaleza ("Modo automático:").
    # Ochenta caracteres acabados en ":" ya son la entradilla de una lista.
    return texto.endswith(':') and len(texto) > _LARGO_DE_TITULO


#: Un encabezado de autoría no es una sección: no debe marcar el nivel de
#: referencia ni acabar en la tabla de contenidos.
_AUTORIA_RX = re.compile(r'(?i)^\s*autor(?:es)?\s*[:.]')

#: Tope de secciones en el nivel más alto para dar por bueno el desplazamiento.
#: Medido sobre el corpus: 252 artículos tienen entre 1 y 5, el máximo normal
#: es 17, y solo uno se dispara a 604 usando los encabezados como etiquetas.
_MAX_SECCIONES_PARA_SUBIR = 30


def _normalizar_niveles_de_seccion(soup) -> None:
    """
    Renumera los encabezados para que la jerarquía empiece en ``h2`` y no
    tenga huecos.

    El título del artículo ocupa el ``h1``, así que las secciones empiezan en
    ``h2``. El origen usa el nivel que le apetece: unos artículos abren en
    ``<h1>``, otros en ``<h2>``, y unos cuantos **escriben todas sus secciones
    en ``<h4>``**. Como ``mkdocs.yml`` lleva ``toc_depth: 3``, esos últimos no
    aparecían en el panel derecho: el artículo tiene estructura pero no se
    puede navegar.

    Se hace con una pila, en una sola pasada: cada encabezado se cuelga del
    último de nivel superior y se le da el nivel que le toca por su posición.
    Eso arregla las dos cosas a la vez:

    - **El desplazamiento.** El primer encabezado siempre sale ``h2``, venga
      del nivel que venga.
    - **Los huecos.** Un artículo que va del título a un ``<h3>`` —o de un
      ``<h2>`` a un ``<h4>``— salta un nivel que no existe. Eran 131 saltos.
      Antes se desplazaba el conjunto en bloque, que corrige el arranque pero
      deja los huecos de en medio intactos.

    Lo que NO se toca, y son los dos casos que hay que respetar:

    - **Los créditos de autoría.** Son ``h5``/``h6`` a propósito (96 "Autor:
      Daniel…", 55 "Autor: Pablo…"), no marcan nivel ni suben al índice. Al
      quedar fuera de la lista, tampoco descolocan la pila.
    - **Un artículo con cientos de encabezados al mismo nivel** no está
      dividido en secciones: los usa como etiquetas de datos. Subirlos
      llenaría el panel derecho de ruido, así que se deja tal cual.

    La jerarquía relativa se conserva siempre: dos hermanos siguen siendo
    hermanos, y un hijo sigue siendo hijo. Lo único que desaparece son los
    niveles vacíos por el medio.
    """
    secciones = [
        t for t in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if t.get_text(strip=True) and not _AUTORIA_RX.match(t.get_text(strip=True))
    ]
    if not secciones:
        return

    niveles = [int(t.name[1]) for t in secciones]

    # Se mira CUALQUIER nivel por debajo de h2, no solo el más alto del
    # artículo. El caso real son los 604 "Tipo Valor: BOOL Valor por defecto:
    # OFF" de "ERP - Parámetros de la aplicación", y ahí el nivel más alto no
    # es el de las etiquetas: el HTML abre con un <h1>, así que mirando solo
    # el más alto el guardián no saltaba y las 604 etiquetas subían a h3.
    if any(nivel > 2 and niveles.count(nivel) > _MAX_SECCIONES_PARA_SUBIR
           for nivel in set(niveles)):
        return

    # (nivel de origen, nivel que se le ha dado). Se desapila mientras el tope
    # no sea estrictamente más alto que el encabezado que llega: sus hermanos
    # y sus sobrinos ya no pueden ser su padre.
    pila: list[tuple[int, int]] = []
    for t in secciones:
        origen = int(t.name[1])
        while pila and pila[-1][0] >= origen:
            pila.pop()
        salida = min(6, pila[-1][1] + 1) if pila else 2
        pila.append((origen, salida))
        t.name = f'h{salida}'


def preprocess_reference_html(article_title: str, html: str) -> str:
    """
    Prepara el HTML de documentación de API para que las secciones
    Implementación / Descripción / Ejemplo de uso salgan como bloques de código
    cuando realmente lo son.
    """
    if not html:
        return html

    soup = BeautifulSoup(html, 'html.parser')

    # Quitar el título duplicado si el HTML repite el título del artículo.
    first_tag = soup.find(['h1', 'h2', 'p'])
    if first_tag and article_title:
        if article_title.lower().strip() == first_tag.get_text(strip=True).lower():
            first_tag.decompose()

    # Degradar a párrafo los encabezados que en realidad son prosa. Se miran
    # TODOS los niveles, no solo los tres primeros: el origen envuelve bloques
    # enteros en un ``<h4>`` —hasta 410 caracteres— y ``_normalizar_niveles_de
    # _seccion`` los sube después a ``h2``, con lo que la prosa acababa en el
    # panel derecho. Eran 36 entradas, una de 1.052 caracteres.
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if _parece_prosa(tag.get_text(strip=True)):
            tag.name = 'p'

    _normalizar_niveles_de_seccion(soup)

    html = str(soup)

    def wrap_implementation(m: re.Match) -> str:
        heading, body, tail = m.groups()
        if _ALREADY_MARKED_CODE_RX.search(body):
            return f"{heading}{body}{tail}"
        cleaned = _html_to_text_lines(body)
        meaningful = [ln for ln in cleaned.splitlines() if ln.strip()]
        if cleaned and any(_VB_LINE_RX.search(ln) for ln in meaningful):
            return f"{heading}{_wrap_code_runs(cleaned, min_run=1)}{tail}"
        return f"{heading}{body}{tail}"

    def wrap_description_signatures(m: re.Match) -> str:
        heading, body, tail = m.groups()
        if _ALREADY_MARKED_CODE_RX.search(body):
            return f"{heading}{body}{tail}"

        # Se recorre el cuerpo preservando TODO lo que hay entre párrafos.
        # Antes se reconstruía solo con los <p> y <table> encontrados, así que
        # cualquier <pre> o <div> del cuerpo desaparecía: en los artículos de
        # referencia eso borraba el ejemplo de C# entero.
        pieces: list[str] = []
        code_parts: list[str] = []
        code_started = False
        last_end = 0

        def flush_code() -> None:
            nonlocal code_started
            if code_parts:
                pieces.append('<pre>' + '\n'.join(code_parts) + '</pre>')
                code_parts.clear()
            code_started = False

        for node_m in re.finditer(r"(?is)<table\b[^>]*>.*?</table>|<p[^>]*>.*?</p>", body):
            gap = body[last_end:node_m.start()]
            last_end = node_m.end()
            node = node_m.group(0)

            if gap.strip():
                flush_code()
                pieces.append(gap)

            if re.match(r"(?is)^<table\b", node):
                flush_code()
                pieces.append(node)
                continue

            plain = html_lib.unescape(re.sub(r"<[^>]+>", "", node)).replace("\xa0", " ").strip()
            if not plain:
                pieces.append(node)
                continue

            if code_started or _VB_SIGNATURE_RX.match(plain):
                code_started = True
                code_parts.append(plain)
            else:
                flush_code()
                pieces.append(f'<p>{plain}</p>')

        flush_code()
        pieces.append(body[last_end:])
        return f"{heading}{''.join(pieces)}{tail}"

    def wrap_example(m: re.Match) -> str:
        heading, body = m.groups()
        if _ALREADY_MARKED_CODE_RX.search(body):
            return f"{heading}{body}"
        cleaned = _html_to_text_lines(body)
        meaningful = [ln for ln in cleaned.splitlines() if ln.strip()]
        code_hits = sum(1 for ln in meaningful if _VB_LINE_RX.search(ln))
        if cleaned and code_hits >= 2:
            return f"{heading}{_wrap_code_runs(cleaned)}"
        return f"{heading}{body}"

    html = re.sub(
        r"(?is)(<p[^>]*>\s*Implementaci\S*n:\s*</p>)(.*?)(<p[^>]*>\s*Descripci\S*n:\s*</p>)",
        wrap_implementation, html, count=1,
    )
    html = re.sub(
        r"(?is)(<p[^>]*>\s*Descripci\S*n:\s*</p>)(.*?)(<p[^>]*>\s*Ejemplo de uso[^<]*</p>|$)",
        wrap_description_signatures, html, count=1,
    )
    html = re.sub(
        r"(?is)(<p[^>]*>\s*Ejemplo de uso[^<]*</p>)(.*)$",
        wrap_example, html, count=1,
    )

    # Al final del todo: las heurísticas de arriba localizan estas secciones
    # buscándolas como <p>, así que convertirlas antes las dejaría ciegas.
    html = _cajas_de_aviso_de_freshdesk(html)
    html = _encabezados_de_word(html)
    html = _parrafos_con_br_a_lista(html)
    html = _tablas_de_una_celda_con_codigo(html)
    return _etiquetas_de_referencia_a_encabezados(html)


_TABLA_RX = re.compile(r'(?is)<table\b.*?</table>')


def _tablas_de_una_celda_con_codigo(html: str) -> str:
    """
    Convierte en ``<pre>`` la tabla de una celda que solo contiene código.

    El origen usa una tabla de una sola celda como recuadro, y a veces lo que
    mete dentro es una consulta o un ``Sub`` con las palabras clave coloreadas
    a mano::

        <table><tr><td><br><span style="color: rgb(44,130,201)">EXEC </span>
        VACIA..Ztest_comprobaciones_postactualizacion @ddbb_cliente<br></td></tr>

    Publicado sale como una tabla con borde, sin monoespaciado ni resaltado, y
    con el color pintado a mano en vez del del tema. Emitiendo un ``<pre>``,
    ``protect_code_blocks()`` lo recoge después y le pone su lenguaje.

    Son 11 tablas en 9 artículos. El criterio es que ``detect_code_lang()``
    reconozca el contenido, el mismo que decide el lenguaje de los demás
    bloques: si no lo reconoce, la tabla se queda como está.
    """
    def convertir(m: re.Match) -> str:
        sopa = BeautifulSoup(m.group(0), 'html.parser')
        celdas = sopa.find_all(['td', 'th'])
        if len(celdas) != 1:
            return m.group(0)
        # Los <br> y los <p> marcan los saltos: sin esto las líneas se pegan
        # unas a otras y el código se vuelve ilegible.
        interior = re.sub(r'(?i)<br\b[^>]*>|</p\s*>|</div\s*>', '\n', celdas[0].decode_contents())
        texto = html_lib.unescape(re.sub(r'<[^>]+>', '', interior)).replace('\xa0', ' ')
        texto = '\n'.join(ln.rstrip() for ln in texto.splitlines()).strip('\n')
        if not texto.strip() or not detect_code_lang(texto):
            return m.group(0)
        # ``quote=False``: dentro de un ``<pre>`` las comillas van literales.
        # Con el escapado por defecto, un ``'`` de una consulta acababa como
        # ``&#x27;`` en el bloque de código, a la vista del lector.
        return f'<pre><code>{html_lib.escape(texto, quote=False)}</code></pre>'

    return _TABLA_RX.sub(convertir, html)


#: La caja de aviso de Freshdesk. Su editor la implementa como un ``<pre>``
#: con la clase ``fd-callout``, y eso la hacía pasar por código.
_CAJA_DE_AVISO_RX = re.compile(
    r'(?is)<pre[^>]*\bclass="[^"]*fd-callout[^"]*"[^>]*>(.*?)</pre>'
)


def _cajas_de_aviso_de_freshdesk(html: str) -> str:
    """
    Saca de ``<pre>`` las cajas de aviso, que no son código.

    Freshdesk dibuja sus avisos con ``<pre class="fd-callout fd-callout--note">``
    —hay 131 en 58 artículos, en tres sabores: ``note`` (81), ``idea`` (43) e
    ``info`` (7)—. Al ser un ``<pre>``, ``protect_code_blocks()`` las apartaba
    como si fueran código, y eso hacía dos daños:

    - **Borraba las imágenes de dentro.** Al aislar el código se le quitan las
      etiquetas HTML reales, así que un ``<img>`` del aviso desaparecía. Eran 3
      capturas, y una captura que falta se nota.
    - Publicaba el texto del aviso como un bloque de código: monoespaciado, en
      gris y sin ajuste de línea. De algunos ya se encargaba después
      ``desenvolver_fences_de_prosa()``, pero curándolo, no evitándolo.

    Convertirlas en ``<div>`` basta: el contenido pasa a convertirse como lo
    que es —prosa con sus imágenes y su marcado— y deja de ser código.
    """
    return _CAJA_DE_AVISO_RX.sub(lambda m: f'<div>{m.group(1)}</div>', html)


_PARRAFO_RX = re.compile(r'(?is)<p\b[^>]*>(.*?)</p>')
_BR_RX = re.compile(r'(?i)<br\b[^>]*>')
#: Un trozo que empieza por negrita, saltándose los envoltorios de estilo.
_EMPIEZA_EN_NEGRITA_RX = re.compile(r'(?is)^\s*(?:<(?:span|em|u|font|a)[^>]*>\s*)*<(?:strong|b)\b')

#: La misma etiqueta, pero sin negrita: ``Agregar (Boolean): Indica si...``.
#: Hay copias del mismo artículo donde el origen perdió los ``<strong>``, y sin
#: esto la lista se reconocía en una y no en la otra.
_ETIQUETA_EN_TEXTO_RX = re.compile(
    r'^[A-Za-z_][\w.]{0,38}(?:\s*\([^)\n]{0,30}\))?\s*:\s+\S'
)


def _trozo_va_etiquetado(trozo: str) -> bool:
    """¿Este trozo empieza por una etiqueta, en negrita o en texto plano?"""
    if _EMPIEZA_EN_NEGRITA_RX.match(trozo):
        return True
    plano = ' '.join(re.sub(r'(?is)<[^>]+>', '', trozo).replace('\xa0', ' ').split())
    return bool(_ETIQUETA_EN_TEXTO_RX.match(plano))

#: Cuántos trozos hacen falta para considerarlo una lista, y qué proporción
#: tiene que ir etiquetada. Con menos de tres no hay patrón que reconocer.
_MIN_TROZOS_DE_LISTA = 3
_MIN_FRACCION_ETIQUETADA = 0.8


def _parrafos_con_br_a_lista(html: str) -> str:
    """
    Convierte en ``<ul>`` los párrafos que en realidad son una lista.

    El origen tiene fichas de referencia donde el autor pulsó Shift+Enter en
    vez de Enter, así que las 24 propiedades de ``Grid - Acceder a
    propiedades de la grid`` son **un solo** ``<p>`` con 24 ``<br>`` dentro.
    Publicado sale un muro de texto.

    La señal de que era una lista es que **todos** los trozos separados por
    ``<br>`` empiezan por una negrita: eso solo pasa cuando se están
    enumerando elementos etiquetados. Hay 346 párrafos con tres o más trozos
    y solo 6 cumplen esto; los otros 340 son prosa con saltos duros
    intencionados —``En los artículos …`` / ``… informará una Naturaleza``—
    y convertirlos en lista los estropearía.
    """
    def convertir(m: re.Match) -> str:
        trozos = [
            t for t in _BR_RX.split(m.group(1))
            if re.sub(r'(?is)<[^>]+>|&nbsp;|\s', '', t)
        ]
        if len(trozos) < _MIN_TROZOS_DE_LISTA:
            return m.group(0)
        etiquetados = sum(1 for t in trozos if _trozo_va_etiquetado(t))
        if etiquetados / len(trozos) < _MIN_FRACCION_ETIQUETADA:
            return m.group(0)
        items = ''.join(f'<li>{t.strip()}</li>' for t in trozos)
        return f'<ul>{items}</ul>'

    return _PARRAFO_RX.sub(convertir, html)


#: Un párrafo cuyo único contenido es un marcador ``_Toc`` de Word.
#:
#: Word nombra así los destinos de **su propio índice**: si un texto lleva un
#: ``<a name="_TocNNNNNN">``, en el documento original era un encabezado. Al
#: pegarlo en Freshdesk se pierde el ``<h2>`` y queda un ``<p>`` con el color
#: del estilo, así que el artículo llega aquí sin una sola sección.
#: El contenido del ancla NO puede cruzar un ``</a>`` ni un ``<p>``. Con un
#: ``(.*?)`` a secas el motor retrocedía hasta un ancla posterior y se tragaba
#: el párrafo entero: en ``ERP - Ventas - Oferta`` el marcador envuelve solo la
#: letra «L» —el primer carácter— y salía un encabezado de 160 caracteres con
#: la frase completa dentro.
_ENCABEZADO_DE_WORD_RX = re.compile(
    r'(?is)<p[^>]*>\s*(?:<(?:span|strong|b|em|u|font)[^>]*>\s*)*'
    r'<a\s+name="_Toc\d+"[^>]*>((?:(?!</a>|</?p\b).)*)</a>'
    r'\s*(?:</(?:span|strong|b|em|u|font)>\s*)*(?:<br[^>]*>\s*)*</p>'
)

#: Un encabezado de Word más largo que esto no es un encabezado: es un párrafo
#: cuyo primer carácter llevaba el marcador. Red de seguridad por si el patrón
#: vuelve a abarcar más de la cuenta.
_MAX_LARGO_ENCABEZADO_WORD = 90


def _encabezados_de_word(html: str) -> str:
    """
    Recupera como ``<h2>`` los encabezados que Word marcó con ``_Toc``.

    Es la señal más fiable de todo el corpus: no hay que deducir nada del
    texto —longitud, puntuación, mayúsculas—, porque el propio Word dice que
    eso era un encabezado. Son 77 en 14 artículos, y sin ellos artículos como
    ``ERP - Compras - Ofertas`` se publicaban con el panel derecho vacío
    aunque tuvieran sus cuatro secciones a la vista.

    Las entradas del índice llevan ``<a href="#_Toc...">``, no ``name=``, así
    que no se tocan.
    """
    def convertir(m: re.Match) -> str:
        # Hay que des-escapar antes de mirar si queda algo: dos de los
        # marcadores envuelven un ``&nbsp;`` y solo, y salía un encabezado
        # cuyo texto era literalmente "&nbsp;".
        texto = html_lib.unescape(re.sub(r'<[^>]+>', '', m.group(1)))
        texto = ' '.join(texto.replace('\xa0', ' ').split())
        if not texto or len(texto) > _MAX_LARGO_ENCABEZADO_WORD:
            return m.group(0)
        return f'<h2>{html_lib.escape(texto, quote=False)}</h2>'

    return _ENCABEZADO_DE_WORD_RX.sub(convertir, html)


#: Las secciones fijas de los artículos de referencia de API. El origen las
#: escribe como párrafo suelto, no como encabezado.
_ETIQUETA_DE_REFERENCIA_RX = re.compile(
    r'(?is)<p[^>]*>\s*(?:<(?:strong|b|span|u|em)[^>]*>\s*)*'
    r'(C\S*digo(?:\s+en)?\s+[^<>:\n]{1,12}|Implementaci\S*n|Descripci\S*n'
    r'|Ejemplo(?:\s+de\s+uso)?|Par\S*metros|Sintaxis)\s*:\s*'
    r'(?:</(?:strong|b|span|u|em)>\s*)*</p>'
)


def _etiquetas_de_referencia_a_encabezados(html: str) -> str:
    """
    Convierte en ``<h2>`` las etiquetas de sección de los artículos de API.

    ``Implementación:``, ``Descripción:``, ``Ejemplo de uso:`` y
    ``Parámetros:`` son la estructura de esa familia de artículos, pero el
    origen las escribe como párrafo suelto. Quedaba una incoherencia visible:
    en el mismo artículo, ``Código VB6:`` salía como encabezado —porque va en
    negrita— y ``Descripción:`` como texto corrido.

    Son 38 artículos, y **30 de ellos no tenían ninguna sección** en el panel
    derecho.
    """
    return _ETIQUETA_DE_REFERENCIA_RX.sub(lambda m: f'<h2>{m.group(1)}</h2>', html)


#: Caracteres que en un bloque delatan codigo. La prosa de esta documentacion
#: no los usa; una firma, una consulta o una asignacion, si.
_SENAL_DE_CODIGO_RX = re.compile(r'[{}<>=;\|]|\(\s*\)|\[\w*\]|::|\bAs\s+\w+\b')


def _fence_es_prosa(cuerpo: str) -> bool:
    """
    Decide si un bloque sin lenguaje es en realidad un parrafo de texto.

    El origen usa ``<pre>`` como caja de aviso: los "NOTA:" y los parrafos
    explicativos largos acaban en un fence. En Material un fence **no hace
    wrap**, asi que salen en gris y con barra de scroll horizontal.

    El criterio es deliberadamente estrecho, porque desenvolver codigo por
    error seria peor que dejar un aviso en gris: nada que huela a sintaxis,
    doce palabras como minimo, y mayoria de palabras en minuscula —lo que
    descarta un ``GRANT IMPERSONATE ANY LOGIN TO AhoraServicio``, que son
    seis palabras y casi todas en mayusculas—.
    """
    if _SENAL_DE_CODIGO_RX.search(cuerpo):
        return False
    if detect_code_lang(cuerpo):
        return False
    palabras = cuerpo.split()
    if len(palabras) < 12:
        return False
    minusculas = sum(1 for w in palabras if w[:1].islower())
    if minusculas / len(palabras) < 0.6:
        return False
    # Una linea indentada es codigo formateado, no un parrafo.
    return not any(ln[:1] in (' ', '\t') for ln in cuerpo.splitlines() if ln.strip())


#: Cualquier fence, con lenguaje o sin él. Hay párrafos que además salieron
#: etiquetados como VB, y pintar prosa española con resaltado de sintaxis es
#: peor todavía que dejarla en gris.
_CUALQUIER_FENCE_RX = re.compile(r'(?ms)^```\w*[ \t]*\r?\n(.*?)^```[ \t]*$')


def desenvolver_fences_de_prosa(md_text: str) -> str:
    """Saca del fence los bloques que resultan ser un parrafo de texto."""
    def quizas(m: re.Match) -> str:
        cuerpo = m.group(1)
        if not _fence_es_prosa(cuerpo):
            return m.group(0)
        # Las lineas del parrafo se unen: venian partidas por el ancho del
        # <pre>, no por voluntad del autor.
        return ' '.join(ln.strip() for ln in cuerpo.splitlines() if ln.strip())

    return _CUALQUIER_FENCE_RX.sub(quizas, md_text)


def repair_vb_reference_markdown(md_text: str, unwrap_short_fences: bool = False) -> str:
    """
    Reetiqueta como ``vb`` los fences que lo parecen y reagrupa las firmas o
    ejemplos VB que hayan quedado como texto plano.
    """
    if not md_text:
        return md_text

    def retag(match: re.Match) -> str:
        lang, body = match.group(1), match.group(2)
        # Solo se etiqueta lo que viene SIN lenguaje. Antes esto pisaba un
        # 'csharp' ya detectado y lo dejaba en 'vb'.
        if not lang.strip():
            lang = detect_code_lang(body) or lang
        return f"```{lang}\n{body}\n```"

    md_text = re.sub(r"```(\w*)\n(.*?)\n```", retag, md_text, flags=re.DOTALL)

    if unwrap_short_fences:
        def unwrap(match: re.Match) -> str:
            body = match.group(1)
            meaningful = [ln for ln in body.splitlines() if ln.strip()]
            return body.strip("\n") if len(meaningful) <= 12 else match.group(0)
        md_text = re.sub(rf"```{VB_LANG}\n(.*?)\n```", unwrap, md_text, flags=re.DOTALL | re.IGNORECASE)

    code_patterns = [
        r"^(Public|Private|Friend)?\s*(Function|Sub|Property)\b",
        r"^End\s+(Function|Sub|Property|If|With|Select)\b",
        r"^(Optional\s+)?[A-Za-z_]\w*\s+As\s+[A-Za-z_]",
        r"^As\s+[A-Za-z_]", r"^Dim\s+\w+", r"^Set\s+\w+\s*=",
        r"^(If|ElseIf|Else|While|Wend|Do|Loop|For|Next)\b",
        r"^Exit\s+(Sub|Function|Do|For)\b", r"^MsgBox\b",
        # Acceso a miembro (gForm.Controls). Se exige un identificador después
        # del punto: sin eso, un apartado como "B.- Pago parcial del efecto"
        # pasaba por código y el título acababa dentro de un bloque ```vbnet.
        # Tras el punto tiene que venir una LETRA: "_Fig.8 Insertar un
        # articulo" es el pie de una figura, no un acceso a miembro, y acababa
        # metido en un bloque ```vbnet.
        r"^[A-Za-z_]\w*\s*=", r"^[A-Za-z_]\w*\.[A-Za-z_]", r'^".*', r"^'.*",
    ]

    #: Un enlace Markdown dentro de un bloque de codigo no se puede pulsar:
    #: se publica como texto literal. Y el codigo reconstruido aqui no lleva
    #: enlaces nunca, asi que su presencia delata que esto es prosa. El caso
    #: real son las equivalencias de "Reglas de No Sujecion en SII,
    #: VeriFactu y TicketBAI", envueltas porque sus lineas empiezan por
    #: comillas, con el enlace a la Agencia Tributaria muerto dentro.
    _ENLACE_MARKDOWN_RX = re.compile(r'\[[^\]]{2,}\]\((?:https?://|\.{1,2}/)[^)\s]+\)')

    def is_code_like(line: str) -> bool:
        stripped = line.strip()
        return bool(stripped) and any(re.search(p, stripped, re.IGNORECASE) for p in code_patterns)

    out: list[str] = []
    run: list[str] = []
    in_fence = False

    def flush_run() -> None:
        if not run:
            return
        trimmed = [ln.strip() for ln in run if ln.strip()]
        code_hits = sum(1 for ln in trimmed if is_code_like(ln))
        strong_start = bool(trimmed) and is_code_like(trimmed[0])
        lleva_enlace = any(_ENLACE_MARKDOWN_RX.search(ln) for ln in trimmed)
        if (trimmed and not lleva_enlace
                and (strong_start or code_hits >= max(2, (len(trimmed) + 1) // 2))):
            # Se pregunta el lenguaje en vez de dar VB por hecho: un bloque
            # reconstruido aqui ya llega etiquetado al retag de arriba, que
            # solo toca los fences SIN lenguaje, asi que un T-SQL suelto se
            # quedaba con resaltado de VB para siempre.
            lenguaje = detect_code_lang(chr(10).join(trimmed)) or VB_LANG
            out.append(f"```{lenguaje}")
            out.extend(trimmed)
            out.append("```")
        else:
            out.extend(run)
        run.clear()

    for line in md_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_run()
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if is_code_like(line) or (run and not stripped):
            run.append(line)
            continue
        flush_run()
        out.append(line)

    flush_run()
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


#: A partir de este nivel, en esta documentación un encabezado ya no marca una
#: sección: es una línea a la que alguien le puso estilo de título en el editor
#: del origen. Por debajo (h2, h3, h4) sí hay estructura de verdad y no se toca.
LABEL_HEADING_MIN_LEVEL = 5

_HEADING_LINE_RX = re.compile(r'^(#{1,6})[ \t]*(.*?)[ \t]*$')


#: Un encabezado que solo dice en qué lenguaje está el trozo que va debajo.
#: Exige el nombre del lenguaje: un "Ejemplo" o un "Código" a secas sí puede
#: ser una sección de verdad, y esos no se tocan.
_ETIQUETA_DE_CODIGO_RX = re.compile(
    r'(?i)^[*_\s]*'
    r'(?:c[oó]digo|ejemplo|sintaxis)?'
    r'(?:\s+(?:en|de|para))?'
    r'\s*(?:vb6|vb\.net|vbnet|vbscript|vb|c\\?\#|c\s*sharp|t-sql|sql'
    r'|javascript|js|\.net|net)'
    r'\s*[:.]?[*_\s]*$')


def encajar_etiquetas_de_codigo(md_text: str) -> str:
    """
    Mete la etiqueta del lenguaje debajo del miembro que documenta.

    Los artículos de referencia del entorno de programación describen miembro
    a miembro, y cada uno trae su ejemplo en los dos lenguajes. El origen los
    escribió con el mismo nivel que el miembro, o con uno más alto::

        ### EditarPorObjeto
        ## Código en VB6
        ## Código en C\\#
        ### EditarPorObjetoyVista

    Así la jerarquía queda del revés: "Código en VB6" gobierna al miembro
    siguiente en vez de colgar del anterior, y sale en la página con letra
    más grande que el nombre del propio miembro. En el índice lateral de
    *Grid - Todo lo que debes saber sobre este control* eso son 96 entradas
    "Código en VB6" y "Código en C#" tapando los 48 miembros reales —de ahí
    anclas como ``#codigo-en-vb6_24``—.

    La etiqueta baja a un nivel por debajo del último encabezado que **no**
    es una etiqueta. Solo se baja, nunca se sube: una etiqueta que ya cuelga
    bien de su miembro se queda como está, y por eso la regla es idempotente.

    Medido sobre el corpus: 254 encabezados en 43 artículos.
    """
    lineas = md_text.split('\n')
    en_fence = False
    nivel_del_miembro = None
    cambiado = False

    for i, linea in enumerate(lineas):
        if linea.lstrip().startswith('```'):
            en_fence = not en_fence
            continue
        if en_fence:
            continue
        m = _HEADING_LINE_RX.match(linea)
        if not m or not m.group(2):
            continue
        nivel, texto = len(m.group(1)), m.group(2)

        if _ETIQUETA_DE_CODIGO_RX.match(texto):
            # Una etiqueta no gobierna secciones, así que tampoco cambia
            # quién es el miembro al que se le cuelgan las siguientes.
            if nivel_del_miembro is not None and nivel <= nivel_del_miembro:
                nuevo = min(nivel_del_miembro + 1, 6)
                if nuevo != nivel:
                    lineas[i] = '#' * nuevo + ' ' + texto
                    cambiado = True
            continue

        nivel_del_miembro = nivel

    return '\n'.join(lineas) if cambiado else md_text


def demote_label_headings(md_text: str) -> str:
    """
    Convierte en negrita los encabezados profundos que no gobiernan nada.

    El origen usa ``<h5>`` y ``<h6>`` como formato, no como estructura. En la
    ficha de un parámetro, por ejemplo, el nombre va en ``h5`` y debajo cuelgan
    dos ``h6`` con sus metadatos::

        ##### **ACTIVAR_CALCULO_DESFASE_HORAS_CONTRATO**
        Parámetro para facturar los posibles desfases.
        ###### ALQUILER (CONTRATOS) - Contratos
        ###### Tipo Valor: BOOL Valor por defecto: ON

    Esos dos ``h6`` no son secciones —"Tipo Valor: BOOL Valor por defecto: OFF"
    sale 282 veces— y llenan el índice lateral de la página de ruido. También
    cae aquí el pie ``##### Autor: ...``, que además era el que provocaba el
    salto de nivel de h1 a h5.

    Se degrada solo si **no gobierna nada**: sin texto debajo y sin un
    encabezado más profundo detrás. Uno que sí tenga contenido es una sección
    aunque esté en h5, y se respeta.
    """
    lineas = md_text.split('\n')

    # Posiciones de los encabezados que están fuera de un fence.
    encabezados: list[tuple[int, int]] = []
    en_fence = False
    for i, linea in enumerate(lineas):
        if linea.lstrip().startswith('```'):
            en_fence = not en_fence
            continue
        if en_fence:
            continue
        m = _HEADING_LINE_RX.match(linea)
        if m and m.group(2):
            encabezados.append((i, len(m.group(1))))

    for orden, (i, nivel) in enumerate(encabezados):
        if nivel < LABEL_HEADING_MIN_LEVEL:
            continue

        siguiente = encabezados[orden + 1] if orden + 1 < len(encabezados) else None
        fin = siguiente[0] if siguiente else len(lineas)
        if '\n'.join(lineas[i + 1:fin]).strip():
            continue                      # gobierna un texto: es una sección
        if siguiente and siguiente[1] > nivel:
            continue                      # es padre de otro encabezado

        texto = _HEADING_LINE_RX.match(lineas[i]).group(2)
        if texto.startswith('**') and texto.endswith('**'):
            lineas[i] = texto             # ya venía en negrita, no se dobla
        else:
            lineas[i] = f'**{texto}**'

    return '\n'.join(lineas)


#: Palabras con las que el origen abre un aviso. No son secciones: son la
#: etiqueta de una llamada de atención, y en el índice de la página aparecían
#: 108 veces "Ejemplo", 35 "NOTA", 32 "Importante"...

#: Siglas y nombres propios que sobreviven a pasar un titulo a minusculas.
#: Sin esto, "TRABAJAR CON SEPA" quedaría en "Trabajar con sepa".
SIGLAS = frozenset({
    'AHORA', 'ERP', 'TPV', 'SGA', 'CRM', 'API', 'SQL', 'IIS', 'BD', 'BBDD',
    'SEPA', 'IVA', 'IRPF', 'AEAT', 'SII', 'DDA', 'GCN', 'FAQ', 'FAQS', 'UE',
    'CIF', 'NIF', 'PDF', 'XML', 'HTML', 'CSS', 'JSON', 'CSV', 'URL', 'FTP',
    'VB', 'NET', 'DLL', 'ID', 'IDS', 'TIC', 'RRHH', 'EPI', 'ADMON', 'SAT',
    'TicketBAI', 'VeriFactu', 'Flexygo', 'Techfun', 'Windows', 'Office',
})

_CALLOUT_RX = re.compile(r'^(#{2,6})[ \t]*([*_ ]*)(.+?)([*_ ]*)[ \t]*$')


def _es_aviso(texto: str) -> bool:
    limpio = texto.strip().strip('*_ ').rstrip(':;.').strip()
    return limpio.lower() in CALLOUT_WORDS


def demote_callout_headings(md_text: str) -> str:
    """
    Pasa a negrita los encabezados que solo dicen "Nota", "Ejemplo", "Recuerda".

    Son la etiqueta de un aviso, no el título de una sección: llenaban el
    índice lateral de entradas que no llevan a ninguna parte concreta. Se
    conserva el énfasis, que es para lo que estaban puestos.
    """
    salida = []
    en_fence = False
    for linea in md_text.split('\n'):
        if linea.lstrip().startswith('```'):
            en_fence = not en_fence
            salida.append(linea)
            continue
        m = None if en_fence else _CALLOUT_RX.match(linea)
        if m and _es_aviso(m.group(3)):
            salida.append(f'**{m.group(3).strip().strip("*_ ")}**')
        else:
            salida.append(linea)
    return '\n'.join(salida)


def _a_frase(texto: str) -> str:
    """Pasa un texto gritado a mayúscula inicial, respetando las siglas."""
    palabras = texto.split(' ')
    salida = []
    for i, palabra in enumerate(palabras):
        nucleo = palabra.strip('*_.,;:()[]¿?¡!"\'')
        if not nucleo or not nucleo.isalpha():
            salida.append(palabra)          # versiones, números, símbolos
        elif nucleo.upper() in SIGLAS:
            salida.append(palabra)          # ERP, SEPA, IVA...
        else:
            salida.append(palabra.lower())
        # La primera palabra con letras abre en mayúscula.
        if not any(c.isalpha() for w in salida[:-1] for c in w):
            hueco = salida[-1]
            for j, c in enumerate(hueco):
                if c.isalpha():
                    salida[-1] = hueco[:j] + c.upper() + hueco[j + 1:]
                    break
    return ' '.join(salida)


#: Palabras que, gritadas y solas en un encabezado, son una palabra y no el
#: nombre de un parámetro.
#:
#: Es una lista y no una regla a propósito. Se intentó deducirlo —"solo
#: letras y todas mayúsculas"— y el propio corpus lo tumba:
#: ``CENTROCOSTELINEAAUTO`` cumple las dos cosas y es un parámetro, no una
#: palabra. Sin un diccionario no hay forma de distinguirlos, así que se
#: enumeran los que salen, igual que ``SIGLAS`` y ``CALLOUT_WORDS``.
#:
#: Añadir una palabra aquí es seguro; el riesgo está en deducirlas.
PALABRAS_DE_SECCION = frozenset({
    'introduccion', 'introducción', 'solucion', 'solución', 'soluciones',
    'contratacion', 'contratación', 'recordatorio', 'parametros', 'parámetros',
    'configuracion', 'configuración', 'facturacion', 'facturación',
    'empresas', 'movimientos', 'asientos', 'novedades', 'disponibles',
    'reservadas', 'alquiladas', 'festivos', 'descripcion', 'descripción',
    'requisitos', 'objetivo', 'objetivos', 'resumen', 'conclusion',
    'conclusión', 'conclusiones', 'funcionamiento', 'observaciones',
    'antecedentes', 'alcance', 'contenido', 'contenidos', 'procedimiento',
    'consideraciones', 'limitaciones', 'permisos', 'ventajas', 'inconvenientes',
    # Salieron al revisar lo que quedaba gritando tras la primera tanda.
    'licencia', 'licencias', 'certificados', 'certificado', 'instalacion',
    'instalación', 'operativa', 'impresion', 'impresión', 'funcionalidad',
    'resultado', 'resultados',
})


def _es_una_palabra_gritada(texto: str) -> bool:
    """
    ¿Este encabezado de una sola palabra es una palabra, o un nombre?

    De una palabra sola no se puede tirar sin más: la mitad son nombres de
    parámetro y bajarlos a minúsculas los destruye. La otra mitad son palabras
    corrientes —``INTRODUCCIÓN``, ``SOLUCIÓN``, ``FACTURACIÓN``— y dejarlas
    gritando descuadra el índice lateral frente a las demás secciones.

    La respuesta sale de ``PALABRAS_DE_SECCION``, que es una lista cerrada.
    Ahí está explicado por qué no puede ser una regla.
    """
    nucleo = texto.strip('*_.,;:()[]¿?¡!"\'')
    return nucleo.lower() in PALABRAS_DE_SECCION


def normalize_shouting_headings(md_text: str) -> str:
    """
    Baja de mayúsculas los encabezados escritos a gritos.

    "TABLA DE CONTENIDOS" sale 133 veces y "REQUISITOS PREVIOS" otras tantas.
    Los de **dos palabras o más** se bajan siempre; los de una sola, solo si
    ``_es_una_palabra_gritada`` dice que es una palabra y no el nombre de un
    parámetro. Las siglas se respetan.
    """
    salida = []
    en_fence = False
    for linea in md_text.split('\n'):
        if linea.lstrip().startswith('```'):
            en_fence = not en_fence
            salida.append(linea)
            continue
        m = None if en_fence else _CALLOUT_RX.match(linea)
        if not m:
            salida.append(linea)
            continue

        texto = m.group(3)
        letras = [c for c in texto if c.isalpha()]
        grita = letras and sum(1 for c in letras if c.isupper()) / len(letras) > 0.85
        palabras = texto.split()
        if grita and (len(palabras) >= 2 or _es_una_palabra_gritada(texto)):
            texto = _a_frase(texto)
        salida.append(f'{m.group(1)} {m.group(2)}{texto}{m.group(4)}'.rstrip())
    return '\n'.join(salida)


def fix_ordered_list_artifacts(md_content: str) -> str:
    """
    Corrige listas ordenadas rotas por html2text cuando el HTML original usa
    ``<li>`` separados para texto, imagen, pie de foto o espacios en blanco.
    """
    out: list[str] = []
    hidden_count = 0
    last_indent: Optional[str] = None
    has_visible = False
    after_media = False

    item_rx = re.compile(r'^(\s*)(\d+)\.\s*(.*)$')
    image_only_rx = re.compile(r'^\s*!\[[^\]]*\]\([^)]+\)\s*$')
    caption_rx = re.compile(r'^\s*_.*_\s*$')

    def is_blankish(text: str) -> bool:
        if not text:
            return True
        normalized = (text.replace('&nbsp;', ' ')
                          .replace('\xa0', ' ')
                          .replace('Â\xa0', ' ')
                          .replace('Â ', ' '))
        return normalized.strip() == ''

    for line in md_content.splitlines():
        m = item_rx.match(line)
        if m:
            indent, num_s, body = m.group(1), m.group(2), m.group(3) or ''

            if image_only_rx.match(body) and has_visible:
                out.append(f'{(last_indent or "")}   {body.strip()}')
                hidden_count += 1
                after_media = True
                continue

            if is_blankish(body) and has_visible:
                hidden_count += 1
                after_media = True
                continue

            try:
                num = int(num_s)
            except ValueError:
                num = 1
            out.append(f'{indent}{max(1, num - hidden_count)}. {body}')
            last_indent = indent
            has_visible = True
            after_media = False
            continue

        if caption_rx.match(line) and after_media and has_visible:
            out.append(f'{(last_indent or "")}   {line.strip()}')
            continue

        if is_blankish(line):
            out.append(line)
            continue

        hidden_count = 0
        last_indent = None
        has_visible = False
        after_media = False
        out.append(line)

    return '\n'.join(out)


def _convert_with_html2text(html: str) -> str:
    """Conversión base con html2text, sin postproceso de imágenes ni enlaces."""
    if not html or not html.strip():
        return ""

    # El código se aparta antes de tocar nada. html2text no produce fences:
    # convierte cada <pre> en texto indentado con 4 espacios y sin lenguaje,
    # de modo que MkDocs lo pintaba sin resaltar, y el postproceso de más abajo
    # lo volvía a partir en varios fences dejando fuera las líneas que no
    # parecían código (un Sub de VB acababa en cuatro cajas distintas).
    counters = {'code': 1}
    html = promover_negritas_a_encabezados(drop_empty_headings(html))
    html, code_map = protect_code_blocks(html, counters)

    handler = html2text.HTML2Text()
    handler.ignore_links = False    # conservar enlaces
    handler.ignore_images = False   # conservar imágenes
    handler.body_width = 0          # sin saltos de línea automáticos
    handler.protect_links = False
    handler.wrap_links = False
    handler.unicode_snob = True     # usar caracteres Unicode reales
    handler.mark_code = False       # ya no hay <pre> que marcar

    md_text = handler.handle(html)

    # Estas dos heurísticas solo deben ver código que llegó SIN <pre>, porque
    # el que venía marcado ya está a salvo en code_map.
    md_text = _extract_loose_sql_blocks(md_text)
    md_text = _add_missing_lang_hints(md_text)
    md_text = _clean_freshdesk_artifacts(md_text)

    # Va ANTES de devolver el código a su sitio: dentro de un bloque, los
    # ángulos son código y no hay que tocarlos. Las tablas todavía son tokens,
    # así que su HTML tampoco corre peligro.
    md_text = escapar_marcadores_entre_angulos(md_text)

    md_text = restore_code_blocks(md_text, code_map)
    md_text = _normalize_markdown_fences(md_text)
    return _collapse_adjacent_fences(md_text).strip()


# ---------------------------------------------------------------------------
# Motor de autor (markdownify)
# ---------------------------------------------------------------------------

_AUTHOR_CODE_MARKERS = [
    r"^'?Sub\s+\w+", r"^End\s+Sub$", r"^'?Function\s+\w+", r"^End\s+Function$",
    r"^Public\s+Class\b", r"^End\s+Class$", r"^Public\s+Sub\b", r"^Private\s+\w+",
    r"^Public\s+Property\b", r"^End\s+Property$", r"^Get$", r"^End\s+Get$",
    r"^Set\s*\(", r"^End\s+Set$", r"^Return\b", r"^MsgBox\s*\(", r"^Dim\s+\w+",
    r"^Set\s+\w+\s*=", r"^If\b", r"^Else\b", r"^ElseIf\b", r"^For\b", r"^Next\b",
    r"^With\b", r"^End\s+With$", r"^\w+\.\w+", r"^\.\w+", r"^'[^']*",
]


def _author_line_is_code(line: str) -> bool:
    return any(re.search(p, line, re.IGNORECASE) for p in _AUTHOR_CODE_MARKERS)


def _author_block_is_code(fragment: str) -> bool:
    """Decide si un fragmento HTML es, en realidad, una o varias líneas de código."""
    text = re.sub(r'(?is)<br\b[^>]*>', '\n', fragment or '')
    text = html_lib.unescape(re.sub(r'<[^>]+>', ' ', text)).replace('\xa0', ' ')
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text).strip()

    lines = [ln.strip() for ln in text.split('\n') if ln.strip()]
    if not lines:
        return False
    if len(lines) == 1:
        return _author_line_is_code(lines[0])

    code_hits = sum(1 for ln in lines if _author_line_is_code(ln))
    return _author_line_is_code(lines[0]) or code_hits >= max(2, (len(lines) + 1) // 2)


def sanitize_author_html(html: str) -> str:
    """Limpieza agresiva del HTML troceado típico de los artículos de autor."""
    if not html or not html.strip():
        return ""

    html = html.replace('\xa0', ' ')
    html = html.replace('&amp;amp;', '&amp;').replace('&amp;nbsp;', '&nbsp;')

    # Quitar spans vacíos y párrafos/divs sin contenido real.
    for _ in range(2):
        html = re.sub(r'(?is)<span[^>]*>\s*</span>', '', html)
        html = re.sub(r'(?is)<p[^>]*>\s*(?:&nbsp;|\s|<br\b[^>]*>)*</p>', '', html)
        html = re.sub(r'(?is)<div[^>]*>\s*(?:&nbsp;|\s|<br\b[^>]*>)*</div>', '', html)

    # Normalizar anchors vacíos típicos de Freshdesk / embeds de vídeo.
    html = re.sub(
        r'(?is)<a([^>]+href=["\']?[^"\'>]+["\']?[^>]*)>\s*'
        r'(?:&nbsp;|\s|<span[^>]*>\s*</span>|<br\b[^>]*>)*</a>',
        r'<a\1>&nbsp;</a>', html,
    )

    # Reducir ráfagas absurdas de <br>.
    html = re.sub(r'(?is)(?:<br\b[^>]*>\s*){3,}', '<br><br>', html)

    def split_mixed_paragraph(m: re.Match) -> str:
        content = m.group(1)
        if re.search(r'(?is)<(?:code|pre)\b', content):
            return m.group(0)
        parts = re.split(r'(?is)<br\b[^>]*>\s*<br\b[^>]*>', content)
        if len(parts) < 2:
            return m.group(0)
        prose = '<br><br>'.join(parts[:-1]).strip()
        tail = parts[-1].strip()
        if not _author_block_is_code(tail):
            return m.group(0)
        return (f'<p>{prose}</p>' if prose else '') + f'<p>{tail}</p>'

    html = re.sub(r'(?is)<p[^>]*>(.*?)</p>', split_mixed_paragraph, html)

    def merge_paragraph_code_blocks(m: re.Match) -> str:
        parts = re.findall(r'(?is)<p[^>]*>\s*<code[^>]*>(.*?)</code>\s*</p>', m.group(0))
        cleaned: list[str] = []
        for part in parts:
            part = re.sub(r'(?is)<br\b[^>]*>', '\n', part)
            part = re.sub(r'(?is)</?(?:p|div)[^>]*>', '\n', part)
            part = re.sub(r'(?is)</?span[^>]*>', '', part)
            cleaned.append(part.strip('\n'))
        merged = '\n'.join(p for p in cleaned if p.strip())
        return f'<pre>{merged}</pre>' if merged.strip() else ''

    html = re.sub(
        r'(?is)(?:<p[^>]*>\s*<code[^>]*>.*?</code>\s*</p>\s*){2,}',
        merge_paragraph_code_blocks, html,
    )

    def normalize_nested_code_paragraph(m: re.Match) -> str:
        paragraph, inner = m.group(0), m.group(1)
        if paragraph.lower().count('<code') < 2 or '<code' not in inner.lower():
            return paragraph
        inner = re.sub(r'(?is)</?code[^>]*>', '', inner)
        if len(re.findall(r'(?is)<br\b[^>]*>', inner)) < 2:
            return f'<p><code>{inner}</code></p>'
        return '<pre>' + re.sub(r'(?is)<br\b[^>]*>', '\n', inner) + '</pre>'

    html = re.sub(r'(?is)<p[^>]*>(.*?)</p>', normalize_nested_code_paragraph, html)

    # Un <code> dentro de un <pre> no aporta nada.
    html = re.sub(
        r'(?is)<pre([^>]*)>(.*?)</pre>',
        lambda m: f'<pre{m.group(1)}>' + re.sub(r'(?is)</?code[^>]*>', '', m.group(2)) + '</pre>',
        html,
    )

    def single_code_para_to_pre(m: re.Match) -> str:
        content = m.group(1)
        if len(re.findall(r'(?is)<br\b[^>]*>', content)) < 2:
            return m.group(0)
        content = re.sub(r'(?is)</?code[^>]*>', '', content)
        return '<pre>' + re.sub(r'(?is)<br\b[^>]*>', '\n', content) + '</pre>'

    html = re.sub(r'(?is)<p[^>]*>\s*<code[^>]*>(.*?)</code>\s*</p>', single_code_para_to_pre, html)

    # Fusionar rachas de párrafos que son todos código plano en un único <pre>.
    def merge_plain_code_paragraphs(block: str) -> str:
        cleaned: list[str] = []
        for part in re.findall(r'(?is)<p[^>]*>(.*?)</p>', block):
            part = re.sub(r'(?is)<br\b[^>]*>', '\n', part)
            # Solo el formato del editor, y SIN des-escapar: lo que sale de
            # aqui vuelve a un <pre>, y quien lo des-escapa bien es
            # ``protect_code_blocks``, que antes quita las etiquetas de
            # verdad. Haciendolo aqui al reves —des-escapar y luego borrar
            # "toda etiqueta"— un ``&lt;soap:Envelope&gt;`` del ejemplo se
            # convertia en marcado y se perdia la peticion entera. Es lo que
            # hacia perder texto al motor de autor en cuanto se le inyectaba
            # marcado de codigo, y por lo que sus dos reglas estaban
            # desactivadas.
            part = _FORMATO_ALREDEDOR_DEL_CODIGO_RX.sub('', part).replace('\xa0', ' ')
            part = re.sub(r'[ \t]+\n', '\n', part)
            part = re.sub(r'\n[ \t]+', '\n', part)
            cleaned.append(part.strip('\n'))
        merged = '\n'.join(p for p in cleaned if p.strip())
        return f'<pre>{merged}</pre>' if merged.strip() else block

    pieces: list[str] = []
    run: list[str] = []
    last_end = 0

    def flush_run() -> None:
        if not run:
            return
        run_html = ''.join(run)
        pieces.append(merge_plain_code_paragraphs(run_html) if len(run) >= 2 else run_html)
        run.clear()

    for m in re.finditer(r'(?is)<p[^>]*>.*?</p>', html):
        pieces.append(html[last_end:m.start()])
        if _author_block_is_code(m.group(0)):
            run.append(m.group(0))
        else:
            flush_run()
            pieces.append(m.group(0))
        last_end = m.end()

    flush_run()
    pieces.append(html[last_end:])
    return ''.join(pieces)


def _convert_with_markdownify(html: str, marcar_codigo: bool = False) -> str:
    """
    Conversión base con markdownify, protegiendo código y anclas vacías.

    ``marcar_codigo`` mete aquí las dos reglas que distinguen el código de la
    prosa. Van **entre** el saneado de autor y ``protect_code_blocks``, y ese
    hueco es el único que sirve: aplicadas antes, ``sanitize_author_html``
    reescribe el marcado recién puesto —une párrafos de código, rehace los
    ``<pre>``— y por el camino se dejaba texto; aplicadas después, el código
    ya no llega a ponerse a salvo y el conversor lo trocea. Por eso las dos
    reglas estuvieron desactivadas en este motor.
    """
    if not html or not html.strip():
        return ""

    html = promover_negritas_a_encabezados(drop_empty_headings(sanitize_author_html(html)))
    if marcar_codigo:
        html = codigo_suelto_en_parrafo_a_pre(html)
        html = sentencia_suelta_a_codigo(html)
    counters = {'link': 1, 'code': 1, 'pseudo': 1}

    html, code_map = protect_code_blocks(html, counters)

    # Ya está el código a salvo: ahora sí se puede des-escapar el resto, pero
    # antes hay que apartar los marcadores tipo <NombreProceso>, que el
    # des-escapado convertiría en marcado y el conversor borraría.
    html, pseudo_map = protect_escaped_pseudo_tags(html, counters)
    html = html.replace('&nbsp;', ' ')
    html = html_lib.unescape(html)

    # ── Proteger anclas vacías (markdownify las descarta) ─────────────────
    empty_link_map: dict[str, str] = {}

    def extract_empty_anchor(m: re.Match) -> str:
        inner = html_lib.unescape(re.sub(r'<[^>]+>', '', m.group(2) or '')).strip()
        # Un ancla que solo lleva una imagen no está vacía: la imagen se ve, y
        # es lo que se pulsa. Apartándola como enlace vacío se publicaba la URL
        # a pelo y el banner desaparecía. markdownify sí sabe convertir esto.
        if inner or re.search(r'(?i)<img\b', m.group(2) or ''):
            return m.group(0)
        href = (m.group(1) or '').strip()
        title_match = re.search(r'(?is)\btitle=["\'](.*?)["\']', m.group(0) or '')
        title = html_lib.unescape(title_match.group(1)).strip() if title_match else ''
        token = f'%%EMPTYLINK_{counters["link"]}%%'
        counters['link'] += 1
        if title:
            safe_title = title.replace('"', "'")
            empty_link_map[token] = f'[]({href} "{safe_title}")'
        else:
            empty_link_map[token] = f'[]({href})'
        return f' {token} '

    html = re.sub(
        r'(?is)<a[^>]+href=["\']?([^"\'\s>]+)["\']?[^>]*>(.*?)</a>',
        extract_empty_anchor, html,
    )

    # Aplanar los saltos estructurales del HTML restante.
    html = re.sub(r'[\r\n]+', ' ', html.replace('\r\n', ' '))

    md_text = markdownify_html(
        html,
        autolinks=False,
        bullets='-',
        code_language='',
        default_title=False,
        escape_asterisks=False,
        escape_underscores=False,
        escape_misc=False,
        heading_style='ATX',
        newline_style='spaces',
        strip_document='strip',
        strip_pre='strip',
        wrap=False,
    )

    for token, replacement in empty_link_map.items():
        md_text = md_text.replace(token, replacement)

    md_text = _extract_loose_sql_blocks(md_text)
    md_text = _add_missing_lang_hints(md_text)
    md_text = _clean_freshdesk_artifacts(md_text)

    # Espaciado que markdownify deja sucio.
    md_text = re.sub(r'\s+([.,:;])', r'\1', md_text)
    md_text = re.sub(r' {2,}', ' ', md_text)
    md_text = re.sub(r'\n ', '\n', md_text)
    md_text = re.sub(r' \n', '\n', md_text)
    md_text = re.sub(r'\n{3,}', '\n\n', md_text)

    # ── Restaurar el código protegido ─────────────────────────────────────
    md_text = restore_code_blocks(md_text, code_map)

    # Última pasada: un ancla vacía que viviera dentro de un bloque de código
    # se restaura ahora, cuando ese bloque ya está de vuelta en el texto.
    for token, replacement in empty_link_map.items():
        md_text = md_text.replace(token, replacement)

    for token, replacement in pseudo_map.items():
        md_text = md_text.replace(token, replacement)

    md_text = re.sub(r'\n{3,}', '\n\n', md_text)
    md_text = _normalize_markdown_fences(md_text)
    return _collapse_adjacent_fences(md_text).strip()


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

#: Una línea "en blanco" que en realidad lleva espacios. El origen las siembra
#: por todas partes —21.678 en el corpus— y derrotan al colapso de ``\n{3,}``,
#: que no las reconoce como vacías: los ficheros acumulaban rachas de
#: ``\n\n  \n\n  \n\n``.
#:
#: Ojo con la diferencia: la línea que **sí** significa algo es la que lleva dos
#: espacios TRAS UN TEXTO, que es el salto duro de Markdown. Una línea que solo
#: tiene espacios no significa nada.
_LINEA_SOLO_ESPACIOS_RX = re.compile(r'(?m)^[ \t]+$')


def limpiar_lineas_en_blanco(md_text: str) -> str:
    """
    Vacía las líneas que solo llevan espacios y colapsa las rachas.

    Se aplica fuera de los fences: dentro, una línea con espacios puede ser
    indentación con significado.

    Comprobado sobre los 1.337 artículos que cambian: en **ninguno** varía el
    texto renderizado. Son 0,6 % menos de fichero y, sobre todo, un ``.md``
    que se puede leer y diferenciar.
    """
    return re.sub(r'\n{3,}', '\n\n', _LINEA_SOLO_ESPACIOS_RX.sub('', md_text))


def convert_standard(
    html: str,
    docs_root: Path,
    md_file_path: Path,
    images_out_dir: Path,
    article_title: str = "",
    article_id: str = "",
    broken_images_log: Optional[list] = None,
) -> str:
    """
    Motor por defecto. Conserva las tablas como HTML crudo, descarga sus
    imágenes y aplica el postproceso de listas y de código VB.
    """
    if broken_images_log is None:
        broken_images_log = []

    html = preprocess_reference_html(article_title, html)
    # Antes de convertir y con el HTML entero: la regla necesita ver de quien
    # cuelga cada color para saber sobre que fondo cae.
    html = quitar_colores_ilegibles(html)
    # Antes de convertir y sobre el HTML entero: las dos necesitan ver el
    # parrafo con sus <br> y el documento con todas sus anclas.
    # Sobre el documento entero, no solo sobre las tablas conservadas: un
    # <h1> cuyo unico contenido es el video se publicaba como un "# " vacio.
    html = desenvolver_encabezados_html_sin_texto(html)
    html = quitar_anclas_vacias_repetidas(html)
    html = quitar_tablas_vacias(html)
    html = codigo_suelto_en_parrafo_a_pre(html)
    html = sentencia_suelta_a_codigo(html)
    html, videos = apartar_videos_de_youtube(html, {'video': 1})
    protected_html, table_map = protect_html_tables(html)

    md_content = _convert_with_html2text(protected_html)
    md_content = download_images_from_markdown(
        md_content, md_file_path, images_out_dir, article_title, broken_images_log,
    )

    for token, table_html in table_map.items():
        local_table_html = download_images_in_html_fragment(
            table_html, docs_root, md_file_path, images_out_dir,
            article_title, broken_images_log,
        )
        # La imagen ya está descargada y el src apunta a local, pero el editor
        # de Freshdesk deja además un data-filelink con la URL original. No se
        # ve en la página y se publica igual.
        local_table_html = limpiar_atributos_de_freshdesk(local_table_html)
        md_content = md_content.replace(token, f'\n\n{local_table_html}\n\n')

    md_content = fix_ordered_list_artifacts(md_content)
    md_content = apply_article_fixes(article_id, article_title, md_content)
    md_content = repair_vb_reference_markdown(
        md_content,
        unwrap_short_fences=article_title.strip() in UNWRAP_SHORT_FENCE_TITLES,
    )
    md_content = _collapse_adjacent_fences(md_content)
    # Al final: para entonces los lenguajes ya están asignados, y así se ven
    # también los párrafos que salieron etiquetados como código.
    md_content = desenvolver_fences_de_prosa(md_content)
    md_content = encajar_etiquetas_de_codigo(md_content)
    md_content = demote_label_headings(md_content)
    md_content = demote_callout_headings(md_content)
    # DESPUÉS de degradar, no antes. ``demote_callout_headings`` deshace las
    # promociones de más arriba —y con razón: un "## Nota" no es una sección—,
    # así que promover aquí es lo único que sobrevive. Los avisos primero: sus
    # palabras ya no están cuando la regla de secciones mira qué negritas
    # quedan sueltas.
    # Las cajas con reglas primero: llevan la palabra y el texto en la misma
    # línea, así que la otra regla no las ve y se estorbarían si fuera al revés.
    md_content = _outside_fences(md_content, avisos_entre_reglas_a_admonitions)
    md_content = _outside_fences(md_content, avisos_a_admonitions)
    # La ultima: el aviso que lleva su texto en la misma linea. Va detras
    # de la que exige la palabra sola, aunque son formas excluyentes.
    md_content = _outside_fences(md_content, avisos_en_linea_a_admonitions)
    md_content = _outside_fences(md_content, promover_negritas_sueltas)
    # Lo último de todo: ya no se crean más encabezados, así que ninguno se
    # queda sin escapar.
    # Antes de normalizar: si el enlace vacío recupera su etiqueta, el
    # encabezado deja de ser kilométrico y no hay nada que degradar.
    md_content = _outside_fences(md_content, juntar_enlace_vacio_con_su_texto)
    md_content = _outside_fences(md_content, normalizar_encabezados_al_final)
    md_content = normalize_shouting_headings(md_content)
    # Segunda pasada, con los encabezados ya definitivos:
    # ``promover_negritas_sueltas`` crea encabezados DESPUES de la primera,
    # y un "##### Autor: ..." que entonces parecia gobernar texto resulta no
    # gobernar nada. Es idempotente, asi que esto solo coge lo que la
    # primera no podia ver.
    md_content = demote_label_headings(md_content)
    # Un solo marcador de vineta por documento: mezclarlos hace que
    # Python-Markdown funda las listas en una sola suelta, y unos items
    # salen espaciados y otros apretados.
    # Antes de unificar las vinetas: los pasos pasan a ser items de lista y
    # tienen que contar para el marcador dominante del documento.
    md_content = pasos_numerados_a_lista(md_content)
    # Con los encabezados ya definitivos: las anclas se calculan sobre ellos.
    # Primero se saca el indice del bloque de codigo; si no, enlazar sus
    # puntos solo consigue que se vea el corchete.
    md_content = desangrar_el_indice(md_content)
    md_content = enlazar_indice_a_las_secciones(md_content)
    md_content = unificar_marcadores_de_lista(md_content)
    # Al final: el bloque del video es HTML en crudo y no hay ninguna regla
    # que tenga nada que decirle.
    md_content = restaurar_videos_de_youtube(md_content, videos)
    return _outside_fences(md_content, limpiar_lineas_en_blanco).strip()


def convert_author(
    html: str,
    docs_root: Path,
    md_file_path: Path,
    images_out_dir: Path,
    article_title: str = "",
    article_id: str = "",
    broken_images_log: Optional[list] = None,
) -> str:
    """Motor para artículos de autor: saneado agresivo + markdownify."""
    if broken_images_log is None:
        broken_images_log = []

    html = quitar_colores_ilegibles(html)
    # Antes de convertir y sobre el HTML entero: las dos necesitan ver el
    # parrafo con sus <br> y el documento con todas sus anclas.
    # Sobre el documento entero, no solo sobre las tablas conservadas: un
    # <h1> cuyo unico contenido es el video se publicaba como un "# " vacio.
    html = desenvolver_encabezados_html_sin_texto(html)
    html = quitar_anclas_vacias_repetidas(html)
    html = quitar_tablas_vacias(html)
    html, videos = apartar_videos_de_youtube(html, {'video': 1})
    # Las dos reglas de código van DENTRO del conversor, entre el saneado de
    # autor y ``protect_code_blocks``. Aplicadas aquí, como en el otro motor,
    # ``sanitize_author_html`` reescribía el marcado recién puesto y por el
    # camino perdía texto: tres artículos se dejaban entre el 18 % y el 23 %.
    md_content = _convert_with_markdownify(html, marcar_codigo=True)
    md_content = apply_article_fixes(article_id, article_title, md_content)
    md_content = download_images_from_markdown(
        md_content, md_file_path, images_out_dir, article_title, broken_images_log,
    )
    md_content = encajar_etiquetas_de_codigo(md_content)
    md_content = demote_label_headings(md_content)
    md_content = demote_callout_headings(md_content)
    # DESPUÉS de degradar, no antes. ``demote_callout_headings`` deshace las
    # promociones de más arriba —y con razón: un "## Nota" no es una sección—,
    # así que promover aquí es lo único que sobrevive. Los avisos primero: sus
    # palabras ya no están cuando la regla de secciones mira qué negritas
    # quedan sueltas.
    # Las cajas con reglas primero: llevan la palabra y el texto en la misma
    # línea, así que la otra regla no las ve y se estorbarían si fuera al revés.
    md_content = _outside_fences(md_content, avisos_entre_reglas_a_admonitions)
    md_content = _outside_fences(md_content, avisos_a_admonitions)
    # La ultima: el aviso que lleva su texto en la misma linea. Va detras
    # de la que exige la palabra sola, aunque son formas excluyentes.
    md_content = _outside_fences(md_content, avisos_en_linea_a_admonitions)
    md_content = _outside_fences(md_content, promover_negritas_sueltas)
    # Lo último de todo: ya no se crean más encabezados, así que ninguno se
    # queda sin escapar.
    # Antes de normalizar: si el enlace vacío recupera su etiqueta, el
    # encabezado deja de ser kilométrico y no hay nada que degradar.
    md_content = _outside_fences(md_content, juntar_enlace_vacio_con_su_texto)
    md_content = _outside_fences(md_content, normalizar_encabezados_al_final)
    md_content = normalize_shouting_headings(md_content)
    # Segunda pasada, con los encabezados ya definitivos:
    # ``promover_negritas_sueltas`` crea encabezados DESPUES de la primera,
    # y un "##### Autor: ..." que entonces parecia gobernar texto resulta no
    # gobernar nada. Es idempotente, asi que esto solo coge lo que la
    # primera no podia ver.
    md_content = demote_label_headings(md_content)
    # Un solo marcador de vineta por documento: mezclarlos hace que
    # Python-Markdown funda las listas en una sola suelta, y unos items
    # salen espaciados y otros apretados.
    # Antes de unificar las vinetas: los pasos pasan a ser items de lista y
    # tienen que contar para el marcador dominante del documento.
    md_content = pasos_numerados_a_lista(md_content)
    # Con los encabezados ya definitivos: las anclas se calculan sobre ellos.
    # Primero se saca el indice del bloque de codigo; si no, enlazar sus
    # puntos solo consigue que se vea el corchete.
    md_content = desangrar_el_indice(md_content)
    md_content = enlazar_indice_a_las_secciones(md_content)
    md_content = unificar_marcadores_de_lista(md_content)
    # Al final: el bloque del video es HTML en crudo y no hay ninguna regla
    # que tenga nada que decirle.
    md_content = restaurar_videos_de_youtube(md_content, videos)
    return _outside_fences(md_content, limpiar_lineas_en_blanco).strip()
