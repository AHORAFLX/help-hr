# Notas del pipeline

Por qué cada regla de conversión es como es: el caso real que la provocó, cómo se midió y qué se descartó por el camino. Se escribe aquí y no en el código porque casi todas nacen de un artículo concreto que se veía mal, y sin ese caso delante la regla parece arbitraria —o peor, parece que sobra—.

Para instalar y ejecutar, ver [README.md](README.md).

## Índice

- [Cómo se convierte, y por qué así](#como-se-convierte-y-por-que-asi)
  - [Por qué el motor se elige una sola vez](#por-que-el-motor-se-elige-una-sola-vez)
  - [El código se aparta antes de convertir](#el-codigo-se-aparta-antes-de-convertir)
  - [El SQL y el VB que vienen como texto plano](#el-sql-y-el-vb-que-vienen-como-texto-plano)
  - [Los `<br>` traen atributos](#los-br-traen-atributos)
  - [Hints de lenguaje](#hints-de-lenguaje)
  - [Cuando el `<pre>` no era código](#cuando-el-pre-no-era-codigo)
- [Por qué el nivel de categoría solo se quita con un producto](#por-que-el-nivel-de-categoria-solo-se-quita-con-un-producto)
- [Encabezados que no eran encabezados](#encabezados-que-no-eran-encabezados)
- [La página de parámetros](#la-pagina-de-parametros)
- [Avisos y encabezados a gritos](#avisos-y-encabezados-a-gritos)
  - [Las viñetas tecleadas a mano](#las-vinetas-tecleadas-a-mano)
- [Tablas vacías](#tablas-vacias)
- [El panel de navegación](#el-panel-de-navegacion)
- [Títulos duplicados](#titulos-duplicados)
- [Reparación de enlaces](#reparacion-de-enlaces)
  - [Qué cuenta como enlace](#que-cuenta-como-enlace)
- [Imágenes](#imagenes)
- [Enlaces que apuntan a Freshdesk](#enlaces-que-apuntan-a-freshdesk)
- [Las tablas se anidan, y eso no lo resuelve una regex](#las-tablas-se-anidan-y-eso-no-lo-resuelve-una-regex)
- [Énfasis con el espacio por dentro](#enfasis-con-el-espacio-por-dentro)
  - [Las tablas se conservan como HTML, y eso cambia las reglas](#las-tablas-se-conservan-como-html-y-eso-cambia-las-reglas)
  - [Un autolink no es una etiqueta](#un-autolink-no-es-una-etiqueta)
  - [El texto alternativo de las imágenes](#el-texto-alternativo-de-las-imagenes)
- [Autoenlaces](#autoenlaces)
- [Enlaces sin texto](#enlaces-sin-texto)
- [Encabezados: de ellos vive el panel derecho](#encabezados-de-ellos-vive-el-panel-derecho)
  - [Los niveles de encabezado se normalizan](#los-niveles-de-encabezado-se-normalizan)
  - [Un encabezado no puede ser un enlace](#un-encabezado-no-puede-ser-un-enlace)
  - [Los títulos escritos a mano](#los-titulos-escritos-a-mano)
  - [Las etiquetas de sección de los artículos de referencia](#las-etiquetas-de-seccion-de-los-articulos-de-referencia)
  - [Los avisos no son secciones](#los-avisos-no-son-secciones)
  - [El énfasis de los encabezados viene anidado](#el-enfasis-de-los-encabezados-viene-anidado)
  - [Los encabezados que Word marcó y Freshdesk perdió](#los-encabezados-que-word-marco-y-freshdesk-perdio)
  - [Las cajas de aviso dibujadas con reglas](#las-cajas-de-aviso-dibujadas-con-reglas)
  - [Cuando Shift+Enter hizo pasar una lista por un párrafo](#cuando-shiftenter-hizo-pasar-una-lista-por-un-parrafo)
  - [El repaso final de los encabezados](#el-repaso-final-de-los-encabezados)
  - [La prosa se degrada en todos los niveles, no solo en los tres primeros](#la-prosa-se-degrada-en-todos-los-niveles-no-solo-en-los-tres-primeros)
  - [Encabezados que no pueden ser un título](#encabezados-que-no-pueden-ser-un-titulo)
  - [Las líneas que parecen vacías y no lo están](#las-lineas-que-parecen-vacias-y-no-lo-estan)
  - [El ancla que perdió su texto](#el-ancla-que-perdio-su-texto)
  - [La tabla de una celda que era un bloque de código](#la-tabla-de-una-celda-que-era-un-bloque-de-codigo)
  - [Portadas de categoría y de carpeta](#portadas-de-categoria-y-de-carpeta)
  - [Las etiquetas que se comen su contenido](#las-etiquetas-que-se-comen-su-contenido)
  - [Cómo se comprueba que no se pierde contenido](#como-se-comprueba-que-no-se-pierde-contenido)
  - [Las clases del editor bloqueaban el estilo del tema](#las-clases-del-editor-bloqueaban-el-estilo-del-tema)
  - [Un solo marcador de viñeta por documento](#un-solo-marcador-de-vineta-por-documento)
  - [La reparación de enlaces no puede entrar en el código](#la-reparacion-de-enlaces-no-puede-entrar-en-el-codigo)
  - [La caja de aviso de Freshdesk venía disfrazada de código](#la-caja-de-aviso-de-freshdesk-venia-disfrazada-de-codigo)
  - [El aviso que lleva su texto en la misma línea](#el-aviso-que-lleva-su-texto-en-la-misma-linea)
  - [Al ascender el rótulo, la captura no se pierde](#al-ascender-el-rotulo-la-captura-no-se-pierde)
  - [La imagen que se quedaba con la URL del enlace](#la-imagen-que-se-quedaba-con-la-url-del-enlace)
  - [El enlace que ya no lleva a ningún sitio](#el-enlace-que-ya-no-lleva-a-ningun-sitio)
  - [Un bloque de código o una imagen sí caben en la caja](#un-bloque-de-codigo-o-una-imagen-si-caben-en-la-caja)
  - [El enlace de una tabla no lo reescribe MkDocs](#el-enlace-de-una-tabla-no-lo-reescribe-mkdocs)
  - [El encabezado que no tenía nada que enseñar](#el-encabezado-que-no-tenia-nada-que-ensenar)
  - [El vídeo que no dejaba ni rastro](#el-video-que-no-dejaba-ni-rastro)
  - [Los adjuntos no se pueden bajar, y hay que decirlo](#los-adjuntos-no-se-pueden-bajar-y-hay-que-decirlo)
  - [Por qué NO se renumeran los encabezados](#por-que-no-se-renumeran-los-encabezados)
  - [Un enlace que solo lleva una imagen no está vacío](#un-enlace-que-solo-lleva-una-imagen-no-esta-vacio)
  - [El color escrito a mano y el modo oscuro](#el-color-escrito-a-mano-y-el-modo-oscuro)
  - [La primera fila que hacía de cabecera sin serlo](#la-primera-fila-que-hacia-de-cabecera-sin-serlo)
  - [Los pasos que el autor numeró a mano](#los-pasos-que-el-autor-numero-a-mano)
  - [El índice escrito a mano que no llevaba a ninguna parte](#el-indice-escrito-a-mano-que-no-llevaba-a-ninguna-parte)
  - [El código que venía metido en un párrafo de prosa](#el-codigo-que-venia-metido-en-un-parrafo-de-prosa)
  - [El enlace vacío que repetía la misma dirección](#el-enlace-vacio-que-repetia-la-misma-direccion)
  - [Los vídeos que ya no se pueden ver](#los-videos-que-ya-no-se-pueden-ver)
  - [La sentencia que va sola en su hueco](#la-sentencia-que-va-sola-en-su-hueco)
  - [La tabla que se publicaba vacía](#la-tabla-que-se-publicaba-vacia)
  - [La etiqueta del lenguaje no es una sección](#la-etiqueta-del-lenguaje-no-es-una-seccion)
  - [Un encabezado que solo lleva un vídeo](#un-encabezado-que-solo-lleva-un-video)
  - [La degradación necesita los encabezados ya definitivos](#la-degradacion-necesita-los-encabezados-ya-definitivos)
  - [Las imágenes que ya no usa nadie](#las-imagenes-que-ya-no-usa-nadie)
  - [El lenguaje de un bloque se decide por recuento](#el-lenguaje-de-un-bloque-se-decide-por-recuento)
  - [La viñeta con más de un espacio](#la-vineta-con-mas-de-un-espacio)
  - [El bloque reconstruido no es VB por defecto](#el-bloque-reconstruido-no-es-vb-por-defecto)
  - [Un enlace no se encierra en un bloque de código](#un-enlace-no-se-encierra-en-un-bloque-de-codigo)
  - [La deuda del motor de autor](#la-deuda-del-motor-de-autor)
  - [El resultado tiene que ser idempotente](#el-resultado-tiene-que-ser-idempotente)
  - [El enlace lleva el título de su destino](#el-enlace-lleva-el-titulo-de-su-destino)
- [Marcadores entre ángulos](#marcadores-entre-angulos)
- [Cuando la URL no es una URL](#cuando-la-url-no-es-una-url)
- [Enlaces a otros productos](#enlaces-a-otros-productos)

## Cómo se convierte, y por qué así

El esqueleto del pipeline: las piezas de las que dependen casi todas las
reglas de más abajo.

### Por qué el motor se elige una sola vez

Antes había dos scripts: `migrate.py` generaba el artículo con el motor estándar y luego `author_articles.py` lo sobrescribía con el suyo, ya **por detrás** de la reparación de enlaces. Así que los artículos de autor nunca la recibían: sus enlaces internos se quedaban apuntando a Freshdesk.

### El código se aparta antes de convertir

Los dos motores llaman a `protect_code_blocks` **antes** de convertir nada: cada `<pre>`/`<code>` se sustituye por un token y se restaura al final como fence con su lenguaje. Es la pieza de la que dependen casi todos los arreglos de calidad:

- html2text **no genera fences**: con `mark_code=False` convierte cada `<pre>` en texto indentado con cuatro espacios y sin lenguaje. Sin esta protección, el 98 % de los bloques de código se pintaban en gris, sin resaltar.
- Al no ver el código, el postproceso ya no lo trocea. Antes, un `Sub` de VB acababa repartido en cuatro cajas distintas con las líneas de continuación sueltas entre ellas.
- Dentro de un `<pre>`, un `&lt;style&gt;` es texto del ejemplo. Des-escapar el documento antes de aislar el código lo convertía en marcado real y el conversor se lo llevaba por delante.

Por la misma razón, las heurísticas que rescatan código escrito como párrafos (`preprocess_reference_html`) **no tocan ninguna sección que ya traiga `<pre>` o `<code>`**: ahí no hay nada que rescatar y solo pueden estropearlo.

### El SQL y el VB que vienen como texto plano

Muchos artículos traen el código sin marcar: párrafos normales con un `SELECT` dentro. `_extract_loose_sql_blocks` los detecta y los envuelve en un fence.

La parte delicada es **dónde termina la racha**. Una línea corta que no acaba en punto parece código, así que el bloque seguía creciendo y se llevaba por delante lo que viniera detrás. El caso real: un enlace a un vídeo y un `**Ver código ejemplo**` que separaban dos ejemplos acabaron *dentro* del bloque de SQL, y el fence se cerró setenta líneas más abajo.

Por eso una línea que ya es Markdown por sí sola —un enlace o imagen en solitario, una línea entera en negrita, un encabezado, una viñeta— **corta la racha** aunque sea corta y no termine en punto. Es `_MD_PROSE_LINE_RX`.

Ojo con el anclaje de esas alternativas: iban con el fin de línea pegado, así que el patrón de encabezado solo casaba un `###` **vacío**. Un encabezado con texto no cortaba nada y acababa dentro del bloque de código, con su negrita y todo. Igual las viñetas.

### Los `<br>` traen atributos

El origen escribe `<br data-identifyelement="571">`, y todas las reglas del conversor usaban un patrón `<br\s*/?>` que no los ve. Era el **30 % de los `<br>`** —19.725 en 680 artículos— escapándose de todo: encabezados que se quedaban vacíos porque el `<br>` inicial no se quitaba, y saltos de línea perdidos **dentro del código**. Ahora todas usan `<br[^>]*>`.

### Hints de lenguaje

`converters.VB_LANG` es `vbnet`, y tiene que seguir siendo un alias que **Pygments reconozca**: `vb` no lo es, y todo bloque etiquetado así se pinta sin resaltar. Hay un test que lo comprueba.

VB, C# y T-SQL comparten demasiada sintaxis para decidir con el primer patrón que encaje: `detect_code_lang` cuenta los marcadores inequívocos de cada uno y gana el que más tenga. Antes devolvía el primer acierto y los ejemplos de C# salían etiquetados como VB.

Dos señales de VB que costó afinar, porque son las que más se parecen a la prosa:

- **Acceso a miembro con punto inicial.** Dentro de un bloque `With`, VB escribe `.EditarPorObjeto = True` o `Set .Coleccion = ...`. No existe en C# ni en T-SQL. Los patrones exigían una letra al principio, así que ese bloque entero se quedaba sin lenguaje.
- **Acceso a miembro normal.** `objeto.Propiedad` exige ahora una **letra** tras el punto. Sin eso, un pie de figura como `_Fig.8 Insertar un artículo_` o un apartado `B.- Pago de la factura` acababan dentro de un ```` ```vbnet ````.


### Cuando el `<pre>` no era código

El origen usa `<pre>` como caja de aviso: los `NOTA:` / `IMPORTANTE:` y bastantes párrafos explicativos acaban dentro de un fence. En Material un fence **no hace wrap**, así que salen en gris y con barra de scroll horizontal. Seis de ellos, además, salían con resaltado de sintaxis de VB, que es peor todavía.

`desenvolver_fences_de_prosa()` los saca del fence y vuelve a unir las líneas —venían partidas por el ancho del `<pre>`, no por voluntad del autor—. Mira **todos** los fences, con lenguaje o sin él.

El criterio es estrecho a propósito, porque desenvolver código por error sería peor que dejar un aviso en gris: ningún carácter de sintaxis (`{}<>=;\|`, paréntesis vacíos, `::`, `As Tipo`), `detect_code_lang` en blanco, doce palabras como mínimo, al menos el 60 % en minúscula, y ninguna línea indentada. Comprobado contra los 1.265 fences que ya tenían lenguaje: solo saltan esos 6, y los 6 son prosa castellana.

Alcance: 80 bloques de 1.418. Los 79 que se quedan sin lenguaje no son código —rutas UNC, un `powershell.exe` suelto, fragmentos de una palabra—.

#### El rótulo de los bloques sin lenguaje

`pymdownx.highlight` lleva `auto_title: true`, así que cada bloque luce su lenguaje como título. Los que lo tienen rotulan `SQL`, `VB.NET`, `C#`, y eso informa. Los **77 que no lo tienen** rotulaban **«Text Only»**, que no dice nada, en **76 páginas**.

Se arregla en `mkdocs.yml`, sin tocar el pipeline, con `auto_title_map: {"Text Only": ""}`: con el mapeo a cadena vacía no se pinta la barra siquiera, y los rótulos útiles se conservan. Comprobado sobre el sitio construido: 0 páginas con «Text Only», 127 que mantienen el de `SQL`.

## Por qué el nivel de categoría solo se quita con un producto

Quitar la carpeta de una categoría que es la única de su producto parece que debería depender solo de la BDD, no de cómo se lance la ejecución. Pero hay nombres de carpeta que **se repiten entre productos**:

| Carpeta | Está en |
|---|---|
| `Versiones` | Sebastian HR, Bruno GMAO, Flexygo |
| `¿Sabías que...` | SAT, CRM, Flexygo |

Son 9 productos de una sola categoría, 525 artículos y 64 carpetas que subirían a la raíz. Quitando el nivel siempre, generar dos de esos productos en el mismo `docs/` los mezclaría: los artículos de Sebastian HR, Bruno GMAO y Flexygo acabarían los tres en una única carpeta `Versiones`, sin forma de saber cuál es de quién.

Por eso la condición mira el ámbito de la ejecución: se quita solo cuando se genera **un** producto. Con varios, cada uno conserva su categoría y no hay colisión posible.

El coste es que la ruta de un artículo depende de cómo se generó, y pasar de «solo este producto» a «todos» mueve sus ficheros. Eso ya estaba resuelto: `find_relocated_articles` los ve como reubicados —no como huérfanos, que siguen vivos en origen— y `--prune-orphans` retira los que quedaron atrás.

## Encabezados que no eran encabezados

El editor del origen deja poner estilo de título a cualquier línea, y la gente lo usa para dar énfasis, no para estructurar. En la ficha de un parámetro, por ejemplo, el nombre va en `h5` y debajo cuelgan dos `h6` con sus metadatos:

```markdown
##### **ACTIVAR_CALCULO_DESFASE_HORAS_CONTRATO**
Parámetro para facturar los posibles desfases.
###### ALQUILER (CONTRATOS) - Contratos
###### Tipo Valor: BOOL Valor por defecto: ON
```

Esos dos `h6` no son secciones —«Tipo Valor: BOOL Valor por defecto: OFF» salía **282 veces**— y llenaban de ruido el índice lateral de la página. `demote_label_headings()` los pasa a negrita: se conserva el énfasis y desaparecen del índice.

El criterio es que **no gobiernen nada**: sin texto debajo y sin un encabezado más profundo detrás. Uno con contenido es una sección aunque esté en `h5`, y se respeta. Y solo se mira de `h5` para abajo (`LABEL_HEADING_MIN_LEVEL`): en `h2`–`h4` sí hay estructura de verdad. Ahí hay casos como un `## Primeros pasos` que no lleva texto propio pero encabeza las secciones siguientes, y degradarlo sería un error.

También cae aquí el pie `##### Autor: ...`, que era el que provocaba 63 de los saltos de nivel de `h1` a `h5`.

## La página de parámetros

`ERP - Parámetros de la aplicación` trae **602 parámetros**, cada uno con su encabezado y tres párrafos: 6.000 líneas de pared por las que hay que bajar a ojo para comparar dos valores.

`_fichas_a_lista()`, en [article_fixes.py](pipeline/article_fixes.py), las convierte en una **lista de definición** (`def_list`, ya activada en `mkdocs.yml`):

```markdown
`ACTIVAR_CALCULO_DESFASE_HORAS_CONTRATO`
:   **BOOL**, por defecto `ON` — ALQUILER (CONTRATOS) - Contratos
    Parámetro para facturar los posibles desfases.
```

Se probó antes con una tabla de cinco columnas y quedó peor: en el ancho de contenido de Material el nombre del parámetro se parte letra a letra —`ACTIVAR_C` / `ALCULO_DE` / `SFASE_HOR`— y la columna de la descripción se sale de la pantalla. La lista de definición pone el nombre en su propia línea, a ancho completo.

Va en `article_fixes` y no en el motor porque es de **un** artículo, que es justo la regla de la casa. La ficha llega ahí con los metadatos todavía como `######`; la transformación admite también la forma en negrita, para poder aplicarla sobre un `.md` ya generado.

Tres cosas que costaron sangre:

- **Lo que no se convierte se copia tal cual.** Una versión anterior filtraba las fichas y sustituía del primer parámetro al último de una tacada, así que las **27 fichas descartadas que caían en medio** —nombres con `Ñ`, con equis minúscula (`PEDIDOSxPLANTA`) o con `&`— desaparecían del artículo. Ahora se recorren todas y las que no son un parámetro se copian sin tocar.
- **Las entidades HTML se deshacen.** El valor por defecto de `OFERTAS_CLI_SELECTUNIONART` es `&#x20;`, y sin deshacerlo el lector veía la entidad dentro de un código en vez del espacio que representa. Y si al deshacerla el valor se queda en nada —`&#x20;` *es* un espacio—, no se anuncia el "por defecto": dejaba un código vacío.
- **El código no se aplasta.** La descripción se junta en una línea, y eso dejaba la consulta SQL de ese mismo parámetro como <code>sql Select Articulos.IdArticulo…</code>: con la etiqueta del lenguaje pegada delante y sin resaltar, porque una marca de apertura con acentos graves dentro de su etiqueta no es un bloque válido. `_saca_codigo()` separa el cuerpo en prosa y bloques, y emite cada bloque con su sangría de cuatro espacios, que dentro de una lista de definición lo mantiene en la definición.

## Avisos y encabezados a gritos

Dos cosas más que el origen escribe como título y no lo son:

- **Los avisos.** "Nota", "Importante", "Recuerda", "Ejemplo"... son la etiqueta de una llamada de atención. "Ejemplo" salía 108 veces en el índice de las páginas. `demote_callout_headings()` los pasa a negrita; la lista está en `CALLOUT_WORDS`. Solo cuando el encabezado **es** la palabra (con dos puntos opcionales): "Ejemplo de uso de la función" sigue siendo una sección.
- **Los gritos.** "TABLA DE CONTENIDOS" aparece 133 veces. `normalize_shouting_headings()` los pasa a mayúscula inicial.

En los gritos hay dos trampas, y las dos están cubiertas:

- **Las siglas.** Sin la lista `SIGLAS`, "TRABAJAR CON SEPA" quedaría en "Trabajar con sepa".
- **Los nombres de parámetro.** `CENTROCOSTELINEAAUTO` es un identificador, no un grito. Los de **dos palabras o más** se bajan siempre; los de una sola, solo si están en `PALABRAS_DE_SECCION`.

Esa lista es una lista y **no una regla**, a propósito. Se intentó deducirlo —«solo letras y todas mayúsculas»— y el propio corpus lo tumba: `CENTROCOSTELINEAAUTO` cumple las dos condiciones y es un parámetro, no una palabra. Sin un diccionario no hay forma de distinguirlos, así que se enumeran, igual que `SIGLAS` y `CALLOUT_WORDS`. Añadir una palabra ahí es seguro; el riesgo está en deducirlas.

Con eso bajan 27 encabezados que antes se quedaban gritando —`INTRODUCCIÓN` ×4, `SOLUCIÓN` ×2, `CONTRATACIÓN`, `FACTURACIÓN`…—. Los que siguen arriba son los correctos: 6 nombres de parámetro, "AHORA API" y "AHORA TPV", y 13 que son el **H1**, o sea el título del artículo en Freshdesk (`ERP - MODALIDAD SEPA`). Esos últimos no los ve el conversor: el H1 lo escribe `migrate.py` con el título tal cual, y cambiarlo cambiaría también la etiqueta del panel. Se arreglan en el origen.

### Las viñetas tecleadas a mano

El autor no usó la lista del editor: tecleó el carácter. Llegan **62 líneas** así, con `•` (39) y `·` (23), y también el `\uf0b7` que mete Word con la fuente Symbol. Markdown no las reconoce, así que se publicaban como un párrafo que empieza con un símbolo, en 13 páginas.

`vinetas_literales_a_lista()` las pasa a `- `. Solo al principio de la línea y solo si hay algo detrás: un `·` en medio de una frase no se toca, y una viñeta sola es un artefacto del que ya se encarga `_EMPTY_LIST_ITEM_RX`.

Y si el origen ya traía la línea **como encabezado** —`<h5>• OFERTAS_OCULTA_EMBALAJE</h5>`— no hay lista que crear, pero el símbolo sobra igual: se publicaba como `## • OFERTAS_OCULTA_EMBALAJE`, con la viñeta dentro del título y, de ahí, dentro de la tabla de contenidos. `_VINETA_EN_ENCABEZADO_RX` se la quita.

Corre **antes** que `_etiquetas_sueltas_a_encabezados` y `promover_negritas_sueltas`, y eso arregla de paso un daño colateral: en `ERP - Almacén - Embalajes` el origen trae dos parámetros en viñeta, y el segundo —`• **OFERTAS_OCULTA_EMBALAJE**`, solo en su párrafo— lo veía la regla de negritas sueltas como un título y lo ascendía a `## • OFERTAS_OCULTA_EMBALAJE`, con la viñeta dentro del encabezado. Convertida antes en item de lista, ya no es candidata.

## Tablas vacías

El mismo editor deja cascarones: `<table><tbody><tr><td style="width: 50%"></td><td></td></tr></tbody></table>`. En la página son un hueco en blanco. `protect_html_tables` descarta las que no tienen **ni texto, ni imagen, ni enlace** — 112 en el corpus—. Las que solo llevan imágenes se conservan: el origen las usa para maquetar galerías, y son 288.

## El panel de navegación

`mkdocs.yml` no lleva `nav:`, así que MkDocs monta el árbol solo: las **secciones** son las carpetas y la **etiqueta de cada página** es su `title` de cabecera YAML, o su H1 si no lo tiene.

Ahí estaba el problema: 231 artículos traen de Freshdesk un título de más de 60 caracteres —el mayor, 165—, y en la barra lateral se partían en cuatro o cinco líneas hasta dejar el árbol inservible.

Por eso, cuando un título no cabe, el generador escribe una cabecera:

```markdown
---
title: "Script - Recargar código de formularios útil para cuando..."
---

# Script - Recargar código de formularios útil para cuando modificamos el código de script de un formulario
```

**El H1 conserva el título entero**: no se pierde nada, solo se acorta la etiqueta del panel y el título de la pestaña. El recorte lo hace `nav_title()` en [pipeline/common.py](pipeline/common.py), que corta por un separador natural (` - `, `: `, ` (`, `, `, `. `) si lo hay dentro del límite y, si no, por la última palabra que quepa. `NAV_TITLE_MAX` es 60.

Las comillas dobles del `title:` no son decorativas: hay títulos con `:` dentro y sin ellas el YAML se rompe.

## Títulos duplicados

Hay artículos distintos que comparten título dentro de la misma carpeta de salida. Reparto:

- El artículo con el `ArticleId` más bajo conserva el nombre limpio, para no renombrar lo ya publicado.
- Los demás pasan a `Título (ArticleId).md`.

El reparto se calcula sobre **todos** los artículos, no solo los del filtro, así que es estable entre ejecuciones. Los grupos afectados quedan listados en `logs/titulos-duplicados.txt`.

## Reparación de enlaces

Cuatro fases, en [pipeline/repair_links.py](pipeline/repair_links.py):

1. **Parches conocidos** — los `LINK_FIXES` de [article_fixes.py](pipeline/article_fixes.py).
2. **Por nombre de fichero** — reapunta a un `.md` cuyo nombre normalizado coincide de forma inequívoca.
3. **Por solape de palabras** — último recurso. Exige `MIN_WORD_OVERLAP` palabras en común y un único ganador.
4. **Validación** — recorre todo y deja el informe.

Las fases 2 y 3 solo **modifican** los ficheros generados en la ejecución; el índice de destinos siempre es el árbol completo. Sin ese acotado, generar una categoría reescribía enlaces de ficheros que estaban correctos.

Si un enlace queda sin resolver es porque apunta a un artículo de una categoría que aún no se ha generado. Eso es normal en una generación parcial.

### Qué cuenta como enlace

Las cuatro fases parsean igual, con `LINK_RX` y `split_link_target()`. Suena a detalle, pero tres bugs vinieron de aquí, y todos acababan en lo mismo: dar por roto un enlace que estaba bien y **reescribirlo**.

- **El destino admite paréntesis.** Hay artículos que los llevan en el nombre (`... (common dialog).md`). La regex antigua cortaba en el primero y se quedaba con media ruta.
- **El título no es parte de la ruta.** Markdown permite `[texto](ruta "título")`. Hay que apartarlo para resolver el destino y devolverlo al recomponer el enlace: reparar uno no puede perder su título.
- **Dentro del código no hay enlaces.** El SQL de esta documentación está lleno de `[Descrip] [varchar](50)`, que es clavado a un enlace Markdown. Las fases que reescriben excluyen los fences y el código en línea **por posiciones**, no sustituyendo el texto, porque cualquier cambio de longitud les descuadraría los desplazamientos.

Antes de esto, la fase 2 veía 195 enlaces rotos y la 4 veía 69: no estaban mirando lo mismo. Ahora las dos ven 72, que son los reales.

## Imágenes

Se descargan al generar, desde S3 o desde Freshdesk, y se reescriben a rutas locales bajo `docs/docs_assets/images`.

Cuando una descarga falla, el artículo se genera igual y la imagen se queda apuntando al servidor remoto. Eso **se anota en `imagenes-no-descargadas.txt`**, junto con las de la wiki interna ya apagada. Antes solo se avisaba por `stderr`: la imagen se quedaba remota, nadie se enteraba, y el enlace acababa caducando.

Si el informe lista alguna, basta con regenerar ese artículo (`--force` acotado a su categoría): las descargas fallan casi siempre por un hipo de red, no porque la imagen no exista.

## Enlaces que apuntan a Freshdesk

El HTML de origen viene lleno de enlaces al propio Freshdesk. Se tratan según a dónde vayan:

| Forma | Qué se hace |
|---|---|
| `/solution/articles/<id>` | Se traduce al `.md` local de ese artículo. |
| `/support/solutions/folders/<id>` | Se traduce a la carpeta local. |
| `/support/solutions/<id>` | Es una **categoría**, no un artículo: se traduce a su carpeta. |
| `/a/solutions/...`, `/a/tickets/...` | Se degradan a texto plano. |
| Cualquier otra | **Red de seguridad**: se degrada a texto plano. |

Los `/a/...` son la trastienda de Freshdesk: piden login de agente, así que para quien lee la documentación no llevan a ninguna parte. Además sus identificadores son de otra cuenta y no están en la BDD, con lo que tampoco se pueden traducir. Se conserva la frase y se pierde el enlace, que no servía.

La última fila importa. Antes, una forma no contemplada —`/support/discussions/topics/`, `/support/login`, una URL con prefijo de idioma `/es/support/...`— se publicaba tal cual. Ahora se degrada, y **se cuenta**: el total sale en `resumen.txt` y el desglose por forma en `enlaces-freshdesk.txt`. Si esa cifra sube, es que falta una regla específica arriba.

## Las tablas se anidan, y eso no lo resuelve una regex

`protect_html_tables` recorre el HTML **contando profundidad**, no buscando con `<table>.*?</table>`. Con el patrón no-codicioso, una tabla dentro de otra casaba desde la apertura de la exterior hasta el cierre de la **interior**, y el cierre de la exterior se quedaba huérfano.

La consecuencia no era estética. El artículo acababa con una tabla sin cerrar y, a partir de ese punto, **Python-Markdown deja de procesar Markdown**: encabezados, negritas, listas y enlaces salían en crudo hasta el final del documento. Eran **378 tablas descompensadas** repartidas por `docs/`, y explicaban la inmensa mayoría de los `**` que se veían literales en la página.

El recorrido también arregla lo que venga descompensado del origen: una tabla sin cerrar se cierra al protegerla, y un `</table>` sin apertura se descarta.

## Énfasis con el espacio por dentro

En Markdown `** Ejemplo**` **no es negrita**: el marcador de apertura tiene que ir pegado al texto. Se renderizan los asteriscos tal cual y el lector los ve en mitad del párrafo. Viene de HTML como `<b><u>texto</u></b>`, que html2text convierte en `** _texto_**`.

`_sacar_espacios_del_enfasis` mueve el espacio fuera de los marcadores. Solo toca **pares equilibrados**: sacar el espacio no cambia nada de lo que se lee, pero un `**` suelto sin pareja es otro problema, y ahí adivinar dónde quería cerrar el autor sería peor que dejarlo.

Quedan unas 50 marcas literales repartidas por la documentación, y **se dejan a propósito**. Son de tres clases: marcadores sin pareja del artículo original, un `***` que el autor escribió como texto, y —la razón de fondo— celdas con `**********` puestas a mano para enmascarar una contraseña. Cualquier limpieza automática se llevaría por delante esa última, que es contenido intencionado.

### Las tablas se conservan como HTML, y eso cambia las reglas

Un `<table>` del origen se preserva en crudo, así que el Markdown lleva atributos HTML dentro. Las reglas que borran o reescriben **URLs sueltas** tienen que saltarse lo que caiga dentro de una etiqueta (`_sub_outside_html`, por posiciones). Sin ese cuidado, una URL dentro de `href="..."` se trataba como URL suelta y al borrarla se llevaba también la comilla de cierre:

```html
<a href="https://ahora.freshdesk.com/a/solutions/categories/44" rel="noopener">Texto</a>
<a href=" rel="noopener">Texto</a>          ← lo que quedaba
```

Los `<a href>` a Freshdesk se tratan aparte, en su propia regla: se traducen si se conoce el destino y, si no, se deshace el ancla dejando su texto.

**Y los atributos también arrastran URLs.** El editor de Freshdesk deja en cada `<img>` un rastro suyo —`data-filelink`, `data-fileid`, `data-linked-resource-*`— y `data-filelink` guarda la URL original en S3. La imagen se descarga bien y el `src` queda apuntando a local, pero esa URL se publicaba igual dentro del HTML: no se ve en la página, está en el fichero, y caduca como cualquier otro enlace a Freshdesk. Eran 126 de las 140 que quedaban. `limpiar_atributos_de_freshdesk` quita cualquier atributo cuyo valor sea una URL de Freshdesk, **salvo `src` y `href`**, de los que se encargan la descarga de imágenes y la corrección de enlaces.

### Un autolink no es una etiqueta

`<https://…>` empieza por `<h`, así que un patrón laxo de etiqueta HTML lo daba por marcado y las reglas no lo tocaban nunca. Por eso `_HTML_TAG_RX` exige un nombre de etiqueta de verdad. Los autolinks a Freshdesk se desenvuelven al entrar en `fix_internal_links`, para que les lleguen todas las reglas y se traduzcan al artículo local en vez de publicarse.

**Las imágenes quedan fuera de todo esto.** Si una no se pudo descargar, sigue apuntando al servidor remoto y ahí se queda: una imagen remota se ve, una borrada no. Van anotadas en `imagenes-no-descargadas.txt`.

### El texto alternativo de las imágenes

Al descargar una imagen su ruta cambia, pero el `alt` se conservaba tal cual y quedaba así:

```markdown
![https://s3.amazonaws.com/cdn.freshdesk.com/…/EfTrxPr….png?157](../../docs_assets/images/quzZvPy….png)
```

La imagen funcionaba, pero un lector de pantalla leía la URL entera y cualquier búsqueda de "freshdesk" la encontraba. Cuando el `alt` no es más que la URL de origen —o cualquier otra URL— se deja vacío, que describe igual de poco y molesta menos.

**El `alt` puede traer saltos de línea**, y ahí había algo peor que un problema estético. `MD_IMAGE_RX` capturaba el alt con `.*?`, y `.` no casa saltos:

```markdown
![Captura de pantalla
Descripción generada automáticamente](https://s3.amazonaws.com/…png)
```

Esas imágenes **no las veía nadie**: ni se descargaban ni se anotaban en `imagenes-no-descargadas.txt`. Se quedaban apuntando a S3 hasta que la URL caducara, en silencio. Ahora el alt se captura con `[^\]]*` —que sí admite saltos y sigue acotado por el corchete de cierre— y se recompone en una sola línea al reescribir, o partiría el propio enlace.

## Autoenlaces

El origen escribe enlaces cuyo texto visible es la propia URL: `[https://ahora.freshdesk.com/.../articles/123-titulo](https://...)`. Dan dos problemas y los dos se han visto en la documentación publicada:

- La regla de URLs sueltas envolvía esa URL —que es el **texto**, no el destino— en otro enlace, y quedaba `[[Enlace Interno](destino)](destino)`. Se renderiza enseñando el Markdown en crudo. De ahí el `(?<!\[)` del `raw_rx`, tan necesario como el `(?<!\]\()`.
- Aunque no se anide, dejar una URL de 120 caracteres como texto visible es ilegible. Cuando el destino se resuelve a un artículo local, el texto pasa a ser **el nombre de ese artículo**.

Y si el enlace de Freshdesk no se puede traducir, no se borra sin más: la frase que lo introducía se quedaba coja —«Versión 4.4.2100 o anterior:» y detrás, nada—. El propio enlace lleva el título en su slug (`/articles/123-portal-de-licencias`), así que se rescata de ahí y queda en cursiva.

## Enlaces sin texto

Un `[](destino.md)` no se ve en la página: el lector no tiene dónde pulsar. El HTML original los genera al envolver una imagen en un `<a>`, o al dejar un ancla con `&nbsp;` dentro.

- Si apunta a un artículo, se le pone como texto el nombre del fichero de destino, que es justo el título que le falta.
- Si apunta a otra cosa, sobra y se quita.
- Si apunta a una URL externa, se le pone la propia URL como texto (los tutoriales en vídeo eran el caso habitual).

Vienen en tres formas, y las tres cuentan:

```markdown
[](Otro%20Articulo.md)
[](A.md "[Enlace Interno](A.md)")     ← con un título que es otro enlace mal formado
[
](B.md)                               ← con el texto partido por un salto de línea duro
```

El título de esos casos se descarta: es un duplicado del propio enlace y no aporta nada.

## Encabezados: de ellos vive el panel derecho

MkDocs construye la tabla de contenidos —el panel de la derecha— con los `##` y `###`. Un artículo sin ellos no tiene por dónde navegarse.

`_parece_prosa()` decide qué encabezado del origen es en realidad una frase y hay que degradar a párrafo. Antes bastaba con que terminase en `.` **o en `:`**, y ahí estaba el problema: los dos puntos al final de un título son de lo más normal en castellano —"Procedimiento almacenado:", "Crear auto numéricos:"— y esa regla se llevaba por delante **205 encabezados** perfectamente válidos.

Ahora los dos puntos no degradan nunca. El punto final sí, pero solo cuando el texto da para una frase: `F.A.Q.` es un título; una línea de noventa caracteres acabada en punto, no.

### Los niveles de encabezado se normalizan

El título del artículo ocupa el `h1`, así que las secciones empiezan en `h2`. Pero el origen usa el nivel que le apetece: unos artículos abren en `<h1>`, otros en `<h2>`, y unos cuantos **escriben todas sus secciones en `<h4>`**. Con `toc_depth: 3` esos últimos no aparecían en el panel derecho: el artículo tiene estructura y no se puede navegar.

`_normalizar_niveles_de_seccion()` los renumera **con una pila**, en una sola pasada: cada encabezado se desapila hasta encontrar uno de nivel estrictamente superior, se cuelga de él y recibe el nivel que le toca por su posición. Eso resuelve las dos cosas a la vez:

- **El arranque.** El primer encabezado sale `h2`, venga del nivel que venga.
- **Los huecos.** Un artículo que va del título a un `<h3>`, o de un `<h2>` a un `<h4>`, salta un nivel que no existe: eran **131 saltos** (`H1→H3` ×91, `H2→H4` ×27, `H1→H4` ×13). La versión anterior desplazaba el conjunto en bloque, lo que corrige el arranque pero deja los huecos de en medio intactos.

La jerarquía relativa se conserva siempre: dos hermanos siguen siendo hermanos y un hijo sigue siendo hijo. Lo único que desaparece son los niveles vacíos por el medio.

Tres salvedades, las tres medidas sobre el corpus:

- **Los créditos de autoría no cuentan.** Son `h5`/`h6` a propósito (96 «Autor: Daniel…», 55 «Autor: Pablo…»), no marcan el nivel de referencia, no suben al índice y, al quedar fuera de la lista, **tampoco descolocan la pila**: un crédito por el medio no puede hacer que la sección siguiente cuelgue de él.
- **Un artículo con cientos de encabezados al mismo nivel no está dividido en secciones**: los usa como etiquetas de datos. `ERP - Parámetros de la aplicación` tiene 604 `<h5>` del tipo «Tipo Valor: BOOL Valor por defecto: OFF»; subirlos llenaba su panel derecho con 1.809 entradas inútiles. Por eso `_MAX_SECCIONES_PARA_SUBIR` corta en 30: medido, 252 artículos tienen entre 1 y 5 secciones en su nivel más alto y el máximo normal es 17.
- **El guardián mira cualquier nivel por debajo de `h2`, no solo el más alto.** Ese HTML abre con un `<h1>`, así que el nivel más alto del artículo *no* es el de las etiquetas; mirando solo el más alto el guardián no saltaba y las 604 subían igual. Tiene su propio test.

Quedan **23 saltos** y son los correctos: los `h5`/`h6` de autoría y las cajas de aviso dibujadas con reglas, que se degradan a propósito por debajo de `toc_depth` para no ensuciar el índice.

### Un encabezado no puede ser un enlace

Un encabezado es un título, y en toda la documentación se ve como un título. Catorce se veían en azul y se podían pulsar, porque el origen —una copia de una página de Microsoft Learn— traía cada sección enlazada a su ancla en el original:

```markdown
## [Limitaciones y restricciones](https://learn.microsoft.com/…#Restrictions)
```

`_encabezados_que_son_un_enlace()` deja el texto y quita el enlace. **No** los degrada a párrafo, que es lo que hace `_degradar_encabezados_imposibles()` con los de navegación (`## [< Codificación…](…)`): ahí el texto es una flecha y no un título, mientras que aquí el texto sí es el título de la sección y el panel derecho lo necesita. Por eso corre **después** de esa degradación, cuando ya solo quedan los que de verdad son un título.

Lo que se pierde son catorce anclas a secciones de una misma página externa, cuyo contenido está ya en el propio artículo. Alcance: 14 encabezados en 1 artículo de 1.500.

### Los títulos escritos a mano

Muchos artículos no usan encabezados: escriben las secciones en negrita, como `<p><strong>1. Comprobaciones previas</strong></p>`. Se lee igual, pero MkDocs no lo mete en el panel derecho, así que el artículo se queda sin forma de navegarse.

`promover_negritas_a_encabezados()` los convierte en `##`. Aquí se está **inventando estructura**, así que el criterio es deliberadamente estrecho: todo el texto visible del párrafo tiene que ir dentro de la negrita, el texto no pasa de 70 caracteres, no termina en punto, y no contiene un enlace —un párrafo que es un enlace en negrita es un enlace, y sin ese corte acababan en el índice encabezados de 200 caracteres con la URL dentro—.

Resultado medido sobre los 1.498 artículos: los navegables pasan del **28 % al 64 %**, con 1.280 encabezados nuevos de 14 caracteres de mediana y ninguno sospechoso.

Los 530 que siguen sin panel derecho **no traen ninguna sección en el origen**, ni como encabezado ni como negrita. Eso se arregla en Freshdesk, no aquí.

### Las etiquetas de sección de los artículos de referencia

Los artículos de la API (`gCn.*`, `EsMultiUbicacion`, los formularios) tienen una estructura fija: `Descripción:`, `Implementación:`, `Parámetros:`, `Ejemplo de uso:`, `Código VB6:`, `Código C#:`. El origen las escribe como párrafo suelto, no como encabezado.

Se veía como una incoherencia dentro del mismo artículo: `Código VB6:` salía como `##` —porque además iba en negrita y la promoción de arriba lo cogía—, mientras que `**Código C#:**` se quedaba en negrita, y con él el ejemplo de C# entero fuera del panel.

`_etiquetas_de_referencia_a_encabezados()` las pasa a `<h2>`. Es una lista cerrada de etiquetas, y el `:` final es obligatorio, así que una frase que empiece igual (`Código fuente completo del formulario:`, `Descripción de la tabla:`) no se toca. Va **al final** de `preprocess_reference_html()`: las heurísticas que rescatan el código de esas secciones las localizan buscándolas como `<p>`, y convertirlas antes las dejaría ciegas.

Alcance medido: 38 artículos con `Implementación:`/`Descripción:` como texto suelto —30 de ellos sin ninguna sección en el panel— y 51 más con `**Código C#:**` en negrita.

### Los avisos no son secciones

El origen marca los avisos poniendo la palabra en negrita en su propio párrafo: `**NOTA:**`, `**Importante**`, `**Recuerda**`, `**Dato**`. Son 133 de las 280 negritas sueltas del corpus.

Promoverlos a `##` —que es lo que haría la regla de secciones— llenaría el panel derecho de entradas «NOTA, NOTA, Aviso» que no sirven para navegar, y le daría a una nota al pie el tamaño de un encabezado. `avisos_a_admonitions()` los convierte en una admonition de Material (`!!! note`, `!!! warning`, `!!! tip`, `!!! info`): dice lo mismo, sale como caja de color y **no entra en el índice**. La extensión `admonition` ya estaba activada en `mkdocs.yml`.

El título conserva la palabra del autor —`!!! tip "Recuerda"`, no `"Tip"`—. El cuerpo puede ser un párrafo corrido (hasta 6 líneas) **o una lista**, que se indenta entera: su final está bien definido —la primera línea en blanco que no va seguida de más lista—, así que no hay nada que suponer. Eran 27 avisos que se quedaban en negrita.

Lo que **no** entra en la caja: un encabezado o un fence detrás del aviso son la sección siguiente, no su texto —88 casos con la forma `**Ejemplo:**` seguido de `## Código VB6:`—; una tabla o una imagen habría que re-indentarlas con cuidado y no compensa (10 casos); y 4 avisos no tienen nada detrás. Esos 102 se quedan en negrita a propósito, y hay un test que lo fija.

Las 147 restantes sí son secciones, y `promover_negritas_sueltas()` las pasa a `##`. Es la misma regla que `promover_negritas_a_encabezados()` hace sobre el HTML, con idéntico criterio (≤70 caracteres, sin punto final, sin enlace), pero sobre el Markdown: la del HTML solo alcanza las negritas que vienen en un `<p>` limpio, y las que cuelgan de un `<div>` o llevan un `<br>` dentro llegaban hasta aquí sin tocar.

#### El orden, que costó tres regeneraciones enteras

Estas dos reglas van **al final de `convert_standard` / `convert_author`, detrás de `demote_callout_headings`**, y ahí tienen que quedarse.

Ya existía `demote_callout_headings()`, que pasa a negrita los encabezados que solo dicen «Nota» o «Ejemplo» —con el mismo razonamiento: no son secciones—. Enganchadas antes de ese paso, cada ejecución promovía y degradaba, y a la salida no llegaba **ni una caja**: 3 admonitions en 1.501 artículos, y las 3 venían ya del origen. La negrita que se quiere convertir *nace* en ese paso, así que hay que ir detrás.

Entre las dos, los avisos van primero, para que sus palabras ya no estén cuando la regla de secciones mire qué negritas quedan sueltas. Hay un test para cada cosa.

La lista de palabras es **`CALLOUT_WORDS`**, la que ya usaba `demote_callout_headings`. Una sola fuente de verdad: con una lista por regla, las dos se peleaban por el mismo texto. `_TIPO_DE_AVISO` solo dice qué caja le toca a cada palabra, y lo que no esté ahí cae en `note`.

Resultado medido: **148 admonitions** (52 `warning`, 43 `note`, 20 `tip`, 19 `info`, 14 `example`) y 6 secciones nuevas. Las cifras que di antes —144 secciones, 11 artículos rescatados— estaban infladas: contaban también lo que ya hace la regla de etiquetas de referencia.

### El énfasis de los encabezados viene anidado

`_pelar_enfasis()` quita el énfasis capa a capa, en bucle, porque viene anidado (`**_Plataforma externa_**`) y con marcadores huérfanos pegados detrás (`..._**__`). Una sola pasada de regex dejaba 67 encabezados con `**` a la vista; el caso que lo delataba llevaba además un `_` **dentro** del texto (`Ahora_Impresion`), que hacía fallar cualquier patrón que prohibiera el marcador por medio.

Se pela solo cuando el par abarca todo el texto —un encabezado con una parte resaltada conserva su marcado— y si al pelar no queda nada, la línea se deja como estaba: mejor un `**` visible que un encabezado sin texto, que rompe el panel derecho. Verificado sobre los 6.070 encabezados del corpus: ni uno pierde texto ni cambia de nivel.

### Los encabezados que Word marcó y Freshdesk perdió

Buena parte de esta documentación se escribió en Word y se pegó en Freshdesk. Al pegarla, el `<h2>` se pierde y queda un párrafo con el color del estilo:

```html
<p><a name="_Toc532416839"><span style="color: rgb(44,130,201);">Barra de menús</span></a></p>
```

Pero Word deja una huella que no admite discusión: `<a name="_TocNNNNNN">` es como nombra los destinos de **su propio índice**, así que ese texto era un encabezado en el documento original. Es la señal más fiable del corpus —no hay que deducir nada de la longitud, la puntuación ni las mayúsculas, como sí hace la promoción de negritas—.

`_encabezados_de_word()` los devuelve a `<h2>`. Solo actúa si el párrafo **no contiene nada más** que el marcador, y las entradas del índice se distinguen porque apuntan al marcador con `href="#_Toc..."` en vez de definirlo con `name=` —promoverlas duplicaría cada sección en el panel—.

Alcance: **75 encabezados en 14 artículos**, y 13 de ellos no tenían ni uno. `ERP - Compras - Ofertas` se publicaba con el panel derecho vacío teniendo sus cuatro secciones a la vista.

**Dos trampas que costaron una ejecución.** El contenido del ancla **no puede cruzar un `</a>` ni un `<p>`**: con un `(.*?)` a secas el motor retrocede hasta un ancla posterior. En `ERP - Ventas - Oferta` el marcador envuelve **solo la letra «L»** —el primer carácter del párrafo— y salía un encabezado de 160 caracteres con la frase entera dentro y otro título pegado detrás. Y hay que **des-escapar antes** de comprobar si queda texto, porque dos marcadores envuelven un `&nbsp;` y nada más, y producían un encabezado cuyo texto era literalmente `&nbsp;`.

Como red de seguridad hay un tope de 90 caracteres: un encabezado de Word más largo que eso no es un encabezado, es un párrafo cuyo primer carácter llevaba el marcador.

### Las cajas de aviso dibujadas con reglas

La otra forma que tiene el origen de dibujar un recuadro: una regla horizontal arriba, otra abajo, y la palabra junto a su texto en la misma línea.

```
---

**NOTA:** El fichero tiene que corresponder a una domiciliación.

---
```

La regla de avisos normal no las ve, porque exige la palabra sola en su párrafo. Publicado quedaban dos separadores y una negrita suelta en medio. `avisos_entre_reglas_a_admonitions()` las convierte, y aquí no hay que adivinar dónde acaba el aviso: acaba en la regla de cierre. Son **65**, todas con palabra de aviso.

Va **antes** de `avisos_a_admonitions()`, o las dos se estorban.

Al revisarlas aparecieron cuatro palabras que faltaban en `CALLOUT_WORDS`: `tip`, `recomendación`, `sugerencia` y `comprobar`. Añadirlas es seguro porque esa lista la comparte `demote_callout_headings`, y **ningún encabezado del corpus se llama así** —comprobado, y hay un test que lo fija—.

### Cuando Shift+Enter hizo pasar una lista por un párrafo

En las fichas de referencia el autor pulsó Shift+Enter en vez de Enter, así que las 24 propiedades de `Grid - Acceder a propiedades de la grid` son **un solo** `<p>` con 24 `<br>` dentro:

```html
<p dir="ltr"><strong>Agregar (Boolean):</strong> Indica si la grid permite agregar registros.<br>
<strong>Editar (Boolean):</strong> Indica si la grid permite editar registros.<br>…
```

Publicado sale un muro de texto. Esto es del origen, no del conversor: el pipeline traducía cada `<br>` a su salto duro de Markdown con total fidelidad.

`_parrafos_con_br_a_lista()` lo convierte en `<ul>`. La señal de que era una lista es que **todos** los trozos separados por `<br>` empiezan por una etiqueta, con un mínimo de tres trozos y el 80 % etiquetados.

Vale de etiqueta la negrita (`<strong>Agregar (Boolean):</strong>`) o el texto plano corto seguido de dos puntos (`Agregar (Boolean): Indica si...`). Las dos formas hacen falta, y el motivo es instructivo: hay **dos artículos** en Freshdesk titulados `Grid - Acceder a propiedades de la grid` —el de Ctrl+F10 con 33 `<strong>` y el de `_ahoraSCO` con 1—. Es la misma lista con las negritas perdidas en el origen, así que exigir negrita la reconocía en una copia y no en la otra.

La etiqueta en texto plano tiene un límite de longitud a propósito: sin él, cualquier frase con dos puntos por medio pasaría por etiqueta y la prosa acabaría troceada en viñetas. Hay un test con tres frases de ese tipo.

El corte es estrecho por necesidad: hay **346 párrafos** con tres o más trozos separados por `<br>` y solo **9** cumplen la condición. Los otros 337 son prosa con saltos intencionados —el `En los artículos …` / `… informará una Naturaleza de tipo Bien` del artículo del Actualizador— y convertirlos en lista los estropearía.

Alcance: 9 párrafos en 7 artículos, 101 entradas. Hay un test que lo comprueba de punta a punta, porque lo que importa es que el `<ul>` llegue al Markdown como viñetas y no se vuelva a fundir en un párrafo.

**Lo que queda sin homogeneizar:** en ese mismo artículo, las diez últimas propiedades (`EditActive`, `Limitar`, `MultiSeleccion`…) sí vienen como párrafos separados en el origen, así que ahora hay una lista de 22 y diez párrafos detrás. Meterlos en la misma lista exigiría suponer que un párrafo que empieza en negrita pertenece a la lista anterior, y eso ya es demasiado.

### El repaso final de los encabezados

`normalizar_encabezados_al_final()` es lo último que se toca, y está ahí por una razón aprendida a golpes: **las reglas que crean encabezados corren después de las que los limpian**, así que cualquier arreglo colocado antes lo deshace la siguiente regla. Han hecho falta tres ejecuciones para dejar de reordenar y empezar a no depender del orden.

Hace dos cosas:

**Quita los dos puntos finales.** Un encabezado es un título, no el arranque de una frase, y en el panel derecho `Descripción:` o `Modo automático:` se leen mal. Eran 987 y encima incoherentes —unos los llevaban y otros no—, y 732 los generaba este mismo pipeline.

**Escapa la `#` final pegada a la palabra.** `## Código C#` se renderiza como «Código C»: Markdown la interpreta como el cierre opcional del encabezado ATX. Son **301 encabezados, 240 de ellos la entrada `Código C` del panel**, y el fallo lo introdujo esta misma casa al quitar los dos puntos, que sin saberlo hacían de escudo. El espacio distingue este caso del cierre ATX legítimo (`## Título ##`), que sí debe seguir desapareciendo: en el corpus hay 301 pegadas y ni un solo cierre, pero el corte se hace igual.

### La prosa se degrada en todos los niveles, no solo en los tres primeros

El origen envuelve bloques enteros en un `<h4>` —hasta 410 caracteres de prosa—. La degradación por `_parece_prosa()` solo miraba `h1`, `h2` y `h3`, así que se escapaban… y después `_normalizar_niveles_de_seccion()` sube el `h4` a `h2`, con lo que la prosa acababa en el panel derecho. Eran **36 entradas, una de 1.052 caracteres**.

Mirando los seis niveles se degradan **29 encabezados de los 2.354** que hay en `h4`-`h6`, y los larguísimos bajan de 36 a 7 —los 7 son títulos legítimos de 98 a 100 caracteres—. Comprobado sobre los 14 artículos afectados: lo único que cambia es el nombre de la etiqueta, **el texto no se altera en ninguno**.

### Encabezados que no pueden ser un título

`_degradar_encabezados_imposibles()` los pasa a párrafo. Dos casos, los dos medidos:

- **El encabezado *es* un enlace.** Son 8, del tipo `## [< Codificación: Manipulación de grids en frmPedidos](...)` —los enlaces de «anterior / siguiente» de una serie de artículos—. Mismo criterio que ya usa `promover_negritas_a_encabezados()`: un párrafo que es un enlace es un enlace.
- **Es demasiado largo.** 15 pasan de 160 caracteres, y ahí no hay títulos: el origen envolvió bloques de prosa en un `<h3>`/`<h4>` y uno llega a **1.052 caracteres**. El título legítimo más largo del corpus tiene 117, así que el corte de 160 no roza ninguno.

Va sobre el **Markdown y al final de la cadena**, y eso es deliberado: así vale para los **dos motores**. `convert_author` no pasa por `preprocess_reference_html`, que es donde vive la degradación por `_parece_prosa()`, y el encabezado de 1.052 caracteres era justo de un artículo de autor.

Comprobado con el texto renderizado en los 9 artículos afectados: 8 salen idénticos y en el noveno un ` -` deja de ser un guion literal para convertirse en la viñeta de una lista de verdad —era una lista que el origen había envuelto en un encabezado—.

### Las líneas que parecen vacías y no lo están

El origen siembra líneas que solo llevan espacios: **21.678 en el corpus**. Derrotan al colapso de `\n{3,}`, que no las reconoce como vacías, así que los ficheros acumulaban rachas de `\n\n  \n\n  \n\n`.

Ojo con la diferencia, que es la razón de que esto no se pudiera hacer a lo bruto: la línea que **sí** significa algo es la que lleva dos espacios **tras un texto**, que es el salto duro de Markdown. Una línea que solo tiene espacios no significa nada. Y la limpieza va **fuera de los fences**, porque dentro una línea con espacios puede ser indentación con significado.

Comprobado sobre los 1.337 artículos que cambian: en **ninguno** varía el texto renderizado. Son 0,6 % menos de fichero y, sobre todo, un `.md` que se puede leer y diferenciar.

### El ancla que perdió su texto

El origen escribe `<h2><a href="url"></a>Permisos</h2>`: el ancla se quedó sin texto y la etiqueta de verdad quedó **fuera, pegada detrás**. Si no se juntan, la regla que etiqueta enlaces vacíos le mete la URL como texto y el encabezado pasa de 157 a 299 caracteres con la URL entera a la vista del lector.

`juntar_enlace_vacio_con_su_texto()` le devuelve la etiqueta. Se exige que ocupe **toda la línea** —opcionalmente tras las almohadillas de un encabezado— y que la etiqueta sea corta: sin eso, en un párrafo se enlazaría la frase completa. Son 16 casos en 3 artículos, 14 de ellos en el mismo.

**El largo de un encabezado se mide sobre lo que se ve.** En `## [Limitaciones y restricciones](https://learn.microsoft.com/...)` el panel lee 28 caracteres y la línea tiene 190. Midiendo la línea, el tope de 160 degradaba las 14 secciones de `Usar el Asistente para planes de mantenimiento` solo por lo larga que era la URL. Ese artículo pasa de 7 secciones —una de ellas un engendro de 296 caracteres— a **20 títulos limpios**.

**Un título que enlaza no es un enlace de navegación.** La flecha de «anterior / siguiente» es lo que los separa: `## [< Codificación: Manipulación de grids](...)` sale del panel, `## [Permisos](https://learn.microsoft.com/...)` se queda. Y un enlace **sin etiqueta** tampoco es un título, porque no se ve nada.

### La tabla de una celda que era un bloque de código

El origen usa una tabla de una sola celda como recuadro, y a veces lo que mete dentro es una consulta o un `Sub`, con las palabras clave **coloreadas a mano**:

```html
<table><tr><td><br><span style="color: rgb(44,130,201)">EXEC </span>
VACIA..Ztest_comprobaciones_postactualizacion @ddbb_cliente<br></td></tr></table>
```

Publicado salía como una tabla con borde, sin monoespaciado ni resaltado, y con un azul pintado a mano en vez del color del tema. `_tablas_de_una_celda_con_codigo()` emite un `<pre>`, y `protect_code_blocks()` lo recoge después y le pone su lenguaje.

Tres detalles que hubo que acertar:

- **Los saltos.** Los `<br>` y los `<p>` marcan las líneas. Sin convertirlos, el código se pega —`frmAux.DescargarlDescCliente=`— y se vuelve ilegible.
- **Las comillas van literales.** Con el escapado por defecto, el `'` de una consulta acababa como `&#x27;` dentro del bloque, a la vista del lector. Lo detectó el control de «no se pierde texto», que marcó 7 artículos.
- **El criterio es `detect_code_lang()`**, el mismo que decide el lenguaje de los demás bloques. Si no reconoce el contenido, la tabla se queda como está: un aviso, una tabla de datos o una celda vacía no se tocan.

Alcance: **26 tablas en 11 artículos**, con 0 pérdida de texto verificada contra el origen completo.

### Portadas de categoría y de carpeta

MkDocs publica **páginas, no directorios**: una carpeta solo tiene URL si lleva un `index.md`. Sin él, `[AHORA API](../../API/)` da 404, y los enlaces de Freshdesk a una carpeta —que `fix_internal_links` sí sabe traducir a su ruta local— llegaban a un directorio sin página y acababan degradados a texto.

Por eso, en el paso **6.b** de `migrate.py`, `escribir_portadas_del_arbol()` recorre las categorías de la ejecución y **da portada a todas sus carpetas**, y a ellas mismas: 15 categorías y 141 carpetas. Va **antes** de la reparación de enlaces a propósito, para que `phase_unwrap_folder_links()` se encuentre la portada ya escrita y reapunte el enlace en lugar de quitarlo.

#### Qué lleva dentro

La portada se escribe en Markdown, con la rejilla de tarjetas que **Material trae de serie**. Ni una línea de CSS propio: `grid cards`, los iconos `:material-...:` y los modificadores `{ .lg .middle }` son del tema, y las tres extensiones que hacen falta —`attr_list`, `md_in_html` y `pymdownx.emoji`— ya estaban en `mkdocs.yml`.

Lo que lista depende del nivel:

| | Lista | La tarjeta lleva |
|---|---|---|
| **Categoría** (`docs/ERP/`) | sus carpetas | nombre y, bajo la raya, cuántos artículos hay dentro |
| **Carpeta** (`docs/ERP/Almacén/`) | sus artículos | el H1 del artículo, y nada más |

Una categoría **no** vuelca los 27 artículos de cada una de sus 45 carpetas: para eso está la portada de la carpeta. Lo que sí lista, debajo de las carpetas, son los artículos que cuelgan directamente de ella.

````markdown
# Actualizador

<!-- portada de categoría generada automáticamente -->

1 carpeta y 15 artículos.

## Carpetas

<div class="grid cards" markdown>

-   :material-folder-outline:{ .lg .middle } **[FAQ](FAQ/index.md)**

    ---

    1 artículo

</div>

## Artículos

<div class="grid cards" markdown>

-   :material-file-document-outline:{ .lg .middle } [Actualizador - Guía de Instalación](Actualizador/Actualizador%20-%20Gu%C3%ADa%20de%20Instalaci%C3%B3n.md)

</div>
````

La tarjeta de un artículo no lleva raya: no hay nada más que contar, y una `---` con un hueco vacío debajo queda peor que no ponerla.

Los dos encabezados `##` solo se ponen cuando hay las dos cosas. En una carpeta hoja —solo artículos— un `## Artículos` sobre la única rejilla de la página no dice nada y encima ensucia la tabla de contenidos.

El `markdown` del `<div>` es de `md_in_html`, y es lo que hace que lo de dentro se siga tratando como Markdown, **incluidos los enlaces**: MkDocs los reescribe como en cualquier otra página. Sin esa palabra el bloque sería HTML crudo, MkDocs no tocaría los enlaces y habría que escribir a mano la URL publicada. Hay un test que ata las tres extensiones a `mkdocs.yml`, porque si alguien quita una la portada no falla: se degrada en silencio —el `<div>` se queda literal, o los iconos salen como texto— en las 153 páginas a la vez.

#### Cuándo se rehace

En **cada** ejecución, y no solo para lo regenerado: el listado de una carpeta cambia en cuanto se le añade, se le quita o se le renombra un artículo, y eso pasa en artículos que no son la portada. Pero **solo se escribe si el contenido cambia**: rehacer un fichero idéntico le cambia la fecha y saca las 156 carpetas en el `git status` todas las semanas. Por eso `escribir_portadas_del_arbol()` devuelve las que de verdad han cambiado en disco, y no el número de carpetas que ha visitado.

Una carpeta **sin artículos no lleva portada** —sería una página en blanco en el panel—, y cuando `--prune-orphans` se lleva el último artículo de una carpeta, `_remove_empty_parents()` borra también la portada que quedaba huérfana.

Y si un enlace apunta a una categoría que **no está en la ejecución** —`TPV` cuando se genera solo el ERP—, no hay página que crear, así que el enlace se queda en texto y se anota en `logs/enlaces-a-categoria.txt`.

#### Detalles que hubo que acertar

Salieron todos de comprobarlo a mano con un proyecto MkDocs mínimo o del `mkdocs build` sobre las categorías reales.

- **El enlace va al `.md`, nunca a la carpeta.** MkDocs solo reescribe los enlaces que reconoce como documento, y con `use_directory_urls` la página vive un nivel más abajo que el fichero. Escrito `FAQ/` se queda corto y da **404 con portada y sin ella**; escrito `FAQ/index.md`, MkDocs lo publica como `FAQ/`, que sí resuelve. Verificado sobre el sitio construido: **1.648 enlaces de portada, 0 rotos**.
- **Hay que reapuntar el enlace aunque la portada ya exista.** Una versión anterior de `phase_unwrap_folder_links()` omitía las carpetas que ya tenían `index.md`, dando por hecho que entonces el enlace resolvía solo. No resuelve, por lo de arriba.
- **La ruta se codifica entera** con `quote()`, no solo los espacios. Hay artículos con `#` en el nombre —que Markdown lee como ancla, dejando el enlace apuntando a un fichero que no existe— y otros con paréntesis, que cierran el enlace antes de tiempo. Los dos salieron en el `mkdocs build`.
- **Los corchetes del título no hacen falta escaparlos.** Hay tres artículos con `]` dentro —`Error "Codigo[3000] Factura duplicada"`, `El editor de formularios [ Ctrl+F10 ]`—; van balanceados y Markdown los admite en el texto del enlace. Comprobado en el HTML generado.
- **La portada lleva una marca** (`<!-- portada de categoría generada automáticamente -->`). Con ella, la nuestra se rehace en cada ejecución y una escrita a mano se respeta.
- **La marca va DETRÁS del `# H1`, nunca delante.** Con el comentario en la primera línea MkDocs no detecta el H1 y titula la página **«Index»**: así salía en el panel izquierdo, en la pestaña del navegador y en los resultados de búsqueda.
- **La subcarpeta que repite el nombre de su madre no es una carpeta**: `docs/Actualizador/Actualizador/` es la categoría doblada en el origen. No sale en la lista de carpetas; sus artículos se listan con los sueltos de la madre.

#### La portada no debe salir como un artículo más

Para eso está `navigation.indexes` en las *features* del tema, y ya está puesta en `mkdocs.yml`. Sin ella, el `index.md` de la categoría aparece como **una entrada más dentro de la sección**; con ella, el título de la sección **es** el enlace a su portada:

```
sin navigation.indexes          con navigation.indexes
  grupo  API                      ENLACE  API   -> API/
  ENLACE Index -> API/            grupo   FAQ
  grupo  FAQ                      ENLACE  ...
```

Es incompatible con `toc.integrate`, que aquí no se usa.

### Las etiquetas que se comen su contenido

`protect_escaped_pseudo_tags()` aparta los `&lt;marcador&gt;` que no son HTML. Pero dejaba pasar los que **sí** son un nombre de etiqueta real, y ahí había una trampa: un artículo documenta una cabecera CSS escrita como

```html
<p>Cabecera:<br>&lt;style&gt;<br>.BlockBody{width:380px;}<br>&lt;/style&gt;</p>
```

Al des-escapar quedaba un `<style>` de verdad, y markdownify lo eliminaba **con todo lo que llevaba dentro**. El lector se quedaba con un «Cabecera:» colgando y sin el CSS. No se perdía la etiqueta: se perdía el contenido.

Y restaurarlas sin escapar tampoco vale: un `<style>` en el Markdown lo **aplica** el navegador como CSS de la página en vez de mostrarlo. Así que estas se devuelven **escapadas**, que es como se leen. Son `style`, `script`, `title`, `textarea`, `template`, `iframe`, `noscript` y `head`: 6 casos en 3 artículos.

### Cómo se comprueba que no se pierde contenido

El control más fuerte del repositorio, y el que encontró lo de arriba: convertir **todo** el origen con el código actual y comparar palabra por palabra contra el HTML de Freshdesk.

```
2.120 artículos comparados -> 7 pierden más del 3 %
```

Y los 7 se explican: uno es la compresión deliberada de las 602 fichas de parámetro, y en los demás las palabras que «faltan» son **fragmentos del origen** —`actua` + `lizar`, `omienza`, `ntroducción`—, porque Freshdesk parte palabras entre elementos (`<span>C</span>omienza`) y la salida las une bien.

Tres trampas del método, que costaron tres intentos:

1. **Emparejar por título no vale.** Hay dos artículos `Gestión de vulnerabilidades` —uno de FlexyGo y otro del ERP— y compararlos entre sí daba un 78 % de pérdida falsa. La clave tiene que ser el `ArticleId` de `generation_state.json`.
2. **`get_text(' ')` parte el código.** Pygments envuelve cada token en un `<span>`, así que el separador convierte `380px` en `380 px`. Hay que deshacer los `<span>` antes.
3. **`get_text('')` pega las palabras del origen.** Sin separador salen engendros como `stockconsulta` o `tickettpv` que no pueden aparecer en la salida, y todo parece perdido: 464 artículos falsos positivos.

### Las clases del editor bloqueaban el estilo del tema

Esto no era limpieza estética: era casi la mitad de las tablas publicándose **sin estilo ninguno**.

Material aplica todo lo suyo con el selector `.md-typeset table:not([class])` —bordes, relleno, cabecera, hover— y envuelve la tabla en un `md-typeset__scrollwrap` con el mismo criterio, para que las anchas se puedan desplazar en vez de desbordarse. Se comprobó en el bundle del tema: el envoltorio lo pone el JS en tiempo de ejecución, y el selector es literalmente `table:not([class])`.

Las tablas que se conservan en crudo llegaban con las clases de **Froala**, el editor de Freshdesk: `fr-no-borders` (676), `fr-alternate-rows` (456), `fr-dashed-borders`… **1.147 de 2.381**. Con ese atributo dejan de cumplir el selector, así que se publicaban sin bordes, sin relleno y sin scroll. Y no hay nada que las estilice en su lugar: en el CSS del tema **no existe una sola regla `fr-`**.

`quitar_clases_del_editor()` las retira, dentro de `limpiar_atributos_de_freshdesk()`. Solo las `fr-*`: si la etiqueta lleva alguna otra clase se conserva y el atributo se queda —el `index.md` usa `<div class="grid cards">` de Material—.

Resultado: **1.147 → 6** tablas con clase (las 6 llevan una clase ajena). Verificado construyendo el mismo artículo antes y después: antes `class=['fr-alternate-rows']` y sin envoltorio, después sin clase y con el estilo del tema.

### Un solo marcador de viñeta por documento

Mezclar `*` y `-` es desorden en el `.md`, y la mezcla la produce la propia casa: html2text emite `*` y `vinetas_literales_a_lista()` emite `-`. `unificar_marcadores_de_lista()` deja el que **ya predomina en ese fichero**, así que solo cambian los 34 que mezclaban en vez de reescribir las 6.895 viñetas del corpus.

El dominante se cuenta sobre el documento **entero**, y por eso la función se salta los fences ella misma en vez de ir envuelta en `_outside_fences`: envuelta, cada trozo entre bloques de código elegía *su* dominante y ocho ficheros seguían mezclando.

**Lo que esto NO arregla, y conviene saberlo.** Hay 37 listas donde unos items salen espaciados y otros apretados. Se investigó y no es el marcador: html2text deja el sub-listado a columna 0 en vez de anidado bajo su item —

```
  * **Estado:** Los diferentes estados son:

- _Generado:_ Los efectos que se generan desde una factura...
```

— y Python-Markdown funde las dos listas en una sola *suelta*. Inferir el anidamiento sería adivinar la estructura, y el efecto visible es solo algo más de aire entre esos items.

### La reparación de enlaces no puede entrar en el código

`fix_internal_links()` aparta el código —bloques ``` y trozos en línea— **antes de tocar nada**, y lo devuelve al final.

Faltaba, y borraba contenido. Dentro de un ejemplo, un `<a href>` es texto del ejemplo, no un enlace que reparar. La regla de anclas lo desenvolvía a su texto visible y, cuando el ancla **solo envolvía una imagen**, ese texto era vacío: desaparecía la línea entera. Así se perdía esto de un ejemplo de HTML —

```html
<div id="{IdEmpleado}"><a href="{path}/Forms/General/View.aspx?ot={ot}">
  <img class="circular" src="../Imagenes/thumbs.aspx?filename={foto}" alt="{Nombre}"></a></div>
```

— y quedaba un `<div id="{IdEmpleado}"></div>` vacío.

`repair_links.py` ya lo tenía en cuenta, y su docstring lo explica: «el SQL de la documentación está lleno de cosas que parecen un enlace». La misma protección faltaba en `common.py`, que corre antes.

**Alcance:** 1 artículo hoy (sus dos copias), pero es una **clase** de fallo: cualquier ejemplo de HTML o Markdown que lleve un enlace dentro se mutilaba, y el corpus no deja de crecer.

**Cómo apareció:** no lo vio ningún barrido de texto. Salió de comparar palabra por palabra el HTML del origen contra el HTML renderizado, artículo por artículo y emparejando por `ArticleId`. El artículo perdía un 25 % de sus palabras y todas eran atributos de HTML —`width`, `href`, `class`, `aspx`, `thumbs`—, que es lo que puso el foco en el ejemplo de código.

### La caja de aviso de Freshdesk venía disfrazada de código

Freshdesk dibuja sus avisos con `<pre class="fd-callout fd-callout--note">`. Al ser un `<pre>`, `protect_code_blocks()` las apartaba como si fueran código, y eso hacía dos daños:

- **Borraba las imágenes de dentro.** Al aislar el código se le quitan las etiquetas HTML reales, así que un `<img>` del aviso desaparecía. Eran 3 capturas, y una captura que falta se nota.
- Publicaba el texto del aviso **en gris y monoespaciado**, sin ajuste de línea. De algunos se encargaba después `desenvolver_fences_de_prosa()`, pero curándolo, no evitándolo.

`_cajas_de_aviso_de_freshdesk()` las convierte en `<div>` antes de que el código se aparte. Son **131 en 58 artículos**: `note` (81), `idea` (43) e `info` (7). Un `<pre>` sin esa clase sigue siendo código.

**Cómo apareció:** contando la estructura del origen contra la de la salida —imágenes, tablas y bloques por artículo—, no el texto. Faltaban 9 imágenes; una estaba dentro de un `<span>` sin texto, y ese `<span>` colgaba de un `fd-callout`.

De paso, esa comparación explicó las otras diferencias de estructura: de **132 tablas** que "faltaban", **123 estaban vacías en el origen** y las 9 restantes son las que se convierten en bloque de código a propósito.

### El aviso que lleva su texto en la misma línea

Una vez las cajas dejan de ser código, salen así: `**NOTA:** Si la intercalación de la instancia es distinta…`. Y esa forma la escribe también el autor a mano. Son **264 párrafos en 166 artículos** —`nota` 167, `importante` 59, `dato` 16, `ejemplo` 13—, y publicados quedaban como una negrita suelta a principio de párrafo, indistinguible del texto que la rodea.

`avisos_en_linea_a_admonitions()` es la tercera y última regla de avisos, y comparte criterio con las otras dos: el párrafo tiene que **empezar** por la palabra en negrita —a media frase es una mención, no un aviso—, y el cuerpo se toma hasta la primera línea en blanco. Una lista que continúa el aviso sí entra en la caja.

Resultado: **270 admonitions nuevas en 173 artículos**, de 221 a 491 en todo el corpus.

### Al ascender el rótulo, la captura no se pierde

`promover_negritas_a_encabezados()` exige que **todo** el texto visible del párrafo vaya dentro de la negrita. Y ahí estaba la trampa: **una imagen no aporta texto visible**, así que

```html
<p><strong>3. Accedemos a UTILIDADES / Validar ficheros:</strong><br><img src="..."></p>
```

cumplía el criterio y se ascendía a `<h2>` **descartando la captura**.

Es la misma trampa que ya había en `drop_empty_headings()`, donde se resolvió desenvolviendo en vez de borrar. Aquí la solución es distinta porque el rótulo **sí** es un título —es un paso numerado—: sube a encabezado y la imagen queda debajo, que es donde va.

Alcance: 7 imágenes en 6 artículos.

**Cómo apareció.** Contando la estructura del origen contra la de la salida, no el texto: faltaban 6 imágenes. Persiguiéndolas una a una, dos compartían forma —un párrafo que empieza en negrita y contiene una captura—, y de ahí salió la regla. Verificado después sobre los 5 artículos afectados: los 5 conservan ahora **todas** sus imágenes (`ERP - Facturas Certificadas y VeriFactu`, 40 de 40).

Con esto, la comparación estructural queda cuadrada del todo:

| diferencia origen → salida | explicación |
|---|---|
| 132 tablas menos | 123 estaban vacías en el origen; 9 se convierten en bloque de código a propósito |
| 6 imágenes menos | eran estas, ya recuperadas |

### La imagen que se quedaba con la URL del enlace

La red de seguridad que degrada las URLs de Freshdesk lleva una guarda `(?<!!)` para no tocar las imágenes: si una no se pudo descargar, sigue apuntando al servidor remoto y ahí se queda, porque una imagen remota se ve y una borrada no.

Pero esa guarda cuida de que el patrón no empiece **en** la imagen, no de que empiece en el corchete que la **envuelve**:

```
[![](S3-de-freshdesk)](otra-url)
```

El patrón casaba `[![](S3…)` y devolvía como texto solo `![`, que pegado al resto daba `![](otra-url)`. **La imagen acababa apuntando al enlace de fuera**, y desaparecía. Arreglado con la otra mitad de la guarda: `\[(?!!\[)`.

Y de raíz: una imagen envuelta en un enlace a Freshdesk se queda **solo en la imagen**, y eso se hace **antes que todo lo demás**. El editor enlaza la miniatura a la imagen grande o a la ficha del artículo; ese enlace no lleva a ninguna parte útil una vez publicado, y mientras está ahí desordena todas las reglas de enlaces, que ven un `[![](img)](url)` y toman el `![` de la imagen por el texto del enlace.

Los cuatro casos quedan fijados con test: imagen en enlace externo (se conserva entero), imagen suelta con URL remota (se conserva), imagen en enlace de Freshdesk (se queda la imagen sola) y enlace de texto a Freshdesk (sigue degradándose a texto).

### El enlace que ya no lleva a ningún sitio

Quedaban **89 enlaces relativos muertos**: apuntaban a un `.md` que no existe en `docs/`. Son artículos que en Freshdesk estaban despublicados o borrados, así que no hay destino que reparar y no lo habrá.

Publicados, cada uno era un 404 con aspecto de enlace bueno. `phase_unwrap_dead_links()` los **degrada a su texto**: se pierde la navegación, que no existía, y se conserva la frase.

```
antes:  consulta las [SGA - EMBALAJES](../SGA/SGA%20-%20EMBALAJES.md) del almacén
ahora:  consulta las SGA - EMBALAJES del almacén
```

Al aplicarlo cayeron 58 y quedaron 31 tercos. Los 31 no eran enlaces Markdown: eran `<a href>` **en crudo dentro de las tablas que se preservan tal cual**, y ninguna regla de Markdown los ve. `_desenvolver_anclas_sin_destino()` los desenvuelve con la misma comprobación contra disco. Total: **89 → 0**.

La fase va **antes** de `phase_tidy_blank_lines`, porque degradar un enlace que ocupaba su propio párrafo deja la línea vacía detrás.

### Un bloque de código o una imagen sí caben en la caja

Al montar las admonitions, el cuerpo se cortaba en cuanto la línea siguiente empezaba por `#`, `<`, `|`, `>`, ` ``` ` o `![`. Los dos últimos estaban de más.

Se comprobó **renderizando con la configuración real del tema**, no por intuición:

| detrás del aviso | dentro de la caja | veredicto |
|---|---|---|
| fence ` ```vbnet ` | `<div class="language-vbnet highlight">` | entra |
| `![](...)` | `<img>` visible | entra |
| `<table>` en crudo | `<p><table>` — HTML inválido | **no entra** |
| `## Encabezado` | sería la sección siguiente, no el aviso | **no entra** |

Así que ahora el fence y la imagen son cuerpo válido, y `_fin_del_bloque()` busca su cierre para no arrastrar el resto del artículo si el fence viniera sin cerrar. Son 3 artículos: los `**Ejemplo**` que tenían su bloque justo debajo.

La tabla se queda fuera a propósito, y hay un test que lo fija.

### El enlace de una tabla no lo reescribe MkDocs

MkDocs reescribe los enlaces Markdown, pero **no los que vienen en crudo dentro de una tabla conservada**: el HTML en bruto lo aparta antes de recorrer el documento. Así que un `<a href="ERP - Modelo 111.md">` salía publicado con el `.md` puesto y daba un 404 **aunque el artículo estuviera ahí al lado**.

Eran **87**, y no salían en ningún sitio: no en el informe de enlaces rotos —el destino existe—, ni en `mkdocs build`, que por el mismo motivo por el que no los reescribe tampoco los avisa. Solo aparecen validando el **sitio construido** contra el disco.

`phase_publish_html_links()` les da la forma con la que MkDocs publica, la de `use_directory_urls`: la página vive en su propia carpeta, así que hay un nivel más que subir y el destino pierde la extensión.

```
antes:  <a href="ERP - Modelo 111.md">Modelo 111</a>
ahora:  <a href="../ERP%20-%20Modelo%20111/">Modelo 111</a>
```

Dos cosas que costaron una vuelta:

- **Las dos fases se pisaban.** `phase_unwrap_dead_links` solo sabía buscar el fichero fuente, así que veía el `../X/` recién puesto y lo tomaba por muerto: degradaba a texto justo los 87 que la otra acababa de arreglar. Ahora `_tiene_destino()` entiende las dos formas, y la publicada la resuelve desde la **carpeta** de la página.
- **`Path.with_suffix` no vale aquí.** Se lleva por delante lo que hay tras el último punto, y estos títulos van llenos —`ERP - Modelo 369. Declaraciones de IVA…`, `AHORA Install 4.4.2400 - …`—. Cinco destinos buenos parecían no existir. El `.md` se **añade**, no se sustituye.

También se cerró la comilla del destino con la **misma** con la que abre: `[^"']*` cortaba en el apóstrofo de `ERP - Modelos 300, 320, 320 y 390 Gipuzkoa 'Ventanilla única'.md`, y esos 4 se quedaban sin traducir.

Con las tres cosas puestas, el sitio construido da **8.788 enlaces y 6.109 imágenes, ninguno roto, y 0 avisos de `mkdocs build`**.

### El encabezado que no tenía nada que enseñar

El editor de Freshdesk deja dentro de las tablas conservadas encabezados vacíos: `<h2><br/></h2>`. Publicados son un hueco en el índice lateral y un ancla que no lleva a nada visible: el lector no ve nada donde el índice le promete una sección. Eran 8 en 3 artículos.

`desenvolver_encabezados_html_sin_texto()` **desenvuelve**, no borra: uno de los 8 es un `<h1>` cuyo único contenido es una captura, y la captura sí se ve. Lo que sobra es que eso sea un encabezado, no la imagen.

### El vídeo que no dejaba ni rastro

El origen trae **106 vídeos de YouTube en 95 artículos**, todos como `<iframe>`. Ni html2text ni markdownify saben qué hacer con esa etiqueta: la borran con todo lo que lleva dentro. La página quedaba sin el vídeo **y sin nada que indicara que existía** —ni un enlace, ni un hueco—, así que el lector no podía ni echarlo en falta.

No lo detectaba ninguna comprobación de las que había: el artículo renderiza, no hay enlaces rotos y el texto está entero. Solo aparece comparando el origen con la página y preguntando por lo que el origen trae y la página no.

El vídeo se aparta **antes** de convertir, dejando una marca de texto plano en su propio párrafo —que es lo único que sobrevive a los dos motores—, y se devuelve al final, cuando ya no queda ninguna regla que tenga nada que decirle:

```html
<span style="display: block; position: relative; padding-bottom: 56.25%; …">
  <iframe src="https://www.youtube.com/embed/ID" … loading="lazy" allowfullscreen></iframe>
</span>
```

Tres decisiones, con su motivo:

- **Los estilos van en línea.** Así el bloque no depende de que nadie añada una hoja de estilos, y una regeneración que rehaga `docs/` no puede dejarlo sin ellos. El `padding-bottom: 56.25%` es la proporción 16:9: es la única forma de que un iframe se estire con el ancho sin franjas negras ni desbordar el móvil.
- **El envoltorio es un `<span display:block>`, no un `<div>`.** Tres de los vídeos vienen **dentro de una tabla conservada**, y ahí el bloque acababa metido en un `<p>` y un `<span>` ajenos: HTML inválido. Un span vale en los tres sitios y se comporta igual.
- **De la URL solo se guarda lo que significa algo.** El editor arrastra `wmode=opaque` y `feature=youtu.be`, y escribe `&amp;` sin des-escapar. Se conservan `list`, `start`, `t` e `index`; lo demás se tira.

Comprobado sobre los dos casos —vídeo suelto y vídeo dentro de tabla— renderizando con la configuración real: sale un `<iframe>` de verdad, colgando de su span.

### Los adjuntos no se pueden bajar, y hay que decirlo

27 artículos llevan ficheros colgados en Freshdesk —38 en total, y varios son contenido de verdad: `sacar usuarios SQL.sql`, dos fuentes `.ttf`, 13 PDF—. No se publican, y no es un descuido del conversor.

Freshdesk sirve los adjuntos con un **enlace firmado de S3 que caduca a los 5 minutos** (`X-Amz-Expires=300`). El que guarda la base de datos lleva caducado desde que se guardó: comprobado, responde **403 con firma y sin ella**. Las imágenes del cuerpo sí son públicas —esas responden 200— y por eso esas sí se descargan.

Así que aquí no hay nada que descargar, y publicar el enlace sería publicar un 404. Lo único honesto es dejar constancia, y eso hace `logs/adjuntos-no-publicados.txt`: artículo, nombre y tamaño de cada fichero, con la explicación de por qué no está.

**El arreglo de verdad no cabe en este repositorio.** Tiene que hacerlo el proceso que rellena `freshdesk_articles`, bajándose el fichero mientras la URL sigue viva. Cuando eso exista, publicar el enlace es trivial.

### Por qué NO se renumeran los encabezados

Se intentó, y se quitó. Queda escrito porque la idea es tentadora y volverá a aparecer.

**El problema aparente.** El índice lateral se dibuja con la sangría que dicta el nivel, así que un artículo que empieza en `###` sin haber usado `##` sale con sus secciones colgando de nada. Medido sobre el HTML publicado salían 101 artículos con la escalera rota.

**El primer descarte: 69 de esos 101 no eran nada.** Eran los `<h2>` y `<h3>` que el editor de Freshdesk dejó **dentro de una tabla conservada**. Esos no entran en el índice: Python-Markdown no recorre el HTML en crudo. Comprobado renderizando una tabla con un `<h3>` dentro — no aparece en el `toc`.

**El segundo descarte, y el importante.** La regla renumeraba los niveles usados a consecutivos, y para saber cuáles se usan hay que contarlos. Contarlos por texto es contar líneas que empiezan por `#`… y este corpus escribe encabezados **dentro de un item de lista**:

```markdown
  * ### **IVA de determinados productos frescos**
```

Python-Markdown publica eso como un `<h3>` de verdad. Al no contarlo, la regla creía que `ERP - Cambios de IVA` usaba `{h2, h4}` y bajaba los `h4` a `h3`: los tres casos que colgaban de «productos frescos» pasaban a ser **hermanos suyos**. Eso no es arreglar una jerarquía, es destruirla, y el origen la traía bien (`h3, h4, h4, h4`).

**La versión segura no vale la pena.** Conservadora —saltarse los documentos con encabezados anidados, y desplazar la escalera entera sin fundir nunca dos niveles— arregla **1 artículo** de 1.652. No compensa mantener una regla que puede aplanar una jerarquía real.

**Lo que sí queda.** Que un salto de nivel casi siempre está ahí por algo: el origen ya escribe así —326 artículos traen la escalera con huecos desde Freshdesk— y el resto de reglas de la casa ya los normalizan al publicar. Y que **medir encabezados sobre el HTML publicado engaña**: hay que contarlos donde los cuenta el `toc`.

### Un enlace que solo lleva una imagen no está vacío

Las dos reglas de «ancla sin texto» —la de las tablas conservadas, en `fix_internal_links`, y la que aparta anclas antes de markdownify— miraban solo el **texto**. Si dentro no había letras, daban el ancla por vacía: la de las tablas la reetiquetaba con su propia URL, y la del motor de autor la apartaba como enlace vacío.

Con un **banner** dentro, eso se comía la imagen:

```html
antes:  <a href="…/AhoraSolucionesFree/"><img src="…/QSPhKXcwe….png"></a>
salía:  <a href="…/AhoraSolucionesFree/">https://www.youtube.com/user/AhoraSolucionesFree/</a>
```

Una imagen sí se ve, y es justo lo que se pulsa. Ahora ambas reglas la respetan; el ancla realmente vacía —ni texto ni imagen— sigue llevando su etiqueta, porque sin nada dentro no hay dónde pulsar.

En el origen hay 7 anclas así, pero solo 1 se perdía de verdad: las otras 6 caen fuera del ERP o van por la ruta de Markdown, que las convierte bien.

**Cómo apareció.** No lo vio ninguna comprobación de texto: la palabra que faltaba era la URL, y las URLs se descartan al comparar. Lo destapó la **comparación estructural**, contando imágenes del origen contra imágenes de la página: 6.111 y 6.110. Una sola de diferencia en todo el corpus.

### El color escrito a mano y el modo oscuro

El editor de Freshdesk pinta los colores **dentro** del HTML del artículo, y un color en línea no cambia con el tema. El sitio tiene dos modos —claro con fondo `#f5f7f8`, oscuro con `#292929`—, así que un color fijo solo puede acertar en uno.

Midiendo el contraste real (WCAG) de cada trozo de texto contra el fondo que le toca, salían **20 trozos ilegibles en modo claro** (contraste por debajo de 3) en 11 artículos: los `1.-`, `2.-`… que numeran los pasos de Techfun en naranja claro, los `NOTA:` verdes de dos Hotfix, un `✘ No disponible` en `#999`.

`quitar_colores_ilegibles()` **suelta el color** en vez de oscurecerlo. Oscurecer conservaría el tono, pero un tono que cumple sobre el fondo claro deja de cumplir sobre el oscuro: se arreglaría un modo estropeando el otro. Sin color propio manda el tema, que acierta en los dos.

Tres cosas que costaron una vuelta, y que son el motivo de que la regla no sea un `sub()` de tres líneas:

- **Quitar el color solo sirve si detrás manda el tema.** En `Cierres de Inventario` la celda pone `color: black`, así que soltar el verde de dentro dejaba **negro sobre negro** en modo oscuro. Se comprobó comparando el corpus contra la publicación anterior: 44 trozos ilegibles en esa página pasaban a 46. Ahora se sueltan los dos —sobre fondo claro el negro no aporta nada, es el que ya pone el tema— y esa página baja a 25.
- **Si el fondo lo escribió el autor, el par se respeta.** Una celda de color con letra oscura dentro funciona igual en los dos modos. Y al revés: un fondo a mano **sin** color de letra recibe uno explícito, porque si no le cae encima el texto del tema y no se lee.
- **`rgba(0, 0, 0, 0)` es transparente, no negro.** El editor lo escribe a punta pala para decir «sin fondo». Tomarlo por negro hacía creer que había texto oscuro sobre negro donde no hay fondo ninguno: 2 falsos positivos que casi acaban en una letra blanca sobre nada.

Resultado medido: **modo claro 20 → 0**, y el modo oscuro **mejora** de 1.892 a 1.873 trozos ilegibles sin haberlo buscado. Quedan esos 1.873 en 136 artículos, que son otra tarea: casi todos son celdas con fondo claro fijado a mano y sin letra propia.

### La primera fila que hacía de cabecera sin serlo

El editor de Freshdesk no distingue cabecera de dato: escribe todas las celdas como `<td>` y marca la primera fila poniéndola en negrita o dándole un fondo gris. Publicado, el tema no tiene forma de saber que eso es una cabecera, así que no la destaca, no la separa del cuerpo y no la deja fija al desplazar la tabla a lo ancho.

`ascender_cabecera_de_tabla()` pasa esa fila a `<th>`, y el listón es alto a propósito: sin ningún `<th>` ya puesto, al menos tres filas, la primera con dos celdas o más, **todas** en negrita o con fondo, y tantas celdas como la fila más ancha. Las tablas de maquetado —970 sin cabecera— no la necesitan y no se tocan.

Son **2.878 celdas en 170 artículos**, bastantes más que las 41 tablas que salían al medir: la medición solo miraba las tablas de primer nivel, y en este corpus la tabla de datos suele ir **dentro** de la de maquetado.

### Los pasos que el autor numeró a mano

En vez de una lista ordenada, el origen trae párrafos sueltos que empiezan por un número, casi siempre en negrita:

```markdown
**1.IBAN** correctamente informado.

**2.** El banco debe tener informado **el código SWIFT/BIC**.
```

La negrita impide que Markdown los reconozca, así que se publican como párrafos independientes: con el espaciado de párrafo, sin sangría colgante y sin que se vea que son los pasos de un mismo procedimiento.

`pasos_numerados_a_lista()` los junta en una lista **apretada** —con una línea en blanco entre items, Python-Markdown envuelve cada uno en un `<p>` y la lista sale con el mismo aire suelto que se quería quitar—. Dos límites, y los dos por un motivo concreto:

- **La racha tiene que empezar en 1.** Python-Markdown no emite `start`, así que una numeración que arranca en el 12 saldría renumerada desde el 1 y diría otra cosa.
- **El separador puede venir doblado.** `**1.-** En la primera opción` consumía solo el punto y publicaba `1. **-** En la primera opción`, con el guion convertido en el texto del paso.

De 172 párrafos en 41 rachas quedan 21 en 3 artículos, que son las que no empiezan en 1.

### El índice escrito a mano que no llevaba a ninguna parte

136 artículos abren con un «Índice» o una «Tabla de contenidos» hecha a mano, y **ninguno de los 136 tenía un solo enlace**: listas de texto plano que enumeran las secciones y no se pueden pulsar. En 3 de ellos, además, los puntos venían sangrados con cuatro espacios, que en Markdown no es una lista sino un **bloque de código**: se publicaban en gris y monoespaciados, con los asteriscos a la vista.

Dos reglas, en este orden: `desangrar_el_indice()` los saca del bloque de código —manda la sangría del **primer** punto, no la menor, porque Markdown lee de arriba abajo— y `enlazar_indice_a_las_secciones()` enlaza cada punto con su sección. **1.694 enlaces internos, ninguno sin destino.**

Cuatro cosas que costaron una vuelta, y que están cada una en un test:

- **El ancla se le pide a Markdown, no se adivina.** `## _Configuración de_ **_ _ERP_**` acaba siendo `configuracion-de-_erp`. Aproximar el texto quitando asteriscos daba `configuracion-de-erp` y dejaba 6 enlaces apuntando a un ancla inexistente. Ahora las secciones se sacan del `toc_tokens` del propio Python-Markdown.
- **El índice acaba donde acaban sus puntos.** Cortar solo al llegar al siguiente encabezado dejaba la regla suelta por el resto del artículo: llegó a enlazar un `* ## TBAI` veinte párrafos más abajo.
- **El texto del punto se envuelve tal cual.** Limpiarlo se llevaba los guiones bajos de `Ahora_Impresion`, que no son énfasis sino parte del nombre.
- **Un asterisco suelto hay que escaparlo.** `Veri*Factu` fuera de un enlace se ve; dentro, Markdown lo lee como apertura de énfasis y desaparece.

### El código que venía metido en un párrafo de prosa

Los artículos de personalización escriben la explicación y la instrucción en el **mismo** párrafo, separadas por `<br>`:

```html
<p>Instrucción para cambiar el puntero del ratón.<br><br>
gCn.Obj.HourglassAll(true)<br><br>gCn.Obj.HourglassAll(False)</p>
```

Publicado, las dos llamadas salían como prosa: sin monoespaciado, sin resaltado y sin distinguirse de la frase que las explica. Son **537 líneas en 107 artículos**.

`codigo_suelto_en_parrafo_a_pre()` parte el párrafo y saca a un `<pre>` solo lo que **es** una sentencia —`Set`, `Dim`, `Sub`, una llamada con punto, un `If … Then`— y solo cuando en el mismo párrafo queda prosa: un párrafo entero de código ya lo recoge otra regla.

El criterio es estrecho a propósito. Con el criterio amplio de `detect_code_lang()` salían **1.615** líneas, y entre ellas descripciones de parámetro como `Campo (STRING): Especifica el nombre del campo`, que no son código. También entiende **T-SQL**, que en esta casa aparece tanto como el VB: la lista de parámetros de un procedimiento, cada uno con su comentario detrás. Con las dos gramáticas son **798 líneas en 114 artículos**.

Dos cosas que costaron una ejecución entera, y que están cada una en un test:

- **No se puede quitar «toda etiqueta» para leer el trozo.** El primer intento limpiaba con `<[^>]+>`, y los ejemplos de webservice llevan XML literal dentro del código: `request = "&lt;soap:Envelope xmlns:soap=…&gt;"`. Un artículo pasó de 815 palabras a 236. Ahora solo se quita el formato que mete el editor —`span`, `font`, `strong`…— y lo demás se respeta.
- **También va en el motor de autor**, desde que se encontró por qué perdía texto allí. Ver «La deuda del motor de autor».

El comentario en castellano no saca al SQL de su sitio: `@CadenaDefault NVARCHAR(1000) = N'', -- Valor por defecto para el nuevo campo` lleva «para» dentro, y el filtro de prosa —pensado para el VB, más laxo— habría partido la lista en dos.

### El enlace vacío que repetía la misma dirección

El editor de Freshdesk deja anclas sin nada dentro. La regla que las etiqueta con su URL las convertía en un enlace más, así que cuando el mismo destino ya estaba enlazado con un texto legible, la página publicaba la dirección dos y tres veces seguidas:

```
_**[https://we.tl/t-h0aLXCuCFw](…)**[https://we.tl/t-h0aLXCuCFw](…)[Descarga documentación](…)_
```

`quitar_anclas_vacias_repetidas()` borra el ancla vacía cuyo destino ya tiene un enlace con texto, y de dos vacías al mismo sitio se queda con la primera. Son **62 anclas en 39 artículos**. La que **no** tiene pareja no se toca: ahí la URL es lo único que se puede enseñar.

Una salvedad que costó un test en rojo: **una imagen dentro sí es contenido**. Sin ella, el ancla de un banner se borraba a sí misma, porque su propio destino figuraba en la lista de los que tienen contenido.

### Los vídeos que ya no se pueden ver

Un vídeo roto no se nota: el hueco del reproductor sale en blanco y el enlace parece bueno hasta que alguien lo pulsa. Y no hay forma de saberlo sin preguntar, porque el problema está **fuera** de esta documentación.

Cada ejecución pregunta por los vídeos enlazados y deja el resultado en `logs/videos-que-no-se-ven.txt`. De los **125** que hay en el corpus, **46 no se ven**, y aparecen en **73 artículos**:

| | |
|---|---|
| 44 | `videos.ahora.es` no responde |
| 2 | el vídeo ya no existe en YouTube (404) |

Los 44 son los enlaces del autor a sus vídeos de ejemplo, todos con la forma `videos.ahora.es/ScriptSamples#NN`. Si el servidor está retirado de verdad, esos enlaces sobran; si es interno y solo falla desde donde se genera, están bien. Esa decisión no la puede tomar el conversor.

Cómo se pregunta, y por qué así:

- **A YouTube por su `oembed`**, que responde 404 si el vídeo ya no existe y 401/403 si es privado o no admite incrustarse. Pedir la página del vídeo no vale: YouTube devuelve 200 igualmente.
- **Un servidor que no contesta se prueba una sola vez** y su veredicto vale para todos sus enlaces. Sin eso, los 44 de `videos.ahora.es` harían esperar seis segundos cada uno y la comprobación duraría más que media ejecución.
- **La URL se recorta en `<` y `>`.** Sin eso, `...list=PL8h4jt35t1wixmi>` daba 404 y el informe denunciaba una lista de reproducción borrada que estaba perfectamente.

Con `--sin-comprobar-videos` la ejecución no pregunta nada, por si se genera sin salida a internet.

### La sentencia que va sola en su hueco

El código no siempre viene en un bloque. El origen deja instrucciones sueltas en su propio párrafo, en una celda de tabla o en un punto de lista, sin nada que las distinga de la prosa que las rodea:

```html
<p><em>SELECT * FROM Conta_Apuntes_Bloqueos_Tipos</em></p>
<li>UPDATE Ceesi_configuracion SET Valor = 'ON' WHERE Parametro = 'SII'</li>
<td>gform.ControlesDDA("NombreControl").Text</td>
```

`sentencia_suelta_a_codigo()` las envuelve en `<code>`. **No en un bloque**: una sentencia dentro de una celda o de un punto de lista no puede ser un bloque sin romper la tabla o la lista, y en un párrafo el código en línea ya la distingue de sobra.

**Sola de verdad.** Si el hueco de al lado también es una sentencia, esto no es una instrucción suelta sino una línea de un bloque, y ese bloque lo reconstruye después `repair_vb_reference_markdown` en un fence con su lenguaje. Marcando la primera línea por su cuenta se rompía esa reconstrucción: en *Tipos de JOIN en el FROM*, un `CREATE TABLE [dbo].[Tab_PruebasA](` se llevó el fence entero y dejó las columnas de debajo como prosa — con `[Descrip] [varchar](50) NULL` publicado **como un enlace roto**, porque en Markdown eso es la sintaxis de un enlace. También se descarta la sentencia que se queda a medias, la que acaba en `(`, `,` o `Then`: la siguiente línea la continúa. Y se descarta si el vecino **continúa** la sentencia sin empezar otra —`from`, `inner join`, `on`, `where`—: en *ERP - Asignación de centros de coste* una consulta viene partida en cinco párrafos y solo el del medio empieza por algo con pinta de sentencia, así que se marcaba ese y quedaba una línea monoespaciada suelta dentro de una consulta que por lo demás iba en texto plano. Peor que dejarla entera.

**Dentro de una celda, la tirada entera.** Fuera se deja en paz porque el fence lo reconstruye `repair_vb_reference_markdown`, pero en una celda no hay fence que reconstruir: la tabla se conserva en HTML tal cual. Así que ahí la consulta partida se marca línea a línea, y la tirada se encadena por dos vías: la cláusula que continúa —`from`, `inner join`, `on`— y la línea anterior que se queda a medias. En el *Hotfix 74* la segunda línea es una lista de columnas pelada, sin forma de sentencia; entra porque la de arriba acaba en coma.

Tres cosas más que hubo que añadir, cada una con su caso real detrás:

- **La regla baja a buscar dentro.** La tabla de referencia de `Buscadores predefinidos` mete cada ejemplo en su propio `<p>` dentro de la celda: mirando solo el primer nivel, la celda se descartaba entera y con ella sus 31 ejemplos. Y la consulta suele venir en cursiva **dentro** de un párrafo con más texto —«Consulta: *SELECT \* FROM x* y mira el resultado»—, que sin bajar tampoco se veía.
- **La énfasis desaparece al marcar el código.** Una consulta en cursiva *y* monoespaciada a la vez es peor que cualquiera de las dos cosas por separado.
- **Una frase que habla de código no es código.** `INSERT INTO: se usa para añadir uno o varios registros` explica el `INSERT`, no lo ejecuta. Aquí el filtro de prosa se aplica también al SQL, al revés que en la lista de parámetros de un procedimiento, donde el comentario en castellano va dentro de la propia línea.

Medido sobre el corpus: el código publicado como texto normal pasa de **130 casos en 36 artículos a 28 en 15**. Lo que queda son tres cosas distintas, y ninguna es un descuido de esta regla: consultas partidas en varios párrafos, que habría que unir y eso ya es adivinar; y cuatro rutas del registro de Windows, un XML y una línea de comandos, que son literales sueltos en mitad de una frase.

### La tabla que se publicaba vacía

El editor de Freshdesk maqueta con tablas, y quedan restos: una tabla de una fila cuyas celdas solo llevan un `<br>` o un espacio duro.

```html
<table style="width: 100%;"><tbody><tr><td style="width: 100.0000%;"></td></tr></tbody></table>
```

Eso no es invisible. Material le pinta su borde y su margen, así que en el artículo sale un recuadro vacío en mitad del texto — los hotfixes de la versión 4.4.2100 los llevaban a pares. `quitar_tablas_vacias()` las tira: **60 tablas en 36 artículos**.

Una tabla cuenta como vacía solo si además no tiene imagen, enlace, `iframe` ni nada que se vea sin llevar una letra; una tabla de capturas no tiene texto y no hay que tocarla.

Y se recorre el texto crudo contando aperturas y cierres en vez de reconstruirlo con BeautifulSoup: la ida y vuelta normaliza el HTML del artículo entero —`&nbsp;` se vuelve el carácter, las etiquetas sueltas se cierran— y aquí solo queremos quitar un trozo, no reescribir el resto. La primera versión sí usaba BeautifulSoup y por eso se le escapaban justo las celdas con `&nbsp;`: el texto que buscaba ya no era el que estaba en el fichero.

### La etiqueta del lenguaje no es una sección

Los artículos de referencia del entorno de programación describen miembro a miembro, y cada miembro trae su ejemplo en los dos lenguajes. El origen los escribió con el mismo nivel que el miembro, o con uno más alto:

```markdown
### EditarPorObjeto
## Código en VB6
## Código en C\#
### EditarPorObjetoyVista
```

La jerarquía queda del revés: «Código en VB6» gobierna al miembro **siguiente** en vez de colgar del anterior, y en la página sale con letra más grande que el nombre del propio miembro. En *Grid - Todo lo que debes saber sobre este control* eso llenaba el índice lateral con 96 entradas «Código en VB6» y «Código en C#» tapando los 48 miembros de verdad — de ahí anclas como `#codigo-en-vb6_24`.

`encajar_etiquetas_de_codigo()` baja la etiqueta a un nivel por debajo del último encabezado que **no** es una etiqueta. Con `toc_depth: 3` eso las saca del índice sin quitarlas de la página: en el Grid, el índice pasa de **150 entradas a 56**.

Dos cosas la hacen segura, y las dos vienen del intento anterior de renumerar encabezados, que hubo que revertir:

- **Solo baja, nunca sube.** Una etiqueta que ya cuelga bien de su miembro se queda como está, y por eso la regla es idempotente.
- **Exige el nombre del lenguaje.** «Código en VB6», «Código C#», «Código SQL» sí; un «Ejemplo» o un «Código» a secas no, porque esos sí pueden ser una sección de verdad.

Medido sobre el corpus: **254 encabezados en 43 artículos**.

### Un encabezado que solo lleva un vídeo

`desenvolver_encabezados_html_sin_texto()` estaba enganchada solo a las tablas conservadas, así que nunca veía el cuerpo del artículo. En *ERP - Importador de Excel* el origen trae `<h1><span class="fr-video"><iframe …></span></h1>`: un encabezado cuyo único contenido es el vídeo. Como el vídeo se aparta a un token —que **sí** es texto—, html2text emitía `# %%VIDEO_1%%` y al restaurarlo quedaba un `#` vacío en la página. Era el único encabezado vacío de todo el corpus.

Ahora la regla se aplica al documento entero, en los dos motores. Medido sobre el origen: **590 encabezados en 358 artículos**, ninguno pierde texto —se desenvuelve, no se borra— y el resultado es idempotente. Los otros 589 ya no se veían, así que en la página solo cambia ese.

### La degradación necesita los encabezados ya definitivos

`demote_label_headings()` pasa a negrita el encabezado que no gobierna nada, pero `promover_negritas_sueltas()` **crea** encabezados después de ella. En *GCN. Cambiar tratamiento de los valores ANSI NULLS* un `##### Autor: …` parecía gobernar el `**Fecha: 15/12/2016**` de debajo, y se libraba; luego esa negrita pasaba a `## Fecha:` y el Autor se quedaba de encabezado.

Por eso la regla se pasa **una segunda vez** al final, con los encabezados ya definitivos. Es idempotente, así que la segunda pasada solo coge lo que la primera no podía ver: 2 encabezados en 1 artículo.

### Las imágenes que ya no usa nadie

Cada ejecución descarga las imágenes de los artículos que publica, pero nunca retiraba las de los que dejaron de publicarse: un artículo pasado a borrador, una captura que el autor sustituyó por otra.

`buscar_imagenes_huerfanas()` las localiza y **no borra nada**: escribe `logs/imagenes-huerfanas.txt` con la lista y el peso. Quien decide es `--prune-orphans`, la misma bandera que retira los artículos huérfanos.

Tres cosas que la hacen segura:

- **«Nadie» no son solo los artículos.** Se busca la mención en `mkdocs.yml` —que declara el logo y el favicon—, en las plantillas de `overrides/` y en las hojas de estilo, donde puede haber un `url()`. Sin eso, la primera ejecución se llevaría por delante el logo del tema.
- **Solo en una ejecución completa.** Si está filtrada por categorías, las imágenes de las que no se han generado parecerían huérfanas. En ese caso ni se buscan.
- **Se compara por la ruta a partir de la carpeta**, no resolviendo los `../..` de cada artículo. Medir eso mal es fácil: un primer intento de contarlas dio 789 ficheros y 54 MB que en realidad estaban todos referenciados.

Medido sobre el corpus de hoy: **0 huérfanas** de 5.499 ficheros.

### El lenguaje de un bloque se decide por recuento

`detect_code_lang()` tenía dos señales débiles con prioridad absoluta, y las dos ganaban a un recuento abrumador de la correcta:

- **JavaScript cortocircuitaba.** `_STRONG_JS_RX` se comprobaba la primera y devolvía sin mirar nada más. Un `window.o` suelto dentro de un comentario, en un script con 66 sentencias T-SQL, bastaba para publicar el bloque entero como JavaScript.
- **La llave suelta contaba como marcador inequívoco de C#.** No lo es: la usan igual JavaScript, Java, C y PowerShell. Un script de PowerShell —`$Servicio = …`, `Get-Service`, `Start-Service`— salía etiquetado `csharp`.

Ahora todos compiten por recuento. El punto y coma final y la llave sola **siguen contando para C#**, porque ahí sí hacen falta: son lo que lo distingue de VB, que no tiene ninguno de los dos. Lo que no pueden es ganar a un lenguaje que también los usa, así que cuando C# gana **solo** por esa puntuación, se cede a JavaScript, PowerShell o SQL si alguno tiene marcadores propios.

Ese matiz no es teórico: quitar la puntuación del recuento a secas dejaba 10 bloques de C# etiquetados como VB, porque el desempate entre los dos favorece a VB. El test `test_deteccion_de_lenguaje`, que ya existía, cazó la regresión.

Y se reforzaron los marcadores de T-SQL con lo que faltaba —`USE`, `GO`, `ALTER DATABASE`, `IF EXISTS(`, `VALUES(`—: sin ellos, un script de administración caía en `csharp` por el punto y coma, y un disparador en `vbnet`.

Medido sobre el corpus: **13 bloques cambian de etiqueta y ninguno empeora** —5 de C# que decían JavaScript, 4 de T-SQL que decían JavaScript o C#, 2 disparadores que decían VB y 1 de PowerShell que decía C#—.

### La viñeta con más de un espacio

`_ITEM_DE_LISTA_RX` exigía **exactamente un espacio** entre la viñeta y el texto, y Markdown admite de uno a cuatro. Una viñeta escrita con dos —`-  Incobrable`— no se contaba para elegir el marcador dominante ni se cambiaba al unificar, así que dos artículos seguían mezclando `*` y `-`.

Y mezclar no es solo desorden en el `.md`: Python-Markdown funde las dos listas en una sola suelta, y unos ítems salen espaciados y otros apretados dentro de la misma lista.

### El bloque reconstruido no es VB por defecto

`repair_vb_reference_markdown()` reagrupa en un fence las líneas de código que llegaron sueltas, y ahí fijaba `vbnet` a mano. Como el reetiquetado de más arriba solo toca los fences **sin** lenguaje —para no pisar un `csharp` ya detectado—, un T-SQL suelto se quedaba con resaltado de VB para siempre, por mucho que el detector supiera distinguirlo. Ahora se le pregunta, con VB de reserva.

### Un enlace no se encierra en un bloque de código

Esa misma reconstrucción toma por código cualquier línea que empiece por comillas. En *ERP - Reglas de No Sujeción en SII, VeriFactu y TicketBAI* eso envolvía una tabla de equivalencias entera —`"OT" en TicketBAI → N1 en VeriFactu`—, y dentro iba un enlace a la Agencia Tributaria que, publicado como texto literal, **no se puede pulsar**.

El código reconstruido aquí no lleva enlaces Markdown nunca, así que su presencia delata que el bloque es prosa. Con esa guarda, la tabla se queda fuera del fence y el enlace vuelve a funcionar.

### La deuda del motor de autor

Durante mucho tiempo `codigo_suelto_en_parrafo_a_pre()` y `sentencia_suelta_a_codigo()` estuvieron **desactivadas** en `convert_author`: al aplicarlas, tres artículos perdían entre el 18 % y el 23 % de su texto. Se dejó anotado que la causa era «una interacción con markdownify», sin más.

No era markdownify. Eran dos cosas, las dos en el camino de autor y ninguna en las reglas.

**Una.** `merge_plain_code_paragraphs()`, dentro de `sanitize_author_html()`, hacía esto:

```python
part = html_lib.unescape(part)          # &lt;soap:Envelope&gt; → <soap:Envelope>
part = re.sub(r'(?is)<[^>]+>', '', part)  # …y ahora se lo lleva como si fuera marcado
```

Des-escapar primero y borrar «toda etiqueta» después destruye el XML literal de los ejemplos de webservice. Es el mismo fallo que ya se había corregido en `codigo_suelto_en_parrafo_a_pre` con `_solo_texto_del_trozo`, y aquí seguía. Ahora solo se quita el formato del editor y **no se des-escapa**: quien lo hace bien es `protect_code_blocks`, que antes quita las etiquetas de verdad y respeta los marcadores del ejemplo.

**Y dos, la de fondo.** Las reglas se aplicaban al HTML *antes* de entrar al conversor, como en el motor estándar. Pero `convert_author` empieza por `sanitize_author_html()`, que reescribe a fondo el marcado de código —une párrafos, rehace los `<pre>`, fusiona rachas— y por el camino se dejaba texto del que acababa de ponerse.

El hueco bueno es **entre el saneado y `protect_code_blocks`**: ahí el saneado ya ha terminado y el código se pone a salvo inmediatamente después. Por eso `_convert_with_markdownify()` recibe ahora `marcar_codigo` y las aplica él mismo.

Medido sobre los 311 artículos del motor de autor: **18 ganan marcado de código y ninguno pierde ni una palabra** —la comprobación es palabra a palabra, no por porcentaje—. Seis bloques más quedan con su lenguaje y unas cuarenta marcas más de código en línea.

### El resultado tiene que ser idempotente

`phase_tidy_blank_lines()` es lo último de `repair_links.py`, y no está por cosmética.

El conversor ya ordena las líneas en blanco, pero las fases de enlaces corren **después**: al degradar una URL o quitar un enlace queda la línea vacía detrás, y el fichero acaba con rachas de tres y cuatro saltos o con una línea de un solo espacio. Eran 5 artículos.

Lo que se busca es que **aplicar las reglas otra vez no cambie nada**. Si al acabar la ejecución la limpieza aún tendría trabajo, el fichero no está en su forma final y no hay forma de comprobar de un vistazo que una ejecución está completa. Con el repaso puesto, el corpus pasa esa prueba: se aplicaron las **diez** reglas de limpieza sobre los 1.652 artículos y ninguna encontró nada que cambiar.

### El enlace lleva el título de su destino

Cuando el origen trae una URL de Freshdesk desnuda, se traduce al artículo local. La etiqueta era `Enlace Interno`, que no le dice nada al lector:

```
Enlace: [Enlace Interno](Asignar%20el%20tipo%20de%20efecto%20de%20la%20eFactura....md)
```

Y la información estaba: el slug de la URL era `asignar-el-tipo-de-efecto-de-la-efactura-a-los-efectos-en-el-erp`. Ahora la etiqueta es el **título del artículo de destino**, que ya conocemos porque acabamos de resolverlo. Se le quita el sufijo `(ArticleId)` de los títulos que colisionan, que en el texto de un enlace no aporta nada.

Eran 9. Las otras etiquetas escuetas del corpus —6 `aquí`, 4 `Enlace`— **no se tocan**: esas las escribió el autor, y reescribir su prosa no es asunto del conversor.

**Cómo apareció:** de la comparación palabra a palabra. `Mensaje 'Element PaymentDetails'` perdía un 6,7 % y las palabras que faltaban eran justo las del slug.

## Marcadores entre ángulos

En el origen viene `&lt;identity impersonate&gt;`. html2text lo des-escapa a `<identity impersonate>`, y el navegador —que no conoce esa etiqueta— **no pinta nada**: el lector se queda sin saber qué subclave buscar.

`escapar_marcadores_entre_angulos()` devuelve el escape a lo que va entre ángulos y no es ni una etiqueta HTML de verdad ni un autolink. Se aplica **antes** de restaurar el código, porque dentro de un bloque los ángulos son código y no se tocan.

## Cuando la URL no es una URL

Hay artículos donde alguien pegó un párrafo entero en el campo del enlace de Freshdesk. Queda esto en el origen:

```html
<a href="http://Modificar%20Cuotas%20Antes%20de%20continuar%20con%20el%20proceso…"></a>
```

Mil y pico caracteres con la prosa del propio artículo, codificada, y un `http://` delante. El ancla está vacía, así que en Freshdesk no se veía. Pero la regla de «enlace sin texto → poner la URL como texto» la convertía en un **muro de 2.264 caracteres** en mitad de la página. Estaba en los siete artículos de la serie de amortizaciones, que comparten ese pie.

`url_es_plausible()` descarta lo que no puede ser una dirección: un espacio en el nombre del servidor —o su forma codificada `%20`— o un tamaño desmedido. Si el enlace no traía texto, se quita entero y no se pierde nada; si traía, se conserva la frase y se tira el enlace, que no llevaba a ninguna parte.

El listón es deliberadamente bajo, y esa es la parte delicada: `http://servidor:puerto/AhoraAPI/api` **es un marcador de posición legítimo** de la documentación de la API. Un criterio más estricto —exigir un host con puerto numérico, por ejemplo— se lo llevaría por delante.

## Enlaces a otros productos

Un artículo de ERP puede enlazar a uno de TPV. Mientras la documentación de TPV no esté publicada, ese enlace apunta a un `.md` que no existe, y ahí es donde acaban casi todos los de `enlaces-rotos.txt`.

**No se corrigen solos, y es a propósito.** El destino no está en `docs/`, así que no hay nada local a lo que reapuntar: lo que toca es sustituir el destino por la URL del sitio de ese producto, del estilo

```
https://ayuda.ahora.es/Flexygo/9.x/Installation/CreatingProduct/
```

Eso se hace **a mano**, con el informe delante. Por eso `enlaces-rotos.txt` va agrupado por destino y no por fichero de origen: todos los enlaces de un mismo grupo llevan la misma URL base, así que se sustituyen de una sentada.

```
----------------------------------------------------------------------
DESTINO: TPV   (57 enlaces)
----------------------------------------------------------------------

ERP\Compras\ERP - Compras - Facturas de acreedor.md
    texto  : tipo de gasto
    destino: ../../TPV/TPV - Configuración y parámetros/TPV - ERP - Configurar tipos de gastos.md
```

Una vez sea una URL absoluta, deja de contar como roto: la validación ignora todo lo externo.

Y una razón más para no bajar `MIN_WORD_OVERLAP`: con el valor 1 que tenía antes, la fase 3 podía reapuntar un enlace de TPV a un artículo de ERP que compartiera una palabra. Con el umbral actual, los 72 se quedan quietos, que es lo que se quiere.
