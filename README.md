# Freshdesk To MkDocs

Repositorio de trabajo para generar documentación MkDocs a partir de los artículos de Freshdesk almacenados en SQL Server.

Esto es lo que hace falta para **usarlo**. El porqué de cada regla de conversión —qué se rompió, cómo se detectó y por qué la regla es como es— está en [NOTAS-DEL-PIPELINE.md](NOTAS-DEL-PIPELINE.md).

## Qué hace este repo

Todo el flujo lo orquesta [migrate.py](migrate.py):

1. Lee categorías, carpetas y artículos de la BDD.
2. Reparte una ruta de salida **única** por artículo (los títulos duplicados llevan su `ArticleId`).
3. Convierte cada artículo a Markdown con uno de los dos motores de [converters.py](pipeline/converters.py).
4. Descarga las imágenes a `docs/docs_assets/images` y reescribe las rutas.
5. Resuelve los enlaces internos de Freshdesk a ficheros `.md` locales.
6. Escribe la portada `index.md` de cada categoría y de cada carpeta, para que tengan URL propia.
7. Ejecuta la reparación y validación de enlaces de [pipeline/repair_links.py](pipeline/repair_links.py).
8. Si todo termina bien, consolida el estado incremental en `generation_state.json`.

### Los dos motores de conversión

| Motor | Base | Cuándo se usa |
|---|---|---|
| `convert_standard` | html2text | Por defecto. Conserva las tablas como HTML crudo. |
| `convert_author` | markdownify | Artículos con HTML muy troceado, detectados por `AUTHOR_MARKERS` en [migrate.py](migrate.py). |

El motor se elige **una sola vez, antes de escribir el fichero**.

## Estructura

```
run.ps1              Lanzador interactivo. Es por donde se empieza.
migrate.py           El orquestador. Único punto de entrada del pipeline.

pipeline/            Los módulos que hacen el trabajo. Nada se ejecuta solo.
  common.py            Nombres de fichero, .env, imágenes, enlaces internos.
  generation_state.py  La memoria: qué se generó, cuándo y dónde.
  converters.py        Los dos motores HTML → Markdown.
  article_fixes.py     Parches de artículos concretos, como datos.
  repair_links.py      Reparación y validación de enlaces relativos.
  reporting.py         Los informes de la ejecución: dónde van y cómo se llaman.

tests/               Tests de regresión. Sin BDD ni red.
logs/                Informes de la última ejecución. Ignorados por git.

docs/                La documentación generada + los estáticos versionados.
overrides/           Tema Material parcheado.
publish_scripts/     Publicación con mike (npm run docs:publish).
mkdocs.yml           Configuración de MkDocs.
generation_state.json  Estado incremental. VERSIONADO a propósito.
```

La regla es simple: en la raíz solo está lo que se ejecuta a mano. Todo lo que
es maquinaria vive en `pipeline/`.

| Archivo | Para qué |
|---|---|
| [run.ps1](run.ps1) | Menú interactivo: elige producto y opciones sin recordar flags. |
| [migrate.py](migrate.py) | Orquestador único. Lee la BDD, genera, informa. |
| [pipeline/common.py](pipeline/common.py) | Utilidades compartidas: nombres, rutas, imágenes, enlaces internos. |
| [pipeline/generation_state.py](pipeline/generation_state.py) | Estado incremental por `ArticleId`. |
| [pipeline/converters.py](pipeline/converters.py) | Los dos motores HTML → Markdown y sus heurísticas. |
| [pipeline/article_fixes.py](pipeline/article_fixes.py) | Parches por artículo y por enlace, como datos. |
| [pipeline/repair_links.py](pipeline/repair_links.py) | Reparación y validación de enlaces relativos. |
| [pipeline/reporting.py](pipeline/reporting.py) | Los informes de cada ejecución: rutas, nombres y limpieza de los viejos. |
| [tests/test_pipeline.py](tests/test_pipeline.py) | Tests de regresión de las piezas. Sin dependencias. |
| [tests/test_ejecucion_completa.py](tests/test_ejecucion_completa.py) | Ensayo del flujo entero con la BDD falseada. |

## Requisitos

- **Python 3.12 o superior** (el código usa sintaxis que no compila en 3.11).
- ODBC Driver 17 for SQL Server.

