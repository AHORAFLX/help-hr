"""
test_pipeline.py
================
Tests de regresión del pipeline. Sin dependencias: se ejecuta con

    python test_pipeline.py

Cada test que empieza por ``test_`` se descubre y se ejecuta. Los que llevan
"BUG" en el nombre fijan un fallo concreto que ya se corrigió, para que no
vuelva a colarse.

Requiere Python 3.12 o superior.
"""

from __future__ import annotations

import re
import sys
import collections
import os
import tempfile
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline import article_fixes, common, converters, generation_state  # noqa: E402
from pipeline import repair_links as links  # noqa: E402


# ---------------------------------------------------------------------------
# Conversión
# ---------------------------------------------------------------------------

def test_bug_imagen_rota_no_lleva_espacio():
    """
    [* ](url) se convertía en '![]( url)' con un espacio dentro del paréntesis,
    y la descarga de imágenes no lo reconocía: la imagen se quedaba apuntando
    a Freshdesk para siempre.
    """
    md = converters._clean_freshdesk_artifacts('[* ](https://s3.amazonaws.com/foo.png)')
    assert md.strip() == '![](https://s3.amazonaws.com/foo.png)', md
    assert common.MD_IMAGE_RX.search(md), 'la descarga de imágenes no reconoce el resultado'


def test_bug_la_negrita_no_se_borra():
    """
    La limpieza de énfasis vacío usaba ``\\*\\s*\\*``, que casa con el "**" de
    CUALQUIER negrita: borraba el marcado de todos los artículos y el texto
    salía plano. Medido en una categoría: 7 negritas renderizadas frente a
    1.228 tras el arreglo.
    """
    limpia = converters._clean_freshdesk_artifacts
    assert limpia('**Código VB6:** texto') == '**Código VB6:** texto'
    assert limpia('**negrita** y _cursiva_') == '**negrita** y _cursiva_'
    assert limpia('***fuerte***') == '***fuerte***'
    # Lo que sí hay que borrar: énfasis sin contenido.
    assert limpia('vacia **** aqui') == 'vacia  aqui'
    assert limpia('vacia **   ** aqui') == 'vacia  aqui'
    assert limpia('cursiva vacia * * aqui') == 'cursiva vacia  aqui'


def test_bug_separador_horizontal_no_queda_en_un_asterisco():
    """
    html2text escribe un <hr> como "* * *". La limpieza de cursivas vacías se
    comía dos de los tres asteriscos y dejaba un " *" suelto en mitad del texto.
    """
    out = converters._convert_with_html2text('<p>Antes</p><hr><p>Despues</p>')
    assert '---' in out, out
    assert not re.search(r'(?m)^\s*\*\s*$', out), f'queda un asterisco huérfano: {out!r}'


def test_bug_item_de_lista_vacio_no_deja_vineta_suelta():
    """Freshdesk usa <li><br></li> como separador; quedaba una viñeta huérfana."""
    out = converters._convert_with_html2text(
        '<ul><li><em>Visible</em>: hace algo.</li><li><br></li>'
        '<li><em>Backcolor</em>: hace otra cosa.</li></ul>'
    )
    assert not re.search(r'(?m)^\s*\*\s*$', out), f'queda una viñeta vacía: {out!r}'
    assert 'Visible' in out and 'Backcolor' in out


def test_bug_enlace_externo_sin_texto_no_queda_invisible():
    """
    En el origen son <a href="...">&nbsp;</a>. Sin etiqueta se renderizan como
    un <a> vacío: el enlace existe pero no se ve, y el lector lo pierde.
    """
    url = 'http://videos.ahora.es/ScriptSamples#68'
    out = common.fix_internal_links(f'Ver el vídeo: []({url})', Path('x.md'), {}, {}, None, [0])
    assert f'[{url}]({url})' in out, out
    # Una imagen sin alt NO es un enlace vacío: no se debe tocar.
    img = '![](https://s3.amazonaws.com/x/y.png)'
    assert common.fix_internal_links(img, Path('x.md'), {}, {}, None, [0]) == img


def test_bug_guiones_escapados_a_la_vista():
    """
    html2text escapa el guion inicial de línea por precaución y dejaba
    "\\--- Los valores disponibles son:" a la vista de quien lee el .md.
    """
    limpia = converters._clean_freshdesk_artifacts
    # Dos o más guiones seguidos de texto: el escape sobra y el texto se queda
    # como texto (no es ni separador ni lista).
    assert limpia('**Titulo**  \n\\--- Los valores son:') == '**Titulo**  \n--- Los valores son:'
    # "8\\." SÍ necesita el escape: sin él sería una lista ordenada que
    # rompería la enumeración de códigos.
    assert limpia('7: Dudoso  \n8\\. Deteriorado') == '7: Dudoso  \n8\\. Deteriorado'
    # Las rutas de Windows llevan barras de verdad: no son escapes.
    ruta = r'Copiar a C:\Program Files (x86)\AHORA\Lib'
    assert limpia(ruta) == ruta


def test_vinetas_tecleadas_a_mano_pasan_a_lista():
    """
    El autor no uso la lista del editor: tecleo el caracter. Llegan 62 lineas
    asi, con el punto medio y con el punto gordo, y Markdown no las reconoce:
    se publicaban como un parrafo que empieza con un simbolo.
    """
    from markdown import Markdown
    punto, gordo = chr(0xb7), chr(0x2022)
    salto = chr(10)

    md = converters.vinetas_literales_a_lista(
        punto + ' Base de datos actualizada' + salto + punto + ' Segunda cosa')
    html = Markdown().convert(md)
    assert html.count('<li>') == 2, html
    assert punto not in md, md

    # Sin espacio detras tambien es una vineta.
    assert converters.vinetas_literales_a_lista(punto + 'Entorno TechFun') == '- Entorno TechFun'
    assert converters.vinetas_literales_a_lista(gordo + '**PEDIDOS**') == '- **PEDIDOS**'
    # En medio de una frase NO se toca.
    frase = 'Un texto con ' + punto + ' en medio'
    assert converters.vinetas_literales_a_lista(frase) == frase
    # Y una vineta sola no es una lista: es un artefacto, y lo limpia otra regla.
    assert converters.vinetas_literales_a_lista(gordo) == gordo


def test_bug_una_vineta_no_puede_acabar_de_encabezado():
    """
    En "ERP - Almacen - Embalajes" el origen trae dos parametros en vineta.
    Uno se quedaba de parrafo y el otro, por ser una negrita sola en su
    parrafo, lo ascendia promover_negritas_sueltas a "## - OFERTAS_OCULTA_
    EMBALAJE", con el simbolo de la vineta dentro del encabezado.

    Convertida antes en item de lista, ya no es candidata a encabezado.
    """
    gordo = chr(0x2022)
    salto = chr(10)
    entrada = 'Texto previo.' + salto * 2 + gordo + '**OFERTAS_OCULTA_EMBALAJE**' + salto * 2 + 'Texto siguiente.'
    salida = converters._clean_freshdesk_artifacts(entrada)
    assert '## ' not in salida, salida
    assert '- **OFERTAS_OCULTA_EMBALAJE**' in salida, salida

    # Y su hermana, que en el origen YA era un encabezado con la vineta
    # dentro: ahi no hay lista que crear, pero el simbolo sobra igual —se
    # colaba en el titulo y de ahi en la tabla de contenidos—.
    assert converters.vinetas_literales_a_lista(
        '## ' + gordo + ' OFERTAS_OCULTA_EMBALAJE') == '## OFERTAS_OCULTA_EMBALAJE'
    assert converters.vinetas_literales_a_lista('## Titulo normal') == '## Titulo normal'


def test_una_palabra_gritada_baja_si_es_una_palabra_de_verdad():
    """
    Antes solo se bajaban los de dos palabras o mas, para no destrozar los
    nombres de parametro. Eso dejaba 27 encabezados gritando —INTRODUCCION,
    SOLUCION, FACTURACION— descuadrados frente al resto del indice.
    """
    baja = ['INTRODUCCI' + chr(0xd3) + 'N', 'SOLUCIONES', 'RECORDATORIO', 'EMPRESAS']
    for palabra in baja:
        salida = converters.normalize_shouting_headings('## ' + palabra)
        assert salida != '## ' + palabra, salida
        assert salida[3].isupper() and salida[4:].islower(), salida

    # Lo que NO se puede tocar: nombres de parametro y siglas.
    for palabra in ('CENTROCOSTE_LINEA_AUTO', 'OFERTAS_DISE' + chr(0xd1) + 'O',
                    'PEDIDOSxPLANTA', 'ERP', 'SEPA', 'IVA'):
        assert converters.normalize_shouting_headings('## ' + palabra) == '## ' + palabra, palabra


def test_vinetas_escritas_a_mano_pasan_a_lista():
    """
    El autor escribe la lista con guiones dentro de un párrafo (<br>), y
    html2text la deja como "\\- ...": ni se ve como lista ni se lee bien.
    """
    from markdown import Markdown
    md = converters._clean_freshdesk_artifacts(
        'Parámetros necesarios:  \n\\- _AsignaAsistente_ : Icono  \n\\- _AssistAddField_ : Campo'
    )
    html = Markdown().convert(md)
    assert '<ul>' in html and html.count('<li>') == 2, html
    assert '\\-' not in md, md


def test_regla_de_guiones_pasa_a_separador():
    """Una línea de solo guiones es un separador, no texto con una barra."""
    from markdown import Markdown
    md = converters._clean_freshdesk_artifacts('**Código en C#:**  \n\\-----------------')
    html = Markdown().convert(md)
    assert '<hr' in html, html
    # Y la línea de arriba NO se convierte en encabezado por la sintaxis setext.
    assert '<h2' not in html, html
    assert '<strong>Código en C#:</strong>' in html, html


def test_bug_comentario_sql_escapado_sin_espacio():
    """
    Un comentario SQL se escribe pegado a los guiones ("--familias hijas") y
    html2text lo escapaba a "\\--familias hijas". La regla pedía un espacio
    detrás, así que esos se quedaban con la barra a la vista.
    """
    assert converters._clean_freshdesk_artifacts('\\--familias hijas') == '--familias hijas'
    assert converters._clean_freshdesk_artifacts('\\----2 Situacion') == '----2 Situacion'
    # Y una línea de solo guiones sigue siendo un separador, no texto.
    assert converters._clean_freshdesk_artifacts('\\-----------------').strip() == '---'


def test_guion_escapado_a_mitad_de_linea():
    """A mitad de línea un guion no tiene significado de bloque: sobra la barra."""
    out = converters._clean_freshdesk_artifacts('**Formato** y **Presentacion** \\-----> Enumeración')
    assert '\\-' not in out, out
    assert '-----> Enumeración' in out, out


def test_negrita_no_se_convierte_en_encabezado():
    """
    Si se quita el escape de un "---" que va SOLO en su línea, la línea de
    arriba se convierte en encabezado (sintaxis setext). No debe pasar.
    """
    from markdown import Markdown
    md = converters._clean_freshdesk_artifacts('**Código VB6:**  \n\\--- Los valores son:')
    html = Markdown().convert(md)
    assert '<h2' not in html, html
    assert '<strong>Código VB6:</strong>' in html, html


def test_la_limpieza_no_entra_en_los_fences():
    """Dentro de un bloque de código un asterisco es código, no marcado."""
    original = '```sql\nSELECT * FROM a, * FROM b\n```\n\n**negrita**'
    assert converters._clean_freshdesk_artifacts(original) == original


def test_negrita_sobrevive_a_la_conversion_completa():
    out = converters._convert_with_html2text(
        '<p><strong>Código VB6:</strong> y <em>cursiva</em>.</p>'
    )
    assert '**Código VB6:**' in out, out


def test_regex_imagen_tolera_espacios_y_title():
    """La descarga debe encontrar la imagen aunque venga con espacio o title."""
    for md in (
        '![alt](https://x/y.png)',
        '![alt]( https://x/y.png)',
        '![alt](https://x/y.png "Un título")',
    ):
        assert common.MD_IMAGE_RX.search(md), md


def test_bug_saltos_de_linea_reales_en_bloques_vb():
    """
    wrap_description_signatures unía las líneas con la cadena literal '\\n'
    en vez de un salto de línea real, y el código salía en una sola línea.
    """
    html = (
        '<p>Descripción:</p>'
        '<p>Public Function Uno(ByVal a As Long) As Long</p>'
        '<p>Public Function Dos(ByVal b As Long) As Long</p>'
        '<p>Ejemplo de uso:</p>'
    )
    out = converters.preprocess_reference_html('Referencia', html)
    assert '\\n' not in out, f'quedan saltos literales: {out!r}'
    assert '<pre>Public Function Uno(ByVal a As Long) As Long\nPublic Function Dos' in out, out


def test_deteccion_de_lenguaje():
    d = converters.detect_code_lang
    assert d('') == ''
    assert d('SELECT * FROM dbo.Clientes WHERE Id = 1') == 'sql'
    assert d('DECLARE @t AS DECIMAL(18,2)\nSELECT @t = SUM(I) FROM F') == 'sql'
    assert d('Dim x As Long\nSet x = Nothing') == converters.VB_LANG
    assert d('Public Function Ver(\n Optional aFecha As Variant)\nAs Variant') == converters.VB_LANG
    assert d('gForm.grdLineas.ActivarScripts = True') == converters.VB_LANG
    assert d('function saluda(n) {\n  console.log(n);\n}') == 'javascript'
    assert d('<div class="x">\n<span>y</span>\n</div>') == 'html'


def test_bug_csharp_no_se_etiqueta_como_vb():
    """
    VB y C# comparten sintaxis; el detector devolvía el primer patrón que
    encajara y un "obj.Prop = true;" de C# caía en el patrón laxo de VB.
    """
    d = converters.detect_code_lang
    assert d('namespace X\n{\npublic class Y : Base\n{\n}\n}') == 'csharp'
    assert d('public void F(IGrid g, ref Valor c)\n{\n    // ...\n}') == 'csharp'
    assert d('IFrm f = (IFrm)gCn.AhoraProceso("X", out _, gCn);\nf.Nombre = "Y";') == 'csharp'


def test_bug_el_hint_de_vb_tiene_lexer_en_pygments():
    """
    'vb' no es un alias de Pygments: los bloques etiquetados así se pintaban
    en gris, sin resaltar nada. El hint tiene que ser uno que exista.
    """
    from pygments.lexers import get_lexer_by_name
    get_lexer_by_name(converters.VB_LANG)  # revienta si el alias no existe
    for lang in ('sql', 'csharp', 'javascript', 'html', 'xml', 'powershell', 'bash', 'json'):
        get_lexer_by_name(lang)


def test_bug_pre_no_acaba_como_texto_indentado():
    """
    html2text no genera fences: convierte cada <pre> en texto indentado con 4
    espacios y sin lenguaje. Además el postproceso lo troceaba después en
    varios fences dejando fuera las líneas que no parecían código.
    """
    out = converters._convert_with_html2text(
        '<p>Antes.</p><pre>Sub Uno(a)\n     ...\nEnd Sub\n\nSub Dos(b)\n     ...\nEnd Sub</pre><p>Despues.</p>'
    )
    assert out.count('```') == 2, f'el bloque se ha partido: {out!r}'
    assert f'```{converters.VB_LANG}' in out, out
    assert '     ...' in out, 'se han perdido las líneas de continuación'
    fuera = re.sub(r'(?s)```.*?```', '', out)
    assert not re.search(r'(?m)^ {4,}\S', fuera), f'queda código indentado fuera del fence: {fuera!r}'


def test_bug_seccion_descripcion_no_borra_el_codigo():
    """
    wrap_description_signatures reconstruía el cuerpo usando solo los <p> y
    <table>, así que cualquier <pre> del medio desaparecía: en los artículos
    de referencia eso borraba el ejemplo de C# entero.
    """
    html = (
        '<p>Implementación:</p><pre>Function F() As Boolean</pre>'
        '<p>Descripción:</p><p>Hace algo.</p>'
        '<p><strong>Código C#:</strong></p>'
        '<pre>namespace N\n{\npublic class C {}\n}</pre>'
    )
    out = converters.preprocess_reference_html('F', html)
    assert 'namespace N' in out, f'se ha perdido el bloque C#: {out!r}'
    assert 'Function F() As Boolean' in out


def test_bug_encabezado_vacio_con_espacio_duro():
    """<h4><br></h4> y <h3>\\xa0</h3> son separadores visuales, no encabezados."""
    out = converters.drop_empty_headings(
        '<h4><br></h4><h3><small>\xa0</small></h3><h3>&nbsp;</h3><h2>Real</h2>'
    )
    assert '<h4' not in out and '<h3' not in out, out
    assert '<h2>Real</h2>' in out


def test_bug_marcador_entre_angulos_fuera_de_pre():
    """
    <NombreProceso> escrito como &lt;...&gt; en un párrafo se convertía en
    marcado al des-escapar y el conversor lo borraba.
    """
    out = converters._convert_with_markdownify(
        '<p>Llamada: lObj.&lt;NombreProceso&gt; &lt;Parámetros&gt;</p>'
    )
    assert '<NombreProceso>' in out, out
    assert '<Parámetros>' in out, out


def test_solo_se_envuelven_las_rachas_de_codigo():
    """
    Las heurísticas de rescate eran todo-o-nada: si en la sección había unas
    pocas líneas de código, metían la sección entera en un <pre>, prosa
    incluida.
    """
    out = converters._wrap_code_runs(
        'Esto es una explicación larga en castellano.\nDim a As Long\nSet a = 1\nY esto es otra explicación.'
    )
    assert out.count('<pre>') == 1, out
    assert 'Esto es una explicación larga' not in out.split('<pre>')[1], out


def test_heuristicas_no_tocan_codigo_ya_marcado():
    """Si la sección ya trae <pre>, las heurísticas no tienen nada que hacer."""
    codigo = '<pre>Dim a\nSet a = 1\nEnd Sub</pre>'
    out = converters.preprocess_reference_html('T', '<p>Ejemplo de uso:</p>' + codigo)
    # El bloque de código sale intacto...
    assert codigo in out, out
    # ...y la etiqueta pasa a ser una sección navegable.
    assert '<h2>Ejemplo de uso</h2>' in out, out


def test_etiquetas_de_referencia_pasan_a_seccion():
    """
    "Implementación:" o "Descripción:" son la estructura de los artículos de
    API, pero el origen las escribe como párrafo suelto. Quedaba una
    incoherencia: en el mismo artículo, "Código VB6:" salía como encabezado
    —porque va en negrita— y "Descripción:" como texto corrido.
    """
    f = converters._etiquetas_de_referencia_a_encabezados
    assert f('<p>Implementación:</p>') == '<h2>Implementación</h2>'
    assert f('<p><strong>Descripción:</strong></p>') == '<h2>Descripción</h2>'
    assert f('<p>Parámetros:</p>') == '<h2>Parámetros</h2>'
    # Una frase que empieza igual no es una etiqueta.
    for html in ('<p>Descripción de la tabla:</p>', '<p>Texto normal</p>'):
        assert f(html) == html, html


def test_bug_la_racha_de_sql_se_corta_ante_la_prosa():
    """
    El bloque de SQL suelto seguía tragando líneas hasta topar con otra cosa,
    y se llevaba por delante el enlace y el "**Ver código ejemplo**" que
    separaban dos ejemplos. El fence acababa cerrándose donde no tocaba.
    """
    entrada = (
        'Texto de entrada.\n'
        '\n'
        "SELECT * FROM Tabla WHERE Id = 1\n"
        'INSERT INTO Otra VALUES (1)\n'
        '\n'
        '[](http://videos.ahora.es/ScriptSamples#80)\n'
        '\n'
        '**Ver código ejemplo**\n'
        '\n'
        'Final.\n'
    )
    salida = converters._extract_loose_sql_blocks(entrada)

    assert salida.count('```') == 2, salida
    bloque = re.search(r'```[^\n]*\n(.*?)```', salida, re.DOTALL).group(1)
    assert 'SELECT' in bloque and 'INSERT' in bloque
    assert 'videos.ahora.es' not in bloque, 'el enlace no puede quedar dentro del código'
    assert 'Ver código ejemplo' not in bloque, 'la prosa tampoco'


def test_bug_la_constante_de_tabla_with_no_partia_el_bloque():
    """
    ";WITH Nombre AS" abre una CTE de T-SQL y no estaba entre los arranques,
    así que la cabecera se quedaba fuera del fence y el código empezaba a media
    sentencia. Admite lista de columnas y el AS en la línea siguiente.
    """
    for linea in (';WITH FAM AS', ';WITH LosEfectos(IdFactura,IdEfecto)',
                  'WITH x AS', ';WITH **FAM** AS'):
        assert converters._SQL_START.match(linea), linea
    # Pero una frase que empieza por "With" no es SQL.
    assert not converters._SQL_START.match('With mucho gusto le atendemos')


def test_bug_el_pie_de_navegacion_no_acaba_dentro_del_codigo():
    """
    El pie de estos artículos son DOS enlaces en la misma línea. La regla solo
    admitía uno, así que no cortaba la racha de SQL y la navegación acababa
    pintada en gris dentro del bloque de código.
    """
    entrada = '\n'.join([
        'SELECT * FROM LosEfectos',
        '',
        '[<< Artículo anterior](A.md) [Siguiente artículo >>](B.md)',
    ])
    salida = converters._extract_loose_sql_blocks(entrada)
    bloque = re.search(r'```[^\n]*\n(.*?)```', salida, re.DOTALL).group(1)
    assert 'Artículo anterior' not in bloque, bloque
    assert salida.count('```') == 2


def test_bug_un_rotulo_en_negrita_corta_la_racha_de_sql():
    """"**Ejemplo** de WITH recursivo para..." separa dos ejemplos: es prosa."""
    entrada = '\n'.join([
        'SELECT 1 FROM Tabla',
        '',
        '**Ejemplo** de WITH recursivo para devolver el árbol de familias:',
        '',
        'SELECT 2 FROM Otra',
    ])
    salida = converters._extract_loose_sql_blocks(entrada)
    assert salida.count('```') == 4, salida
    assert '**Ejemplo** de WITH' in salida.split('```')[2]


def test_sql_suelto_se_envuelve_en_fence():
    md = converters._extract_loose_sql_blocks('Texto previo.\n\nSELECT 1\nFROM dbo.T\n')
    assert '```sql' in md, md


def test_lista_ordenada_con_imagen_intercalada():
    """Los <li> que solo llevan imagen no deben consumir número de la lista."""
    md = converters.fix_ordered_list_artifacts(
        '1. Primer paso\n2. ![](img/a.png)\n3. Segundo paso\n'
    )
    assert '1. Primer paso' in md
    assert '2. Segundo paso' in md, md
    assert '![](img/a.png)' in md


def test_conversion_estandar_completa():
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        md_file = docs / 'Cat' / 'Carp' / 'Art.md'
        md_file.parent.mkdir(parents=True)
        out = converters.convert_standard(
            '<h1>Titulo</h1><p>Un párrafo.</p><table><tr><td>celda</td></tr></table>',
            docs, md_file, docs / 'docs_assets' / 'images', 'Art', '1',
        )
        assert 'Un párrafo.' in out
        assert '<table>' in out, 'la tabla debe conservarse como HTML crudo'


def test_bug_style_escapado_dentro_de_pre_no_se_pierde():
    """
    El motor de autor des-escapaba el documento entero ANTES de aislar el
    código, así que un '&lt;style&gt;' de un ejemplo se convertía en etiqueta
    real y markdownify se llevaba el bloque entero por delante.
    """
    out = converters._convert_with_markdownify(
        '<p>Cabecera:</p><div><pre>&lt;style&gt;\n.BlockBody{width:380px;}\n&lt;/style&gt;</pre></div>'
    )
    assert '.BlockBody{width:380px;}' in out, out
    assert '<style>' in out, out


def test_bug_marcador_entre_angulos_no_se_borra():
    """<NombreLibreria.NombreClase> es contenido del ejemplo, no una etiqueta."""
    out = converters._convert_with_markdownify(
        '<pre>Set lObj = CreateObject ("&lt;NombreLibreria.NombreClase&gt;")\n'
        'lObj.&lt;NombreProceso&gt;</pre>'
    )
    assert '<NombreLibreria.NombreClase>' in out, out
    assert '<NombreProceso>' in out, out


def test_bug_token_de_ancla_no_sobrevive_en_la_salida():
    """Un ancla vacía dentro de un <pre> dejaba el token %%EMPTYLINK_n%% a la vista."""
    out = converters._convert_with_markdownify(
        '<pre>HTML:\n<a href="https://ejemplo.com/x"></a>\n{Nombre}</pre>'
    )
    assert '%%' not in out, out


def test_fences_adyacentes_se_unen():
    md = converters._collapse_adjacent_fences('```vb\nDim a\n```\n```vb\nDim b\n```\n')
    assert md.count('```') == 2, md
    assert 'Dim a' in md and 'Dim b' in md


def test_conversion_autor_completa():
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        md_file = docs / 'Cat' / 'Carp' / 'Art.md'
        md_file.parent.mkdir(parents=True)
        out = converters.convert_author(
            '<p>Autor: Daniel</p><p><code>Dim x As Long</code></p>'
            '<p><code>Set x = Nothing</code></p>',
            docs, md_file, docs / 'docs_assets' / 'images', 'Art', '1',
        )
        assert '```' in out, out


# ---------------------------------------------------------------------------
# Parches de artículo
# ---------------------------------------------------------------------------

def test_parches_solo_aplican_a_su_articulo():
    md = 'Texto.\n##### Autor: Daniel Ernesto Lutz Llano\nMás texto.'
    tocado = article_fixes.apply_article_fixes('154000128795', '', md)
    intacto = article_fixes.apply_article_fixes('000000000000', '', md)
    assert tocado != md, 'el parche no se aplicó a su artículo'
    assert intacto == md, 'el parche se aplicó a un artículo que no le corresponde'


def test_bug_no_vuelve_el_parche_que_dejaba_un_fence_sin_cerrar():
    """
    El artículo 154000130031 tenía un parche que borraba el ``` de cierre de
    un bloque, creyendo que sobraba. Lo que sobraba en realidad era que la
    racha de SQL se hubiera tragado la prosa; el parche convertía ese fallo en
    uno peor, un fence sin cerrar que descuadraba el resto del artículo.
    """
    for fix in article_fixes.ARTICLE_FIXES:
        assert '154000130031' not in (fix.article_ids or ()), \
            'ese artículo se arregla en _extract_loose_sql_blocks, no con un parche'


def test_catalogo_de_parches_es_coherente():
    for fix in article_fixes.ARTICLE_FIXES:
        assert fix.reason, 'todo parche necesita explicar por qué existe'
        assert fix.article_ids or fix.titles, f'parche sin destinatario: {fix.reason}'
        for pattern, _repl, flags in fix.substitutions:
            re.compile(pattern, flags)  # revienta si el patrón es inválido
    for fix in article_fixes.LINK_FIXES:
        assert fix.reason and fix.path
        for pattern, _repl, flags in fix.substitutions:
            re.compile(pattern, flags)


# ---------------------------------------------------------------------------
# Enlaces internos
# ---------------------------------------------------------------------------

def test_bug_el_autoenlace_no_se_anida_dentro_de_otro():
    """
    El origen escribe autoenlaces: [https://...articles/123](https://...). La
    regla de URLs sueltas envolvía esa URL —que es el TEXTO del enlace— en otro
    enlace, y quedaba [[Enlace Interno](destino)](destino), que se renderiza
    enseñando el Markdown en crudo.
    """
    url = 'https://ahora.freshdesk.com/es/support/solutions/articles/44001807882-erp-lic'
    destino = str(Path('docs/Cat/Carp/ERP - Licenciamiento.md').resolve())
    salida = common.fix_internal_links(
        f'Ver: [{url}]({url})', Path('docs/Cat/Carp/A.md'),
        {'44001807882': destino}, {}, None, [0],
    )
    assert '[[' not in salida, salida
    # Y el texto visible pasa a ser el nombre del artículo, no la URL.
    assert '[ERP - Licenciamiento]' in salida, salida


def test_bug_un_enlace_de_freshdesk_sin_texto_no_se_borra_entero():
    """
    Al degradarlo se quedaba en nada y la frase que lo introducía se quedaba
    coja: "Versión 4.4.2100 o anterior:" y detrás, el vacío. El propio enlace
    lleva el título en su slug.
    """
    url = ('https://ahora.freshdesk.com/es/support/solutions/articles/'
           '44001761035-portal-gestion-de-licencias')
    salida = common.fix_internal_links(
        f'.- Versión 4.4.2100 o anterior: []({url})',
        Path('docs/Cat/Carp/A.md'), {}, {}, None, [0],
    )
    assert 'Portal gestion de licencias' in salida, salida
    assert 'freshdesk' not in salida


