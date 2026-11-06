# Versión 10.0

La versión 10.0 incorpora nuevas formas de gestionar permisos, noticias y reservas, y amplía las opciones de instalación e integración. También mejora el control de jornada, las aprobaciones y el uso diario de la aplicación.

## Lo más destacado

### Permisos por horas

Registra permisos por horas y consúltalos en el calendario y el planificador del empleado. No descuentan días del saldo; sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada, y se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: restricciones de ausencias](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Ayuda integrada

Consulta la ayuda desde la navegación de la aplicación, sin salir de tu entorno de trabajo. Así tienes a mano la información para resolver dudas mientras utilizas Sebastian HR.

### Noticias por audiencia

Limita quién puede ver las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para que cada noticia llegue a las personas correspondientes.

### Reservas recurrentes

Crea reservas repetidas para varios recursos a la vez, con una frecuencia de días, semanas, meses o años. Puedes excluir fines de semana y festivos; si alguna fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección.

### Incidencias de jornada

La detección de incidencias tiene en cuenta tolerancias, pausas, descansos y límites de horas, y señala el día en que se superan los límites semanales, mensuales o anuales. Si un día no tiene horario previsto, no genera una incidencia por fichajes ausentes.

[Más información: incidencias de jornada](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

## Otras novedades

### Instalación y despliegue

- Puedes instalar Sebastian HR como una aplicación y abrirla desde la dirección de inicio configurada.
- Puedes desplegar Sebastian HR con Docker y configurar ambas bases de datos en una misma instancia.
- Los documentos subidos a la aplicación ya no se incluyen en los paquetes publicados.
- La aplicación incorpora un modo de mantenimiento.

### Ausencias y aprobaciones

- Puedes definir un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- Los tipos de vacaciones y ausencias reciben automáticamente su flujo de aprobación. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- La conversación de una solicitud se mantiene unificada durante la validación y la revisión. [Más información](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md)
- Las cancelaciones siguen el grupo de tipos correspondiente, ordenado en listas y menús; también puedes gestionar vacaciones sin fechas de inicio y fin. [Más información](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)

### Fichajes

- Puedes ignorar o reactivar varios fichajes desde la lista diaria; los ignorados no afectan al cálculo de ubicación del día.
- La vista agrupada muestra y permite filtrar los días con fin de turno automático y los fichajes de salida creados al cerrar un turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- Puedes consultar el código de acceso del empleado en el Punto de Acceso aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes

- Puedes generar informes desde la gestión agrupada mensual o semanal de fichajes. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- El Libro de Registro de Jornada distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- Puedes crear y consultar partes de gastos con una experiencia mejorada en dispositivos móviles.

### Integraciones y WebAPI

- La integración con terminales Kapri/Kimaldi permite gestionar fichajes con identificadores NFC. [Más información](../integraciones/kapri.es.md)
- Se incorpora la integración con Kapri. [Más información](../integraciones/kapri.es.md)
- Puedes crear cursos mediante nuevas operaciones de la WebAPI y consultar descripciones más completas de sus procesos, parámetros y vistas. [Más información](../integraciones/web-api.es.md)

### Interfaz y acceso

- La pantalla de inicio de sesión renueva su imagen y estilos; el asistente de configuración adopta los colores de Sebastian HR.
- Los avisos, alertas y cuadros de confirmación y solicitud de datos adoptan el estilo de Sebastian HR.
- Los procesos muestran el término «Entrada» en el idioma disponible.

### Turnos y planificación

- Los turnos muestran colores asignados por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- En el modo LITE puedes consultar los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se muestran solo las solicitudes de los tipos elegidos y se completan correctamente las acciones y los pasos pendientes. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
    - **Ausencias:** vuelven a funcionar el borrado de solicitudes pasadas sin restricciones y la cancelación sin días seleccionados, y se evitan incidencias de descanso incorrectas. [Más información](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)
    - **Empleados:** se corrigen la edición de contratos, la visualización de fotografías y estados, las excepciones de teletrabajo, los cursos, las inscripciones, los documentos y el botón QR.
    - **Fichajes:** se corrigen la actualización tras fichar, las fechas, los duplicados, los festivos, la ubicación, las jornadas de 24 horas, los comentarios y los turnos nocturnos. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/casos-de-uso-de-fichajes.es.md)
    - **Jornadas y planificación:** se recuperan la resolución en lote y los cálculos correctos de descansos, turnos y horas previstas, y vuelve a funcionar la navegación por patrones. [Más información](../turnos-y-planificacion/turnos.es.md)
    - **Informes e importación:** se corrigen las fechas de periodo, los resúmenes de jornada, los calendarios y saldos de vacaciones, y la lectura de hojas y plantillas de fichajes. [Más información](../informes/catalogo-de-informes.es.md)
    - **Instalación e integraciones:** se recuperan los recursos visuales y el inicio de Docker, y vuelven a funcionar las comprobaciones de licencia y conexión. [Más información](../introduccion/requisitos-de-instalacion.es.md)
    - **Navegación móvil:** vuelven a funcionar los desplegables en paneles y dispositivos móviles, y se muestra correctamente el menú lateral.
    - **Procesos y solicitudes:** se corrigen las fechas de informes, las gestiones de vacaciones y fichajes, los formularios largos en móvil, las notificaciones y el envío anónimo de sugerencias.
    - **WebAPI:** las solicitudes de ausencia se procesan correctamente aunque lleguen varias al mismo tiempo. [Más información](../integraciones/web-api.es.md)