```powershell
pip install -r requirements.txt
```

Para construir y publicar la documentación:

```powershell
pip install -r requirements-docs.txt
```

## Configuración

Crea un `.env` en la raíz. Con autenticación integrada de Windows no hay contraseña que guardar:

```env
AUTHOR_ARTICLES_CONNECTION_STRING=DRIVER={ODBC Driver 17 for SQL Server};Server=SERVIDOR\INSTANCIA;Database=Brain;Trusted_Connection=yes;TrustServerCertificate=yes;
```

Con usuario y contraseña:

```env
AUTHOR_ARTICLES_CONNECTION_STRING=DRIVER={ODBC Driver 17 for SQL Server};Server=SERVIDOR\INSTANCIA;Database=Brain;UID=usuario;PWD=password;TrustServerCertificate=yes;
```

## Uso

### Lo normal: el lanzador

```powershell
.\run.ps1
```

Pregunta qué producto generar —con la lista sacada de la propia base de datos, y el número de artículos de cada uno— y qué opciones quieres. Antes de tocar nada enseña la orden equivalente y pide confirmación. No hay que recordar ningún flag.

Al terminar deja el resumen de la ejecución por pantalla y en `logs/resumen.txt`.

### A mano

Por producto:

```bash
python migrate.py --product "ERP"
```

Por categoría:

```bash
python migrate.py --categories "Actualizador"
```

Todo:

```bash
python migrate.py --all
```

Hay que indicar **siempre** uno de los tres. Si no hay ninguno y la consola es interactiva, se pregunta; en una ejecución desatendida el script falla con un mensaje claro en lugar de quedarse colgado esperando un `input()`.

### Opciones útiles

| Opción | Efecto |
|---|---|
| `--force` | Ignora el estado incremental y regenera todo lo que encaje con el filtro. |
| `--clean-output` | Borra las categorías generadas de `docs/`. **Conserva** `docs_assets`, `javascripts`, `stylesheets` y las portadas `index*.md`. |
| `--only-author` / `--skip-author` | Restringe al motor de autor, o lo excluye. |
| `--include-drafts` | Genera también los borradores. Por defecto se omiten. |
| `--prune-orphans` | Borra los `.md` que sobran: artículos eliminados en origen, pasados a borrador, movidos de carpeta o renombrados (solo dentro del filtro). |
| `--skip-link-repair` | No ejecuta la fase de enlaces. Útil para iterar rápido. |
| `--category-contains` / `--product-contains` | Coincidencia parcial en lugar de exacta. |
| `--list-products` | Lista los productos con su recuento de artículos y sale. Es lo que alimenta el menú de `run.ps1`. |

### Tests

```bash
python tests/test_pipeline.py
python tests/test_ejecucion_completa.py
```

Ninguno necesita BDD ni red.

- `test_pipeline.py` prueba las piezas por separado: conversión, enlaces, estado, rutas.
- `test_ejecucion_completa.py` prueba el flujo entero de `migrate.main()` con la base de datos falseada: qué se genera, qué se deja en paz, qué se limpia y qué pasa cuando algo falla.

Pasa los dos antes de tocar el motor de conversión o el incremental.

## Un producto de una sola categoría

Si la ejecución genera **un único producto** y ese producto tiene **una sola categoría**, la carpeta de la categoría no se crea: sus carpetas van directas a `docs/`.

```
python migrate.py --product "CRM"

docs/FAQ (CRM)/Conector CRM - Office 365.md        en vez de
docs/CRM by flexygo/FAQ (CRM)/Conector CRM - Office 365.md
```

Todo el sitio es ese producto, así que el nivel no distingue nada y el lector se lo come para llegar a cualquier artículo. La ejecución lo dice al empezar:

```
[*] «CRM by flexygo» es la única categoría de este producto: sus carpetas van directas a docs/.
    Los enlaces a la categoría llevan a «FAQ (CRM)».
```

Cada carpeta que sube recibe su portada `index.md`, igual que antes. Los enlaces que apuntaban a la categoría van a la primera carpeta del producto —la primera por nombre—, porque al no haber carpeta de categoría no hay ninguna página que la represente.