def test_enlaces_a_la_trastienda_de_freshdesk_se_degradan():
    """
    /a/solutions y /a/tickets piden login de agente: para el lector no llevan a
    ningún sitio, y sus ids son de otra cuenta, así que tampoco se pueden
    traducir. Se conserva la frase y se pierde el enlace.
    """
    ruta = Path('docs/Cat/Carp/A.md')
    con_texto = '[Ver la carpeta](https://ahora.freshdesk.com/a/solutions/folders/44001194885) y sigue.'
    assert common.fix_internal_links(con_texto, ruta, {}, {}, None, [0]) == 'Ver la carpeta y sigue.'

    crudo = 'Mira https://ahora.freshdesk.com/a/tickets/81535 para el detalle.'
    assert 'freshdesk' not in common.fix_internal_links(crudo, ruta, {}, {}, None, [0])


def test_categoria_de_freshdesk_se_traduce_a_su_carpeta():
    """/support/solutions/<id> es una categoría, no un artículo."""
    destinos = {'154000119363': str(Path('docs/TPV').resolve())}
    salida = common.fix_internal_links(
        '[la doc de TPV](https://ahora.freshdesk.com/support/solutions/154000119363)',
        Path('docs/ERP/Carp/A.md'), {}, {}, None, [0], destinos,
    )
    assert salida == '[la doc de TPV](../../TPV/)', salida


def test_enlaces_sin_texto_visible():
    """Un [](destino) no se ve en la página: el lector no tiene dónde pulsar."""
    ruta = Path('docs/Cat/Carp/A.md')

    def arregla(texto):
        return common.fix_internal_links(texto, ruta, {}, {}, None, [0])

    # A un artículo: su nombre de fichero es el título que le falta.
    assert arregla('Ver [](Otro%20Articulo.md).') == 'Ver [Otro Articulo](Otro%20Articulo.md).'
    # Con un título mal formado detrás, que se descarta.
    assert arregla('[](A.md "[Enlace Interno](A.md)")texto') == '[A](A.md)texto'
    # Con el texto partido por un salto de línea duro.
    assert arregla('[  \n](B.md)') == '[B](B.md)'
    # A algo que no es un artículo: sobra entero.
    assert arregla('x [](/erp/uploads/abc/image.png) y') == 'x  y'
    # Uno con texto no se toca.
    assert arregla('[Texto](C.md)') == '[Texto](C.md)'


def test_enlace_por_id_de_articulo():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        origen = root / 'Cat' / 'A.md'
        destino = root / 'Cat' / 'B.md'
        origen.parent.mkdir(parents=True)
        destino.write_text('x', encoding='utf-8')

        counter = [0]
        out = common.fix_internal_links(
            '[Ver B](https://ahora.freshdesk.com/support/solutions/articles/999-b)',
            origen, {'999': str(destino)}, {}, None, counter,
        )
        assert out == '[Ver B](B.md)', out
        assert counter[0] == 1


def test_bug_una_palabra_comun_no_basta_para_reasignar():
    """
    El umbral anterior (una sola palabra de 3+ letras) reapuntaba enlaces a
    artículos sin relación. Ahora hace falta un solape real.
    """
    assert links.MIN_WORD_OVERLAP >= 3, 'el umbral de solape se ha vuelto a bajar'
    assert common.MIN_FUZZY_TOKEN_OVERLAP >= 2


def test_reparacion_por_nombre_de_fichero():
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        (docs / 'Cat').mkdir(parents=True)
        destino = docs / 'Cat' / 'Configuración Inicial.md'
        destino.write_text('# destino', encoding='utf-8')
        origen = docs / 'Cat' / 'Origen.md'
        origen.write_text('[Ver](Configuracion Inicial.md)', encoding='utf-8')

        by_name, _ = links._build_file_index(docs)
        unfixable: list[str] = []
        broken, fixed = links.phase_exact_name_repair(docs, [origen], by_name, unfixable)
        assert (broken, fixed) == (1, 1), (broken, fixed)
        assert 'Configuraci%C3%B3n%20Inicial.md' in origen.read_text(encoding='utf-8') \
            or 'Configuración%20Inicial.md' in origen.read_text(encoding='utf-8')


def test_bug_titulo_markdown_no_convierte_un_enlace_bueno_en_roto():
    """
    Markdown admite [texto](ruta "título"). El comprobador se tragaba el
    título como parte de la ruta, daba el enlace por roto y la fase 2 lo
    reescribía apuntando a otro sitio y sin el título.
    """
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        (docs / 'Cat').mkdir(parents=True)
        (docs / 'Cat' / 'Destino.md').write_text('# destino', encoding='utf-8')
        origen = docs / 'Cat' / 'Origen.md'
        origen.write_text('[Ver](Destino.md "Teclas de acceso rápido")', encoding='utf-8')

        assert list(links._iter_broken_links(origen.read_text(encoding='utf-8'), origen)) == []

        by_name, _ = links._build_file_index(docs)
        broken, fixed = links.phase_exact_name_repair(docs, [origen], by_name, [])
        assert (broken, fixed) == (0, 0), 'un enlace válido no se toca'
        assert origen.read_text(encoding='utf-8') == '[Ver](Destino.md "Teclas de acceso rápido")'


def test_bug_parentesis_en_el_nombre_no_recorta_la_ruta():
    """
    La regex antigua cortaba en el primer ')': un artículo cuyo nombre lleva
    paréntesis quedaba con media ruta y se daba por roto.
    """
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        (docs / 'Cat').mkdir(parents=True)
        (docs / 'Cat' / 'Abrir archivo (common dialog).md').write_text('x', encoding='utf-8')
        origen = docs / 'Cat' / 'Origen.md'
        origen.write_text('[Ver](Abrir archivo (common dialog).md)', encoding='utf-8')

        assert list(links._iter_broken_links(origen.read_text(encoding='utf-8'), origen)) == []


def test_reparar_un_enlace_conserva_su_titulo():
    """Reapuntar un enlace no puede perder el título por el camino."""
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        (docs / 'Cat').mkdir(parents=True)
        (docs / 'Cat' / 'Configuración Inicial.md').write_text('# destino', encoding='utf-8')
        origen = docs / 'Cat' / 'Origen.md'
        origen.write_text('[Ver](Configuracion Inicial.md "Un título")', encoding='utf-8')

        by_name, _ = links._build_file_index(docs)
        broken, fixed = links.phase_exact_name_repair(docs, [origen], by_name, [])
        assert (broken, fixed) == (1, 1), (broken, fixed)
        assert '"Un título"' in origen.read_text(encoding='utf-8'), origen.read_text(encoding='utf-8')


def test_bug_el_sql_no_se_confunde_con_un_enlace():
    """
    La documentación está llena de SQL con corchetes: [Descrip] [varchar](50)
    parece un enlace Markdown. Las fases 2 y 3 llegaban a reescribir dentro de
    un bloque de código.
    """
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        (docs / 'Cat').mkdir(parents=True)
        origen = docs / 'Cat' / 'Origen.md'
        origen.write_text(
            'Texto normal.\n'
            '\n'
            '```sql\n'
            'CREATE TABLE T (\n'
            '  [Id] [int] NOT NULL,\n'
            '  [Descrip] [varchar](50) NULL\n'
            ')\n'
            '```\n'
            '\n'
            'Y un `[inline] [varchar](max)` también.\n',
            encoding='utf-8',
        )

        rotos = list(links._iter_broken_links(origen.read_text(encoding='utf-8'), origen))
        assert rotos == [], [r.url for r in rotos]

        antes = origen.read_text(encoding='utf-8')
        by_name, by_words = links._build_file_index(docs)
        links.phase_exact_name_repair(docs, [origen], by_name, [])
        links.phase_overlap_repair(docs, [origen], by_words, [])
        assert origen.read_text(encoding='utf-8') == antes, 'no se puede tocar el código'


def test_informe_de_enlaces_rotos_agrupa_por_destino():
    """
    Estos enlaces se corrigen a mano, cambiando el destino por la URL del sitio
    del producto. Todos los de un mismo destino llevan la misma URL base, así
    que el informe los junta en vez de ordenarlos por fichero de origen.
    """
    rotos = [
        {'file': 'ERP\\Compras\\A.md', 'link': '../../TPV/x.md', 'text': 'ver', 'target': 'TPV'},
        {'file': 'ERP\\Ventas\\B.md', 'link': '../../TPV/y.md', 'text': '', 'target': 'TPV'},
        {'file': 'ERP\\Ventas\\C.md', 'link': '../../SGA/z.md', 'text': 'otro', 'target': 'SGA'},
    ]
    motivos = [links.UnrepairedLink('ERP\\Compras\\A.md', '../../TPV/x.md', 'sin candidato')]

    texto = '\n'.join(links.build_broken_links_report(rotos, motivos))

    assert 'DESTINO: TPV   (2 enlaces)' in texto, texto
    assert 'DESTINO: SGA   (1 enlaces)' in texto, texto
    # El grupo grande va primero: es el que más trabajo ahorra de una sentada.
    assert texto.index('DESTINO: TPV') < texto.index('DESTINO: SGA')
    # El motivo del intento fallido se conserva en el informe único.
    assert 'motivo : sin candidato' in texto
    # Un enlace sin texto no inventa una línea vacía.
    assert 'texto  : \n' not in texto

    assert links.build_broken_links_report([]) == [], 'sin rotos no hay informe'


def test_separar_destino_y_titulo():
    assert links.split_link_target('ruta.md "Un título"') == ('ruta.md', '"Un título"')
    assert links.split_link_target("ruta.md 'Otro'") == ('ruta.md', "'Otro'")
    assert links.split_link_target('ruta%20(x).md') == ('ruta%20(x).md', '')
    # Unas comillas dentro del nombre no son un título.
    assert links.split_link_target('el "raro".md') == ('el "raro".md', '')
    assert links.build_link('t', 'a.md', '"T"') == '[t](a.md "T")'
    assert links.build_link('t', 'a.md') == '[t](a.md)'


def test_indice_de_ficheros_no_se_corrompe():
    """phase_exact_name_repair extendía la lista del índice, corrompiéndolo."""
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        (docs / 'Cat').mkdir(parents=True)
        (docs / 'Cat' / 'Destino Largo De Verdad.md').write_text('x', encoding='utf-8')
        origen = docs / 'Cat' / 'Origen.md'
        origen.write_text('[a](Destino Largo De Verdad Extra.md)', encoding='utf-8')

        by_name, _ = links._build_file_index(docs)
        antes = {k: len(v) for k, v in by_name.items()}
        links.phase_exact_name_repair(docs, [origen], by_name, [])
        despues = {k: len(v) for k, v in by_name.items()}
        assert antes == despues, f'el índice se modificó: {antes} → {despues}'


def test_solo_se_tocan_los_ficheros_indicados():
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        docs.mkdir(parents=True)
        intocable = docs / 'NoTocar.md'
        intocable.write_text('[roto](Inexistente.md)', encoding='utf-8')
        original = intocable.read_text(encoding='utf-8')

        links.run_pipeline(docs, only_files=[], skip_validation=True)
        assert intocable.read_text(encoding='utf-8') == original


# ---------------------------------------------------------------------------
# Estado incremental
# ---------------------------------------------------------------------------

def test_bug_titulos_duplicados_no_se_pisan():
    """
    Dos artículos distintos con el mismo título escribían en el mismo .md y
    solo sobrevivía el último: contenido perdido en silencio.
    """
    import migrate

    def art(aid, titulo):
        return migrate.Article(
            article_id=aid, title=titulo, description='<p>x</p>',
            category_id='10', folder_id='20', updated_at='',
        )

    articulos = [art('300', 'Mismo Título'), art('100', 'Mismo Título'), art('200', 'Otro')]
    docs = Path('docs')
    paths, collisions = migrate.assign_output_paths(articulos, docs, {'10': 'Cat'}, {'20': 'Carp'})

    assert len(set(paths.values())) == 3, f'rutas repetidas: {paths}'
    assert len(collisions) == 1
    # El id más bajo conserva el nombre limpio; el resto llevan su Id.
    assert paths['100'].name == 'Mismo Título.md', paths['100']
    assert paths['300'].name == 'Mismo Título (300).md', paths['300']
    assert paths['200'].name == 'Otro.md'


def test_reparto_de_rutas_es_estable():
    """El reparto no puede depender del orden en que llegan los artículos."""
    import migrate

    def art(aid):
        return migrate.Article(article_id=aid, title='T', description='', category_id='1',
                               folder_id='2', updated_at='')

    ids = ['5', '3', '9']
    a = migrate.assign_output_paths([art(i) for i in ids], Path('docs'), {'1': 'C'}, {'2': 'F'})[0]
    b = migrate.assign_output_paths([art(i) for i in reversed(ids)], Path('docs'), {'1': 'C'}, {'2': 'F'})[0]
    assert a == b, (a, b)


def test_bug_clean_output_no_borra_lo_versionado():
    """
    --clean-output hacía rmtree de docs/ entero y se llevaba por delante el
    tema, los estáticos y las portadas de idioma, que están en git.
    """
    import migrate

    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        (docs / 'docs_assets' / 'images').mkdir(parents=True)
        (docs / 'docs_assets' / 'images' / 'a.png').write_bytes(b'x')
        (docs / 'stylesheets').mkdir()
        (docs / 'index.md').write_text('portada', encoding='utf-8')
        (docs / 'Categoria Generada').mkdir()
        (docs / 'Categoria Generada' / 'a.md').write_text('x', encoding='utf-8')

        migrate.clean_generated_docs(docs)

        assert (docs / 'docs_assets' / 'images' / 'a.png').exists(), 'borró las imágenes'
        assert (docs / 'stylesheets').exists(), 'borró los estáticos'
        assert (docs / 'index.md').exists(), 'borró la portada'
        assert not (docs / 'Categoria Generada').exists(), 'no borró lo generado'


def test_estado_incremental():
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        md = out_dir / 'a.md'
        md.write_text('x', encoding='utf-8')

        run = generation_state.RunState(out_dir)
        run.record(
            '1', title='A', product='ERP', category_id='10', category_name='Cat',
            folder_id='20', folder_name='Carp', path='a.md',
            source_updated_at='2026-01-01T00:00:00Z',
        )
        generation_state.finalize_generation_state(out_dir, run)

        state = generation_state.load_generation_state(out_dir)
        assert state['articles']['1']['title'] == 'A'
        assert not generation_state.get_run_state_path(out_dir).exists()

        # Sin cambios en origen: no hay que regenerar.
        assert not generation_state.should_generate_article(state, '1', '2026-01-01T00:00:00Z', md)
        # Cambió el updated_at: sí hay que regenerar.
        assert generation_state.should_generate_article(state, '1', '2026-06-01T00:00:00Z', md)
        # El fichero ya no está: hay que regenerar.
        md.unlink()
        assert generation_state.should_generate_article(state, '1', '2026-01-01T00:00:00Z', md)


def test_huerfanos_se_acotan_a_las_categorias_procesadas():
    state = {
        'meta': {},
        'articles': {
            '1': {'category_id': '10', 'path': 'docs/a.md'},
            '2': {'category_id': '99', 'path': 'docs/b.md'},
        },
    }
    # El artículo 2 es de otra categoría: no se toca aunque no esté vivo.
    orphans = generation_state.find_orphan_articles(state, live_article_ids=set(), scoped_category_ids={'10'})
    assert set(orphans) == {'1'}, orphans


def test_borradores_se_distinguen_de_los_publicados():
    """
    La tabla no viene pre-filtrada: hay 132 borradores mezclados con los
    publicados y se estaban generando como documentación buena.
    """
    import json as _json

    import migrate

    def parse(**campos):
        base = {'Id': 1, 'Title': 'T', 'Description': '', 'CategoryId': '10', 'FolderId': '20'}
        return migrate._parse_article(_json.dumps(base | campos))

    assert parse(Status=1).is_draft
    assert not parse(Status=2).is_draft
    # Sin campo de estado, o con basura, se publica: el peor caso de un cambio
    # de nombre en el JSON es no filtrar nada, nunca omitirlo todo en silencio.
    assert not parse().is_draft
    assert not parse(Status='vete a saber').is_draft


def test_bug_articulo_movido_deja_duplicado():
    """
    Mover un artículo de categoría, o cambiarle el título, dejaba el .md
    antiguo en docs/ para siempre: sigue vivo en origen, así que no es
    huérfano y nadie lo miraba.
    """
    import migrate

    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        vieja = out_dir / 'docs' / 'CatVieja' / 'Carp' / 'Mi Articulo.md'
        nueva = out_dir / 'docs' / 'CatNueva' / 'Carp' / 'Mi Articulo.md'
        for ruta in (vieja, nueva):
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_text('x', encoding='utf-8')

        state = {'meta': {}, 'articles': {'999': {'path': 'docs/CatVieja/Carp/Mi Articulo.md'}}}

        movidos = generation_state.find_relocated_articles(
            state, {'999': nueva}, out_dir, scoped_article_ids={'999'},
        )
        assert set(movidos) == {'999'}, movidos
        assert movidos['999'][0] == 'docs/CatVieja/Carp/Mi Articulo.md'
        assert movidos['999'][1] == 'docs/CatNueva/Carp/Mi Articulo.md'

        # Y el borrado se lleva también la carpeta que se queda vacía.
        assert migrate.delete_generated_md(movidos['999'][0], out_dir, out_dir / 'docs')
        assert not vieja.exists()
        assert not vieja.parent.exists(), 'la carpeta vacía debería desaparecer'
        assert nueva.exists(), 'jamás se puede borrar la copia nueva'


def test_reubicado_no_se_toca_si_falta_el_fichero_nuevo():
    """Si la conversión del artículo movido falló, el .md viejo se queda."""
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        vieja = out_dir / 'docs' / 'Vieja' / 'A.md'
        vieja.parent.mkdir(parents=True)
        vieja.write_text('x', encoding='utf-8')
        nueva = out_dir / 'docs' / 'Nueva' / 'A.md'          # no existe

        state = {'meta': {}, 'articles': {'1': {'path': 'docs/Vieja/A.md'}}}
        movidos = generation_state.find_relocated_articles(
            state, {'1': nueva}, out_dir, scoped_article_ids={'1'},
        )
        assert movidos == {}, movidos


def test_reubicados_se_acotan_a_los_articulos_de_la_ejecución():
    """Generar una categoría no puede tocar ficheros de las demás."""
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        vieja = out_dir / 'docs' / 'Otra' / 'B.md'
        nueva = out_dir / 'docs' / 'Nueva' / 'B.md'
        for ruta in (vieja, nueva):
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_text('x', encoding='utf-8')

        state = {'meta': {}, 'articles': {'2': {'path': 'docs/Otra/B.md'}}}
        movidos = generation_state.find_relocated_articles(
            state, {'2': nueva}, out_dir, scoped_article_ids={'99'},
        )
        assert movidos == {}, movidos


def test_run_state_no_reescribe_en_cada_articulo():
    """El volcado a disco es por lotes, no por artículo."""
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)
        run = generation_state.RunState(out_dir)
        run.record('1', title='A', product='', category_id='', category_name='',
                   folder_id='', folder_name='', path='a.md', source_updated_at='')
        assert not generation_state.get_run_state_path(out_dir).exists(), \
            'no debería escribir en disco tras un solo artículo'
        run.flush()
        assert generation_state.get_run_state_path(out_dir).exists()


def test_ejecución_interrumpida_se_reanuda():
    """
    Si la ejecución muere a medias, lo ya generado queda en el estado de la
    ejecución. Al relanzar hay que recuperarlo en lugar de rehacerlo.
    """
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp)

        muerta = generation_state.RunState(out_dir)
        muerta.record('1', title='A', product='', category_id='10', category_name='Cat',
                      folder_id='20', folder_name='Carp', path='docs/Cat/Carp/A.md',
                      source_updated_at='2026-01-01T00:00:00Z')
        muerta.flush()

        reanudada = generation_state.RunState(out_dir, resume=True)
        assert set(reanudada.articles()) == {'1'}, reanudada.articles()

        # Sin resume se empieza de cero y el fichero temporal se descarta.
        limpia = generation_state.RunState(out_dir)
        assert limpia.articles() == {}
        assert not generation_state.get_run_state_path(out_dir).exists()


def test_parte_de_la_ejecución():
    """El parte tiene que contar lo que ha cambiado, no lo que hay."""
    import migrate

    lineas = migrate.build_run_report(
        {
            'nuevos': 3, 'actualizados': 7, 'movidos': 1, 'retirados': 2,
            'borradores': 132, 'errores': 0, 'enlaces': 44,
            'pendientes_de_borrar': 0,
        }
    )
    texto = '\n'.join(lineas)

    assert 'Artículos nuevos' in texto and ': 3' in texto
    assert 'Borradores omitidos' in texto and ': 132' in texto
    # Sin ficheros pendientes ni errores, no se avisa de nada.
    assert '--prune-orphans' not in texto
    assert 'reintentar' not in texto


def test_parte_avisa_de_lo_que_queda_pendiente():
    import migrate

    texto = '\n'.join(migrate.build_run_report(
        {
            'nuevos': 0, 'actualizados': 0, 'movidos': 4, 'retirados': 0,
            'borradores': 0, 'errores': 2, 'enlaces': 0,
            'pendientes_de_borrar': 4,
        }
    ))

    assert '--prune-orphans' in texto, 'tiene que decir cómo limpiar lo que sobra'
    assert 'reintentar' in texto, 'tiene que decir que los errores se reintentan'


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def test_etiqueta_del_panel_de_navegacion():
    """
    MkDocs usa el H1 como etiqueta del nav. Hay títulos de 165 caracteres que
    en la barra lateral se parten en cinco líneas, así que la etiqueta se
    recorta —solo la etiqueta: el H1 conserva el título entero—.
    """
    corto = 'ERP - Compras - Facturas de acreedor'
    assert common.nav_title(corto) == corto, 'lo que cabe no se toca'
    assert common.front_matter(corto) == '', 'ni lleva cabecera'

    largo = ('Script - Recargar código de formularios útil para cuando '
             'modificamos el código de script de un formulario')
    etiqueta = common.nav_title(largo)
    assert len(etiqueta) <= common.NAV_TITLE_MAX, etiqueta
    assert largo.startswith(etiqueta.rstrip('.')), 'la etiqueta es un prefijo del título'

    # Se corta por un separador natural cuando lo hay.
    assert common.nav_title(
        'Grid - Estilos - Cambiar tamaño de fila y letra del grid, alineación de texto'
    ) == 'Grid - Estilos - Cambiar tamaño de fila y letra del grid'

    # Y nunca se corta a mitad de palabra.
    sin_separadores = 'palabra ' * 20
    assert not common.nav_title(sin_separadores).replace('...', '').endswith('palabr')


def test_la_cabecera_yaml_no_se_rompe_con_dos_puntos():
    """Un ':' sin comillas convierte el YAML en una clave y revienta el build."""
    fm = common.front_matter(
        'AHORA Install: no se pudo importar SqlDatabaseCredential, pero uno o varios objetos'
    )
    assert fm.startswith('---\ntitle: "'), fm
    assert fm.endswith('"\n---\n\n'), fm

    import yaml  # MkDocs lo trae; si falla, es que la cabecera no es válida
    assert isinstance(yaml.safe_load(fm.strip().strip('-')), dict)


def test_encabezados_que_solo_eran_una_etiqueta():
    """
    El origen usa h5/h6 como formato, no como estructura: en la ficha de un
    parámetro, "Tipo Valor: BOOL Valor por defecto: OFF" es un h6 y sale 282
    veces. Llenaban el índice lateral de la página de ruido.
    """
    ficha = '\n'.join([
        '##### **PARAM_UNO**', '',
        'Descripción del parámetro.', '',
        '###### ALQUILER (CONTRATOS) - Contratos', '',
        '###### Tipo Valor: BOOL Valor por defecto: ON', '',
        '##### Autor: Fulano de Tal',
    ])
    salida = converters.demote_label_headings(ficha)

    assert '**ALQUILER (CONTRATOS) - Contratos**' in salida
    assert '**Tipo Valor: BOOL Valor por defecto: ON**' in salida
    assert '**Autor: Fulano de Tal**' in salida
    assert '######' not in salida
    # El que sí gobierna un texto sigue siendo un encabezado.
    assert '##### **PARAM_UNO**' in salida
    # Y no se dobla la negrita del que ya venía en negrita.
    assert '****' not in salida


def test_los_avisos_no_son_secciones():
    """
    "Nota", "Ejemplo" o "Recuerda" son la etiqueta de una llamada de atención,
    no el título de una sección: llenaban el índice de la página de entradas
    que no llevan a ninguna parte. "Ejemplo" salía 108 veces.
    """
    for encabezado, esperado in (
        ('## Importante', '**Importante**'),
        ('## Recuerda', '**Recuerda**'),
        ('##### NOTA:', '**NOTA:**'),
        ('### **Nota**', '**Nota**'),
    ):
        assert converters.demote_callout_headings(encabezado) == esperado, encabezado

    # Un encabezado que solo empieza por la palabra sigue siendo una sección.
    for intacto in ('## Ejemplo de uso de la función', '## Introducción', '# Nota'):
        assert converters.demote_callout_headings(intacto) == intacto, intacto


def test_los_encabezados_a_gritos_pasan_a_frase():
    normaliza = converters.normalize_shouting_headings

    assert normaliza('## TABLA DE CONTENIDOS') == '## Tabla de contenidos'
    assert normaliza('## REQUISITOS PREVIOS') == '## Requisitos previos'
    # Las siglas se respetan.
    assert normaliza('## TRABAJAR CON SEPA') == '## Trabajar con SEPA'
    assert normaliza('## 1.2. LIBRO DE IVA') == '## 1.2. Libro de IVA'
    # Una sola palabra suele ser el nombre de un parámetro: no se toca.
    assert normaliza('## CENTROCOSTELINEAAUTO') == '## CENTROCOSTELINEAAUTO'
    # Y lo que ya estaba bien se queda como está.
    assert normaliza('## Ya estaba bien') == '## Ya estaba bien'

    # Dentro de un bloque de código no se toca nada.
    codigo = '```sql\nSELECT * FROM TABLA DE PRUEBAS\n```'
    assert normaliza(codigo) == codigo
    assert converters.demote_callout_headings('```\n## Nota\n```') == '```\n## Nota\n```'


def test_un_encabezado_que_gobierna_algo_no_se_degrada():
    con_texto = '##### Requisitos\n\nHace falta esto y lo otro.\n\n## Otra cosa'
    assert converters.demote_label_headings(con_texto) == con_texto

    padre = '##### Grupo\n\n###### Hijo\n\ntexto'
    assert converters.demote_label_headings(padre) == padre

    # Por encima de h5 no se toca nada: ahí sí hay estructura de verdad.
    seccion = '## Primeros pasos\n\n## Recomendable: reiniciar\n\nTexto.'
    assert converters.demote_label_headings(seccion) == seccion


def test_las_tablas_vacias_se_descartan():
    """
    El editor del origen deja cascarones sin nada dentro: en la página son un
    hueco en blanco.
    """
    vacia = ('<p>antes</p><table class="fr-no-borders"><tbody><tr>'
             '<td style="width: 50%"></td><td></td></tr></tbody></table><p>después</p>')
    salida, tablas = common.protect_html_tables(vacia)
    assert tablas == {}, 'la tabla vacía no se conserva'
    assert 'antes' in salida and 'después' in salida, 'lo de alrededor se respeta'

    _, solo_nbsp = common.protect_html_tables('<table><tbody><tr><td>&nbsp;</td></tr></tbody></table>')
    assert solo_nbsp == {}, 'un &nbsp; no es contenido'

    # Con contenido sí se protege, y una galería de imágenes cuenta.
    for html in ('<table><tbody><tr><td>Dato</td></tr></tbody></table>',
                 '<table><tbody><tr><td><img src="x.png"></td></tr></tbody></table>'):
        _, tablas = common.protect_html_tables(html)
        assert len(tablas) == 1, html


def test_nombres_de_fichero_seguros():
    assert common.get_safe_filename('a/b:c*d', 'fb') == 'a-b-c-d'
    assert common.get_safe_filename('   ', 'fallback') == 'fallback'
    assert common.get_safe_filename('nombre.', 'fb') == 'nombre'


