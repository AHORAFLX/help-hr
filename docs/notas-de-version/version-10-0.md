# Versión 10.0

La versión 10.0 amplía las opciones para gestionar ausencias, noticias y reservas, y facilita el acceso a la ayuda y a Sebastian HR desde asistentes de IA. También actualiza la plataforma y mejora la gestión de fichajes, jornadas e informes.

## Lo más destacado

### Permisos por horas

Puedes configurar cada tipo de permiso para que se solicite por días, por horas o de ambas formas. Las horas no descuentan días de permiso y, si el permiso es retribuido o no retribuido, aparece en la exportación de nómina y se incluye en el cálculo de la jornada.

[Más información: horas de vacaciones](../horas/horas-de-vacaciones.es.md)

### Ayuda desde la aplicación

Abre la ayuda desde el botón de la barra superior sin salir de Sebastian HR. La guía se adapta a tu perfil y muestra la información pertinente para empleados o para el equipo de RR. HH. y responsables.

[Más información: ayuda de Sebastian HR](../index.es.md)

### Visibilidad de noticias

Decide quién puede ver las noticias de cada categoría según su área, empresa, oficina, equipo o empleado. Configura las reglas en «Visibilidad de la categoría»; si una categoría no tiene reglas, las noticias siguen siendo visibles para todo el mundo.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Reserva varios recursos a la vez y repite las reservas cada cierto número de días, semanas, meses o años. Puedes elegir una fecha o una posición concreta en las repeticiones mensuales y anuales, excluir fines de semana y festivos, y revisar los conflictos antes de corregirlos.

### MCP y WebAPI

Conecta asistentes compatibles con MCP para consultar datos y realizar gestiones con tus propias palabras, según los permisos de tu perfil. Un administrador debe activar MCP en la configuración de la WebAPI y autorizar a los usuarios; cada usuario conecta su asistente a la dirección de la aplicación terminada en /mcp e inicia sesión.

[Más información: configuración de WebAPI](../integraciones/web-api.es.md)

### Actualización a Flexygo 10

Sebastian HR funciona ahora sobre Flexygo 10. La actualización renueva, entre otros elementos, los calendarios anuales de vacaciones y ausencias, y permite conectar asistentes de IA mediante MCP.

[Más información: versiones de Sebastian HR](../introduccion/ediciones-lite-y-pro.es.md)

## Otras novedades

### Ausencias y solicitudes

- **Gestión de ausencias:** registra desde la lista de ausencias no planificadas el tipo que elijas y fija límites mínimos y máximos para las solicitudes. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Cómputo:** configura si las ausencias no remuneradas cuentan en las horas teóricas.
- **Solicitudes y avisos:** las cancelaciones tienen un tipo propio y los correos indican las fechas y el tipo de solicitud. [Más información](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md)

### Fichajes y dispositivos

- **Descansos:** una nueva incidencia avisa si el descanso fichado supera el previsto en el turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Gestión diaria:** ignora o reactiva varios fichajes a la vez y consulta o filtra los días con fin de turno automático. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Terminales Kapri:** permite fichar con una tarjeta NFC o un código QR. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Punto de acceso:** muestra el código que estás escribiendo aunque esté configurado como oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Gastos e informes

- **Partes de gastos:** añade líneas desde el móvil mediante un formulario y adjunta sus justificantes; el asistente también puede adjuntar la foto del ticket.
- **Informes de fichajes:** genéralos desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-control-horario.es.md)
- **Libro de Registro de Jornada:** incluye el desglose diario de ausencias y permisos y un resumen por tipo. [Más información](../informes/informes-de-control-horario.es.md)

### Jornadas y planificación

- **Incidencias de jornada:** las de entrada retrasada, salida anticipada y límites del turno respetan las tolerancias; las de descanso aparecen antes de validar la jornada. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Aplicación y experiencia

- **Modo de mantenimiento:** los administradores pueden activarlo desde el menú superior.
- **Aplicación instalable:** instala Sebastian HR en el ordenador o el móvil desde el navegador.
- **Inicio de sesión:** se renueva el diseño de la pantalla.
- **Avisos y cuadros:** las alertas, confirmaciones y peticiones de datos tienen un diseño nuevo con un color y un icono para cada tipo.

### WebAPI y asistentes

- **Ausencias:** el asistente puede adjuntar el justificante al registrar una ausencia y consultar el detalle de una solicitud. [Más información](../integraciones/web-api.es.md)
- **Notificaciones:** consulta desde la WebAPI las notificaciones disponibles en la aplicación. [Más información](../integraciones/web-api.es.md)
- **Noticias:** la WebAPI permite marcarlas como leídas y consultar su estado de lectura. [Más información](../integraciones/web-api.es.md)
- **Permisos:** las operaciones y los datos de la WebAPI se limitan según los permisos del usuario. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** vuelve a funcionar la configuración de flujos y la lista de validación muestra las solicitudes, comentarios y resultados correctos. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
    - **Ausencias y vacaciones:** se corrigen el cómputo de horas, las solicitudes y cancelaciones, la edición de días pasados, los formularios de las listas y la inserción de fichajes planificados. [Más información](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)
    - **Empleados:** vuelven a funcionar la edición de contratos y cursos, la inscripción dentro de plazo, el envío de documentos a firmar, los avisos y las fichas. [Más información](../empleados-y-organizacion/modificacion-masiva-de-empleados.es.md)
    - **Fichajes:** se corrigen el acceso, las solicitudes de cambio, las zonas horarias, la planificación, la actualización de pantalla y los registros en turnos nocturnos o desde otras ubicaciones. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/casos-de-uso-de-fichajes.es.md)
    - **Informes, importaciones e integraciones:** vuelven a funcionar las plantillas de Excel, los informes y las conexiones con los sistemas integrados. [Más información](../informes/catalogo-de-informes.es.md)
    - **Jornadas:** se corrigen el cálculo, las incidencias, los descansos, la planificación y la resolución de incidencias para que reflejen correctamente cada turno y fichaje. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
    - **Navegación:** se corrigen acciones sin proceso asociado y la visualización de formularios, listas, menús y ventanas en móviles y tabletas.
    - **Planificación:** se recuperan las acciones del planificador y se corrigen la cancelación de reservas, la duración de turnos y las horas mostradas para permisos. [Más información](../turnos-y-planificacion/cuadrantes.es.md)
    - **Plataforma y WebAPI:** se corrigen las traducciones de tipos y la información devuelta por la lista de sugerencias. [Más información](../integraciones/web-api.es.md)