**Solo cuando se genera un producto.** Si la ejecución abarca varios, la categoría se conserva; el porqué está en [NOTAS-DEL-PIPELINE.md](NOTAS-DEL-PIPELINE.md). Y cambiar de ámbito mueve los ficheros de sitio: eso lo detecta `find_relocated_articles` y lo limpia `--prune-orphans`.

## Borradores

Un artículo de Freshdesk lleva un `status` dentro de su JSON: `1` es borrador y `2` publicado. La tabla **no viene pre-filtrada**, así que por defecto el script omite los borradores y lo dice por consola. Con `--include-drafts` se generan igualmente.

El filtro se aplica en Python, no en el SQL, por dos razones:

- El reparto de rutas necesita ver **todos** los artículos para que el desempate de títulos duplicados no cambie según lo que se genere en cada ejecución.
- Un artículo que pasa de publicado a borrador tiene que poder detectarse como sobrante para que `--prune-orphans` retire su `.md`.

Solo se omite el valor `1` exacto. Si algún día cambia el nombre de la clave en el JSON, el peor caso es no filtrar nada —lo que se hacía antes—, nunca omitir en silencio la documentación entera.

## Estado incremental

- `generation_state.json`: estado consolidado por artículo, con su ruta y su `updated_at` de origen. **Es la memoria del proceso: tiene que estar versionado.** Sin él, la siguiente ejecución regenera los más de 2.000 artículos.
- `.generation_run_state.json`: estado de la ejecución en curso. Se vuelca por lotes de 200 artículos.

Un artículo se regenera si su `ArticleId` no está en el estado, si su `updated_at` de origen ha cambiado, o si su `.md` no está en disco.

### La huella del pipeline

`meta.pipeline_fingerprint` guarda un hash de `common.py`, `converters.py`, `article_fixes.py` y `repair_links.py`. Si cambia, se regenera todo una vez y se avisa por consola:

```
[*] El pipeline ha cambiado desde la última ejecución: se regenera todo
    (huella 9f2c1a4b7d3e5068 → 4c8e0b1a6f2d9375)
```

Sin esto, el estado solo miraba el `updated_at` del artículo en Freshdesk. Un arreglo del conversor o de los enlaces **solo alcanzaba a los artículos que por casualidad cambiaran en origen**, y el resto se quedaba con la salida antigua indefinidamente, sin ningún aviso. Pasó de verdad: se corrigieron las reglas de enlaces y la documentación siguió cuatro horas con los enlaces viejos, porque los `.md` se habían escrito cuatro minutos antes de tocar el código.

Un estado sin huella —de una versión anterior— también cuenta como cambio: no hay forma de saber con qué código se generó.

### Qué pasa cuando algo falla

El estado consolida **siempre lo que se ha generado bien**. Un artículo que falla al convertir no llega al estado, así que su entrada se queda con el `updated_at` viejo (o no existe) y la ejecución siguiente lo reintenta sola. El proceso devuelve código de salida `1` para que se note, pero sin tirar la contabilidad del resto.

Esto importa en una ejecución periódica: antes, **un solo** artículo defectuoso impedía escribir el estado entero, y a la semana siguiente el script daba por no generados los más de 2.000 artículos y volvía a sobrescribir todos los `.md` sin modificar.

Si lo que falla es la reparación de enlaces, los `.md` están generados y el estado consolidado: relánzala aparte con `python -m pipeline.repair_links`.

## Ficheros que sobran

Hay dos formas de que un `.md` se quede en `docs/` sin dueño, y el script las distingue:

| Caso | Qué ha pasado | Cómo se detecta |
|---|---|---|
| **Huérfano** | El artículo ya no existe en origen, o ha pasado a borrador. | Está en el estado y no en la lista de publicables. |
| **Reubicado** | El artículo sigue vivo, pero le han cambiado la categoría, la carpeta o el título. | La ruta guardada en el estado no es la que le toca ahora. |

Un reubicado **no** es un huérfano: como sigue existiendo en origen, sin esta comprobación su fichero anterior se quedaría en `docs/` para siempre. Su `.md` nuevo se genera solo, porque el incremental ve que la ruta nueva no existe.

Sin `--prune-orphans` solo se informa; no se borra nada. Al borrar, las carpetas que se quedan vacías se retiran también.