def test_claves_de_busqueda_de_titulo():
    keys = common.build_article_lookup_keys('ERP - Configuración de Áreas (v.5)')
    assert 'erp configuracion de areas v 5' in keys
    assert any('configuracion de areas' in k for k in keys)


def test_url_de_imagen_se_limpia():
    sucia = 'https://x/y​.png\n'
    assert common._sanitize_image_url(sucia) == 'https://x/y.png'


def test_bug_atributos_de_editor_con_url_de_freshdesk():
    """
    El editor de Freshdesk deja en cada <img> un data-filelink con la URL
    original en S3. La imagen se descarga y el src queda local, pero esa URL se
    publicaba igual dentro del HTML de la tabla: 126 casos en docs/.
    """
    s3 = 'https://s3.amazonaws.com/cdn.freshdesk.com/data/x.png?1557'
    img = (f'<img class="fr-fic" data-fileid="204" data-filelink="{s3}" '
           f'src="../../docs_assets/images/y.png" width="50">')
    out = common.limpiar_atributos_de_freshdesk(img)
    assert 'freshdesk' not in out, out
    # Lo que sí significa algo se queda.
    assert 'src="../../docs_assets/images/y.png"' in out
    assert 'width="50"' in out
    # La clase del editor NO se queda: en el CSS del tema no existe una sola
    # regla "fr-", y en una tabla ese atributo bloquea todo el estilo de
    # Material, que va con el selector table:not([class]).
    assert 'fr-fic' not in out, out


def test_href_y_src_no_se_tocan_al_limpiar_atributos():
    """De esos dos se encargan la descarga de imágenes y la corrección de enlaces."""
    original = '<a href="https://ahora.freshdesk.com/support/solutions/articles/1-x">T</a>'
    assert common.limpiar_atributos_de_freshdesk(original) == original


def test_bug_autolink_confundido_con_etiqueta_html():
    """
    ``<https://…>`` empieza por ``<h``: con un patrón laxo de etiqueta pasaba
    por HTML, así que las reglas lo daban por intocable y se publicaba.
    """
    assert not common._HTML_TAG_RX.fullmatch('<https://ahora.freshdesk.com/x>')
    for etiqueta in ('<img src="a.png">', '<td>', '</table>', '<br/>'):
        assert common._HTML_TAG_RX.fullmatch(etiqueta), etiqueta

    destino = str(Path('docs/A/B/Otro.md').resolve())
    resuelto = _fix('- <https://ahora.freshdesk.com/support/solutions/articles/44-x>',
                    arts={'44': destino})
    # La etiqueta es el titulo del destino, no un 'Enlace Interno' generico.
    assert resuelto == '- [Otro](Otro.md)', resuelto
    # Sin destino conocido se degrada, y los ángulos se van con él.
    assert 'freshdesk' not in _fix('- <https://ahora.freshdesk.com/support/solutions/articles/99-x>')
    # Un autolink ajeno a Freshdesk no se toca.
    ajeno = '- <https://learn.microsoft.com/x>'
    assert _fix(ajeno) == ajeno


def test_bug_alt_con_salto_de_linea_impedia_la_descarga():
    """
    Con ``.*?`` el alt no podía llevar saltos, así que esas imágenes no las
    veía nadie: ni se descargaban ni se anotaban como fallidas, y se quedaban
    apuntando a S3 hasta caducar.
    """
    s3 = 'https://s3.amazonaws.com/cdn.freshdesk.com/data/x.png?1632'
    salto = chr(10)
    md = f'![Captura de pantalla{salto}{salto}Descripción generada automáticamente]({s3})'

    m = common.MD_IMAGE_RX.search(md)
    assert m, 'la descarga de imágenes no ve un alt con salto de línea'

    # Y el alt se recompone en una sola línea, o parte el propio enlace.
    alt = common.alt_util(m.group(1), m.group(2))
    assert salto not in alt
    assert alt == 'Captura de pantalla Descripción generada automáticamente'


# ---------------------------------------------------------------------------
# Énfasis y tablas anidadas
# ---------------------------------------------------------------------------

def test_bug_negrita_con_espacio_dentro_no_renderiza():
    """
    En Markdown ``** Ejemplo**`` NO es negrita: el marcador de apertura tiene
    que ir pegado al texto. Se veían los asteriscos en mitad de la página.
    Salía de HTML como <b><u>texto</u></b>, que html2text pasa a ``** _x_**``.
    """
    f = converters._sacar_espacios_del_enfasis
    assert f('** Ejemplo**') == '**Ejemplo**'
    assert f('**Ejemplo **') == '**Ejemplo**'
    assert f('** Ejemplo **') == '**Ejemplo**'
    assert f('texto ** _Recomendable_** mas') == 'texto **_Recomendable_** mas'
    assert f('__ Negrita alterna__') == '__Negrita alterna__'
    # Un cuerpo que solo son marcadores es basura de la conversión.
    assert f('** __**') == ''
    # Lo que ya está bien no se toca, ni se inventan espacios.
    assert f('**Bien** no se toca') == '**Bien** no se toca'
    assert f('**a** y **b**') == '**a** y **b**'
    assert f('***fuerte***') == '***fuerte***'
    # Un ** sin pareja es otro problema: adivinar dónde cierra sería peor.
    assert f('un ** suelto sin pareja') == 'un ** suelto sin pareja'


def test_negrita_arreglada_si_renderiza():
    from markdown import Markdown
    roto = '** Ejemplo** de uso'
    assert '<strong>' not in Markdown().convert(roto)
    arreglado = converters._sacar_espacios_del_enfasis(roto)
    assert '<strong>Ejemplo</strong>' in Markdown().convert(arreglado)


def test_bug_tabla_anidada_dejaba_el_html_sin_cerrar():
    """
    Con ``<table>.*?</table>`` una tabla dentro de otra casaba hasta el cierre
    de la INTERIOR, y el de la exterior se quedaba huérfano. El artículo
    acababa con una tabla sin cerrar y Python-Markdown dejaba de procesar
    Markdown a partir de ahí: 378 tablas descompensadas en docs/.
    """
    def balance(s):
        return (len(re.findall(r'(?i)<table[ >]', s)), len(re.findall(r'(?i)</table>', s)))

    anidada = 'A<table><tr><td><table><tr><td>i</td></tr></table></td></tr></table>B'
    resto, mapa = common.protect_html_tables(anidada)
    assert len(mapa) == 1, 'la tabla exterior debe salir entera, con la interior dentro'
    assert '<table' not in resto, resto
    recompuesto = resto
    for k, v in mapa.items():
        recompuesto = recompuesto.replace(k, v)
    assert balance(recompuesto) == (2, 2), balance(recompuesto)


def test_tablas_sueltas_y_descompensadas():
    """El origen trae tablas sin cerrar y cierres sin apertura."""
    resto, mapa = common.protect_html_tables('A<table><tr><td>x</td></tr>B')
    assert len(mapa) == 1
    assert next(iter(mapa.values())).endswith('</table>'), 'hay que cerrarla'

    # Un cierre sin apertura se descarta: dejarlo descompensa el documento.
    resto, mapa = common.protect_html_tables('A</table>B')
    assert not mapa and resto == 'AB', (resto, mapa)


def test_dos_tablas_seguidas_siguen_siendo_dos():
    resto, mapa = common.protect_html_tables(
        'A<table><tr><td>1</td></tr></table>M<table><tr><td>2</td></tr></table>B'
    )
    assert len(mapa) == 2
    assert 'M' in resto and 'A' in resto and 'B' in resto


def test_el_markdown_sobrevive_despues_de_una_tabla_anidada():
    """Lo que de verdad se rompía: todo lo que venía detrás salía en crudo."""
    from markdown import Markdown
    html = ('<p>Antes</p><table><tr><td><table><tr><td>i</td></tr></table></td></tr></table>'
            '<h3>Fichero CVS</h3><p>Texto <strong>en negrita</strong>.</p>')
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        md_file = docs / 'a' / 'b.md'
        md_file.parent.mkdir(parents=True)
        md = converters.convert_standard(html, docs, md_file, docs / 'img', 'T', '1')
    salida = Markdown().convert(md)
    assert '<strong>en negrita</strong>' in salida, salida
    assert 'Fichero CVS' in salida


# ---------------------------------------------------------------------------
# URLs que no son URLs
# ---------------------------------------------------------------------------

MONSTRUO = ('http://Modificar%20Cuotas%20Antes%20de%20continuar%20con%20el%20proceso'
            '%20de%20amortizaci%C3%B3n,%20se%20podr%C3%A1%20modificar%20el%20cuadro')


def test_bug_un_parrafo_pegado_en_el_campo_del_enlace():
    """
    Hay artículos donde alguien pegó un párrafo entero en el campo del enlace:
    queda un href de mil caracteres con la prosa del propio artículo. La regla
    de "enlace sin texto -> poner la URL como texto" lo convertía de invisible
    en un muro de 2.264 caracteres. Eran 7 artículos de amortizaciones.
    """
    assert not common.url_es_plausible(MONSTRUO)
    # Sin texto: el enlace sobra entero, no se pierde nada.
    assert _fix(f'Ver [Cuadro](x.md)[]({MONSTRUO})') == 'Ver [Cuadro](x.md)'
    # Con texto: se conserva la frase y se tira el enlace, que no lleva a nada.
    assert _fix(f'Ver [Cuadro contable]({MONSTRUO}) aqui') == 'Ver Cuadro contable aqui'


def test_un_marcador_de_posicion_no_es_una_url_rota():
    """
    ``http://servidor:puerto/api`` sale así a propósito en la documentación de
    la API. El listón tiene que dejarlo pasar.
    """
    assert common.url_es_plausible('http://servidor:puerto/AhoraAPI/api')
    original = 'Llama a [la API](http://servidor:puerto/AhoraAPI/api)'
    assert _fix(original) == original


def test_urls_normales_siguen_siendo_plausibles():
    for url in ('https://docs.flexygo.com/setup/x.zip',
                'http://videos.ahora.es/ScriptSamples#68',
                'https://192.168.1.10:8080/x',
                'https://ahora.es/a/b?c=1&d=2#e'):
        assert common.url_es_plausible(url), url
    for url in ('', 'http://', 'http://' + 'a' * 400):
        assert not common.url_es_plausible(url), url


def test_bug_freshdesk_sin_esquema_en_la_url():
    """
    El origen trae también enlaces sin esquema (``//ahora.freshdesk.com``).
    Las reglas pedían ``https?://`` y esos se colaban enteros.
    """
    out = _fix('[ahora.freshdesk.com](//ahora.freshdesk.com) en Techfun')
    # El enlace desaparece; la frase, que nombra el portal, se conserva.
    assert '](' not in out and '//' not in out, out
    assert out == 'ahora.freshdesk.com en Techfun'


def test_bug_ancla_html_vacia_con_destino_local():
    """
    Un ``<a href="x.md"></a>`` dentro de una tabla no se ve: el lector no
    tiene dónde pulsar. Las reglas de Markdown no llegan ahí, porque la tabla
    se conserva en crudo.
    """
    out = _fix('<td><a href="../../ERP/X/ERP%20-%20Crear%20nueva%20empresa.md"></a></td>')
    assert '>ERP - Crear nueva empresa</a>' in out, out

    # Externa: la propia URL como texto, igual que en Markdown.
    out = _fix('<td><a href="http://cc.ahora.es/erp/issues/15231"></a></td>')
    assert '>http://cc.ahora.es/erp/issues/15231</a>' in out, out

    # Sin destino aprovechable, el ancla sobra entera.
    assert _fix('<td><a href="#seccion"></a></td>') == '<td></td>'

    # Y una que sí tiene texto no se toca.
    original = '<td><a href="x.md">Texto</a></td>'
    assert _fix(original) == original


def test_bug_encabezado_que_empieza_por_br():
    """
    ``<h3><br>TEXTO</h3>``: el <br> inicial empuja el texto a la línea
    siguiente, el ``###`` se queda vacío y el título acaba como un párrafo.
    Se perdía por partida doble.
    """
    d = converters.drop_empty_headings
    assert d('<h3><br><strong>REQUISITOS</strong></h3>') == '<h3><strong>REQUISITOS</strong></h3>'
    # El <br> puede venir envuelto en etiquetas: mirar el borde literal no basta.
    assert d('<h3><span style="x"><br></span><strong>EJ</strong></h3>') ==         '<h3><span style="x"></span><strong>EJ</strong></h3>'
    # Vacíos de verdad, por texto visible y no por lista de etiquetas.
    assert d('<h3><br></h3>') == ''
    assert d('<h2><font>&nbsp;</font></h2>') == ''
    # Lo que tiene texto se queda igual, <br> intermedios incluidos.
    assert d('<h3>Normal</h3>') == '<h3>Normal</h3>'
    assert d('<h3>Con <br> en medio</h3>') == '<h3>Con <br> en medio</h3>'


def test_bug_encabezado_que_acaba_en_dos_puntos():
    """
    Se degradaba a párrafo cualquier encabezado terminado en "." o ":". Los dos
    puntos al final de un título son normales en castellano, y esa regla se
    llevaba 205 encabezados de sección. Sin ellos el artículo se queda sin
    tabla de contenidos y el panel derecho de MkDocs no tiene por dónde navegar.
    """
    p = converters._parece_prosa
    assert not p('Procedimiento almacenado:')
    assert not p('Crear auto numéricos:')
    assert not p('F.A.Q.')
    assert not p('Introducción')
    # Una frase de verdad sí es prosa.
    assert p('4. Asignar dicho impuesto e IVA en la ficha del cliente para que aplique bien.')
    assert p('La Cláusula OUTPUT permite retornar los registros de un update, insert o '
             'delete, y esto ya es claramente un párrafo entero.')


def test_encabezado_con_dos_puntos_llega_al_markdown():
    html = '<h2>Procedimiento almacenado:</h2><p>Texto.</p>'
    out = converters.preprocess_reference_html('T', html)
    # La sección más alta del artículo queda en h2: el h1 lo ocupa el título.
    assert '<h2>Procedimiento almacenado:</h2>' in out, out


def test_bug_marcador_entre_angulos_se_pierde_al_renderizar():
    """
    En el origen es ``&lt;identity impersonate&gt;``. html2text lo des-escapa y
    el navegador, al no conocer esa etiqueta, no pinta nada: el lector se queda
    sin saber qué subclave buscar.
    """
    out = converters._convert_with_html2text(
        '<p>Buscaremos la subclave &lt;identity impersonate&gt; y listo</p>'
    )
    assert '&lt;identity impersonate&gt;' in out, out

    esc = converters.escapar_marcadores_entre_angulos
    # Ni los autolinks ni las etiquetas de verdad se tocan.
    assert esc('<https://x.es/y>') == '<https://x.es/y>'
    assert esc('texto <b>negrita</b>') == 'texto <b>negrita</b>'
    assert esc('<td>celda</td>') == '<td>celda</td>'


def test_negritas_sueltas_pasan_a_encabezado():
    """
    Muchos artículos escriben las secciones a mano, en negrita, en vez de con
    un encabezado. MkDocs construye el panel derecho con los ##, así que esos
    artículos se quedaban sin forma de navegarse: eran 529.
    """
    pr = converters.promover_negritas_a_encabezados
    assert pr('<p><strong>1. Comprobaciones previas</strong></p>') == '<h2>1. Comprobaciones previas</h2>'
    assert pr('<p><strong><u>Modo automático:</u></strong></p>') == '<h2>Modo automático:</h2>'
    assert pr('<p><b>DESDE VERSIÓN 4.4.2100</b></p>') == '<h2>DESDE VERSIÓN 4.4.2100</h2>'


def test_no_se_promueve_lo_que_no_es_un_titulo():
    """Aquí se inventa estructura, así que el criterio tiene que ser estrecho."""
    pr = converters.promover_negritas_a_encabezados
    for html in (
        # Hay texto fuera de la negrita: es un párrafo con una parte resaltada.
        '<p><strong>Nota:</strong> esto es un párrafo normal.</p>',
        # Termina en punto: es una frase.
        '<p><strong>Esto es una frase entera en negrita.</strong></p>',
        # Demasiado largo para ser un título.
        '<p><strong>' + 'x' * 80 + '</strong></p>',
        # Sin negrita, o vacío.
        '<p>Texto normal</p>',
        '<p>&nbsp;</p>',
        # Un enlace en negrita es un enlace: si no, acababa en el índice un
        # encabezado de 200 caracteres con la URL dentro.
        '<p><strong><a href="https://learn.microsoft.com/x">Doc</a></strong></p>',
    ):
        assert pr(html) == html, html


def test_titulo_con_dos_puntos_pero_largo_es_prosa():
    """Un título con dos puntos es corto; ochenta caracteres ya es una frase."""
    p = converters._parece_prosa
    assert not p('Modo automático:')
    assert p('Todo registro presentado tiene una clave única compuesta por los siguientes campos:')


def test_bug_ancla_traducida_se_quedaba_sin_etiqueta():
    """
    La etiqueta de un ancla vacía se sacaba de la URL de Freshdesk ORIGINAL.
    La red de seguridad borraba después esa URL del texto visible y el ancla
    se quedaba vacía: un enlace que existe, apunta bien, y no se ve.
    Hay que sacarla del destino YA resuelto.
    """
    destino = str(Path('docs/A/B/ERP - Crear nueva empresa.md').resolve())
    out = common.fix_internal_links(
        '<td><a href="https://ahora.freshdesk.com/support/solutions/articles/44-erp"></a></td>',
        Path('docs/A/B/c.md'), {'44': destino}, {}, {}, [0], {},
    )
    assert '>ERP - Crear nueva empresa</a>' in out, out
    assert not re.search(r'<a[^>]*>\s*</a>', out), out
    assert 'freshdesk' not in out, out


def test_bug_negrita_vacia_partida_por_un_salto():
    """
    El origen parte la negrita vacia con un salto duro, dejando el marcador
    de apertura en una linea y el de cierre en la siguiente. Exigiendolos en
    la misma linea quedaban 301 lineas sueltas con un "**" a la vista.
    """
    limpia = converters._clean_freshdesk_artifacts
    assert '**' not in limpia('Texto\n\n**  \n**\n\nMas texto')
    assert '**' not in limpia('a **** b')
    # Una negrita de verdad, aunque ocupe dos lineas, no se toca.
    assert limpia('**Importante**') == '**Importante**'
    intacta = '**Titulo\ncontinuado**'
    assert limpia(intacta) == intacta


def _niveles(out):
    return [f'h{a}' for a, _ in re.findall(r'<h([1-6])[^>]*>(.*?)</h\1>', out)]


def test_bug_secciones_en_h4_invisibles_en_el_panel():
    """
    Hay articulos que escriben todas sus secciones en <h4>. Con toc_depth: 3
    esos titulos no aparecen en el panel derecho: el articulo tiene estructura
    y no se puede navegar.
    """
    out = converters.preprocess_reference_html('T', '<h4>Token (JWT)</h4><h4>Procedimientos</h4>')
    assert _niveles(out) == ['h2', 'h2'], out


def test_la_jerarquia_relativa_se_conserva():
    """
    El desplazamiento iba en dos pasos —un h2 → h3 fijo y luego el ajuste— y
    aplastaba la jerarquia: un articulo con h2 y h3 acababa con las dos
    secciones al mismo nivel.
    """
    pre = converters.preprocess_reference_html
    assert _niveles(pre('T', '<h2>Uno</h2><h3>Uno.uno</h3>')) == ['h2', 'h3']
    assert _niveles(pre('T', '<h1>Uno</h1><h2>Uno.uno</h2>')) == ['h2', 'h3']
    assert _niveles(pre('T', '<h4>Padre</h4><h5>Hijo</h5>')) == ['h2', 'h3']


def test_la_autoria_no_sube_al_indice():
    """Los creditos son h5/h6 a proposito y no pintan nada en la navegacion."""
    pre = converters.preprocess_reference_html
    assert _niveles(pre('T', '<h5>Autor: Pablo Pellicer</h5>')) == ['h5']
    assert _niveles(pre('T', '<h4>Seccion</h4><h5>Autor: Pablo</h5>')) == ['h2', 'h5']


def test_los_niveles_no_dejan_huecos():
    """
    Antes se desplazaba el conjunto en bloque: eso corrige el arranque pero
    deja intactos los huecos de en medio. Eran 131 saltos —del titulo a un h3,
    de un h2 a un h4— que descuadran la tabla de contenidos.

    Ahora se renumera con una pila: cada encabezado se cuelga del ultimo de
    nivel superior, asi que la jerarquia relativa se conserva y lo unico que
    desaparece son los niveles vacios.
    """
    pre = converters.preprocess_reference_html
    # Del titulo directo a un h3: 91 casos, los mas comunes.
    assert _niveles(pre('T', '<h3>A</h3><h3>B</h3>')) == ['h2', 'h2']
    # De un h2 a un h4 y vuelta: 27 casos.
    assert _niveles(pre('T', '<h2>A</h2><h4>B</h4><h4>C</h4><h2>D</h2>')) == [
        'h2', 'h3', 'h3', 'h2']
    # Del titulo a un h4: 13 casos.
    assert _niveles(pre('T', '<h4>A</h4><h5>B</h5>')) == ['h2', 'h3']
    # Lo que ya estaba bien no se toca.
    assert _niveles(pre('T', '<h2>A</h2><h3>B</h3><h3>C</h3><h2>D</h2>')) == [
        'h2', 'h3', 'h3', 'h2']
    # Bajar y volver a subir: los hermanos siguen siendo hermanos.
    assert _niveles(pre('T', '<h2>A</h2><h4>B</h4><h6>C</h6><h4>D</h4><h2>E</h2>')) == [
        'h2', 'h3', 'h4', 'h3', 'h2']
    # Y no se pasa de h6.
    assert _niveles(pre(
        'T', '<h1>A</h1><h2>B</h2><h3>C</h3><h4>D</h4><h5>E</h5><h6>F</h6>')) == [
        'h2', 'h3', 'h4', 'h5', 'h6', 'h6']


def test_bug_la_autoria_no_descoloca_la_pila():
    """
    Un credito por el medio no puede hacer que la seccion siguiente cuelgue de
    el: queda fuera de la lista, asi que la pila ni lo ve.
    """
    pre = converters.preprocess_reference_html
    assert _niveles(pre('T', '<h2>A</h2><h5>Autor: Daniel</h5><h4>B</h4>')) == [
        'h2', 'h5', 'h3']


def test_bug_el_guardian_de_etiquetas_mira_todos_los_niveles():
    """
    El HTML de "ERP - Parametros de la aplicacion" abre con un <h1>, asi que
    su nivel mas alto NO es el de las 604 etiquetas. Mirando solo el mas alto
    el guardian no saltaba y las etiquetas subian igual a h3.
    """
    pre = converters.preprocess_reference_html
    muchos = ''.join('<h5>Tipo Valor: BOOL %d</h5>' % i for i in range(40))
    assert set(_niveles(pre('T', '<h1>Titulo</h1>' + muchos))) == {'h1', 'h5'}


def test_no_se_suben_cientos_de_etiquetas_de_datos():
    """
    Un articulo con cientos de encabezados al mismo nivel no esta dividido en
    secciones: los usa como etiquetas. Subirlos llenaba el panel derecho con
    1.809 entradas del tipo "Tipo Valor: BOOL Valor por defecto: OFF".
    """
    pre = converters.preprocess_reference_html
    muchos = ''.join('<h5>Tipo Valor: BOOL %d</h5>' % i for i in range(40))
    assert set(_niveles(pre('T', muchos))) == {'h5'}
    # Con pocas si se sube: son secciones de verdad.
    pocas = ''.join('<h5>Seccion %d</h5>' % i for i in range(5))
    assert set(_niveles(pre('T', pocas))) == {'h2'}


def test_bug_apartado_convertido_en_bloque_de_codigo():
    """
    "B.- Pago parcial del efecto" encajaba en el patron de acceso a miembro de
    VB (identificador + punto) y el titulo acababa dentro de un fence vbnet.
    """
    rep = converters.repair_vb_reference_markdown
    for texto in ('B.- Pago parcialmente el efecto. Dejando pendiente una parte.',
                  'C.- Pagar el efecto por un importe inferior al real.',
                  'D..-Pagar el efecto y unos gastos adicionales.'):
        assert '```' not in rep(texto), rep(texto)
    # El VB de verdad se sigue detectando.
    codigo = 'gForm.Controls("Botonera").Visible = True\ngForm.Refresh'
    assert '```' in rep(codigo)


def test_bug_br_con_atributos_no_se_reconocia():
    """
    El origen escribe <br data-identifyelement="571">. Todas las reglas del
    conversor usaban un patron `<br\\s*/?>` que no ve los atributos, asi que
    el 30% de los <br> (19.725 en 680 articulos) se escapaba: encabezados que
    se quedaban vacios y saltos de linea perdidos DENTRO del codigo.
    """
    d = converters.drop_empty_headings
    esperado = '<h2><strong>Instalacion</strong></h2>'
    assert d('<h2><br data-x="1"><strong>Instalacion</strong></h2>') == esperado
    assert d('<h3><br data-y="2"></h3>') == ''
    # Y el <br> pelado sigue funcionando igual.
    assert d('<h3><br></h3>') == ''

    # Dentro del codigo, un <br> con atributos es un salto de linea.
    out = converters._convert_with_html2text(
        '<pre>Dim a<br data-z="3">Set a = 1<br>End Sub</pre>'
    )
    assert out.count('\n') >= 4, out
    assert 'Dim a' in out and 'End Sub' in out


def test_enfasis_redundante_en_encabezados():
    """
    "## **Token (JWT)**" se renderiza como un h2 con un <strong> dentro:
    redundante, porque el encabezado ya destaca. Eran el 20% de todos.
    """
    f = converters._quitar_enfasis_de_encabezados
    assert f('## **Token (JWT)**') == '## Token (JWT)'
    assert f('### **_Requisitos previos_**') == '### Requisitos previos'
    assert f('## _Cursiva_') == '## Cursiva'


def test_el_enfasis_parcial_de_un_encabezado_se_respeta():
    """Solo se quita cuando abarca TODO el texto del encabezado."""
    f = converters._quitar_enfasis_de_encabezados
    for texto in ('## Normal', '## **a** y **b**',
                  '## Texto con **parte** resaltada', 'texto normal **negrita**'):
        assert f(texto) == texto, texto


def test_bug_un_encabezado_no_cortaba_la_racha_de_codigo():
    """
    Las alternativas de _MD_PROSE_LINE_RX estaban ancladas con el fin de
    linea, asi que el patron de encabezado solo casaba un "###" VACIO: uno
    con texto nunca cortaba la racha y acababa dentro del bloque de codigo.
    Lo mismo con las viñetas.
    """
    RX = converters._MD_PROSE_LINE_RX
    assert RX.match('### **Utilizacion de Memoria**')
    assert RX.match('## Titulo normal')
    assert RX.match('- una viñeta con texto')
    # Una linea de SQL no corta nada: es justo lo que se quiere agrupar.
    assert not RX.match('SELECT * FROM T')

    entrada = 'EXEC sp_configure\n\n### Utilizacion de Memoria\n\nEs conveniente ajustar.'
    out = converters._extract_loose_sql_blocks(entrada)
    bloques = re.findall(r'(?s)```\w*\n(.*?)```', out)
    assert not [b for b in bloques if 'Utilizacion' in b], out


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# Enlaces a Freshdesk dentro del HTML crudo
# ---------------------------------------------------------------------------

def _fix(md, arts=None, folders=None, cats=None):
    return common.fix_internal_links(
        md, Path('docs/A/B/c.md'), arts or {}, {}, folders or {}, [0], cats or {},
    )


def test_bug_borrar_url_suelta_rompia_el_html():
    """
    Las tablas se conservan como HTML crudo. La regla que borraba URLs sueltas
    de Freshdesk entraba también dentro de href="..." y se llevaba la comilla
    de cierre, dejando ``<a href=" rel="noopener">``. Había 49 así en docs/.
    """
    for url in (
        'https://ahora.freshdesk.com/a/solutions/categories/44',
        'https://ahora.freshdesk.com/support/solutions/articles/123-x',
    ):
        out = _fix(f'<td><a href="{url}" rel="noopener">Texto</a></td>')
        assert 'href=" ' not in out and 'href=""' not in out, out
        assert 'Texto' in out, 'se ha perdido el texto del enlace'


