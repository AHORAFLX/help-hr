# Versión 10.0

Sebastian HR 10.0 amplía la gestión de permisos, la planificación de recursos y las conexiones con asistentes de IA. También renueva la plataforma y mejora el trabajo diario con fichajes, jornadas e informes.

## Lo más destacado

### Permisos por horas

Ahora puedes configurar cada tipo de permiso para solicitarlo por días, por horas o de ambas formas. Las horas no descuentan días de permiso; además, las horas retribuidas y no retribuidas aparecen en la exportación de nómina y cuentan en el cálculo de la jornada.

[Más información: horas de vacaciones](../horas/horas-de-vacaciones.es.md)

### Ayuda dentro de la aplicación

Abre la guía desde el botón de ayuda de la barra superior y consulta la información sin salir de Sebastian HR. El contenido se adapta a tu perfil: verás la guía para empleados o la destinada a RR. HH. y responsables.

[Más información: guía de ayuda](../index.es.md)

### Visibilidad de noticias

Decide quién puede ver las noticias de cada categoría según su área, empresa, oficina, equipo o empleado. Configura las reglas en «Visibilidad de la categoría»: sin reglas, la categoría es visible para todo el mundo; con reglas, basta con cumplir una para verla.

[Más información: visibilidad por categoría](../documentos-y-comunicacion/visibilidad-de-documentos-por-categoria.es.md)

### Reservas recurrentes

Reserva varios recursos a la vez y repite las reservas cada cierto número de días, semanas, meses o años. Puedes definir fechas mensuales o anuales concretas, excluir fines de semana y festivos, y revisar los conflictos antes de corregirlos sin rellenar de nuevo el formulario.

### Asistentes conectados con MCP

Conecta asistentes compatibles con MCP y otras aplicaciones mediante la WebAPI. Los asistentes pueden consultar datos y realizar gestiones con instrucciones en lenguaje natural, siempre dentro de los permisos de cada usuario; un administrador activa MCP y autoriza el acceso.

[Más información: conexión con la WebAPI](../integraciones/web-api.es.md)

### Actualización de plataforma

Sebastian HR funciona ahora sobre Flexygo 10. La actualización renueva, entre otros elementos, los calendarios anuales de vacaciones y ausencias; la conexión con asistentes mediante MCP se explica en otra novedad de esta versión.

## Otras novedades

### Ausencias y solicitudes

- Puedes asignar ausencias desde la lista de ausencias no planificadas, fijar límites de días por solicitud y excluir ciertos tipos no remunerados de las horas teóricas. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- Las cancelaciones de ausencias tienen un tipo de solicitud propio, y los correos detallan las fechas y el tipo de solicitud. [Más información](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md)

### Fichajes

- Una nueva incidencia avisa si el descanso fichado supera el previsto; también puedes filtrar los días con fin de turno automático. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- Ignora o reactiva varios fichajes a la vez desde la gestión diaria, y muestra el código que tecleas en el punto de acceso. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)
- Conecta terminales Kapri de Kimaldi para que el personal fiche con una tarjeta NFC o un código QR. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)

### Jornadas y turnos

- Las incidencias por entrada retrasada, salida anticipada o límites del turno tienen en cuenta las tolerancias configuradas. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- Las incidencias por descanso entre jornadas o por más de seis horas sin pausa aparecen antes de validar la jornada. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

### Gastos e informes

- El asistente puede adjuntar la foto de un ticket a una línea de gasto; desde el móvil, añade líneas a un parte y adjunta justificantes.
- Genera informes desde la gestión agrupada mensual o semanal de fichajes. El Libro de Registro de Jornada desglosa ausencias y permisos por día y tipo. [Más información](../informes/informes-de-control-horario.es.md)

### Plataforma y configuración

- Los administradores pueden activar el modo mantenimiento desde el menú superior, y puedes instalar Sebastian HR como aplicación desde el navegador.
- Se renueva el diseño de inicio de sesión y el de los avisos y cuadros de alerta, confirmación y petición de datos.
- En modo LITE, puedes consultar los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Integraciones y WebAPI

- Las integraciones pueden marcar notificaciones como leídas, consultar su lista y el detalle de una solicitud, y marcar noticias como leídas o consultar su estado. [Más información](../integraciones/web-api.es.md)
- El asistente puede adjuntar el justificante de una ausencia y extraer las fechas y horas que falten. [Más información](../integraciones/web-api.es.md)
- Las llamadas a procesos de la WebAPI requieren la colección y aplican los permisos del usuario. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** vuelven a guardarse y mostrarse correctamente los pasos, comentarios y solicitudes; los flujos que validan todos los pasos resuelven la solicitud al recibir una respuesta. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
    - **Ausencias:** se corrigen el cálculo de horas, las solicitudes y cancelaciones, las opciones de las listas, la inserción de fichajes planificados y la gestión de compensaciones y horarios. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
    - **Empleados:** vuelven a funcionar la edición de festivos, contratos y habilidades; se corrigen permisos, cursos, documentos, avisos, sugerencias y la foto de la ficha.
    - **Fichajes:** se corrigen el punto de acceso, la hora y zona horaria, la planificación, las solicitudes, la ubicación, la actualización de jornadas y la gestión diaria. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/casos-de-uso-de-fichajes.es.md)
    - **Jornadas:** se corrigen las incidencias, los turnos partidos, los festivos trabajados, la planificación y el cálculo de descansos y horas computables. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
    - **Informes e importaciones:** vuelven a cargarse las plantillas de Excel; los informes respetan periodos y filtros, y muestran correctamente fechas y ausencias. [Más información](../informes/catalogo-de-informes.es.md)
    - **Instalación e integraciones:** los paquetes ya no incluyen archivos de documentos subidos y vuelven a funcionar las consultas de licencias y la conexión con AHORA ERP. [Más información](../integraciones/integracion-con-ahora-erp.es.md)
    - **Navegación:** se corrigen los botones y formularios largos, los menús laterales y las listas desplegables en móviles y tabletas.
    - **Noticias y planificación:** vuelven a abrirse noticias y documentos y se registran sus lecturas; también se corrigen las reservas, los turnos y los patrones.
    - **Plataforma y WebAPI:** se corrigen las traducciones de tipos de solicitud y fichaje, y la lista de sugerencias incluye la reacción del usuario. [Más información](../integraciones/web-api.es.md)