Dos salvaguardas para no borrar nunca la única copia de un artículo: solo se mira lo que está dentro del filtro de la ejecución —un artículo movido *desde* una categoría que no se está generando necesita `--all` para limpiarse— y se exige que el fichero nuevo exista ya en disco.

## Cosas que no se deben hacer

- No bajes `MIN_WORD_OVERLAP` ni `MIN_FUZZY_TOKEN_OVERLAP`. Con umbrales de 1 los enlaces se reasignan a artículos sin relación.
- No pongas en `VB_LANG` (ni en ningún fence) un alias que Pygments no conozca: el bloque se pinta sin resaltar y no avisa nadie.
- No toques las reglas de limpieza de énfasis sin un test delante. `\*\s*\*` parece que borra cursivas vacías, pero casa con el `**` de **toda** negrita y deja el documento entero en texto plano. Por lo mismo, el separador `* * *` de un `<hr>` hay que normalizarlo **antes** de mirar el énfasis.
- No conviertas antes de llamar a `protect_code_blocks`. Es lo que impide que el código se trocee, se reindente o se pierda.
- No metas parches de artículos concretos dentro del motor: van a [article_fixes.py](pipeline/article_fixes.py).
- **No parchees con un `ArticleFix` lo que es un fallo del motor.** Hubo uno que borraba el ```` ``` ```` de cierre de un bloque «porque sobraba». Lo que sobraba en realidad era que la racha de SQL se hubiera tragado la prosa, y el parche convertía ese fallo en otro peor: un fence sin cerrar que descuadraba el resto del artículo. Si el mismo síntoma puede salir en otro artículo, el sitio del arreglo es el motor.
- Cuidado al aflojar `_ESCAPED_DASH_RUN_RX`. Pide que tras los guiones venga algo que **no sea otro guion**: si se admite cualquier carácter, `-{2,}` se come todos los guiones de una línea separadora menos el último y toma ese por el texto, robándole la línea a la regla de `---`.
- No edites `generation_state.json` a mano.
- No despliegues con `mike` desde este repo si el repo final de documentación es otro.
- No subas `.env` al remoto.
- No asumas que dos artículos con el mismo título son el mismo documento.

## Informes de la ejecución

Todos en `logs/`, colgando del directorio de salida, e ignorados por git. Los escribe [pipeline/reporting.py](pipeline/reporting.py), que es el único módulo que sabe dónde van y cómo se llaman.

Dos reglas, y la segunda es la importante:

1. **Todos los informes de una ejecución van juntos.** Antes `migrate.py` escribía en `<output_dir>/logs` y `repair_links.py` en la carpeta del repositorio: al generar con `--output-dir`, los informes de una misma ejecución acababan repartidos en dos sitios.
2. **Lo que está en la carpeta es de esta ejecución.** Si un informe no tiene nada que contar, su fichero no se escribe, y si quedaba uno viejo con ese nombre, se retira. Un informe de errores de la semana pasada sobreviviendo a una ejecución limpia es la peor clase de log: dice que hay errores y no hay forma de saber que no son de ahora.

| Informe | Contenido |
|---|---|
| `resumen.txt` | Qué ha cambiado en esta ejecución, y el índice de los demás. **Siempre está.** |
| `articulos-con-error.txt` | Artículos que no se pudieron convertir. Se reintentan solos. |
| `enlaces-rotos.txt` | Enlaces a documentación que no está en `docs/`. Se corrigen a mano. |
| `titulos-duplicados.txt` | Títulos que colisionan y qué nombre le tocó a cada uno. |
| `imagenes-no-descargadas.txt` | Imágenes que no se pudieron descargar. |

Así que **si en `logs/` solo está `resumen.txt`, la ejecución no tuvo ninguna incidencia**. No hace falta abrir nada más ni comparar fechas.

El resumen es lo que se lee para saber si la ejecución ha ido bien, y lo que conviene pegar en el mensaje del commit de la documentación:

```
RESUMEN DE LA EJECUCIÓN
======================================================================
Ejecución del 2026-09-03T09:52:11Z

Artículos nuevos                : 12
Artículos actualizados          : 31
Artículos movidos o renombrados : 2
Artículos retirados             : 1
Borradores omitidos             : 132
Errores de conversión           : 0
Enlaces internos resueltos      : 87