def test_ancla_html_se_traduce_si_conocemos_el_destino():
    destino = str(Path('docs/A/B/Otro.md').resolve())
    out = _fix('<td><a href="https://ahora.freshdesk.com/support/solutions/articles/123-x">T</a></td>',
               arts={'123': destino})
    assert '<a href="Otro.md">T</a>' in out, out


def test_ancla_html_sin_destino_se_queda_en_texto():
    """Un enlace que pide login de agente no le sirve a nadie; la frase sí."""
    out = _fix('<td><a href="https://ahora.freshdesk.com/a/tickets/9">Ticket 9</a></td>')
    assert out == '<td>Ticket 9</td>', out


def test_ancla_ajena_a_freshdesk_no_se_toca():
    original = '<td><a href="https://learn.microsoft.com/x" rel="noopener">MS</a></td>'
    assert _fix(original) == original


def test_red_de_seguridad_para_formas_no_previstas():
    """Una URL de Freshdesk con una forma nueva se degrada, no se publica."""
    out = _fix('Mira [esto](https://ahora.freshdesk.com/algo/nuevo/999) por favor')
    assert 'freshdesk' not in out, out
    assert 'Mira esto por favor' in out, out


def test_categoria_desconocida_se_degrada():
    """Antes se quedaba apuntando a Freshdesk por no estar en category_paths."""
    out = _fix('Ver [la guía](https://ahora.freshdesk.com/support/solutions/44000675746)')
    assert 'freshdesk' not in out, out
    assert 'la guía' in out


def test_contador_de_enlaces_freshdesk():
    formas = common.contar_enlaces_freshdesk(
        'a https://x.freshdesk.com/a/tickets/1 b https://x.freshdesk.com/support/solutions/2'
    )
    assert formas['/a/tickets/'] == 1
    assert formas['/support/solutions/ (categoría)'] == 1
    assert not common.contar_enlaces_freshdesk('sin enlaces')


# ---------------------------------------------------------------------------
# Texto alternativo de las imágenes
# ---------------------------------------------------------------------------

def test_bug_alt_de_imagen_con_la_url_de_origen():
    """
    Al descargar la imagen la ruta cambia, pero el alt conservaba la URL de S3:
    un lector de pantalla leía la URL entera y cualquier grep la encontraba.
    """
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        md_file = docs / 'a.md'
        md_file.parent.mkdir(parents=True)
        url = 'https://s3.amazonaws.com/cdn.freshdesk.com/x/y.png'
        # Sin red: la descarga falla y el enlace se queda igual, pero el alt
        # ya no se propaga a la salida cuando sí se descarga.
        assert common.alt_util(url, url) == ''
        assert common.alt_util('Pantalla de inicio', url) == 'Pantalla de inicio'
        assert common.alt_util('', url) == ''


# ---------------------------------------------------------------------------
# Huella del pipeline
# ---------------------------------------------------------------------------

def test_huella_del_pipeline_detecta_cambios_de_codigo():
    """
    El estado solo miraba el updated_at del artículo, así que un arreglo del
    conversor no alcanzaba a lo ya generado. La huella cierra ese agujero.
    """
    huella = generation_state.calcular_huella_pipeline()
    assert huella and len(huella) == 16
    assert generation_state.calcular_huella_pipeline() == huella, 'no es estable'

    estado = {'meta': {'pipeline_fingerprint': huella}, 'articles': {'1': {}}}
    assert not generation_state.pipeline_ha_cambiado(estado, huella)
    assert generation_state.pipeline_ha_cambiado(estado, 'otra')

    # Un estado antiguo, sin huella, cuenta como cambio: no se sabe con qué
    # código se generó.
    assert generation_state.pipeline_ha_cambiado({'meta': {}, 'articles': {'1': {}}}, huella)
    # Un estado vacío no fuerza nada: no hay nada generado que invalidar.
    assert not generation_state.pipeline_ha_cambiado({'meta': {}, 'articles': {}}, huella)


def test_la_huella_se_guarda_al_consolidar():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        rs = generation_state.RunState(out)
        rs.record('1', title='A', product='', category_id='', category_name='',
                  folder_id='', folder_name='', path='a.md', source_updated_at='')
        generation_state.finalize_generation_state(out, rs, pipeline_fingerprint='abc123')
        estado = generation_state.load_generation_state(out)
        assert estado['meta']['pipeline_fingerprint'] == 'abc123'


def test_la_red_de_seguridad_respeta_las_imagenes():
    """
    Una imagen que no se pudo descargar sigue apuntando al servidor remoto.
    Degradarla la borraría: una imagen remota se ve, una borrada no. Y el
    ``]`` de cierre tampoco se puede comer, o se rompe la sintaxis.
    """
    s3 = 'https://s3.amazonaws.com/cdn.freshdesk.com/data/x.png?157'
    assert _fix(f'![foto]({s3})') == f'![foto]({s3})'
    assert _fix(f'![]({s3})') == f'![]({s3})'
    # En cambio el alt que solo repite la URL sobra, y la imagen local se queda.
    assert _fix(f'![{s3}](../img/y.png)') == '![](../img/y.png)'


def test_bug_encabezado_con_solo_una_imagen_borraba_la_captura():
    """
    El origen envuelve cada captura en su propio <h2><img></h2>. Como no hay
    texto visible, drop_empty_headings las daba por vacias y borraba la
    imagen con el encabezado: 19 capturas perdidas solo en "Importador de
    ficheros TXT", 43 en todo el corpus. Si hay imagen, se desenvuelve.
    """
    out = converters.drop_empty_headings('<h2><img src="a.png"></h2>')
    assert 'a.png' in out, out
    assert '<h2' not in out, out
    # Un encabezado de verdad vacio sigue desapareciendo.
    assert converters.drop_empty_headings('<h2> <br/> </h2>').strip() == ''


def test_bug_anclas_vacias_repetidas_duplicaban_el_enlace():
    """
    El origen deja varias <a> vacias al mismo articulo que ya esta enlazado
    con texto. Etiquetarlas todas producia el mismo enlace repetido cuatro
    veces seguidas. Si el destino ya se ve enlazado, la vacia sobra.
    """
    destino = str(Path('docs/A/B/ERP - Crear nueva empresa.md').resolve())
    url = 'https://ahora.freshdesk.com/support/solutions/articles/44-erp'
    # La basura va ANTES del enlace bueno: por eso se mira el documento entero
    # antes de sustituir nada.
    md = f'<a href="{url}"></a><a href="{url}"></a>\n[Crear empresa]({url})'
    out = common.fix_internal_links(
        md, Path('docs/A/B/c.md'), {'44': destino}, {}, {}, [0], {},
    )
    assert out.count('ERP - Crear nueva empresa') == 0, out
    assert out.count('Crear empresa') == 1, out
    assert not re.search(r'<a[^>]*>\s*</a>', out), out


def test_pie_de_figura_no_es_codigo():
    """
    "_Fig.8 Insertar un articulo_" acababa dentro de un ```vbnet: la regla de
    acceso a miembro veia "Fig.8" como "objeto.propiedad". Se exige una LETRA
    tras el punto.
    """
    assert converters.detect_code_lang('Fig.8 Insertar un articulo con propiedades') == ''
    assert converters.detect_code_lang('B.- Pago de la factura') == ''
    assert converters.detect_code_lang('gForm.Controls("x").TabIndex = 0') == converters.VB_LANG


def test_vb6_suelto_se_reconoce():
    """
    El bloque de VB6 de "Tabulacion de Controles" salia sin lenguaje: eran
    asignaciones sobre colecciones indexadas y comentarios con comilla, que
    el patron laxo no contemplaba.
    """
    codigo = (
        "' Orden de tabulacion\n"
        'gForm.Controls("txtNombre").TabIndex = 0\n'
        'gForm.Controls("txtApellido").TabIndex = 1\n'
    )
    assert converters.detect_code_lang(codigo) == converters.VB_LANG


def test_marcador_de_negrita_huerfano_se_borra():
    """
    Un "**" solo en su linea, sin pareja, quedaba impreso. Se borra la linea
    entera, pero sin fusionar dos negritas contiguas legitimas.
    """
    limpia = converters._clean_freshdesk_artifacts
    assert '**' not in limpia('Texto\n\n**\n\nMas texto')
    # Dos negritas seguidas siguen siendo dos.
    assert limpia('**uno**\n\n**dos**').count('**') == 4


def test_etiquetas_de_codigo_tambien_pasan_a_seccion():
    """
    En el mismo articulo, "Codigo VB6:" salia como encabezado y
    "**Codigo C#:**" como negrita suelta. Eran 51 articulos con esa
    incoherencia, y el ejemplo de C# no se podia alcanzar desde el panel.
    """
    f = converters._etiquetas_de_referencia_a_encabezados
    assert f('<p><strong>Código C#:</strong></p>') == '<h2>Código C#</h2>'
    assert f('<p><strong>Código en C#:</strong></p>') == '<h2>Código en C#</h2>'
    assert f('<p>Ejemplo:</p>') == '<h2>Ejemplo</h2>'
    # Una frase larga que empieza por "Código" no es una etiqueta.
    for html in ('<p>El código C# de este ejemplo:</p>',
                 '<p>Código fuente completo del formulario:</p>'):
        assert f(html) == html, html


def test_acceso_con_punto_inicial_es_vb():
    """
    Dentro de un bloque With, VB accede a los miembros con punto inicial
    (".Coleccion = ..."). Los patrones exigian una letra al principio, asi
    que el bloque de "Formulario de mantenimiento con Coleccion" se quedaba
    sin lenguaje y salia en gris.
    """
    d = converters.detect_code_lang
    assert d('.EditarPorObjeto = True') == converters.VB_LANG
    assert d('Set .Coleccion = gcn.Obj.dameColeccion ("Articulos")') == converters.VB_LANG
    assert d('.campo ("IdArticulo").Coleccion = "Articulos"') == converters.VB_LANG
    # Prosa que empieza por punto o lleva un punto por medio, no.
    assert d('.NET Framework 4.8 = requisito') == ''
    assert d('Ver el apartado 3. Configuracion = importante') == ''


def test_etiqueta_suelta_en_markdown_pasa_a_seccion():
    """
    No todas las etiquetas llegan en un <p> limpio: algunas cuelgan de un
    <div> o llevan un <br> dentro de la negrita, y la regla del HTML no las
    alcanza. Quedaban 13 repartidas por el corpus.
    """
    f = converters._etiquetas_sueltas_a_encabezados
    assert '## Código VB6' in f('Devuelve un valor.  \n  \n**Código VB6:**\n\ntexto')
    assert '## Parámetros' in f('Agrega un item.  \n  \nParámetros:\n\n- aId')


def test_etiqueta_a_media_frase_no_parte_el_parrafo():
    """
    Hay articulos donde "parámetros:" es la segunda linea de un bloque que
    empieza con el nombre del procedimiento. Ahi no es una seccion, es parte
    de la frase: promoverla partiria el parrafo por la mitad.
    """
    f = converters._etiquetas_sueltas_a_encabezados
    for md in ('zInsertaCampoTabla\nparámetros:\n\ntexto',
               'Fin.\n\nCódigo fuente completo del formulario:\n\ntexto',
               'Fin.\n\nDescripción de la tabla:\n\ntexto'):
        assert f(md) == md, md


def test_parrafo_dentro_de_fence_se_desenvuelve():
    """
    El origen usa <pre> como caja de aviso, asi que los "NOTA:" y los
    parrafos explicativos acaban en un fence. En Material un fence no hace
    wrap: salen en gris y con barra de scroll horizontal. Eran 74 bloques.
    """
    f = converters.desenvolver_fences_de_prosa
    md = ('```\nImportante: la ventana de peticion de datos de usuario de la '
          'API traslada el usuario a la subcuenta generada para el ticket.\n```')
    assert '```' not in f(md), f(md)
    assert 'Importante:' in f(md)


def test_prosa_etiquetada_como_codigo_tambien_se_desenvuelve():
    """
    Seis parrafos en castellano salian con resaltado de sintaxis de VB, que
    es peor todavia que dejarlos en gris. Por eso la regla mira todos los
    fences, no solo los que no llevan lenguaje.
    """
    md = ('```vbnet\n"Carga" es un metodo comun a todos los IForm de la '
          'aplicacion y por tanto debe ser declarado explicitamente.\n```')
    assert '```' not in converters.desenvolver_fences_de_prosa(md)


def test_el_codigo_no_se_desenvuelve():
    """
    Desenvolver codigo por error seria peor que dejar un aviso en gris, asi
    que el criterio es estrecho: nada que huela a sintaxis, doce palabras
    minimo, y mayoria en minuscula.
    """
    f = converters.desenvolver_fences_de_prosa
    for md in (
        '```vbnet\nSub Main()\n  Dim x As String\nEnd Sub\n```',
        # Seis palabras y casi todas en mayusculas: no es prosa.
        '```\nGRANT IMPERSONATE ANY LOGIN TO AhoraServicio\n```',
        # Indentado: es codigo formateado, no un parrafo.
        '```\n    una linea larga de texto indentado que ocupa bastante y '
        'tiene mas de doce palabras sueltas\n```',
    ):
        assert f(md) == md, md


def test_verbos_sql_que_faltaban():
    """
    T-SQL admite "DELETE tabla FROM ...", sin FROM pegado, y GRANT/DENY
    faltaban del todo: los permisos de AHORA SSO salian sin lenguaje.
    """
    d = converters.detect_code_lang
    assert d('GRANT IMPERSONATE ANY LOGIN TO AhoraServicio') == 'sql'
    assert d('DELETE Conf_Facturas_Lineas   FROM Deleted, Conf_Facturas') == 'sql'


def test_aviso_en_negrita_pasa_a_admonition():
    """
    El origen marca los avisos poniendo la palabra en negrita en su propio
    parrafo. Promoverlos a "##" llenaria el panel derecho de entradas
    "NOTA, NOTA, Aviso" que no sirven para navegar; una admonition dice lo
    mismo, sale como caja de color y no entra en el indice.
    """
    f = converters.avisos_a_admonitions
    out = f('texto\n\n**NOTA:**\n\nEste parametro afecta a todas las empresas.\n\notro\n')
    assert '!!! note "NOTA"' in out, out
    assert '    Este parametro afecta' in out, out
    # El titulo conserva la palabra del autor: "Recuerda" dice mas que "Tip".
    assert '!!! tip "Recuerda"' in f('a\n\n**Recuerda**\n\nGuarda los cambios.\n\nb\n')
    assert '!!! warning "Importante"' in f('a\n\n**Importante**\n\nNo cierres la ventana.\n\nb\n')


def test_aviso_con_lista_entra_en_la_caja():
    """
    Una lista si cabe en el cuerpo: se indenta entera. El limite esta bien
    definido —la primera linea en blanco que NO va seguida de mas lista—, asi
    que no hay que suponer nada. Eran 27 avisos que se quedaban en negrita.
    """
    f = converters.avisos_a_admonitions
    out = f('texto\n\n**NOTA:**\n\n- primer punto\n- segundo punto\n\notro\n')
    assert '!!! note "NOTA"' in out, out
    assert '    - primer punto' in out and '    - segundo punto' in out, out
    # "otro" es el parrafo siguiente, no parte del aviso.
    assert '\notro' in out, out
    # Una lista con hueco por medio sigue siendo la misma lista.
    out = f('t\n\n**NOTA:**\n\n- uno\n\n- dos\n\nfin\n')
    assert '    - uno' in out and '    - dos' in out, out
    # Numerada tambien.
    assert '    1. Primero' in f('t\n\n**Ejemplos**\n\n1. Primero\n2. Segundo\n\nfin\n')


def test_lo_que_no_es_cuerpo_de_aviso():
    """
    Un encabezado detras del aviso es la seccion siguiente, no su texto: son
    88 casos con la forma "**Ejemplo:**" + "## Codigo VB6". Una tabla en
    crudo NO cabe en la caja —comprobado con la configuracion real: indentada
    dentro de una admonition, Python-Markdown la deja como <p><table>, que es
    HTML invalido—. Y sin nada detras no hay caja que montar.
    """
    f = converters.avisos_a_admonitions
    for md in ('t' + chr(10)*2 + '**Ejemplo:**' + chr(10)*2 + '## Codigo VB6' + chr(10)*2 + 'cosas' + chr(10),
               't' + chr(10)*2 + '**Ejemplo:**' + chr(10)*2 + '<table><tr><td>x</td></tr></table>' + chr(10)*2 + 'fin' + chr(10),
               't' + chr(10)*2 + '**Ejemplo:**' + chr(10)):
        assert '!!!' not in f(md), md


def test_un_bloque_de_codigo_o_una_imagen_SI_caben_en_la_caja():
    """
    Comprobado con la configuracion real del tema: el fence indentado dentro
    de una admonition sale con su resaltado, y la imagen se ve. Eran los
    avisos que quedaban con un "**Ejemplo**" suelto y su bloque justo debajo.
    """
    f = converters.avisos_a_admonitions
    nl = chr(10); c3 = chr(96) * 3
    out = f('a' + nl*2 + '**Ejemplo**' + nl*2 + c3 + 'vbnet' + nl + 'Sub X()' + nl + 'End Sub' + nl + c3 + nl*2 + 'fin')
    assert '!!! example "Ejemplo"' in out, out
    assert '    ' + c3 + 'vbnet' in out and '    End Sub' in out, out
    out = f('a' + nl*2 + '**Ejemplo**' + nl*2 + '![](../img/foto.png)' + nl*2 + 'fin')
    assert '    ![](../img/foto.png)' in out, out


def test_un_fence_sin_cerrar_no_arrastra_el_articulo():
    """
    Si el bloque no estuviera cerrado, tomarlo como cuerpo metera el resto
    del articulo dentro de la caja. Mejor dejarlo como esta.
    """
    nl = chr(10); c3 = chr(96) * 3
    md = 'a' + nl*2 + '**Ejemplo**' + nl*2 + c3 + 'vbnet' + nl + 'Sub X()' + nl
    assert '!!!' not in converters.avisos_a_admonitions(md)


def test_negrita_suelta_en_markdown_pasa_a_seccion():
    """
    promover_negritas_a_encabezados() hace esto sobre el HTML, pero solo
    alcanza las que vienen en un <p> limpio. Las que cuelgan de un <div> o
    llevan un <br> dentro llegaban hasta aqui sin tocar.
    """
    f = converters.promover_negritas_sueltas
    assert '## MetodoRedondeo TBAI' in f('a\n\n**MetodoRedondeo TBAI**\n\nb\n\nc\n')
    # Las palabras de aviso las coge la regla de admonitions, no esta.
    assert f('a\n\n**NOTA:**\n\nb\n\nc\n') == 'a\n\n**NOTA:**\n\nb\n\nc\n'


def test_negrita_que_no_es_una_seccion():
    """
    Mismo criterio que la regla del lado HTML: un parrafo que es un enlace en
    negrita es un enlace, y una frase acabada en punto es una frase.
    """
    f = converters.promover_negritas_sueltas
    for md in ('a\n\n**Procedimiento de gestion de facturas rectificativas.**\n\nb\n\nc\n',
               'a\n\n**[Techfun - Buscador](../Buscador/Techfun.md)**\n\nb\n\nc\n',
               'a\n\n**' + 'x' * 80 + '**\n\nb\n\nc\n'):
        assert f(md) == md, md


def test_enfasis_anidado_en_encabezado_se_pela():
    """
    El enfasis venia anidado y con marcadores huerfanos pegados detras. Una
    sola pasada de regex no llegaba, y quedaban 67 encabezados con "**" a la
    vista. El caso que lo delataba llevaba ademas un "_" DENTRO del texto
    (Ahora_Impresion), que hacia fallar cualquier patron que prohibiera el
    marcador por medio.
    """
    f = converters._pelar_enfasis
    assert f('**Token (JWT)**') == 'Token (JWT)'
    assert f('_**Agregar una plataforma**_') == 'Agregar una plataforma'
    assert (f('**_Plataforma externa B2BRouter: configuración._**__')
            == 'Plataforma externa B2BRouter: configuración.')
    # Un marcador de apertura sin cierre tambien se imprime tal cual.
    assert f('**Módulo eFactura:') == 'Módulo eFactura:'


def test_enfasis_parcial_en_encabezado_se_conserva():
    """
    Un encabezado con una parte resaltada conserva su marcado: solo se pela
    el enfasis que abarca TODO el texto.
    """
    f = converters._pelar_enfasis
    for t in ('Configuración **avanzada** del ERP',
              '_Configuración de_ **_ERP_**',
              '**a** y **b**',
              'Ahora_Impresion normal'):
        assert f(t) == t, t


def test_encabezado_no_se_queda_vacio():
    """
    Si al pelar no queda nada, se deja la linea como estaba: mejor un "**"
    a la vista que un encabezado sin texto, que rompe el panel derecho.
    """
    assert converters._quitar_enfasis_de_encabezados('## ****') == '## ****'


def test_los_avisos_se_convierten_DESPUES_de_degradar():
    """
    Este es el orden que costo tres regeneraciones enteras.

    ``demote_callout_headings`` pasa a negrita los encabezados que solo dicen
    "Nota" o "Ejemplo" —y con razon: no son secciones—. Al enganchar la
    conversion a admonitions ANTES de ese paso, cada ejecución promovia y
    degradaba, y a la salida no llegaba ni una caja: 3 admonitions en 1.501
    articulos, y las 3 venian ya en el origen.

    La regla tiene que ir DETRAS del degradado, que es donde nace la negrita
    que se quiere convertir.
    """
    md = 'texto\n\n## Nota\n\nEste parametro afecta a todas las empresas.\n\nfin\n'
    # Orden correcto: degradar y luego convertir.
    bien = converters._outside_fences(
        converters.demote_callout_headings(md), converters.avisos_a_admonitions,
    )
    assert '!!! note "Nota"' in bien, bien
    # Orden equivocado: el degradado se come la promocion y no queda caja.
    mal = converters.demote_callout_headings(
        converters._outside_fences(md, converters.avisos_a_admonitions),
    )
    assert '!!!' not in mal, mal


def test_una_sola_lista_de_palabras_de_aviso():
    """
    Las dos reglas se peleaban por el mismo texto si cada una llevaba su
    lista. La fuente de verdad es CALLOUT_WORDS, la que ya usaba
    demote_callout_headings.
    """
    # Toda palabra de aviso tiene un tipo de caja, aunque sea el de por defecto.
    for palabra in converters.CALLOUT_WORDS:
        md = f'a\n\n**{palabra}**\n\nUn texto de aviso suficientemente largo.\n\nb\n'
        assert '!!! ' in converters.avisos_a_admonitions(md), palabra
    # Y la regla de secciones no toca ninguna de ellas.
    for palabra in converters.CALLOUT_WORDS:
        md = f'a\n\n**{palabra}**\n\nb\n\nc\n'
        assert converters.promover_negritas_sueltas(md) == md, palabra


def test_etiquetas_de_referencia_sobreviven_al_degradado():
    """
    "Código C#:" y "Descripción:" no son avisos: siguen siendo secciones al
    final de la cadena. "Ejemplo:" si lo es, y acaba en caja.
    """
    md = ('t\n\n**Código C#:**\n\ncodigo\n\n**Descripción:**\n\ntexto\n\n'
          '**Ejemplo:**\n\nUn ejemplo con texto de sobra para la caja.\n\nfin\n')
    out = converters._outside_fences(md, converters._etiquetas_sueltas_a_encabezados)
    out = converters.demote_callout_headings(converters.demote_label_headings(out))
    out = converters._outside_fences(out, converters.avisos_a_admonitions)
    assert '## Código C#' in out, out
    assert '## Descripción' in out, out
    assert '!!! example "Ejemplo"' in out, out


def test_enlace_a_un_host_se_queda_en_texto():
    """
    El editor de Freshdesk enlaza lo que le parece un dominio. En OAUTH2 lo
    que hay es el valor de un parametro —SERVIDOR_CORREO =
    smtp.office365.com:587— y publicado quedaba un enlace muerto a un
    servidor de correo.
    """
    f = converters.quitar_enlaces_a_un_host
    assert f('[smtp.office365.com:587](//smtp.office365.com:587)') == 'smtp.office365.com:587'
    assert f('[ahora.es](//ahora.es/)') == 'ahora.es'
    # Un enlace con ruta si va a una pagina: no se toca.
    for md in ('[doc](//ahora.es/manual/index.html)',
               '[doc](https://ahora.es)',
               '[doc](../otro%20articulo.md)',
               '![img](//cdn.ahora.es)'):
        assert f(md) == md, md


def test_encabezado_marcado_por_word_se_recupera():
    """
    Word nombra los destinos de su propio indice con "_Toc": si un texto
    lleva un <a name="_TocNNNNNN">, en el documento original era un
    encabezado. Al pegarlo en Freshdesk se pierde el <h2> y queda un <p> con
    el color del estilo.

    Es la senal mas fiable del corpus —no hay que deducir nada del texto— y
    sin ella "ERP - Compras - Ofertas" se publicaba con el panel derecho
    vacio aunque tuviera sus cuatro secciones a la vista. Son 77 en 15
    articulos, 13 de los cuales no tenian ni un encabezado.
    """
    f = converters._encabezados_de_word
    html = ('<p><a name="_Toc532416839">'
            '<span style="color: rgb(44, 130, 201);">Barra de menús</span></a></p>')
    assert f(html) == '<h2>Barra de menús</h2>', f(html)
    # Un salto de linea dentro del texto se colapsa.
    html = '<p><a name="_Toc1">Ejecutar scripts\ntras la actualización</a></p>'
    assert f(html) == '<h2>Ejecutar scripts tras la actualización</h2>', f(html)


def test_entrada_del_indice_de_word_no_es_un_encabezado():
    """
    Las entradas del indice apuntan al marcador con href="#_Toc...", no lo
    definen con name=. Promoverlas duplicaria cada seccion en el panel.
    """
    f = converters._encabezados_de_word
    for html in ('<p><a href="#_Toc532416839">Barra de menús</a></p>',
                 # Un parrafo con mas cosas dentro tampoco es un encabezado.
                 '<p><a name="_Toc1">Titulo</a> y ademas texto corrido</p>'):
        assert f(html) == html, html


def test_caja_de_aviso_hecha_con_reglas():
    """
    El origen dibuja el recuadro con una regla horizontal arriba y otra
    abajo, y mete la palabra y el texto en la MISMA linea, asi que la regla
    de avisos normal no las ve. Publicado quedaban dos separadores y una
    negrita suelta en medio. Son 65 en el corpus.
    """
    f = converters.avisos_entre_reglas_a_admonitions
    out = f('texto\n\n---\n\n**Tip:** Si pulsamos **F3** activaremos un asistente.\n\n---\n\nsigue\n')
    assert '!!! tip "Tip"' in out, out
    assert '    Si pulsamos **F3** activaremos un asistente.' in out, out
    assert '---' not in out, out
    # El origen deja a veces dos puntos, uno en la negrita y otro fuera.
    assert '    A pesar de todo.' in f('a\n\n---\n\n**IMPORTANTE:** : A pesar de todo.\n\n---\n\nb\n')


def test_reglas_sin_aviso_dentro_no_se_tocan():
    """
    Dos reglas horizontales son un separador legitimo. Solo se convierte si
    lo que hay en medio empieza por una palabra de aviso en negrita.
    """
    f = converters.avisos_entre_reglas_a_admonitions
    for md in ('a\n\n---\n\nTexto normal sin aviso.\n\n---\n\nb\n',
               'a\n\n---\n\n**Resultado:** el total sale mal.\n\n---\n\nb\n'):
        assert f(md) == md, md


def test_las_palabras_nuevas_no_degradan_ningun_encabezado():
    """
    CALLOUT_WORDS la comparte demote_callout_headings, asi que anadir una
    palabra degrada cualquier encabezado que se llame igual. Se comprobo que
    el corpus no tiene ninguno con estas, y el test lo deja fijado.
    """
    for palabra in ('tip', 'recomendación', 'sugerencia', 'comprobar'):
        assert palabra in converters.CALLOUT_WORDS, palabra
        assert palabra in converters._TIPO_DE_AVISO, palabra


