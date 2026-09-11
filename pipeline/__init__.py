"""
pipeline
========
Los módulos que hacen el trabajo de la migración de Freshdesk a MkDocs.

El único punto de entrada es ``migrate.py``, en la raíz del repositorio. Aquí
dentro no hay nada que se ejecute solo, con una excepción: la reparación de
enlaces se puede lanzar suelta con ``python -m pipeline.repair_links``.

Qué hay en cada módulo, en el orden en que los usa una ejecución:

- ``common``           – utilidades compartidas: nombres de fichero seguros,
                         lectura del ``.env``, descarga de imágenes y
                         resolución de enlaces internos.
- ``generation_state`` – la memoria del proceso: qué artículo se generó,
                         cuándo y en qué ruta. Es lo que hace incremental la
                         ejecución semanal.
- ``converters``       – los dos motores HTML → Markdown.
- ``article_fixes``    – parches de artículos concretos, escritos como datos.
- ``repair_links``     – reparación y validación de los enlaces relativos,
                         siempre la última fase.

Requiere Python 3.12 o superior.
"""