Informes de esta ejecución, en la carpeta logs/:
  enlaces-rotos.txt  Enlaces a documentación que no está en docs/. Se corrigen a mano.
```

## Si la ejecución se corta

El avance se vuelca a `.generation_run_state.json` cada 200 artículos. Si el proceso muere (Ctrl+C, caída, corte de red al descargar imágenes), la ejecución siguiente lo detecta, avisa y **reanuda**: no repite lo que ya estaba escrito en disco.

Con `--force` se ignora ese fichero y se empieza de cero.

Ojo al matiz de los 200: si el corte llega antes de ese primer volcado, no hay nada que reanudar.

## El tema está clavado a una versión de Material

`overrides/main.html` **no es un override normal**: es una copia completa del `base.html` de Material, con la maquetación propia dentro (`fh-sidebar`, `fh-sidebarheader`, `fh-maincontainer`, `fh-rightsidebar`, el `<dialog>` de navegación, sin footer).

Esa copia lleva los nombres de los assets del tema **escritos a mano**, y Material les pone un hash en el nombre que cambia en cada versión:

```jinja
<link rel="stylesheet" href="{{ 'assets/stylesheets/main.342714a4.min.css' | url }}">
<script src="{{ 'assets/javascripts/bundle.13a4f30d.min.js' | url }}"></script>
```

Si actualizas `mkdocs-material`, esos ficheros dejan de existir, dan 404 y **el sitio se sirve sin CSS ni JavaScript**: HTML desnudo, con los checkboxes de la navegación a la vista. No hay ningún error en el build, así que no avisa nadie.

Por eso `requirements-docs.txt` fija `mkdocs-material==9.6.14`. **No subas esa versión sin actualizar a la vez los cuatro assets del override.** Para saber cuáles toca poner:

```bash
python -c "import material,os,re,pathlib; p=pathlib.Path(os.path.dirname(material.__file__))/'templates'/'base.html'; print(*sorted(set(re.findall(r'assets/[a-z/]+/[A-Za-z0-9_.-]+[.](?:css|js)', p.read_text(encoding='utf-8')))), sep='\n')"
```

La solución de fondo es reescribir el override como `{% extends "base.html" %}` dejando solo los bloques personalizados, para que Material inyecte siempre sus propios assets. Implica revisar la maquetación a ojo, porque el override reestructura el DOM entre bloques que Material no expone limpiamente.

### Otras notas del entorno

- El plugin de i18n instalado es `mkdocs-i18n`, que es el que espera `mkdocs.yml` (`plugins: - i18n:`). No es el mismo paquete que `mkdocs-static-i18n`.
- Windows reserva el puerto 8000 (Hyper-V/WSL), así que `mkdocs serve` falla con `WinError 10013`. Usa otro: `mkdocs serve -a 127.0.0.1:8080`.

## Publicación con MkDocs y Mike

Este repo genera contenido; no tiene por qué ser el repo final de publicación.

1. Generar aquí la documentación.
2. Llevar `docs`, `mkdocs.yml` y `overrides` al repo real si procede.
3. Validar con `mkdocs build`.
4. Publicar desde el repo correcto con `mike deploy latest`.

## Mantenimiento

Antes de tocar el incremental, prueba al menos:

1. `python tests/test_pipeline.py` y `python tests/test_ejecucion_completa.py`.
2. Ejecución completa de una categoría pequeña (`--categories "Actualizador"`).
3. Segunda ejecución seguida: debe generar 0 artículos.
4. Corte a mitad (Ctrl+C) y reejecución: debe rehacer lo pendiente.
5. Un artículo con `updated_at` nuevo.
6. Un artículo borrado en origen, con y sin `--prune-orphans`.

Y si tocas la conversión o los enlaces, comprueba además sobre `docs/` ya generado:

- Ningún fichero con un número impar de marcas ```` ``` ````.
- Ningún enlace a `freshdesk.com/a/`.
- Ningún `[](...)` sin texto.
- Ningún `%%CBLK_n%%` ni ningún otro token del conversor a la vista.
- Ninguna etiqueta del panel de más de `NAV_TITLE_MAX` caracteres. Se miran sobre el sitio ya construido, no sobre los `.md`: la etiqueta sale de la cabecera YAML, no del H1.