def test_parrafo_con_br_que_era_una_lista():
    """
    En las fichas de referencia el autor pulso Shift+Enter en vez de Enter,
    asi que las 24 propiedades de "Grid - Acceder a propiedades de la grid"
    son UN SOLO <p> con 24 <br> dentro. Publicado sale un muro de texto.

    La senal de que era una lista es que TODOS los trozos empiezan por
    negrita: eso solo pasa enumerando elementos etiquetados.
    """
    f = converters._parrafos_con_br_a_lista
    html = ('<p dir="ltr"><strong>Agregar (Boolean):</strong> Permite agregar.<br>'
            '<strong>Editar (Boolean):</strong> Permite editar.<br>'
            '<strong>Eliminar (Boolean):</strong> Permite eliminar.</p>')
    out = f(html)
    assert out.count('<li>') == 3, out
    assert '<ul>' in out and '<p' not in out, out
    assert '<li><strong>Agregar (Boolean):</strong> Permite agregar.</li>' in out, out


def test_prosa_con_saltos_duros_no_es_una_lista():
    """
    Hay 346 parrafos con tres o mas trozos separados por <br> y solo 6 son
    una lista. Los otros 340 son prosa con saltos intencionados —el
    "En los articulos ... / ... informara una Naturaleza" del Actualizador—
    y convertirlos en lista los estropearia.
    """
    f = converters._parrafos_con_br_a_lista
    prosa = ('<p>En los articulos &hellip;<br>&hellip; informara una Naturaleza de '
             'tipo Bien, si es Inventariable.<br>&hellip; informara una Naturaleza de '
             'tipo Servicio, si no lo es.</p>')
    assert f(prosa) == prosa
    # Con menos de tres trozos no hay patron que reconocer.
    dos = '<p><strong>Uno:</strong> a<br><strong>Dos:</strong> b</p>'
    assert f(dos) == dos
    # Y si solo una parte va etiquetada, tampoco.
    mixto = ('<p><strong>Uno:</strong> a<br>texto suelto<br>mas texto suelto<br>'
             'y mas texto</p>')
    assert f(mixto) == mixto


def test_la_lista_sobrevive_al_motor_de_conversion():
    """
    Comprobado de punta a punta: el <ul> tiene que llegar al Markdown como
    vinetas, no volver a fundirse en un parrafo.
    """
    html = ('<h3>Control Grid</h3>'
            '<p dir="ltr"><strong>Agregar (Boolean):</strong> Permite agregar.<br>'
            '<strong>Editar (Boolean):</strong> Permite editar.<br>'
            '<strong>Eliminar (Boolean):</strong> Permite eliminar.</p>')
    md = converters._convert_with_html2text(
        converters.preprocess_reference_html('Grid - Acceder a propiedades', html),
    )
    vinetas = [ln for ln in md.splitlines() if ln.strip().startswith('*')]
    assert len(vinetas) == 3, md
    assert '**Agregar (Boolean):**' in vinetas[0], vinetas[0]


def test_lista_reconocida_aunque_el_origen_perdiera_la_negrita():
    """
    Hay DOS articulos en Freshdesk titulados "Grid - Acceder a propiedades de
    la grid": el de Ctrl+F10 (id 154000128261) trae 33 <strong> y el de
    _ahoraSCO (id 154000129983) trae 1. Es la misma lista con las negritas
    perdidas en el origen, asi que exigir negrita la reconocia en una copia y
    no en la otra.

    La etiqueta en texto plano —"Agregar (Boolean): Indica si..."— sirve
    igual de senal.
    """
    f = converters._parrafos_con_br_a_lista
    html = ('<p>Agregar (Boolean): Indica si permite agregar.<br>'
            'Editar (Boolean): Indica si permite editar.<br>'
            'Coleccion: Le pasaremos la coleccion de objetos.</p>')
    out = f(html)
    assert out.count('<li>') == 3, out
    assert '<ul>' in out, out


def test_la_etiqueta_tiene_que_ser_corta():
    """
    Sin el limite de longitud, cualquier frase con dos puntos por medio
    pasaria por etiqueta y la prosa acabaria troceada en vinetas.
    """
    f = converters._parrafos_con_br_a_lista
    prosa = ('<p>Cuando se trata de una prestacion de servicios intracomunitaria: '
             'hay que revisar el parametro.<br>'
             'Si el cliente es extranjero y no comunitario: se aplica otra regla.<br>'
             'En cualquier otro caso: se deja como esta.</p>')
    assert f(prosa) == prosa, f(prosa)


def test_encabezado_no_acaba_en_dos_puntos():
    """
    Un encabezado es un titulo, no el arranque de una frase, y en el panel
    derecho "Descripcion:" o "Modo automatico:" se leen mal. Eran 987 y
    encima incoherentes: unos los llevaban y otros no. De ellos 732 son las
    etiquetas de referencia que promueve este mismo pipeline, asi que buena
    parte de la incoherencia era propia.
    """
    f = converters._quitar_enfasis_de_encabezados
    assert f('## Descripción:') == '## Descripción'
    assert f('## Código C#:') == '## Código C#'
    assert f('## Modo por pasos (NO Recomendable):') == '## Modo por pasos (NO Recomendable)'
    # Los dos puntos por MEDIO no se tocan.
    assert f('## 1:1 en la relación') == '## 1:1 en la relación'


def test_enfasis_y_dos_puntos_en_el_mismo_encabezado():
    """
    En "**Cuentas** :" el ":" de en medio impedia ver el par de negritas, asi
    que la negrita se quedaba puesta. Se pela otra vez despues de quitar los
    dos puntos.
    """
    assert converters._quitar_enfasis_de_encabezados('### **Cuentas** :') == '### Cuentas'


def test_el_encabezado_nunca_se_queda_sin_texto():
    """
    Si al quitar los dos puntos no queda nada, se deja como estaba: mejor un
    ":" a la vista que un encabezado vacio, que rompe el panel derecho.
    """
    f = converters._quitar_dos_puntos_finales
    assert f(':') == ':'
    assert f('::') == '::'
    assert f('Titulo:') == 'Titulo'


def test_el_ancla_de_word_no_se_traga_el_parrafo():
    """
    En "ERP - Ventas - Oferta" el marcador de Word envuelve SOLO la letra "L"
    —el primer caracter del parrafo— y el resto de la frase queda fuera del
    ancla pero dentro del mismo <p>.

    Con un (.*?) a secas el motor retrocedia hasta un ancla POSTERIOR y se
    tragaba el parrafo entero: salia un encabezado de 160 caracteres con la
    frase completa y otro titulo pegado detras. El contenido del ancla no
    puede cruzar un </a> ni un <p>.
    """
    f = converters._encabezados_de_word
    html = ('<p><span><a name="_Toc534965562"><span>L</span></a></span>'
            '<span>a oferta no es un documento requerido para iniciar el proceso '
            'de venta, se utiliza a modo de presupuesto.</span></p>'
            '<p><a name="_Toc534965563">Alta de nueva oferta</a></p>')
    out = f(html)
    # El parrafo de prosa se queda como parrafo...
    assert 'a oferta no es un documento' in out, out
    assert '<h2>L</h2>' not in out, out
    # ...y el encabezado de verdad si se recupera.
    assert '<h2>Alta de nueva oferta</h2>' in out, out
    assert not re.search(r'(?is)<h2>.{90,}</h2>', out), out


def test_ancla_de_word_demasiado_larga_se_rechaza():
    """
    Red de seguridad: un encabezado de Word mas largo que el tope no es un
    encabezado, es un parrafo cuyo primer caracter llevaba el marcador.
    """
    largo = 'x' * (converters._MAX_LARGO_ENCABEZADO_WORD + 1)
    html = f'<p><a name="_Toc1">{largo}</a></p>'
    assert converters._encabezados_de_word(html) == html


def test_ancla_de_word_con_solo_un_espacio_duro():
    """
    Dos de los marcadores envuelven un &nbsp; y nada mas. Sin des-escapar
    antes de comprobar, salia un encabezado cuyo texto era literalmente
    "&nbsp;".
    """
    f = converters._encabezados_de_word
    for html in ('<p><a name="_Toc1">&nbsp;</a></p>',
                 '<p><a name="_Toc2"><span>&nbsp; &nbsp;</span></a></p>'):
        assert '<h2>' not in f(html), f(html)
    # Y un &nbsp; POR MEDIO se convierte en espacio normal.
    out = f('<p><a name="_Toc3">Opcion 2: desde&nbsp;"Gestion"</a></p>')
    assert out == '<h2>Opcion 2: desde "Gestion"</h2>', out


def test_la_almohadilla_de_C_sostenido_sobrevive():
    """
    "## Codigo C#" se renderiza como "Codigo C": Markdown interpreta la
    almohadilla final como el cierre opcional del encabezado ATX. Eran 301
    encabezados —240 entradas "Codigo C" en el panel— y lo introdujo este
    mismo pipeline al quitar los dos puntos, que sin saberlo hacian de escudo.
    """
    import markdown
    f = converters.normalizar_encabezados_al_final
    assert f('## Código C#') == '## Código C' + chr(92) + '#'
    md = markdown.Markdown()
    assert '>Código C#<' in md.convert(f('## Código C#'))


def test_el_cierre_ATX_legitimo_no_se_escapa():
    """
    "## Titulo ##" es la forma de cierre de Markdown y debe seguir
    desapareciendo. El espacio es lo que lo distingue de un "C#" pegado a la
    palabra: en el corpus hay 301 pegadas y ni un solo cierre, pero el corte
    se hace igual.
    """
    f = converters.normalizar_encabezados_al_final
    assert f('## Título ##') == '## Título ##'
    assert f('## Trabajar con SEPA') == '## Trabajar con SEPA'


def test_los_dos_puntos_se_quitan_al_final_de_la_cadena():
    """
    La limpieza de encabezados corre ANTES de las reglas que crean
    encabezados nuevos, asi que quedaba un "## Pasos para solucionarlo:" a la
    vista. El arreglo no puede depender del orden: se repasa al final.
    """
    f = converters.normalizar_encabezados_al_final
    assert f('## Pasos para solucionarlo:') == '## Pasos para solucionarlo'
    assert f('## Código C#:') == '## Código C' + chr(92) + '#'
    # Los dos puntos por MEDIO no se tocan, y un encabezado no se queda vacio.
    assert f('## 1:1 en la relación') == '## 1:1 en la relación'
    assert f('## :') == '## :'


def test_la_prosa_se_degrada_en_TODOS_los_niveles():
    """
    El origen envuelve bloques enteros en un <h4> —hasta 410 caracteres— y
    _normalizar_niveles_de_seccion los sube despues a h2, con lo que la prosa
    acababa en el panel derecho. Mirar solo h1-h3 dejaba 36 entradas asi, una
    de 1.052 caracteres.
    """
    prosa = ('En todos los documentos (las ofertas, pedidos, albaranes y facturas) '
             'se puede renumerar el documento. Para ello hay que entrar en la '
             'opcion correspondiente y seguir los pasos indicados.')
    out = converters.preprocess_reference_html('T', f'<h4>{prosa}</h4>')
    assert '<h4>' not in out and '<h2>' not in out, out
    assert prosa[:40] in out, out
    # Un titulo largo pero que NO es prosa se conserva.
    titulo = 'Asignación de localizaciones por defecto al empleado (para Ficha)'
    assert '<h' in converters.preprocess_reference_html('T', f'<h4>{titulo}</h4>')


def test_un_encabezado_que_es_un_enlace_no_es_un_encabezado():
    """
    Son los 8 enlaces de navegacion del tipo "## [< Codificacion:
    Manipulacion de grids en frmPedidos](...)". Mismo criterio que ya usa
    promover_negritas_a_encabezados: un parrafo que es un enlace es un
    enlace.
    """
    f = converters.normalizar_encabezados_al_final
    md = '## [< Codificación: Manipulación de grids en frmPedidos](Codificacion.md)'
    out = f(md)
    assert not out.startswith('#'), out
    # El enlace se conserva entero: no se pierde nada.
    assert '[< Codificación: Manipulación de grids en frmPedidos](Codificacion.md)' in out
    # Un titulo que SOLO lleva un enlace dentro sigue siendo un titulo.
    assert f('## Ver el [manual](x.md) de instalación').startswith('## ')


def test_un_encabezado_que_es_solo_un_enlace_pierde_el_enlace():
    """
    Un encabezado es un titulo, y en toda la documentacion se ve como un
    titulo. Estos catorce se veian en azul y se podian pulsar, porque el
    origen —una copia de una pagina de Microsoft Learn— traia cada seccion
    enlazada a su ancla en el original.

    No se degradan a parrafo, que es lo que se hace con los de navegacion:
    aqui el texto SI es un titulo de seccion y el panel derecho lo necesita.
    Lo que sobra es el enlace.
    """
    f = converters.normalizar_encabezados_al_final
    assert f('## [Limitaciones y restricciones](https://learn.microsoft.com/x#R)'
             ) == '## Limitaciones y restricciones'
    # Con titulo entre comillas tambien.
    assert f('### [Permisos](https://learn.microsoft.com/a "Un titulo")') == '### Permisos'
    # Un titulo que solo LLEVA un enlace dentro no se toca.
    assert f('## Ver el [manual](x.md) de instalación'
             ) == '## Ver el [manual](x.md) de instalación'
    # Y un H1 es el titulo del articulo: no lo escribe el conversor.
    assert f('# [No toco los H1](x.md)') == '# [No toco los H1](x.md)'


def test_un_encabezado_larguisimo_no_es_un_encabezado():
    """
    15 encabezados pasan de 160 caracteres y ahi no hay titulos: el origen
    envolvio bloques de prosa en un <h3>/<h4> y uno llega a 1.052. El titulo
    legitimo mas largo del corpus tiene 117.
    """
    f = converters.normalizar_encabezados_al_final
    prosa = 'Para cambiar el tamano de la fila utilizaremos la propiedad. ' * 4
    assert not f(f'## {prosa}').startswith('#')
    # 117 caracteres siguen siendo un titulo.
    assert f('## ' + 'A' * 117).startswith('## ')


def test_el_degradado_vale_para_los_DOS_motores():
    """
    Esta regla va sobre el Markdown y al final de la cadena a proposito:
    convert_author NO pasa por preprocess_reference_html, que es donde vive
    la degradacion por _parece_prosa, y el encabezado de 1.052 caracteres era
    justo de un articulo de autor.
    """
    import inspect
    for motor in (converters.convert_standard, converters.convert_author):
        fuente = inspect.getsource(motor)
        assert 'normalizar_encabezados_al_final' in fuente, motor.__name__


def test_lineas_en_blanco_con_espacios():
    """
    El origen siembra lineas que parecen vacias pero llevan espacios —21.678
    en el corpus— y derrotan al colapso de \n{3,}, que no las reconoce como
    vacias: los ficheros acumulaban rachas de "\n\n  \n\n  \n\n".
    """
    f = converters.limpiar_lineas_en_blanco
    assert f('a\n\n  \n\n  \n\nb') == 'a\n\nb'
    assert f('a\n\n\t\n\nb') == 'a\n\nb'


def test_el_salto_duro_de_markdown_no_se_toca():
    """
    La linea que SI significa algo es la que lleva dos espacios TRAS UN
    TEXTO: es el salto duro. Una que solo tiene espacios no significa nada.
    """
    f = converters.limpiar_lineas_en_blanco
    assert f('linea con salto  \nsiguiente') == 'linea con salto  \nsiguiente'
    assert f('  texto indentado') == '  texto indentado'


def test_dentro_de_un_fence_los_espacios_se_respetan():
    """
    Dentro de un bloque de codigo una linea con espacios puede ser
    indentacion con significado, asi que la limpieza va por fuera.
    """
    md = '```vbnet\nSub X()\n    \n    Dim a\nEnd Sub\n```'
    assert converters._outside_fences(md, converters.limpiar_lineas_en_blanco) == md


def test_el_enlace_sin_texto_recupera_su_etiqueta():
    """
    El origen escribe <h2><a href="url"></a>Permisos</h2>: el ancla se quedo
    sin texto y la etiqueta de verdad quedo fuera, pegada detras. Si no se
    juntan, la regla que etiqueta enlaces vacios le mete la URL como texto y
    el encabezado pasa de 157 a 299 caracteres con la URL a la vista.

    Son 16 casos en 3 articulos, 14 de ellos en el mismo.
    """
    f = converters.juntar_enlace_vacio_con_su_texto
    out = f('## [](https://learn.microsoft.com/x#Permissions)Permisos')
    assert out == '## [Permisos](https://learn.microsoft.com/x#Permissions)', out
    assert f('[](https://x.com/y)Requisitos previos') == '[Requisitos previos](https://x.com/y)'


def test_no_se_enlaza_una_frase_entera():
    """
    Se exige que ocupe toda la linea y que la etiqueta sea corta. Sin eso, en
    un parrafo se enlazaria la frase completa.
    """
    f = converters.juntar_enlace_vacio_con_su_texto
    for md in ('[](https://x.com/y)' + 'texto muy largo ' * 8,
               'Ver [](https://x.com/y)Permisos',
               '## [Permisos](https://x.com/y)',
               '![](../img/x.png)Pie de figura'):
        assert f(md) == md, md


def test_el_largo_del_encabezado_se_mide_sobre_lo_que_SE_VE():
    """
    En "## [Limitaciones y restricciones](https://learn.microsoft.com/...)" el
    panel lee 28 caracteres y la linea tiene 190. Midiendo la linea se
    degradaban las 14 secciones de "Usar el Asistente para planes de
    mantenimiento" por lo larga que era la URL.
    """
    f = converters.normalizar_encabezados_al_final
    url = 'https://learn.microsoft.com/es-es/sql/relational-databases/maintenance-plans/use-the-maintenance-plan-wizard?view=sql-server-ver16#Restrictions'
    md = f'## [Limitaciones y restricciones]({url})'
    assert len(md) > 160, len(md)
    # Sigue siendo un encabezado: lo que no puede pasar es que la longitud de
    # la URL lo degrade a parrafo. Que ademas pierda el enlace es otra regla
    # —_encabezados_que_son_un_enlace— y tiene su propio test.
    assert f(md).startswith('## Limitaciones y restricciones'), f(md)


def test_un_titulo_que_enlaza_no_es_un_enlace_de_navegacion():
    """
    La flecha de "anterior / siguiente" es lo que distingue un enlace de
    navegacion de un titulo que ademas enlaza a algun sitio. Sin ese corte se
    degradaban tambien las secciones que enlazan a la documentacion de
    Microsoft, que SI son secciones.
    """
    f = converters.normalizar_encabezados_al_final
    # Navegacion: fuera del panel.
    assert not f('## [< Codificación: Manipulación de grids](x.md)').startswith('#')
    assert not f('## [Codificación: Ejecutando procedimientos >](x.md)').startswith('#')
    # Titulo que enlaza: se queda.
    assert f('## [Permisos](https://learn.microsoft.com/x)').startswith('## ')
    # Un enlace sin etiqueta no se ve: tampoco es un titulo.
    assert not f('## [](https://x.com/y)').startswith('#')


def test_tabla_de_una_celda_con_codigo_pasa_a_bloque():
    """
    El origen usa una tabla de una sola celda como recuadro, y a veces mete
    dentro una consulta con las palabras clave coloreadas a mano. Publicado
    salia como tabla con borde, sin monoespaciado ni resaltado, y con el
    color pintado a mano en vez del del tema. Son 26 tablas en 11 articulos.
    """
    f = converters._tablas_de_una_celda_con_codigo
    html = ('<table style="width:100%"><tbody><tr><td><br/>'
            '<span style="color: rgb(44,130,201);">EXEC </span>'
            'VACIA..Ztest @a,@b<br/><br/></td></tr></tbody></table>')
    out = f(html)
    assert out == '<pre><code>EXEC VACIA..Ztest @a,@b</code></pre>', out


def test_las_comillas_del_codigo_van_literales():
    """
    Dentro de un <pre> las comillas no se escapan: con el escapado por
    defecto, un "'" de una consulta acababa como "&#x27;" en el bloque, a la
    vista del lector.
    """
    html = ("<table><tbody><tr><td>SELECT * FROM Clientes "
            "WHERE IdCliente = '00000'</td></tr></tbody></table>")
    out = converters._tablas_de_una_celda_con_codigo(html)
    assert "'00000'" in out, out
    assert '&#x27;' not in out, out


def test_los_saltos_del_codigo_se_conservan():
    """
    Los <br> y los <p> marcan los saltos. Sin convertirlos, las lineas se
    pegan unas a otras —"frmAux.DescargarlDescCliente="— y el codigo se
    vuelve ilegible.
    """
    html = ('<table><tbody><tr><td>Sub Main()<br/>Dim a As String<br/>'
            'End Sub</td></tr></tbody></table>')
    out = converters._tablas_de_una_celda_con_codigo(html)
    assert 'Sub Main()\nDim a As String\nEnd Sub' in out, out


def test_una_tabla_que_no_es_codigo_se_queda_como_esta():
    """
    El criterio es que detect_code_lang reconozca el contenido, el mismo que
    decide el lenguaje de los demas bloques. Un aviso o una tabla de datos no
    se tocan.
    """
    f = converters._tablas_de_una_celda_con_codigo
    for html in (
        '<table><tbody><tr><td><p><strong>IMPORTANTE</strong></p>'
        '<p>Antes de actualizar hay que revisar la configuracion.</p></td></tr></tbody></table>',
        '<table><tbody><tr><td>Objeto</td><td>Nombre</td></tr>'
        '<tr><td>gCn</td><td>DameValorCampo</td></tr></tbody></table>',
        '<table><tbody><tr><td><br/></td></tr></tbody></table>',
    ):
        assert f(html) == html, html


def test_categoria_que_existe_recibe_portada_y_el_enlace_se_reapunta():
    """
    MkDocs publica paginas, no directorios: una carpeta solo tiene URL si
    lleva un index.md. Si la categoria esta en la ejecución, se le da portada y
    el enlace se reapunta a ella.

    Y se reapunta al .md, NUNCA a la carpeta: MkDocs solo reescribe los
    enlaces que reconoce como documento, y con use_directory_urls la pagina
    vive un nivel mas abajo que el fichero. Escrito "a la carpeta" se queda
    corto y da 404 aunque la portada exista.
    """
    import tempfile
    from pipeline.repair_links import phase_unwrap_folder_links
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        (raiz / 'API' / 'Instalacion').mkdir(parents=True)
        (raiz / 'TPV' / 'Entorno').mkdir(parents=True)
        (raiz / 'TPV' / 'Entorno' / 'x.md').write_text(
            '# Un articulo TPV' + chr(10), encoding='utf-8')
        art = raiz / 'API' / 'Instalacion' / 'a.md'
        art.write_text('Ver [AHORA TPV](../../TPV/) para el detalle.' + chr(10),
                       encoding='utf-8')

        quitados = phase_unwrap_folder_links(raiz)
        # No se ha quitado nada: se ha arreglado.
        assert quitados == [], quitados
        assert (raiz / 'TPV' / 'index.md').is_file()
        salida = art.read_text(encoding='utf-8')
        assert '[AHORA TPV](../../TPV/index.md)' in salida, salida


def test_la_portada_de_una_categoria_lista_sus_carpetas():
    """
    La portada de una categoria lista sus carpetas, con cuantos articulos
    tiene cada una. Los articulos de dentro los lista la portada de su
    carpeta, no esta.

    Es Markdown y nada mas: ni HTML crudo, ni clases, ni hojas de estilo.
    """
    import tempfile
    from pipeline.repair_links import escribir_portada
    salto = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        cat = Path(tmp) / 'API'
        (cat / 'Instalacion').mkdir(parents=True)
        (cat / 'FAQ').mkdir()
        (cat / 'Instalacion' / 'uno.md').write_text(
            '# AHORA API - Instalacion' + salto, encoding='utf-8')
        (cat / 'FAQ' / 'dos.md').write_text(
            '# Se ha denegado el permiso' + salto, encoding='utf-8')
        (cat / 'FAQ' / 'tres.md').write_text('# Otra mas' + salto, encoding='utf-8')
        texto = escribir_portada(cat).read_text(encoding='utf-8')

        # El H1 va PRIMERO: con el comentario delante, MkDocs no detecta el
        # H1 y titula la pagina 'Index' —en el panel, en la pestaña del
        # navegador y en la busqueda—. La marca va detras.
        assert texto.startswith('# API' + salto), texto
        assert '<!-- portada' in texto, texto
        # Tarjetas de Material: el componente es del tema, no hay CSS propio.
        assert '<div class="grid cards" markdown>' in texto, texto
        assert '**[FAQ](FAQ/index.md)**' in texto, texto
        assert '**[Instalacion](Instalacion/index.md)**' in texto, texto
        # La tarjeta es solo el nombre: ni raya, ni recuento de articulos.
        assert '---' not in texto, texto
        assert 'artículo' not in texto, texto
        # Sin articulos sueltos no hay encabezados que ensuciar la tabla de
        # contenidos: la unica lista de la pagina no necesita titulo.
        assert '## ' not in texto, texto


def test_mkdocs_trae_lo_que_las_portadas_necesitan():
    """
    Las tarjetas de la portada no son CSS nuestro: son el componente 'grid
    cards' de Material, y se apoyan en tres extensiones que ya estaban en
    mkdocs.yml. Si alguien quita una, la portada no da error: se degrada en
    silencio —el <div> se queda literal, o los iconos salen como texto—, y
    eso no lo ve nadie hasta que mira las 153 paginas.

    - md_in_html   el <div class="grid cards" markdown> y su contenido
    - attr_list    los modificadores { .lg .middle } del icono
    - pymdownx.emoji  los :material-...:
    """
    raiz = Path(__file__).resolve().parent.parent
    config = (raiz / 'mkdocs.yml').read_text(encoding='utf-8')
    for extension in ('md_in_html', 'attr_list', 'pymdownx.emoji'):
        assert extension in config, extension
    # Y navigation.indexes, o la portada sale como una entrada mas dentro de
    # su propia seccion en lugar de ser el titulo de la seccion.
    assert 'navigation.indexes' in config, config


def test_los_enlaces_de_la_portada_van_al_md():
    """
    Siempre al .md, nunca a la carpeta: MkDocs solo reescribe los enlaces que
    reconoce como documento, y con use_directory_urls la pagina vive un nivel
    mas abajo que el fichero. Escrito 'FAQ/' se queda corto y da 404.
    """
    import tempfile
    from pipeline.repair_links import escribir_portada
    salto = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        cat = Path(tmp) / 'API'
        (cat / 'FAQ').mkdir(parents=True)
        (cat / 'FAQ' / 'con espacio.md').write_text('# Con espacio' + salto, encoding='utf-8')
        (cat / 'suelto.md').write_text('# Suelto' + salto, encoding='utf-8')
        texto = escribir_portada(cat).read_text(encoding='utf-8')
        assert '(FAQ/index.md)' in texto, texto
        assert '(suelto.md)' in texto, texto

        hoja = escribir_portada(cat / 'FAQ').read_text(encoding='utf-8')
        assert '(con%20espacio.md)' in hoja, hoja
        # Y la portada no se lista a si misma: solo esta el articulo.
        assert 'index.md' not in hoja, hoja
        assert hoja.count(salto + '-   ') == 1, hoja


def test_todas_las_carpetas_reciben_portada():
    """
    Cada carpeta tiene que tener su index.md, no solo las categorias.

    MkDocs publica paginas, no directorios: un enlace de Freshdesk a una
    carpeta llegaba a un directorio sin pagina y acababa degradado a texto.
    """
    import tempfile
    from pipeline.repair_links import escribir_portadas_del_arbol
    salto = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        cat = Path(tmp) / 'API'
        (cat / 'Instalacion').mkdir(parents=True)
        (cat / 'Vacia').mkdir()
        (cat / 'Instalacion' / 'uno.md').write_text('# Uno' + salto, encoding='utf-8')
        (cat / 'suelto.md').write_text('# Suelto' + salto, encoding='utf-8')

        escritas, respetadas = escribir_portadas_del_arbol([cat])
        assert (cat / 'index.md').is_file(), 'la categoria se queda sin portada'
        assert (cat / 'Instalacion' / 'index.md').is_file(), 'la carpeta se queda sin portada'
        # Una carpeta sin articulos no lleva portada: seria una pagina en
        # blanco en el panel de navegacion.
        assert not (cat / 'Vacia' / 'index.md').exists(), 'portada de carpeta vacia'
        assert (escritas, respetadas) == (2, 0), (escritas, respetadas)

        # En la portada de una carpeta hoja el listado es plano, sin grupos.
        hoja = (cat / 'Instalacion' / 'index.md').read_text(encoding='utf-8')
        assert hoja.startswith('# Instalacion' + salto), hoja
        assert '[Uno](uno.md)' in hoja, hoja
        # La tarjeta de un articulo es solo el titulo: no hay nada mas que
        # contar, y una raya con un hueco vacio debajo queda peor.
        assert '---' not in hoja, hoja
        assert '##' not in hoja, hoja


