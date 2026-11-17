# Versión 10.0

Sebastian HR 10.0 amplía la gestión de ausencias, noticias y reservas, y renueva la plataforma. También incorpora nuevas opciones para fichar, planificar y consultar información, junto con mejoras en la experiencia diaria.

## Lo más destacado

### Permisos por horas

Configura cada tipo de permiso para que se solicite por días, por horas o de ambas formas. Los permisos por horas no descuentan días y sus horas retribuidas y no retribuidas aparecen en la exportación de nómina y cuentan al calcular la jornada.

[Más información: horas de vacaciones](../horas/horas-de-vacaciones.es.md)

### Ayuda dentro de la aplicación

Abre la guía desde el botón de ayuda de la barra superior y consulta la información sin salir de Sebastian HR. El contenido se adapta a tu perfil: verás la guía para empleados o la dirigida a RR. HH. y responsables.

[Más información: guía de ayuda](../index.es.md)

### Visibilidad de noticias

Decide quién puede ver las noticias de cada categoría según su área, empresa, oficina, equipo o empleado. Configura las reglas en «Visibilidad de la categoría»; si una categoría no tiene reglas, seguirá siendo visible para todo el mundo.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas repetidas

Reserva varios recursos a la vez y repite las reservas cada cierto número de días, semanas, meses o años. En las repeticiones mensuales y anuales puedes elegir una fecha o una posición, como el último viernes, y excluir fines de semana y festivos.

[Más información: cuadrantes de planificación](../turnos-y-planificacion/cuadrantes.es.md)

### Web API y asistentes de IA

Conecta asistentes compatibles con MCP para consultar datos y hacer gestiones con instrucciones en lenguaje natural, según los permisos de cada usuario. Un administrador activa MCP y autoriza a los usuarios; después, cada uno conecta su asistente a la dirección de Sebastian HR terminada en `/mcp` e inicia sesión.

[Más información: Web API](../integraciones/web-api.es.md)

### Actualización de plataforma

Sebastian HR funciona ahora sobre Flexygo 10. La actualización renueva, entre otras cosas, los calendarios anuales de vacaciones y ausencias; la conexión de asistentes de IA mediante MCP también está disponible en esta versión.

## Otras novedades

### Ausencias y solicitudes

- **Solicitudes de ausencia:** puedes registrar una ausencia para empleados de la lista de ausencias no planificadas y establecer días mínimos y máximos por solicitud. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Cálculo de horas:** configura los tipos de ausencia no remunerada para que no cuenten en las horas teóricas.
- **Cancelaciones:** las solicitudes para cancelar ausencias tienen ahora un tipo propio, separado del de cancelar vacaciones.
- **Notificaciones:** los correos de solicitudes de vacaciones y ausencias indican las fechas solicitadas. [Más información](../documentos-y-comunicacion/configuracion-de-notificaciones.es.md)

### Fichajes y dispositivos

- **Gestión diaria:** puedes ignorar o reactivar varios fichajes a la vez y filtrar los días con fin de turno automático. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Terminales Kapri:** conecta terminales de Kimaldi para que los empleados fichen con una tarjeta NFC o un código QR. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Punto de acceso:** puedes mostrar el código que tecleas aunque esté configurado como oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes

- **Gestión de fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Libro de Registro de Jornada:** consulta el desglose diario de ausencias y permisos, con un resumen por tipo. [Más información](../informes/informes-de-control-horario.es.md)

### Jornadas y planificación

- **Incidencias de jornada:** las alertas por retrasos, salidas anticipadas y límites de turno respetan las tolerancias; las de descanso aparecen antes de validar la jornada. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Plataforma e interfaz

- **Modo mantenimiento:** los administradores pueden activarlo desde el menú superior.
- **Aplicación instalable:** instala Sebastian HR en el ordenador o el móvil desde el navegador.
- **Interfaz:** se renueva el diseño de inicio de sesión y el de los avisos, confirmaciones y peticiones de datos.

### Gastos y Web API

- **Partes de gastos:** desde el móvil, añade líneas al formulario y adjunta los justificantes.
- **Procesos de la Web API:** las llamadas deben incluir la colección correspondiente y respetar los permisos del usuario. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** vuelven a guardarse los pasos y a mostrarse correctamente los comentarios y solicitudes filtradas; los flujos simultáneos se resuelven al aceptar o denegar.
    - **Ausencias:** vuelven a funcionar las listas, opciones y fichajes planificados; se corrigen las cancelaciones, los avisos y la gestión de días pasados y no laborables.
    - **Empleados:** se corrigen la edición de contratos, los cursos, las inscripciones, la firma de documentos, las notificaciones, las sugerencias y la ficha del empleado.
    - **Fichajes:** se corrigen la hora y la zona horaria, la actualización tras fichar, las solicitudes, las restricciones de turno y los controles de ubicación.
    - **Informes e integraciones:** vuelven a funcionar las importaciones; los informes respetan periodos y filtros, y se corrigen las conexiones con otras aplicaciones.
    - **Jornadas:** se corrigen el cálculo de horas, las incidencias, la planificación, los descansos, los festivos y los turnos de empleados sin planificación.
    - **Navegación:** se corrigen los botones de acciones y la visualización de formularios, menús y listas desplegables en móviles y tabletas.
    - **Planificación:** vuelven a funcionar los patrones, la selección y el arrastre de turnos; al cambiar un turno se actualiza su duración.
    - **Instalación y traducciones:** los paquetes ya no incluyen archivos de documentos subidos y se corrige la traducción de tipos de solicitud y fichaje.