def test_una_portada_escrita_a_mano_se_respeta():
    import tempfile
    from pipeline.repair_links import escribir_portadas_del_arbol
    salto = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        cat = Path(tmp) / 'API'
        cat.mkdir(parents=True)
        (cat / 'uno.md').write_text('# Uno' + salto, encoding='utf-8')
        mia = '# Lo escribi yo' + salto
        (cat / 'index.md').write_text(mia, encoding='utf-8')

        escritas, respetadas = escribir_portadas_del_arbol([cat])
        assert (escritas, respetadas) == (0, 1), (escritas, respetadas)
        assert (cat / 'index.md').read_text(encoding='utf-8') == mia, 'la ha pisado'


def test_bug_una_portada_sin_cambios_no_se_reescribe():
    """
    Rehacer un fichero identico le cambia la fecha y lo saca en el git status
    de las 156 carpetas todas las semanas.
    """
    import tempfile
    from pipeline.repair_links import escribir_portada
    salto = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        cat = Path(tmp) / 'API'
        cat.mkdir(parents=True)
        (cat / 'uno.md').write_text('# Uno' + salto, encoding='utf-8')
        portada = escribir_portada(cat)
        marca = portada.stat().st_mtime_ns
        escribir_portada(cat)
        assert portada.stat().st_mtime_ns == marca, 'la ha reescrito sin cambios'


def test_bug_los_nombres_con_almohadilla_o_parentesis_se_escapan():
    """
    Un '#' en el nombre lo lee Markdown como ancla y el enlace se queda
    apuntando a un fichero que no existe; un parentesis cierra el enlace
    antes de tiempo. Los dos salieron en el 'mkdocs build'.
    """
    import tempfile
    from pipeline.repair_links import escribir_portada
    salto = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        cat = Path(tmp) / 'API'
        cat.mkdir(parents=True)
        (cat / 'De VBScript a C# (4.4.2400).md').write_text('# Traducir' + salto, encoding='utf-8')
        texto = escribir_portada(cat).read_text(encoding='utf-8')
        assert '(De%20VBScript%20a%20C%23%20%284.4.2400%29.md)' in texto, texto


def test_la_carpeta_que_repite_el_nombre_de_su_madre_no_es_un_grupo():
    """
    docs/Actualizador/Actualizador/ es la categoria doblada en el origen, no
    un grupo: separarla dejaba la portada con dos listas seguidas sin titulo.
    """
    import tempfile
    from pipeline.repair_links import escribir_portada
    salto = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        cat = Path(tmp) / 'Actualizador'
        (cat / 'Actualizador').mkdir(parents=True)
        (cat / 'FAQ').mkdir()
        (cat / 'Actualizador' / 'uno.md').write_text('# Uno' + salto, encoding='utf-8')
        (cat / 'FAQ' / 'dos.md').write_text('# Dos' + salto, encoding='utf-8')
        texto = escribir_portada(cat).read_text(encoding='utf-8')
        # No sale como carpeta: sus articulos se listan con los sueltos.
        assert '[Actualizador](Actualizador/index.md)' not in texto, texto
        assert '[FAQ](FAQ/index.md)' in texto, texto
        # Pero la ruta del enlace sigue llevando la subcarpeta.
        assert '[Uno](Actualizador/uno.md)' in texto, texto
        # Y las carpetas van antes que los articulos sueltos.
        assert texto.index('## Carpetas') < texto.index('## Artículos'), texto


def test_categoria_que_no_esta_en_la_ejecución_se_queda_en_texto():
    """
    Si la categoria no se ha generado no hay pagina que crear, asi que el
    enlace se queda en texto para no publicar un 404. Es el caso de TPV
    cuando se genera solo el ERP.
    """
    import tempfile
    from pipeline.repair_links import phase_unwrap_folder_links
    salto = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        (raiz / 'API' / 'Instalacion').mkdir(parents=True)
        art = raiz / 'API' / 'Instalacion' / 'a.md'
        art.write_text('Ver [AHORA TPV](../../TPV/) para el detalle.' + salto,
                       encoding='utf-8')

        quitados = phase_unwrap_folder_links(raiz)
        assert len(quitados) == 1, quitados
        assert quitados[0].text == 'AHORA TPV', quitados[0]
        assert quitados[0].target == '../../TPV/', quitados[0]
        assert 'no está en esta ejecución' in quitados[0].folder, quitados[0]
        assert art.read_text(encoding='utf-8') == 'Ver AHORA TPV para el detalle.' + salto


def test_carpeta_que_YA_tiene_portada_tambien_se_reapunta():
    """
    Comprobado a mano con un proyecto MkDocs minimo: un enlace a carpeta NO
    lo reescribe MkDocs, y con use_directory_urls la pagina vive un nivel mas
    abajo que el fichero, asi que '../../TPV/' resuelve a '/API/TPV/' y da 404
    **aunque la portada exista**. Solo funciona escrito al .md.

    Por eso hay que reapuntarlo igual, y por eso una version anterior de esta
    fase estaba mal: omitia las carpetas que ya tenian index.md.
    """
    import tempfile
    from pipeline.repair_links import phase_unwrap_folder_links
    salto = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        (raiz / 'API' / 'Instalacion').mkdir(parents=True)
        (raiz / 'TPV').mkdir()
        portada = raiz / 'TPV' / 'index.md'
        portada.write_text('# TPV escrita a mano' + salto, encoding='utf-8')
        art = raiz / 'API' / 'Instalacion' / 'a.md'
        art.write_text('Ver [AHORA TPV](../../TPV/).' + salto, encoding='utf-8')

        assert phase_unwrap_folder_links(raiz) == []
        assert '[AHORA TPV](../../TPV/index.md)' in art.read_text(encoding='utf-8')
        # Y una portada que ya existia no se pisa.
        assert portada.read_text(encoding='utf-8') == '# TPV escrita a mano' + salto


def test_la_fase_respeta_only_files():
    """
    Como las demas fases: en una ejecución incremental solo se toca lo que se ha
    vuelto a generar. Sin esto, una generacion de una sola categoria
    reescribia enlaces de ficheros que estaban correctos.
    """
    import tempfile
    from pipeline.repair_links import phase_unwrap_folder_links
    salto = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        (raiz / 'A').mkdir()
        (raiz / 'B').mkdir()
        uno = raiz / 'A' / 'uno.md'
        dos = raiz / 'B' / 'dos.md'
        texto = 'Ver [AHORA TPV](../TPV/).' + salto
        uno.write_text(texto, encoding='utf-8')
        dos.write_text(texto, encoding='utf-8')
        assert len(phase_unwrap_folder_links(raiz, [uno])) == 1
        assert 'AHORA TPV](' not in uno.read_text(encoding='utf-8')
        assert dos.read_text(encoding='utf-8') == texto


def test_el_informe_de_enlaces_a_categoria():
    """
    Quitar un enlace es perder informacion, asi que tiene que quedar en el
    log: el lector debe poder decidir si esa categoria merece una pagina
    indice o si el enlace estaba de mas.
    """
    from pipeline.repair_links import EnlaceACategoria, build_category_links_report
    enlaces = [
        EnlaceACategoria('API/Instalacion/a.md', 'AHORA TPV', '../../TPV/', 'TPV'),
        EnlaceACategoria('API/Instalacion/b.md', 'AHORA API', '../../API/', 'API'),
        EnlaceACategoria('API/Instalacion/c.md', 'AHORA TPV', '../../TPV/', 'TPV'),
    ]
    lineas = build_category_links_report(enlaces)
    texto = '\n'.join(lineas)
    # Va agrupado por carpeta de destino, que es donde se toma la decision.
    assert 'CARPETA: TPV   (2 enlace(s))' in texto, texto
    assert 'CARPETA: API   (1 enlace(s))' in texto, texto
    # Y con lo necesario para reconstruir cada uno.
    assert 'API/Instalacion/a.md' in texto
    assert 'texto conservado : AHORA TPV' in texto
    assert 'destino que tenía: ../../TPV/' in texto
    # Dice como recuperarlos.
    assert 'index.md' in texto


def test_sin_enlaces_a_categoria_no_hay_informe():
    """
    La regla de reporting.py: lo que no tiene nada que contar no escribe
    fichero, para que la carpeta de logs sea siempre de esta ejecución.
    """
    from pipeline.repair_links import build_category_links_report
    assert build_category_links_report([]) == []


def test_el_informe_esta_en_el_catalogo():
    """
    Si no esta en DESCRIPCIONES no aparece en el indice del resumen, y un log
    que nadie encuentra no sirve de nada. Tampoco se retiraria al empezar la
    ejecución siguiente.
    """
    from pipeline import reporting
    assert reporting.ENLACES_A_CATEGORIA in reporting.DESCRIPCIONES
    assert reporting.ENLACES_A_CATEGORIA in reporting.NOMBRES


def test_la_portada_generada_se_rehace_y_la_escrita_a_mano_no():
    """
    La portada lleva una marca que dice quien la escribio. La nuestra se
    rehace en cada ejecución —los articulos de la categoria cambian, y un
    listado obsoleto es peor que no tenerlo—; una escrita a mano se respeta.
    """
    import tempfile
    from pipeline.repair_links import (
        MARCA_PORTADA_GENERADA, es_portada_generada,
        escribir_indice_de_categoria, phase_unwrap_folder_links,
    )
    salto = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        (raiz / 'API' / 'Instalacion').mkdir(parents=True)
        (raiz / 'TPV' / 'Entorno').mkdir(parents=True)
        (raiz / 'TPV' / 'Entorno' / 'viejo.md').write_text('# Viejo' + salto, encoding='utf-8')
        art = raiz / 'API' / 'Instalacion' / 'a.md'
        art.write_text('Ver [AHORA TPV](../../TPV/).' + salto, encoding='utf-8')

        # Primera pasada: se crea la portada, y lleva la marca.
        phase_unwrap_folder_links(raiz)
        portada = raiz / 'TPV' / 'index.md'
        assert es_portada_generada(portada)
        assert MARCA_PORTADA_GENERADA in portada.read_text(encoding='utf-8')
        # La portada de la categoria lista la carpeta.
        contenido = portada.read_text(encoding='utf-8')
        assert '**[Entorno](Entorno/index.md)**' in contenido, contenido

        # Llega una carpeta nueva y el enlace vuelve: la portada se rehace.
        #
        # Tiene que ser una CARPETA y no un articulo: la portada de una
        # categoria lista sus carpetas, no los articulos de dentro, asi que un
        # articulo nuevo no la cambia. De eso se encarga la portada de su
        # carpeta, que escribe escribir_portadas_del_arbol.
        (raiz / 'TPV' / 'Perifericos').mkdir()
        (raiz / 'TPV' / 'Perifericos' / 'nuevo.md').write_text(
            '# Nuevo' + salto, encoding='utf-8')
        art.write_text('Ver [AHORA TPV](../../TPV/).' + salto, encoding='utf-8')
        phase_unwrap_folder_links(raiz)
        contenido = portada.read_text(encoding='utf-8')
        assert '**[Perifericos](Perifericos/index.md)**' in contenido, contenido

        # Si alguien la reescribe a mano, se respeta.
        portada.write_text('# Portada a mano' + salto, encoding='utf-8')
        art.write_text('Ver [AHORA TPV](../../TPV/).' + salto, encoding='utf-8')
        phase_unwrap_folder_links(raiz)
        assert portada.read_text(encoding='utf-8') == '# Portada a mano' + salto
        # Pero el enlace se reapunta igual: sin el .md daria 404.
        assert '[AHORA TPV](../../TPV/index.md)' in art.read_text(encoding='utf-8')


def test_un_style_escapado_no_se_lleva_su_contenido():
    """
    El caso que lo destapo: un articulo documenta una cabecera CSS escrita
    como "&lt;style&gt;.BlockBody{width:380px;}...&lt;/style&gt;" en un
    parrafo. Al des-escapar quedaba un <style> de verdad, markdownify lo
    eliminaba CON SU CONTENIDO, y el lector se quedaba con un "Cabecera:"
    colgando y sin el CSS.

    No se pierde la etiqueta: se pierde todo lo que hay dentro. Lo encontro
    una comparacion palabra a palabra del origen contra la salida.
    """
    html = ('<p>Cabecera:<br>&lt;style&gt;<br>.BlockBody{width:380px;}<br>'
            '.BlockFooter{margin-left:10px;}<br>&lt;/style&gt;</p>')
    out = converters._convert_with_markdownify(html)
    assert '380px' in out, out
    assert 'margin-left:10px' in out, out


def test_el_style_recuperado_no_se_ejecuta():
    """
    Restaurarlo sin escapar tampoco vale: un <style> en el Markdown lo
    APLICA el navegador como CSS de la pagina en vez de mostrarlo. Se
    devuelve escapado, que es como se ve.
    """
    import markdown
    from bs4 import BeautifulSoup
    html = '<p>Cabecera:<br>&lt;style&gt;<br>.X{width:1px;}<br>&lt;/style&gt;</p>'
    out = converters._convert_with_markdownify(html)
    render = BeautifulSoup(markdown.Markdown().convert(out), 'html.parser')
    # Ni un solo <style> de verdad en la pagina...
    assert render.find('style') is None, out
    # ...y el texto del ejemplo se lee.
    assert 'width:1px' in render.get_text(), out


def test_las_demas_etiquetas_que_se_comen_su_contenido():
    """
    La misma trampa la tienen script, textarea, iframe y compania: el
    conversor no borra la etiqueta, borra lo que lleva dentro.
    """
    for etq, dentro in (('script', 'alert(1)'), ('textarea', 'texto dentro'),
                        ('iframe', 'contenido del marco'), ('noscript', 'sin javascript')):
        html = f'<p>Ejemplo:<br>&lt;{etq}&gt;{dentro}&lt;/{etq}&gt;</p>'
        out = converters._convert_with_markdownify(html)
        assert dentro in out, (etq, out)


def test_un_pseudo_marcador_sigue_recuperandose():
    """
    Lo de siempre no se rompe: "<NombreLibreria.NombreClase>" no es una
    etiqueta HTML y se recupera sin escapar, para que otras reglas lo traten.
    """
    html = '<p>Set lObj = CreateObject("&lt;NombreLibreria.NombreClase&gt;")</p>'
    out = converters._convert_with_markdownify(html)
    assert 'NombreLibreria.NombreClase' in out, out


def test_las_clases_del_editor_bloquean_el_estilo_del_tema():
    """
    No es limpieza estetica: Material aplica TODO lo suyo con el selector
    ".md-typeset table:not([class])" —bordes, relleno, cabecera, hover— y
    envuelve la tabla en un md-typeset__scrollwrap con el mismo criterio.

    Una tabla con class="fr-no-borders" deja de cumplirlo, asi que se
    publicaba sin ningun estilo y sin scroll. Y no hay nada que la estilice en
    su lugar: en el CSS del tema no existe una sola regla "fr-". Eran 1.147 de
    2.381 tablas, casi la mitad.
    """
    f = common.quitar_clases_del_editor
    assert f('<table class="fr-no-borders" style="width:100%">') == '<table style="width:100%">'
    assert f('<table class="fr-alternate-rows fr-no-border">') == '<table>'
    assert f('<td class="fr-inner">x</td>') == '<td>x</td>'


def test_una_clase_que_no_es_del_editor_se_conserva():
    """
    Solo se quitan las "fr-*". Si la etiqueta lleva alguna otra, se conserva y
    el atributo se queda: el index.md usa <div class="grid cards"> de Material.
    """
    f = common.quitar_clases_del_editor
    assert f('<table class="fr-no-borders mi-clase">') == '<table class="mi-clase">'
    assert f('<div class="grid cards" markdown>') == '<div class="grid cards" markdown>'
    assert f('<table style="width:100%">') == '<table style="width:100%">'


def test_la_limpieza_de_tablas_incluye_las_clases():
    """
    Va dentro de limpiar_atributos_de_freshdesk, que es por donde pasan las
    tablas conservadas en crudo.
    """
    out = common.limpiar_atributos_de_freshdesk(
        '<table class="fr-alternate-rows"><tr><td class="fr-inner">x</td></tr></table>')
    assert 'fr-' not in out, out
    assert '<table>' in out, out


def test_un_solo_marcador_de_vineta_por_documento():
    """
    La mezcla la produce la propia casa: html2text emite "*" y
    vinetas_literales_a_lista() emite "-". Eran 34 documentos mezclando.

    Se unifica al marcador que YA predomina en ese fichero, no a uno fijo: asi
    solo cambian los que mezclan, en vez de reescribir las 6.895 vinetas del
    corpus por una cuestion de estilo.
    """
    n = chr(10)
    f = converters.unificar_marcadores_de_lista
    assert f('* uno' + n + '* dos' + n + n + '- tres' + n) == '* uno' + n + '* dos' + n + n + '* tres' + n
    assert f('- uno' + n + '- dos' + n + '- tres' + n + n + '* cuatro' + n) == (
        '- uno' + n + '- dos' + n + '- tres' + n + n + '- cuatro' + n)
    # Sin mezcla no se toca nada.
    assert f('* uno' + n + '* dos' + n) == '* uno' + n + '* dos' + n


def test_el_marcador_dominante_se_cuenta_sobre_el_documento_entero():
    """
    Envuelta en _outside_fences, cada trozo entre bloques de codigo elegia SU
    dominante y ocho ficheros seguian mezclando. Por eso la funcion se salta
    los fences ella misma.
    """
    n = chr(10)
    md = ('* uno' + n + '* dos' + n + '* tres' + n + n
          + '```' + n + 'codigo' + n + '```' + n + n
          + '- cuatro' + n)
    out = converters.unificar_marcadores_de_lista(md)
    assert '- cuatro' not in out, out
    assert '* cuatro' in out, out


def test_dentro_de_un_fence_las_vinetas_no_se_tocan():
    """Un "-" dentro de un bloque de codigo es codigo, no una lista."""
    n = chr(10)
    md = '* uno' + n + n + '```' + n + '- dentro del fence' + n + '```' + n + n + '- dos' + n
    out = converters.unificar_marcadores_de_lista(md)
    assert '- dentro del fence' in out, out


def test_ni_el_enfasis_ni_el_separador_son_una_lista():
    """
    El espacio tras el marcador es lo que distingue un item de un "*enfasis*"
    o de un "---" separador.
    """
    n = chr(10)
    f = converters.unificar_marcadores_de_lista
    md = '*enfasis* y mas' + n + '---' + n + '- item' + n + '* otro' + n
    out = f(md)
    assert '*enfasis* y mas' in out, out
    assert n + '---' + n in out, out


def test_una_tabla_conservada_no_lleva_ninguna_clase():
    """
    Al limpiar las de Froala quedaron 6 tablas con clases de otras
    procedencias: MsoNormalTable (Word), varias de Tailwind
    —seguramente contenido pegado desde otra herramienta—,
    ticket-editor-apply-border, table table-sm...

    Ninguna esta definida en ninguna hoja de estilo del sitio —comprobado
    contra extra_css y overrides/— asi que no pintan nada y si estorban: con
    el atributo puesto la tabla pierde todo el estilo del tema y el
    contenedor con scroll.
    """
    f = common.quitar_clases_de_tabla
    assert f('<table class="MsoNormalTable" border="1">') == '<table border="1">'
    assert f('<table class="min-w-full border-collapse text-sm">') == '<table>'
    assert f('<td class="ticket-editor-apply-border">x</td>') == '<td>x</td>'
    assert f('<table border="1">') == '<table border="1">'


def test_solo_se_tocan_las_etiquetas_de_tabla():
    """
    Acotado por etiqueta a proposito: la portada a mano usa
    <div class="grid cards"> de Material, y eso no se toca.
    """
    f = common.quitar_clases_de_tabla
    assert f('<div class="grid cards" markdown>') == '<div class="grid cards" markdown>'
    assert f('<img class="algo" src="x.png">') == '<img class="algo" src="x.png">'


def test_la_limpieza_de_tablas_las_deja_sin_clase():
    """De punta a punta, por donde pasan las tablas conservadas en crudo."""
    out = common.limpiar_atributos_de_freshdesk(
        '<table class="MsoNormalTable"><tr><td class="fr-inner">x</td></tr></table>')
    assert 'class' not in out, out


def test_un_enlace_dentro_de_un_ejemplo_no_se_repara():
    """
    Dentro de un bloque de codigo, un <a href> es texto del ejemplo, no un
    enlace que reparar. fix_internal_links no apartaba el codigo —
    repair_links.py si lo hacia, y su docstring explica por que— asi que la
    regla de anclas lo desenvolvia a su texto visible. Y cuando el ancla solo
    envolvia una imagen, ese texto era VACIO: desaparecia la linea entera del
    ejemplo de HTML.

    Lo encontro la comparacion palabra a palabra del origen contra la salida.
    """
    cerca = chr(96) * 3
    n = chr(10)
    md = ('Texto normal.' + n * 2 + cerca + 'html' + n
          + '<div id="{IdEmpleado}"><a href="{path}/Forms/General/View.aspx">'
          + '<img class="circular" src="../Imagenes/thumbs.aspx?f={foto}" alt="{N}"></a></div>' + n
          + cerca + n)
    out = common.fix_internal_links(md, Path('docs/a/b/c.md'), {}, {}, {}, [0], {})
    assert 'thumbs.aspx' in out, out
    assert 'View.aspx' in out, out
    assert '<img' in out, out


def test_el_codigo_en_linea_tambien_se_aparta():
    """
    Un `[Descrip] [varchar](50) NULL` en linea parece un enlace Markdown y no
    lo es. Es el mismo motivo por el que repair_links.py aparta el codigo.
    """
    tick = chr(96)
    md = f'La columna {tick}[Descrip] [varchar](50) NULL{tick} es obligatoria.'
    out = common.fix_internal_links(md, Path('docs/a/b/c.md'), {}, {}, {}, [0], {})
    assert out == md, out


def test_los_enlaces_de_verdad_siguen_reparandose():
    """
    Apartar el codigo no puede desactivar la reparacion: fuera del bloque, un
    enlace de Freshdesk sigue traduciendose al articulo local.
    """
    cerca = chr(96) * 3
    n = chr(10)
    destino = str(Path('docs/A/B/ERP - Crear nueva empresa.md').resolve())
    url = 'https://ahora.freshdesk.com/support/solutions/articles/44-erp'
    md = (f'Ver [Crear empresa]({url}).' + n * 2
          + cerca + 'html' + n + f'<a href="{url}">ejemplo</a>' + n + cerca + n)
    out = common.fix_internal_links(md, Path('docs/A/B/c.md'), {'44': destino}, {}, {}, [0], {})
    fuera, dentro = out.split(cerca)[0], out.split(cerca)[1]
    assert 'freshdesk' not in fuera, fuera
    assert 'Crear%20nueva%20empresa' in fuera or 'Crear nueva empresa' in fuera, fuera
    # Y dentro del ejemplo la URL se queda tal cual.
    assert url in dentro, dentro


def test_la_caja_de_aviso_de_freshdesk_no_es_codigo():
    """
    Freshdesk dibuja sus avisos con <pre class="fd-callout fd-callout--note">.
    Al ser un <pre>, protect_code_blocks las apartaba como si fueran codigo, y
    eso hacia dos danos: publicaba el texto en gris y monoespaciado, y
    **borraba las imagenes de dentro** —al aislar el codigo se le quitan las
    etiquetas HTML reales—.

    Hay 131 en 58 articulos: note (81), idea (43) e info (7); 3 con imagen.
    """
    f = converters._cajas_de_aviso_de_freshdesk
    html = ('<pre class="fd-callout fd-callout--note">NOTA: hay que revisarlo'
            '<img src="foto.png"></pre>')
    out = f(html)
    assert '<pre' not in out, out
    assert '<img src="foto.png">' in out, out
    assert 'NOTA: hay que revisarlo' in out, out
    # Los tres sabores.
    for tipo in ('note', 'idea', 'info'):
        assert '<pre' not in f(f'<pre class="fd-callout fd-callout--{tipo}">x</pre>')


def test_un_pre_de_codigo_de_verdad_sigue_siendo_codigo():
    """Solo se saca del <pre> lo que lleva la clase fd-callout."""
    f = converters._cajas_de_aviso_de_freshdesk
    for html in ('<pre>SELECT * FROM Clientes</pre>',
                 '<pre class="language-sql line-numbers">SELECT 1</pre>'):
        assert f(html) == html, html


def test_aviso_con_su_texto_en_la_misma_linea():
    """
    Es la forma en que salen las cajas fd-callout una vez dejan de tratarse
    como codigo, y tambien la que escribe el autor a mano: 264 parrafos en 166
    articulos. Publicados quedaban como una negrita suelta a principio de
    parrafo, indistinguible del texto que la rodea.
    """
    n = chr(10)
    f = converters.avisos_en_linea_a_admonitions
    out = f('texto' + n * 2 + '**NOTA:** Si la intercalacion es distinta.' + n * 2 + 'fin')
    assert '!!! note "NOTA"' in out, out
    assert '    Si la intercalacion es distinta.' in out, out
    # Los dos puntos pueden ir fuera de la negrita.
    assert '!!! warning "IMPORTANTE"' in f('a' + n * 2 + '**IMPORTANTE**: es un json.' + n * 2 + 'b')
    # Y la lista que continua el aviso entra en la caja.
    out = f('a' + n * 2 + '**NOTA:** hay varios casos:' + n + '- uno' + n + '- dos' + n * 2 + 'b')
    assert '    - uno' in out and '    - dos' in out, out


def test_el_aviso_tiene_que_ABRIR_el_parrafo():
    """
    A media frase no es un aviso, es una mencion. Y una negrita que no es
    palabra de aviso tampoco se toca.
    """
    n = chr(10)
    f = converters.avisos_en_linea_a_admonitions
    for md in ('En este caso **NOTA:** no abre el parrafo.' + n,
               'a' + n * 2 + '**Resultado:** el total sale mal.' + n * 2 + 'b',
               'a' + n * 2 + '**NOTA:**' + n * 2 + 'b'):
        assert '!!!' not in f(md), md


def test_al_ascender_el_rotulo_la_captura_no_se_pierde():
    """
    Es la misma trampa que en drop_empty_headings: una imagen no aporta texto
    visible, asi que "<p><strong>3. Accedemos a UTILIDADES:</strong><br>
    <img src=...></p>" cumplia el criterio de "todo el texto esta en la
    negrita" y se ascendia DESCARTANDO la captura.

    El rotulo si es un titulo de paso, asi que sube a encabezado y la captura
    queda debajo, que es donde va. Eran 7 imagenes en 6 articulos.
    """
    f = converters.promover_negritas_a_encabezados
    out = f('<p><strong>3. Accedemos a UTILIDADES:</strong><br/><img src="foto.png"></p>')
    assert out == '<h2>3. Accedemos a UTILIDADES:</h2><p><img src="foto.png"></p>', out
    # Tambien cuando la imagen va DENTRO de la negrita.
    out = f('<p><strong>Paso 1<img src="foto.png"></strong></p>')
    assert '<h2>Paso 1</h2>' in out and 'foto.png' in out, out
    # Y con varias.
    out = f('<p><strong>Paso 2</strong><br/><img src="a.png"><img src="b.png"></p>')
    assert 'a.png' in out and 'b.png' in out, out


def test_lo_que_ya_funcionaba_no_cambia():
    """Una negrita sola sigue ascendiendo; con texto detras, sigue sin hacerlo."""
    f = converters.promover_negritas_a_encabezados
    assert f('<p><strong>Requisitos previos</strong></p>') == '<h2>Requisitos previos</h2>'
    original = '<p><strong>Nota</strong> y mas texto</p>'
    assert f(original) == original


def test_la_red_de_seguridad_no_se_come_el_corchete_de_la_imagen():
    """
    El "(?<!!)" cuida de que el patron no empiece EN la imagen, pero no de que
    empiece en el corchete que la ENVUELVE. Con
    "[![](S3-de-freshdesk)](otra-url)" casaba "[![](S3...)" y devolvia como
    texto solo "![", que pegado al resto daba "![](otra-url)": la imagen se
    quedaba apuntando al enlace de fuera y desaparecia.
    """
    S3 = 'https://s3.amazonaws.com/cdn.freshdesk.com/x/foto.png'
    md = f'[![]({S3})](https://www.youtube.com/user/Ahora/)'
    out = common.fix_internal_links(md, Path('docs/a/b/c.md'), {}, {}, {}, [0], {})
    assert 'foto.png' in out, out
    assert '](https://www.youtube.com/user/Ahora/)' in out, out


def test_una_imagen_envuelta_en_un_enlace_a_freshdesk_se_queda_sola():
    """
    El editor enlaza la miniatura a la imagen grande o a la ficha del
    articulo. Ese enlace no lleva a ninguna parte util una vez publicado, y
    mientras esta ahi desordena las reglas de enlaces.
    """
    S3 = 'https://s3.amazonaws.com/cdn.freshdesk.com/x/foto.png'
    FD = 'https://ahora.freshdesk.com/support/solutions/articles/44-x'
    out = common.fix_internal_links(f'[![]({S3})]({FD})', Path('docs/a/b/c.md'),
                                    {}, {}, {}, [0], {})
    assert out.strip() == f'![]({S3})', out


def test_un_enlace_de_texto_a_freshdesk_sigue_degradandose():
    """La red de seguridad no se desactiva: un enlace de texto se queda en texto."""
    FD = 'https://ahora.freshdesk.com/support/solutions/articles/44-x'
    out = common.fix_internal_links(f'[Ver la ficha]({FD})', Path('docs/a/b/c.md'),
                                    {}, {}, {}, [0], {})
    assert 'freshdesk' not in out, out
    assert 'Ver la ficha' in out, out


def test_una_imagen_en_un_enlace_externo_no_se_toca():
    """Un enlace a YouTube o a otro sitio es legitimo: se conserva entero."""
    md = '[![](../img/foto.png)](https://www.youtube.com/x/)'
    out = common.fix_internal_links(md, Path('docs/a/b/c.md'), {}, {}, {}, [0], {})
    assert out == md, out


def test_las_lineas_en_blanco_se_ordenan_al_final_de_la_ejecución():
    """
    El conversor ya las ordena, pero las fases de enlaces corren DESPUES: al
    degradar una URL o quitar un enlace queda la linea vacia detras, y el
    fichero acaba con rachas de tres y cuatro saltos, o con una linea de un
    solo espacio. Eran 5 articulos.

    Lo que se busca no es cosmetica: es que el resultado sea IDEMPOTENTE. Si
    al acabar la ejecución las reglas de limpieza aun tendrian trabajo, el
    fichero no esta en su forma final.
    """
    import tempfile
    from pipeline.repair_links import phase_tidy_blank_lines
    n = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        art = raiz / 'a.md'
        art.write_text('# T' + n * 4 + 'texto' + n + '   ' + n + 'mas' + n, encoding='utf-8')
        assert phase_tidy_blank_lines(raiz) == 1
        salida = art.read_text(encoding='utf-8')
        assert n * 3 not in salida, repr(salida)
        assert n + '   ' + n not in salida, repr(salida)
        # Y ya no queda trabajo: es idempotente.
        assert phase_tidy_blank_lines(raiz) == 0


def test_el_repaso_final_no_toca_los_bloques_de_codigo():
    """Dentro de un fence, una linea con espacios puede ser indentacion."""
    import tempfile
    from pipeline.repair_links import phase_tidy_blank_lines
    n = chr(10); cerca = chr(96) * 3
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        art = raiz / 'a.md'
        codigo = cerca + 'vbnet' + n + 'Sub X()' + n + '    ' + n + '    Dim a' + n + 'End Sub' + n + cerca
        art.write_text('# T' + n * 2 + codigo + n, encoding='utf-8')
        phase_tidy_blank_lines(raiz)
        assert codigo in art.read_text(encoding='utf-8')


def test_el_repaso_final_respeta_only_files():
    """Como las demas fases: en incremental solo se toca lo regenerado."""
    import tempfile
    from pipeline.repair_links import phase_tidy_blank_lines
    n = chr(10)
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        uno = raiz / 'uno.md'; dos = raiz / 'dos.md'
        sucio = '# T' + n * 4 + 'texto' + n
        uno.write_text(sucio, encoding='utf-8'); dos.write_text(sucio, encoding='utf-8')
        assert phase_tidy_blank_lines(raiz, [uno]) == 1
        assert dos.read_text(encoding='utf-8') == sucio


def test_el_enlace_lleva_el_titulo_del_destino():
    """
    Antes se ponia "Enlace Interno", que no le dice nada al lector. En
    "Mensaje 'Element PaymentDetails'" quedaba "Enlace: [Enlace
    Interno](...)" donde el origen traia la URL con su slug
    —asignar-el-tipo-de-efecto-de-la-efactura-a-los-efectos-en-el-erp—, asi
    que la informacion estaba y se tiraba.

    El titulo lo sabemos: acabamos de resolver el destino.
    """
    destino = str(Path('docs/A/B/Asignar el tipo de efecto de la eFactura.md').resolve())
    url = 'https://ahora.freshdesk.com/support/solutions/articles/44001897430-asignar'
    out = common.fix_internal_links(f'Enlace: {url}', Path('docs/A/B/c.md'),
                                    {'44001897430': destino}, {}, {}, [0], {})
    assert '[Asignar el tipo de efecto de la eFactura]' in out, out
    assert 'Enlace Interno' not in out, out


def test_el_titulo_del_destino_pierde_el_sufijo_de_colision():
    """
    Los titulos que colisionan llevan su ArticleId en el nombre del fichero.
    En el texto de un enlace ese numero no aporta nada.
    """
    f = common._titulo_del_destino
    assert f('docs/A/ERP - Crear nueva empresa (154000129759).md') == 'ERP - Crear nueva empresa'
    assert f('docs/A/ERP - Crear nueva empresa.md') == 'ERP - Crear nueva empresa'
    # Y si al quitar el sufijo no queda nada, se cae a lo de antes.
    assert f('docs/A/(154000129759).md') == 'Enlace interno'


def main() -> int:
    tests = [(name, obj) for name, obj in sorted(globals().items())
             if name.startswith('test_') and callable(obj)]

    passed = 0
    failures: list[tuple[str, str]] = []

    for name, test in tests:
        try:
            test()
        except Exception:
            failures.append((name, traceback.format_exc()))
            print(f'FALLA  {name}')
        else:
            passed += 1
            print(f'ok     {name}')

    print(f'\n{passed}/{len(tests)} tests correctos.')
    for name, tb in failures:
        print(f'\n===== {name} =====\n{tb}')

    return 1 if failures else 0



def test_el_enlace_html_a_un_md_hay_que_traducirlo():
    """
    MkDocs reescribe los enlaces Markdown, pero no los <a href> que vienen en
    crudo dentro de una tabla conservada: el HTML en bruto lo aparta antes de
    recorrer el documento. Esos 87 enlaces salian publicados con el .md puesto
    y daban un 404 aunque el articulo estuviera al lado, y no aparecian ni en
    el informe de enlaces rotos —el destino existe— ni en mkdocs build.

    La traduccion es la de use_directory_urls: un nivel mas arriba y sin
    extension.
    """
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        (docs / 'ERP').mkdir(parents=True)
        (docs / 'ERP' / 'Modelo 111.md').write_text('# M', encoding='utf-8')
        origen = docs / 'ERP' / 'Modelos.md'
        origen.write_text('<table><tr><td><a href="Modelo 111.md">Modelo 111</a></td></tr></table>',
                          encoding='utf-8')
        assert links.phase_publish_html_links(docs) == 1
        out = origen.read_text(encoding='utf-8')
        assert 'href="../Modelo%20111/"' in out, out
        assert '>Modelo 111</a>' in out, out


def test_el_destino_se_cierra_con_su_propia_comilla():
    """
    4 articulos enlazan a un .md con un apostrofo en el titulo. Un [^"']* como
    cuerpo del destino cortaba ahi y dejaba el enlace sin traducir.
    """
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        docs.mkdir(parents=True)
        (docs / "Modelos 300 y 390 Gipuzkoa 'Ventanilla unica'.md").write_text('# M', encoding='utf-8')
        origen = docs / 'a.md'
        origen.write_text(
            '<a href="Modelos 300 y 390 Gipuzkoa ' + chr(39) + 'Ventanilla unica' + chr(39) + '.md">V</a>',
            encoding='utf-8')
        assert links.phase_publish_html_links(docs) == 1
        assert '.md"' not in origen.read_text(encoding='utf-8')


def test_el_enlace_html_sin_destino_no_se_traduce():
    """De ese se encarga _desenvolver_anclas_sin_destino: se deja en texto."""
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        docs.mkdir(parents=True)
        origen = docs / 'a.md'
        origen.write_text('<a href="No existe.md">x</a>', encoding='utf-8')
        assert links.phase_publish_html_links(docs) == 0
        assert 'No existe.md' in origen.read_text(encoding='utf-8')


def test_un_encabezado_html_sin_texto_deja_de_ser_encabezado():
    """
    El editor de Freshdesk deja <h2><br/></h2> dentro de las tablas: un hueco
    en el indice lateral y un ancla sin nada que ver. Se desenvuelve en lugar
    de borrarse porque uno de los 8 es un <h1> cuyo unico contenido es una
    captura, y la captura si se ve.
    """
    f = common.desenvolver_encabezados_html_sin_texto
    assert f('<td><p>x</p><h2><br/></h2></td>') == '<td><p>x</p><br/></td>'
    assert f('<h2 style="a: b">&nbsp;</h2>') == '&nbsp;'
    assert '<img src="a.png">' in f('<h1><span><img src="a.png"></span></h1>')
    # Y un encabezado con texto no se toca.
    assert f('<h2>Titulo de verdad</h2>') == '<h2>Titulo de verdad</h2>'



def test_la_forma_publicada_no_parece_un_enlace_muerto():
    """
    Las dos fases nuevas se pisaban: phase_publish_html_links deja el enlace
    como "../X/", y phase_unwrap_dead_links, que solo sabia buscar el fichero
    fuente, lo tomaba por muerto y se comia justo lo que la otra acababa de
    arreglar. La forma publicada se resuelve desde la CARPETA de la pagina, un
    nivel mas abajo que el fichero.
    """
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        (docs / 'ERP').mkdir(parents=True)
        (docs / 'ERP' / 'Modelo 111.md').write_text('# M', encoding='utf-8')
        origen = docs / 'ERP' / 'Modelos.md'
        origen.write_text('<a href="../Modelo%20111/">Modelo 111</a>', encoding='utf-8')
        assert links.phase_unwrap_dead_links(docs) == 0
        assert 'href=' in origen.read_text(encoding='utf-8')


def test_el_md_se_ANADE_al_destino_no_sustituye_su_extension():
    """
    Path.with_suffix se lleva por delante lo que hay tras el ultimo punto, y
    estos titulos van llenos: "ERP - Modelo 369. Declaraciones de IVA...",
    "AHORA Install 4.4.2400 - ...". Cinco destinos buenos parecian no existir
    y sus enlaces se degradaban a texto.
    """
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        (docs / 'ERP').mkdir(parents=True)
        (docs / 'ERP' / 'Modelo 369. Declaraciones de IVA.md').write_text('# M', encoding='utf-8')
        origen = docs / 'ERP' / 'Modelos.md'
        origen.write_text(
            '<a href="../Modelo%20369.%20Declaraciones%20de%20IVA/">369</a>', encoding='utf-8')
        assert links.phase_unwrap_dead_links(docs) == 0
        assert 'href=' in origen.read_text(encoding='utf-8')


def test_la_forma_publicada_sin_destino_si_se_degrada():
    """La red no puede quedarse tan floja que ya no atrape nada."""
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / 'docs'
        (docs / 'ERP').mkdir(parents=True)
        origen = docs / 'ERP' / 'Modelos.md'
        origen.write_text('<a href="../No%20existe/">x</a>', encoding='utf-8')
        assert links.phase_unwrap_dead_links(docs) == 1
        assert origen.read_text(encoding='utf-8') == 'x'



def test_el_video_de_youtube_sobrevive_a_la_conversion():
    """
    Ni html2text ni markdownify saben que hacer con un <iframe>: lo borran con
    todo lo que lleva dentro. En 57 articulos eso dejaba la pagina sin el video
    y sin rastro de que existiera, asi que el lector no podia ni echarlo en
    falta. Son 106 videos, todos de YouTube.
    """
    f = converters.apartar_videos_de_youtube
    html = ('<p>Mira:</p><iframe width="640" height="360" '
            'src="https://www.youtube.com/embed/eybCcon7skM?&amp;wmode=opaque" '
            'frameborder="0" allowfullscreen="" class="fr-draggable"></iframe>')
    out, videos = f(html, {'video': 1})
    assert '<iframe' not in out, out
    assert '<p>%%VIDEO_1%%</p>' in out, out
    # De la URL solo se queda lo que significa algo.
    assert videos['%%VIDEO_1%%'] == 'https://www.youtube.com/embed/eybCcon7skM', videos


def test_de_la_url_del_video_solo_se_guarda_lo_que_significa_algo():
    """
    El editor arrastra wmode=opaque y feature=youtu.be, que no pintan nada, y
    escribe &amp; sin des-escapar. La lista de reproduccion si importa.
    """
    f = converters.apartar_videos_de_youtube
    _, v = f('<iframe src="https://www.youtube.com/embed/ID1?feature=youtu.be&amp;'
             'wmode=opaque"></iframe>', {'video': 1})
    assert v['%%VIDEO_1%%'] == 'https://www.youtube.com/embed/ID1', v
    _, v = f('<iframe src="https://www.youtube.com/embed/ID2?list=PL9&amp;'
             'wmode=opaque"></iframe>', {'video': 1})
    assert v['%%VIDEO_1%%'] == 'https://www.youtube.com/embed/ID2?list=PL9', v


def test_el_video_se_publica_como_reproductor_responsive():
    """
    Los estilos van en linea a proposito: el bloque no depende de que nadie
    anada una hoja de estilos, y una regeneracion que rehaga docs/ no puede
    dejarlo sin ellos. El 56.25% es la proporcion 16:9.
    """
    g = converters.restaurar_videos_de_youtube
    out = g('a' + chr(10) * 2 + '%%VIDEO_1%%' + chr(10) * 2 + 'b',
            {'%%VIDEO_1%%': 'https://www.youtube.com/embed/ID'})
    assert '%%VIDEO' not in out, out
    assert 'padding-bottom: 56.25%' in out, out
    assert 'src="https://www.youtube.com/embed/ID"' in out, out
    assert 'allowfullscreen' in out and 'loading="lazy"' in out, out
    # Y queda a nivel de documento, que es donde Python-Markdown respeta el
    # HTML en crudo: si lo indentara o lo pegara a un parrafo, saldria escapado.
    assert (chr(10) * 2 + '<span style="display: block') in out, out


def test_un_iframe_que_no_es_de_youtube_no_se_toca():
    """La regla no puede convertirse en un pasa-todo de HTML ajeno."""
    f = converters.apartar_videos_de_youtube
    html = '<iframe src="https://ejemplo.local/panel"></iframe>'
    out, videos = f(html, {'video': 1})
    assert out == html and not videos, (out, videos)


def test_los_dos_motores_salvan_el_video():
    """
    La regla tiene que estar enganchada en convert_standard y en convert_author:
    95 de los articulos con video van por el primero, pero no todos.
    """
    html = ('<p>Texto.</p><iframe width="640" height="360" '
            'src="https://www.youtube.com/embed/ABC123?&amp;wmode=opaque"></iframe>')
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        for motor in (converters.convert_standard, converters.convert_author):
            md = motor(html, raiz, raiz / 'a.md', raiz / 'img', 'T', '1', [])
            assert 'youtube.com/embed/ABC123' in md, (motor.__name__, md)
            assert '%%VIDEO' not in md, (motor.__name__, md)



def test_los_adjuntos_del_articulo_quedan_anotados():
    """
    Freshdesk sirve los adjuntos con un enlace firmado de S3 que caduca a los
    5 minutos (X-Amz-Expires=300), asi que el que hay en la base de datos ya
    no vale: responde 403 con firma y sin ella. Las imagenes del cuerpo si son
    publicas, y por eso esas si se descargan.

    No hay nada que descargar y publicar el enlace seria publicar un 404, asi
    que lo unico honesto es dejar constancia. Son 38 ficheros en 27 articulos,
    y varios son contenido de verdad.
    """
    import migrate
    articulo = migrate._parse_article(
        '{"id": 7, "title": "Cambio de servidor", "description": "x",'
        ' "attachments": [{"name": "sacar usuarios SQL.sql", "size": 5379}]}')
    assert articulo.attachments, articulo
    lineas = migrate.lineas_de_adjuntos([articulo])
    texto = chr(10).join(lineas)
    assert 'sacar usuarios SQL.sql' in texto, texto
    assert 'Cambio de servidor' in texto and '(7)' in texto, texto
    # El informe tiene que decir por que no estan, no solo que faltan.
    assert 'caduca' in texto, texto


def test_sin_adjuntos_no_hay_informe():
    """Un informe vacio en la carpeta solo hace dudar de si la ejecución fue bien."""
    import migrate
    sin = migrate._parse_article('{"id": 1, "title": "T", "description": "x"}')
    assert migrate.lineas_de_adjuntos([sin]) == []


def test_el_tamano_del_adjunto_se_lee_a_la_primera():
    """Coma decimal y punto de millares, y MB cuando pasa del mega."""
    import migrate
    f = migrate._tamano_legible
    assert f(5379) == '5,3 KB', f(5379)
    assert f(3145728) == '3,0 MB', f(3145728)
    assert f(None) == '0,0 KB', f(None)
    assert f('no es un numero') == 'tamaño desconocido', f('no es un numero')




def test_un_enlace_que_solo_lleva_una_imagen_no_esta_vacio():
    """
    Las dos reglas de "ancla sin texto" miraban solo el texto: si dentro no
    habia letras, sustituian el ancla por su URL de etiqueta. Con un banner
    dentro eso **se comia la imagen** y publicaba la direccion a pelo.

    Son 7 anclas en 7 articulos; una es el banner del canal de YouTube de los
    Hotfix. Lo encontro la comparacion estructural: 5 imagenes en el origen y
    4 publicadas.
    """
    h = ('<table><tr><td><a href="https://www.youtube.com/user/AhoraSolucionesFree/">'
         '<img src="../img/banner.png"></a></td></tr></table>')
    out = common.fix_internal_links(h, Path('docs/a/b.md'), {}, {}, {}, [0], {})
    assert '<img src="../img/banner.png">' in out, out
    assert '>https://www.youtube.com/user/' not in out, out


def test_el_motor_de_autor_tampoco_se_come_la_imagen_del_enlace():
    """
    markdownify descarta las anclas sin texto, por eso se apartan antes. Pero
    con una imagen dentro sabe convertirlas de sobra, y apartarlas perdia la
    imagen.
    """
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        h = ('<p>Antes.</p><p><a href="https://www.youtube.com/user/Ahora/">'
             '<img src="../img/banner.png"></a></p><p>Despues.</p>')
        for motor in (converters.convert_author, converters.convert_standard):
            md = motor(h, raiz, raiz / 'a.md', raiz / 'img', 'T', '1', [])
            assert '../img/banner.png' in md, (motor.__name__, md)
            assert '](https://www.youtube.com/user/Ahora/)' in md, (motor.__name__, md)


def test_el_ancla_vacia_de_verdad_sigue_llevando_su_etiqueta():
    """
    Sin nada dentro —ni texto ni imagen— el lector no tiene donde pulsar, y
    ahi la URL de etiqueta si es lo mejor que se puede hacer.
    """
    h = '<table><tr><td><a href="https://ejemplo.local/manual"></a></td></tr></table>'
    out = common.fix_internal_links(h, Path('docs/a/b.md'), {}, {}, {}, [0], {})
    assert '<a href="https://ejemplo.local/manual"></a>' not in out, out



def test_el_color_que_no_se_lee_se_suelta():
    """
    El editor de Freshdesk pinta los colores dentro del HTML, y un color en
    linea NO cambia con el tema. Habia verdes y naranjas que sobre el fondo
    claro del sitio daban contraste 1.9: el lector no los veia. Sin color
    propio manda el tema, que se lee en claro y en oscuro.
    """
    f = common.quitar_colores_ilegibles
    assert f('<p><span style="color: rgb(251, 160, 38);">1.-</span></p>') == '<p><span>1.-</span></p>'
    assert 'text-align: center' in f('<td style="text-align: center; color: #999;">x</td>')
    assert 'color' not in f('<td style="text-align: center; color: #999;">x</td>')


def test_un_color_que_si_se_lee_no_se_toca():
    """La regla no es una limpieza de estilos: solo quita lo que no se ve."""
    f = common.quitar_colores_ilegibles
    for html in ('<span style="color: rgb(40, 50, 78);">Azul oscuro</span>',
                 '<p style="color: black;">Texto normal</p>',
                 '<p>Sin estilos</p>'):
        assert f(html) == html, html


def test_si_el_fondo_lo_pone_el_autor_el_par_se_respeta():
    """
    Una celda de color con letra oscura dentro la decidio el autor y funciona
    igual en los dos modos: ahi no hay nada que arreglar.
    """
    f = common.quitar_colores_ilegibles
    html = ('<td style="background-color: rgb(40,50,78);">'
            '<span style="color: rgb(251, 160, 38);">x</span></td>')
    out = f(html)
    # El naranja sobre el azul oscuro se lee: no se toca.
    assert 'color: rgb(251, 160, 38)' in out, out
    # A la celda si se le pone letra: lo que caiga directamente en ella, sin
    # color propio, recibiria el texto oscuro del tema sobre un fondo oscuro.
    assert 'color: #ffffff' in out, out


def test_quitar_el_color_solo_sirve_si_detras_manda_el_tema():
    """
    En "Cierres de Inventario" la celda pone ``color: black``, asi que soltar
    el verde de dentro dejaba negro sobre negro en modo oscuro. Se sueltan los
    dos: sobre fondo claro el negro no aporta nada —es el color que ya pone el
    tema— y sobre el oscuro es justo lo que no deja leer.
    """
    f = common.quitar_colores_ilegibles
    out = f('<td style="color: black; font-size: 15px;">'
            '<span style="color: rgb(97, 189, 109);">5,66</span></td>')
    assert 'color: black' not in out, out
    assert 'rgb(97, 189, 109)' not in out, out
    assert 'font-size: 15px' in out, out
    # Pero si ese negro cuelga de un fondo a mano, es lo unico que hace
    # legible la celda y no se toca.
    dentro = ('<div style="background-color: rgb(0,0,0);">'
              '<td style="color: black;"><span style="color: rgb(97, 189, 109);">x</span></td></div>')
    assert 'color: black' in f(dentro), f(dentro)


def test_un_fondo_a_mano_sin_letra_recibe_una_letra():
    """
    Con el fondo fijado y sin color de letra, en modo claro le cae encima el
    texto oscuro del tema. Si el fondo es oscuro, no se lee.
    """
    f = common.quitar_colores_ilegibles
    out = f('<td style="background-color: rgb(0, 0, 0);">Texto</td>')
    assert 'color: #ffffff' in out, out


def test_rgba_transparente_no_es_negro():
    """
    ``rgba(0, 0, 0, 0)`` es transparente, y el editor lo escribe a punta pala
    para decir "sin fondo". Tomarlo por negro hacia creer que habia texto
    oscuro sobre negro donde no hay fondo ninguno.
    """
    assert common._a_rgb('rgba(0, 0, 0, 0)') is None
    assert common._a_rgb('rgba(0, 0, 0, 0.5)') == (0, 0, 0)
    assert common._a_rgb('var(--theme-hyperlink)') is None



def test_la_primera_fila_que_hace_de_cabecera_pasa_a_th():
    """
    El editor de Freshdesk no distingue cabecera de dato: escribe todo en
    <td> y marca la primera fila con negrita o fondo. El tema no tiene forma
    de saber que eso es una cabecera, asi que no la destaca ni la separa.
    """
    f = common.ascender_cabecera_de_tabla
    datos = ('<table><tr><td style="background-color: rgb(239,239,239);"><strong>Cliente</strong></td>'
             '<td style="background-color: rgb(239,239,239);"><strong>Tipo</strong></td></tr>'
             '<tr><td>a</td><td>b</td></tr><tr><td>c</td><td>d</td></tr></table>')
    out = f(datos)
    assert out.count('<th') == 2, out
    assert 'Cliente' in out and 'Tipo' in out, out


def test_la_tabla_de_maquetado_no_lleva_cabecera():
    """
    El liston es alto a proposito: 41 tablas de datos frente a 970 de
    maquetado, que no necesitan cabecera ninguna.
    """
    f = common.ascender_cabecera_de_tabla
    for html in ('<table><tr><td>solo texto</td></tr><tr><td>mas</td></tr><tr><td>y mas</td></tr></table>',
                 '<table><tr><td><strong>A</strong></td><td><strong>B</strong></td></tr>'
                 '<tr><td>1</td><td>2</td></tr></table>',
                 '<table><tr><th>A</th><th>B</th></tr><tr><td>1</td><td>2</td></tr>'
                 '<tr><td>3</td><td>4</td></tr></table>'):
        assert f(html) == html, html


def test_los_pasos_numerados_a_mano_se_hacen_lista():
    """
    El origen trae parrafos sueltos que empiezan por un numero en negrita. La
    negrita impide que Markdown los reconozca, asi que se publican como
    parrafos independientes, sin sangria colgante y sin que se vea que son los
    pasos de un mismo procedimiento.
    """
    f = converters.pasos_numerados_a_lista
    nl = chr(10)
    out = f('Intro:' + nl * 2 + '**1.IBAN** informado.' + nl * 2
            + '**2.** El banco con **SWIFT**.' + nl * 2 + '**3.** Marcada como **activa**.')
    assert '1. **IBAN** informado.' in out, out
    assert '2. El banco con **SWIFT**.' in out, out
    # Apretada: con linea en blanco entre items la lista sale con el mismo
    # aire suelto que tenian los parrafos.
    assert nl + '2. ' in out and nl * 2 + '2. ' not in out, out


def test_el_separador_doble_no_se_queda_de_texto():
    """``**1.-** En la primera opcion`` dejaba un ``1. **-** En la primera``."""
    f = converters.pasos_numerados_a_lista
    nl = chr(10)
    out = f('**1.-** uno' + nl * 2 + '**2.-** dos' + nl * 2 + '**3.-** tres')
    assert out == '1. uno' + nl + '2. dos' + nl + '3. tres', out


def test_una_racha_que_no_empieza_en_1_se_queda_como_esta():
    """
    Python-Markdown no emite ``start``, asi que una racha que empieza en el 12
    saldria renumerada desde el 1 y diria otra cosa. Y con dos seguidos puede
    ser casualidad.
    """
    f = converters.pasos_numerados_a_lista
    nl = chr(10)
    for md in ('**3.** a' + nl * 2 + '**4.** b' + nl * 2 + '**5.** c',
               '**1.** a' + nl * 2 + '**2.** b',
               '**1.** a' + nl * 2 + '**5.** b' + nl * 2 + '**9.** c'):
        assert f(md) == md, md


def test_el_indice_a_mano_se_convierte_en_enlaces():
    """
    136 articulos abren con un indice escrito a mano y NINGUNO tiene un solo
    enlace: el lector lo lee, intenta pulsarlo y no pasa nada.
    """
    f = converters.enlazar_indice_a_las_secciones
    nl = chr(10)
    out = f('# T' + nl * 2 + '## Índice' + nl * 2 + '  * Configuración previa' + nl
            + '  * No existe' + nl * 2 + '## Configuración previa' + nl * 2 + 'x')
    assert '[Configuración previa](#configuracion-previa)' in out, out
    # Lo que no case con una seccion se queda en texto: un enlace a ninguna
    # parte es peor que ningun enlace.
    assert '  * No existe' in out, out


def test_el_ancla_se_le_pide_a_markdown_no_se_adivina():
    """
    ``## _Configuracion de_ **_ _ERP_**`` acaba siendo ``configuracion-de-_erp``.
    Aproximar el texto quitando asteriscos daba ``configuracion-de-erp`` y
    dejaba 6 enlaces apuntando a un ancla que no existe.
    """
    f = converters.enlazar_indice_a_las_secciones
    nl = chr(10)
    out = f('# T' + nl * 2 + '## Índice' + nl * 2 + '  * Configuración de ERP' + nl * 2
            + '## _Configuración de_ **_ _ERP_**' + nl * 2 + 'x')
    assert '(#configuracion-de-_erp)' in out, out


def test_el_indice_acaba_donde_acaban_sus_puntos():
    """
    Cortar solo al llegar al siguiente encabezado dejaba la regla suelta por
    el resto del articulo: llego a enlazar un ``* ## TBAI`` veinte parrafos
    mas abajo.
    """
    f = converters.enlazar_indice_a_las_secciones
    nl = chr(10)
    out = f('# T' + nl * 2 + '## Índice' + nl * 2 + '  * Uno' + nl * 2 + 'texto normal'
            + nl * 2 + '  * Uno' + nl * 2 + '## Uno' + nl * 2 + 'x')
    assert out.count('](#uno)') == 1, out


def test_el_texto_del_punto_no_se_toca_al_enlazarlo():
    """
    Limpiarlo se llevaba por delante los guiones bajos de ``Ahora_Impresion``,
    que no son enfasis sino parte del nombre. Y un asterisco suelto
    —``Veri*Factu``— desaparece en cuanto el texto entra en un enlace.
    """
    f = converters.enlazar_indice_a_las_secciones
    nl = chr(10)
    out = f('# T' + nl * 2 + '## Índice' + nl * 2 + '  * Módulo Ahora_Impresion' + nl * 2
            + '## Módulo Ahora_Impresion' + nl * 2 + 'x')
    assert '[Módulo Ahora_Impresion]' in out, out
    out = f('# T' + nl * 2 + '## Índice' + nl * 2 + '  * Veri*Factu' + nl * 2
            + '## Veri*Factu' + nl * 2 + 'x')
    assert '[Veri' + chr(92) + '*Factu]' in out, out


def test_el_indice_sangrado_sale_del_bloque_de_codigo():
    """
    Con cuatro espacios o mas, Markdown no ve una lista: ve un BLOQUE DE
    CODIGO, y el indice se publica en gris y monoespaciado con los asteriscos
    a la vista. Manda la sangria del primer punto, no la menor: Markdown lee
    de arriba abajo.
    """
    f = converters.desangrar_el_indice
    nl = chr(10)
    out = f('# T' + nl * 2 + '## Índice' + nl * 2 + '    * Uno' + nl + '      * Uno.a'
            + nl + '  * Dos' + nl * 2 + '## Uno')
    assert nl + '* Uno' + nl in out, out
    assert nl + '  * Uno.a' + nl in out, out     # el subnivel conserva su distancia
    # Una lista que ya es lista no se toca.
    sana = '# T' + nl * 2 + '## Índice' + nl * 2 + '  * Uno' + nl + '  * Dos'
    assert f(sana) == sana



def test_el_codigo_metido_en_un_parrafo_de_prosa_sale_a_un_pre():
    """
    El origen escribe la explicacion y la instruccion en el MISMO parrafo,
    separadas por <br>. Publicado, las llamadas salian como prosa: sin
    monoespaciado, sin resaltado y sin distinguirse de la frase que las
    explica. Son 537 lineas en 107 articulos.
    """
    f = common.codigo_suelto_en_parrafo_a_pre
    out = f('<p>Instrucción para cambiar el puntero.<br><br>'
            'gCn.Obj.HourglassAll(true)<br><br>gCn.Obj.HourglassAll(False)</p>')
    assert '<pre><code>gCn.Obj.HourglassAll(true)' in out, out
    assert '<p>Instrucción para cambiar el puntero.</p>' in out, out


def test_una_descripcion_de_parametro_no_es_codigo():
    """
    El criterio es estrecho a proposito: sin el, ``Campo (STRING): nombre del
    campo`` pasaba por codigo y salian 1.615 falsos positivos en vez de 537.
    """
    f = common.codigo_suelto_en_parrafo_a_pre
    for html in ('<p>Campo (STRING): Especifica el nombre del campo.<br>'
                 'Format (STRING): Indica el formato.</p>',
                 '<p>Una frase.<br>Otra frase distinta.</p>',
                 '<p>Sin saltos de linea.</p>'):
        assert f(html) == html, html


def test_el_ancla_vacia_que_repite_un_enlace_se_borra():
    """
    El editor deja anclas sin nada dentro, y la regla que las etiqueta con su
    URL las convertia en un enlace mas: la misma direccion repetida dos y tres
    veces seguidas. Son 62 en 39 articulos.
    """
    f = common.quitar_anclas_vacias_repetidas
    out = f('<p><a href="https://we.tl/x"></a><a href="https://we.tl/x"></a>'
            '<a href="https://we.tl/x">Descarga</a></p>')
    assert out.count('<a ') == 1, out
    assert '>Descarga<' in out, out
    # Dos vacias al mismo sitio: se queda la primera.
    out = f('<p><a href="http://v/x"></a></p><p><a href="http://v/x"></a></p>')
    assert out.count('<a ') == 1, out


def test_el_ancla_vacia_sin_pareja_se_respeta():
    """Ahi la URL es lo unico que se puede enseñar."""
    f = common.quitar_anclas_vacias_repetidas
    html = '<p><a href="http://videos.ahora.es/ScriptSamples#112"></a></p>'
    assert f(html) == html


def test_el_ancla_con_imagen_no_se_borra_a_si_misma():
    """
    Una imagen dentro SI es contenido. Sin esta salvedad el ancla de un banner
    se borraba sola, porque su propio destino figuraba en la lista de los que
    tienen contenido.
    """
    f = common.quitar_anclas_vacias_repetidas
    html = '<a href="http://v/x"><img src="banner.png"></a>'
    assert '<img' in f(html), f(html)



def test_se_reconocen_las_cuatro_formas_de_enlazar_un_video():
    """
    El corpus enlaza vídeos de cuatro maneras —incrustado, watch, youtu.be y
    lista de reproducción— más el servidor propio de la casa. Si una forma se
    escapa, ese vídeo no se comprueba nunca.
    """
    casos = {
        '<iframe src="https://www.youtube.com/embed/ABC123?list=PL9"></iframe>':
            'https://www.youtube.com/embed/ABC123?list=PL9',
        'ver [aquí](https://www.youtube.com/watch?v=Lvd04LOBz-I)':
            'https://www.youtube.com/watch?v=Lvd04LOBz-I',
        'corto https://youtu.be/KNthectkFT4 fin':
            'https://youtu.be/KNthectkFT4',
        'lista https://www.youtube.com/playlist?list=PL8h4jt35t1wi fin':
            'https://www.youtube.com/playlist?list=PL8h4jt35t1wi',
        'propio http://videos.ahora.es/ScriptSamples#112 fin':
            'http://videos.ahora.es/ScriptSamples#112',
    }
    for texto, esperado in casos.items():
        encontrados = [m.group(0) for rx in common._VIDEOS_ENLAZADOS_RX
                       for m in rx.finditer(texto)]
        assert esperado in encontrados, (texto, encontrados)


def test_la_url_del_video_no_se_lleva_lo_que_tiene_pegado():
    """
    Un ``>`` pegado al final hacía que la lista ``...npR>`` diera 404 y saliera
    en el informe como una lista de reproducción borrada que no lo estaba.
    """
    texto = 'ver <https://www.youtube.com/playlist?list=PL8h4jt35t1wixmi>'
    for rx in common._VIDEOS_ENLAZADOS_RX:
        for m in rx.finditer(texto):
            assert '>' not in m.group(0), m.group(0)


def test_un_servidor_caido_se_prueba_una_sola_vez():
    """
    Los 44 enlaces a ``videos.ahora.es`` esperarían seis segundos cada uno. El
    veredicto del servidor vale para todos sus enlaces, y así la comprobación
    no alarga la ejecución.
    """
    caidos = {'videos.ahora.es'}
    se_ve, motivo = common._se_ve_el_video('http://videos.ahora.es/Manual/10', caidos)
    assert se_ve is False, (se_ve, motivo)
    assert motivo == 'el servidor no responde', motivo



def test_el_sql_metido_en_un_parrafo_tambien_sale_a_un_pre():
    """
    La forma mas comun del T-SQL en esta casa es la lista de parametros de un
    procedimiento, cada uno con su comentario detras. Publicada como prosa se
    lee fatal: sin monoespaciado no se ve donde acaba un parametro y empieza
    el siguiente.
    """
    f = common.codigo_suelto_en_parrafo_a_pre
    out = f('<p>Con esta instrucción situamos el campo:<br>zInsertaCampoTabla<br>'
            '@Tabla NVARCHAR(1000), -- Tabla en la que se quiere insertar el campo<br>'
            '@Nullable BIT, -- Si acepta o no valores NULL</p>')
    assert '<pre><code>@Tabla NVARCHAR(1000)' in out, out
    assert '@Nullable BIT' in out, out


def test_el_comentario_en_castellano_no_saca_al_sql_de_su_sitio():
    """
    ``@CadenaDefault NVARCHAR(1000) = N'', -- Valor por defecto para el nuevo
    campo`` lleva "para" dentro. El filtro de prosa, pensado para el VB, lo
    habria partido en dos: media lista en un bloque y media en otro.
    """
    assert common._es_sentencia(
        "@CadenaDefault NVARCHAR(1000) = N'', -- Valor por defecto para el nuevo campo")


def test_el_xml_literal_del_codigo_se_conserva():
    """
    Quitar "toda etiqueta" para leer el trozo se llevaba por delante el XML de
    los ejemplos de webservice: un articulo perdio 579 de sus 815 palabras.
    Solo se quita el formato que mete el editor.
    """
    t = common._solo_texto_del_trozo(
        '<span>request = "&lt;soap:Envelope xmlns:soap=x&gt;"</span>')
    assert t == 'request = "<soap:Envelope xmlns:soap=x>"', t



def test_la_sentencia_que_va_sola_en_su_hueco_se_marca_como_codigo():
    """
    El origen deja instrucciones sueltas en su propio parrafo, en una celda o
    en un punto de lista, sin nada que las distinga de la prosa. Son 426
    huecos en 75 articulos.
    """
    f = common.sentencia_suelta_a_codigo
    assert f('<p><em>SELECT * FROM Conta_Apuntes</em></p>') == \
        '<p><code>SELECT * FROM Conta_Apuntes</code></p>'
    assert f("<li>UPDATE Ceesi_configuracion SET Valor = 'ON'</li>") == \
        "<li><code>UPDATE Ceesi_configuracion SET Valor = 'ON'</code></li>"
    assert f('<td>gform.ControlesDDA("NombreControl").Text</td>') == \
        '<td><code>gform.ControlesDDA("NombreControl").Text</code></td>'


def test_la_regla_baja_a_buscar_dentro():
    """
    Dos formas en las que el codigo no esta a primer nivel: la tabla de
    referencia mete cada ejemplo en su propio <p> dentro de la celda, y la
    consulta viene en cursiva dentro de un parrafo con mas texto. Sin bajar,
    la celda se descartaba entera con sus 31 ejemplos y las 41 cursivas se
    quedaban fuera.
    """
    f = common.sentencia_suelta_a_codigo
    out = f('<td width="300"><p>Set lCol = gcn.DamenewCollection</p></td>')
    assert '<p><code>Set lCol = gcn.DamenewCollection</code></p>' in out, out
    out = f('<p>Consulta: <em>SELECT * FROM Ceesi_Edi_Tipos</em> y mira.</p>')
    assert out == '<p>Consulta: <code>SELECT * FROM Ceesi_Edi_Tipos</code> y mira.</p>', out


def test_la_enfasis_desaparece_al_marcar_el_codigo():
    """Una consulta en cursiva Y monoespaciada es peor que cualquiera de las dos."""
    f = common.sentencia_suelta_a_codigo
    out = f('<p><strong>select * from CEESI_Informes where idInforme = 128</strong></p>')
    assert '<strong>' not in out and '<code>' in out, out


def test_una_frase_que_habla_de_codigo_no_es_codigo():
    """
    ``INSERT INTO: se usa para anadir uno o varios registros`` es una frase que
    explica el INSERT. Aqui el filtro de prosa se aplica tambien al SQL.
    """
    f = common.sentencia_suelta_a_codigo
    for html in ('<li>INSERT INTO: se usa para añadir uno o varios registros a una tabla</li>',
                 '<p>Este párrafo es prosa normal y corriente del artículo.</p>',
                 '<p>Texto <strong>importante</strong> normal.</p>'):
        assert f(html) == html, html



def test_una_linea_de_un_bloque_no_es_una_sentencia_suelta():
    """
    Si el hueco de al lado tambien es una sentencia, esto es una linea de un
    bloque, y ese bloque lo reconstruye despues repair_vb_reference_markdown
    en un fence. Marcando la primera linea por su cuenta se rompia esa
    reconstruccion: en "Tipos de JOIN en el FROM" el CREATE TABLE se llevo el
    fence entero y dejo las columnas de prosa, con
    ``[Descrip] [varchar](50) NULL`` publicado como un ENLACE ROTO.
    """
    f = common.sentencia_suelta_a_codigo
    # Se queda a medias: la linea siguiente la continua.
    md = '<p>CREATE TABLE [dbo].[Tab](</p><p>[Id] [int] NOT NULL,</p>'
    assert f(md) == md, f(md)
    # Dos sentencias seguidas: es un bloque.
    md = '<p>SELECT * FROM Tab_A</p><p>SELECT * FROM Tab_B</p>'
    assert f(md) == md, f(md)
    # Y una sola, rodeada de prosa, si se marca.
    out = f('<p>Ejemplo.</p><p>SELECT * FROM Tab_A</p><p>Fin.</p>')
    assert '<p><code>SELECT * FROM Tab_A</code></p>' in out, out


def test_una_consulta_partida_en_parrafos_no_se_marca_a_trozos():
    """
    En "ERP - Asignacion de centros de coste" una consulta viene partida en
    cinco parrafos. Solo el del medio empieza por algo con pinta de
    sentencia, asi que se marcaba ese y quedaba una linea monoespaciada
    suelta dentro de una consulta que por lo demas iba en texto plano: peor
    que dejarla entera. Una clausula suelta —from, inner join, on, where—
    continua la sentencia anterior, no empieza otra.
    """
    f = common.sentencia_suelta_a_codigo
    md = ('<p><strong>Factura:</strong> select top 1 Del.CentroCoste</p>'
          '<p>from Delegaciones Del inner join Series_Facturacion_Prov sf on</p>'
          '<p>sf.IdDelegacion = del.IdDelegacion inner join Facturas_Prov_Cab fpc</p>'
          '<p>on fpc.SerieFactura = sf.SerieFactura</p>')
    assert f(md) == md, f(md)


def test_la_tabla_que_se_publicaria_vacia_se_tira():
    """
    El editor de Freshdesk maqueta con tablas y quedan restos: una fila con
    celdas que solo llevan un <br> o un espacio duro. Material le pinta su
    borde, asi que sale un recuadro vacio en mitad del articulo.
    """
    f = common.quitar_tablas_vacias
    assert f('<p>a</p><table><tbody><tr><td><br/></td></tr></tbody></table><p>b</p>') == '<p>a</p><p>b</p>'
    assert f('<table><tbody><tr><td>&nbsp;</td></tr></tbody></table>') == ''
    # Lo que se ve sin llevar una letra no se toca.
    con_imagen = '<table><tbody><tr><td><img src="x.png"/></td></tr></tbody></table>'
    assert f(con_imagen) == con_imagen
    con_texto = '<table><tbody><tr><td>Hola</td></tr></tbody></table>'
    assert f(con_texto) == con_texto
    # Anidada: en 'ERP - Declaracion INTRASTAT' la tabla vacia cuelga de la
    # misma celda que la captura. La de fuera se queda, la de dentro sobra.
    anidada = ('<table><tbody><tr><td><img src="x.png"/>'
               '<table><tbody><tr><td></td></tr></tbody></table>'
               '</td></tr></tbody></table>')
    fuera = f(anidada)
    assert '<img src="x.png"/>' in fuera, fuera
    assert fuera.count('<table') == 1, fuera
    # Y es idempotente.
    uno = f('<p>a</p><table><tbody><tr><td> </td></tr></tbody></table>')
    assert f(uno) == uno


def test_en_una_celda_la_consulta_partida_se_marca_entera():
    """
    Fuera, una consulta partida en varios parrafos se deja en paz porque el
    fence lo reconstruye repair_vb_reference_markdown. Dentro de una celda no
    hay fence que reconstruir —la tabla se conserva en HTML tal cual—, asi
    que ahi se marca linea a linea. Es "ERP - Centros de Coste Automaticos",
    donde cada fila lleva su consulta en tres <p>.
    """
    f = common.sentencia_suelta_a_codigo
    celda = ('<table><tr><td><p>Select cd.Padre from clientes_datos cd</p>'
             '<p>inner join Pedidos_Cli_Cabecera pcc</p>'
             '<p>on pcc.IdCliente = cd.IdCliente where pcc.IdPedido =</p>'
             '</td></tr></table>')
    salida = f(celda)
    assert salida.count('<code>') == 3, salida
    assert f(salida) == salida, 'no es idempotente'

    # La tirada se encadena tambien por la linea que se queda a medias: en el
    # Hotfix 74 la lista de columnas pelada no tiene forma de sentencia, pero
    # la de arriba acaba en coma, asi que la termina.
    hotfix = ('<table><tr><td>'
              '<p><em>INSERT INTO Ofertas_Cli_Totales_Bases (IdOferta, Revision,</em></p>'
              '<p><em>IVAEuros, IVAMoneda, TotalBaseMoneda)</em></p>'
              '<p><em>SELECT O.IdOferta , O.Revision , K.IdIva</em></p>'
              '</td></tr></table>')
    otra = f(hotfix)
    assert otra.count('<code>') == 3, otra
    assert '<em>' not in otra, otra
    assert f(otra) == otra, 'no es idempotente'


def test_la_etiqueta_del_lenguaje_cuelga_del_miembro():
    """
    Los articulos de referencia describen miembro a miembro y cada uno trae
    su ejemplo en dos lenguajes, escritos con el mismo nivel que el miembro o
    con uno mas alto. Asi "Codigo en VB6" gobernaba al miembro SIGUIENTE en
    vez de colgar del anterior: el indice de "Grid - Todo lo que debes saber"
    pasaba de 56 entradas utiles a 150, con 96 etiquetas tapando los miembros.
    """
    f = converters.encajar_etiquetas_de_codigo
    md = '\n'.join([
        '# T', '', '## GridUsuario', '', '### EditarPorObjeto', '',
        'Descripcion.', '', '## Codigo en VB6', '', r'## Codigo en C\#', '',
        '### EditarPorObjetoyVista', '',
    ])
    salida = f(md)
    assert '#### Codigo en VB6' in salida, salida
    assert r'#### Codigo en C\#' in salida, salida
    assert '### EditarPorObjetoyVista' in salida, salida
    assert f(salida) == salida, 'no es idempotente'

    # Nunca sube de nivel: la que ya cuelga bien se queda. Y un "Ejemplo" o
    # un "Codigo" a secas si pueden ser una seccion de verdad.
    ok = '\n'.join(['# T', '', '## Miembro', '', '### Codigo en VB6', '',
                    '## Ejemplo', '', '## Codigo', ''])
    assert f(ok) == ok, f(ok)


def test_un_encabezado_que_solo_lleva_el_video_no_es_un_encabezado():
    """
    En "ERP - Importador de Excel" el origen trae
    ``<h1><span class="fr-video"><iframe ...></span></h1>``. La regla que
    desenvuelve los encabezados sin texto solo se aplicaba a las tablas
    conservadas, asi que ese h1 llegaba entero al motor: el video se apartaba
    a un token —que SI es texto—, html2text emitia "# %%VIDEO_1%%" y al
    restaurarlo quedaba un "# " vacio en la pagina, el unico de todo el
    corpus. Ahora la regla se aplica al documento entero.
    """
    f = common.desenvolver_encabezados_html_sin_texto
    solo_video = ('<h1><span class="fr-video"><iframe src="https://www.youtube.com/'
                  'embed/VZVW3zkRcdI"></iframe></span></h1>')
    salida = f(solo_video)
    assert '<h1>' not in salida, salida
    assert '<iframe' in salida, salida

    # El que si tiene texto no se toca, aunque lleve un video dentro.
    con_texto = '<h2>Importador de Excel</h2>'
    assert f(con_texto) == con_texto


def test_imagenes_huerfanas_respeta_lo_que_menciona_cualquiera():
    """
    Una imagen sobra cuando NO la menciona nadie. Y "nadie" no son solo los
    articulos: mkdocs.yml declara el logo y el favicon, y una hoja de estilos
    puede traer un url(). Sin mirar ahi, la primera ejecución con
    --prune-orphans se llevaria por delante el logo del tema.
    """
    import migrate
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        docs = raiz / 'docs'
        imgs = docs / 'docs_assets' / 'images'
        (imgs / 'logos').mkdir(parents=True)
        (docs / 'ERP').mkdir()

        for nombre in ('usada.png', 'sobra.png', 'en_css.png'):
            (imgs / nombre).write_bytes(b'x')
        (imgs / 'logos' / 'marca.svg').write_bytes(b'x')

        (docs / 'ERP' / 'art.md').write_text(
            '# T\n\n![](../docs_assets/images/usada.png)\n', encoding='utf-8')
        (docs / 'estilo.css').write_text(
            'body{background:url(../docs_assets/images/en_css.png)}', encoding='utf-8')
        (raiz / 'mkdocs.yml').write_text(
            'theme:\n  logo: docs_assets/images/logos/marca.svg\n', encoding='utf-8')

        anterior = Path.cwd()
        try:
            os.chdir(raiz)
            huerfanas = migrate.buscar_imagenes_huerfanas(docs, imgs)
        finally:
            os.chdir(anterior)

    nombres = sorted(f.name for f in huerfanas)
    assert nombres == ['sobra.png'], nombres


def test_la_vineta_con_dos_espacios_tambien_se_unifica():
    """
    Markdown admite de uno a cuatro espacios entre la vineta y el texto.
    Exigiendo exactamente uno, una vineta como ``-  Incobrable`` no se
    contaba ni se cambiaba, y dos articulos seguian mezclando ``*`` y ``-``.
    Mezclar no es solo desorden: Python-Markdown funde las dos listas en una
    suelta y unos items salen espaciados y otros apretados.
    """
    f = converters.unificar_marcadores_de_lista
    md = '\n'.join([
        '* Dudoso cobro: paso posterior al impagado.',
        '',
        '-  Incobrable: estado posterior al dudoso cobro.',
        '',
        '* Compensacion: check que informa de la compensacion.',
        '',
    ])
    salida = f(md)
    assert '-  Incobrable' not in salida, salida
    assert '* Incobrable' in salida, salida
    assert f(salida) == salida, 'no es idempotente'


def test_el_lenguaje_de_un_bloque_se_decide_por_recuento():
    """
    Dos senales debiles con prioridad absoluta ganaban a un recuento
    abrumador de la correcta: un ``window.o`` suelto dentro de un script de
    66 sentencias T-SQL publicaba el bloque como JavaScript, y la llave
    suelta ``}`` —que PowerShell usa igual que C#— dejaba un script de
    PowerShell etiquetado como csharp.
    """
    f = converters.detect_code_lang

    sql_con_ruido = '\n'.join([
        'ALTER TABLE [dbo].[Pers_Clientes] DROP CONSTRAINT [FK_Pers];',
        'GO',
        "-- ojo con window.oferta al migrar",
        'CREATE TABLE [dbo].[Pers_Clientes] (Id int);',
        'SELECT * FROM Pers_Clientes;',
    ])
    assert f(sql_con_ruido) == 'sql', f(sql_con_ruido)

    powershell = '\n'.join([
        '$Servicio = "AHORA API 500_H75"',
        '$Estado = Get-Service -Name $Servicio -ErrorAction SilentlyContinue',
        'if ($Estado -and $Estado.Status -ne "Running") {',
        '    Start-Service -Name $Servicio',
        '}',
    ])
    assert f(powershell) == 'powershell', f(powershell)

    # T-SQL de administracion: sin USE, GO ni IF EXISTS( entre los marcadores,
    # estos bloques caian en csharp por el punto y coma, o en vbnet.
    admin = chr(10).join([
        'USE master;',
        'GO',
        "sp_configure 'show advanced options', 1;",
        'ALTER DATABASE DEMOS SET RECOVERY SIMPLE;',
    ])
    assert f(admin) == 'sql', f(admin)

    disparador = chr(10).join([
        'IF EXISTS(SELECT 1 FROM inserted) BEGIN',
        'UPDATE C SET Descuento = 100 FROM Contactos C;',
        'END',
    ])
    assert f(disparador) == 'sql', f(disparador)


def test_un_enlace_no_se_encierra_en_un_bloque_de_codigo():
    """
    La reconstruccion de bloques sueltos toma por codigo cualquier linea que
    empiece por comillas, y en "Reglas de No Sujecion en SII, VeriFactu y
    TicketBAI" eso envolvia una tabla de equivalencias entera. Dentro iba un
    enlace a la Agencia Tributaria que, publicado como texto literal, no se
    puede pulsar. El codigo reconstruido nunca lleva enlaces Markdown, asi
    que su presencia delata que esto es prosa.
    """
    f = converters.repair_vb_reference_markdown
    md = '\n'.join([
        'Se podria establecer la siguiente equivalencia:',
        '',
        '"OT" en TicketBAI -> N1 en VeriFactu',
        '"RL" e "IE" en TicketBAI -> N2 en VeriFactu',
        '"VT" NO se corresponde - [Enlace](https://sede.agenciatributaria.gob.es/x.html).',
        '',
    ])
    salida = f(md)
    assert '```' not in salida, salida
    assert '[Enlace](https://sede.agenciatributaria.gob.es/x.html)' in salida, salida


def test_un_bloque_reconstruido_no_es_VB_por_defecto():
    """
    ``flush_run`` fijaba ``vbnet`` a mano. Y como el retag de mas arriba solo
    toca los fences SIN lenguaje, un T-SQL suelto se quedaba con resaltado de
    VB para siempre, por mucho que el detector supiera distinguirlo.
    """
    f = converters.repair_vb_reference_markdown
    md = '\n'.join([
        'Ejemplo de disparador:',
        '',
        'IF EXISTS(SELECT 1 FROM inserted)',
        'UPDATE C SET Descuento = 100 FROM Contactos C',
        'DELETE FROM Contactos_Tmp',
        '',
    ])
    salida = f(md)
    assert '```sql' in salida, salida


def test_el_motor_de_autor_no_pierde_el_xml_literal_al_marcar_codigo():
    """
    Las dos reglas de codigo estuvieron desactivadas en el motor de autor
    porque tres articulos perdian entre el 18 % y el 23 % de su texto. La
    causa eran dos cosas, las dos en el camino de autor y ninguna en las
    reglas:

    1. ``merge_plain_code_paragraphs`` des-escapaba el parrafo y DESPUES
       borraba "toda etiqueta". Un ``&lt;soap:Envelope&gt;`` del ejemplo se
       convertia en marcado y se perdia la peticion entera.
    2. Las reglas se aplicaban ANTES de ``sanitize_author_html``, que
       reescribe el marcado recien puesto. Ahora entran despues, en el hueco
       que hay hasta ``protect_code_blocks``.
    """
    ejemplo = (
        '<p>Ejemplo de llamada a un webservice:<br><br>'
        'Sub MainPost()<br>'
        'Dim request<br>'
        'request = "&lt;?xml version = \'1.0\'?&gt;" &amp; _<br>'
        '"&lt;soap:Envelope xmlns:soap = \'http://www.midom.org/soap-envelope\'&gt;" &amp;_<br>'
        '"&lt;soap:Header&gt;" &amp;_<br>'
        '"&lt;CodigoFranquicia&gt;02708&lt;/CodigoFranquicia&gt;" &amp;_<br>'
        'End Sub</p>'
    )
    sin = converters._convert_with_markdownify(ejemplo)
    con = converters._convert_with_markdownify(ejemplo, marcar_codigo=True)

    # Lo que importa: marcar el codigo no puede costar ni una palabra.
    palabras = lambda t: collections.Counter(
        w.lower() for w in re.findall(r"[\w'-]+", re.sub(r'(?m)^```.*$', ' ', t)) if len(w) > 1)
    faltan = palabras(sin) - palabras(con)
    assert not faltan, f'se pierden palabras: {faltan}'

    # Y el XML del ejemplo tiene que seguir ahi, no convertido en marcado.
    assert 'soap:Envelope' in con, con
    assert 'CodigoFranquicia' in con, con


if __name__ == '__main__':
    sys.exit(main())
