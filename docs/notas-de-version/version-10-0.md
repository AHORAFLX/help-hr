# Versión 10.0

Sebastian HR 10.0 amplía la gestión de ausencias, fichajes y planificación. También incorpora opciones de despliegue y cambios en la navegación, los informes y los procesos de aprobación.

## Lo más destacado

### Permisos por horas

Registra permisos por horas y consúltalos en el calendario y el planificador del empleado. No descuentan días del saldo, pero sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada, y se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: horas de vacaciones](../horas/horas-de-vacaciones.es.md)

### Terminales Kapri y Kimaldi

Integra terminales Kapri y Kimaldi para gestionar fichajes con identificadores NFC. Puedes asociar identificadores a empleados y procesar los eventos de los terminales; también puedes configurar opciones relacionadas y borrar identificadores desde la lista.

[Más información: terminales Kapri](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)

### Ayuda integrada

Consulta la ayuda desde el propio entorno de Sebastian HR, sin salir de la aplicación. El nuevo espacio reúne el acceso a la documentación para que puedas resolver tus dudas mientras utilizas la herramienta.

[Más información: ayuda de Sebastian](../index.es.md)

### Noticias según visibilidad

Decide quién puede ver las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para que cada persona vea solo las noticias que le corresponden.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Crea reservas repetidas para varios recursos a la vez y define su frecuencia en días, semanas, meses o años. Puedes excluir fines de semana y festivos; si alguna fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección.

[Más información: planificación de turnos](../turnos-y-planificacion/cuadrantes.es.md)

### Incidencias de jornada

La detección de incidencias tiene en cuenta tolerancias del turno, pausas, descansos y límites de horas. Los límites semanales, mensuales y anuales se señalan el día en que se superan, y no se avisa de fichajes ausentes si ese día no hay horario previsto.

[Más información: incidencias de jornada](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

## Otras novedades

### Ausencias y vacaciones

- **Límites de solicitud:** fija un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Cancelaciones:** sigue el grupo de tipos correspondiente y permite gestionar solicitudes aunque no tengan fechas de inicio y fin. [Más información](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)

### Instalación y plataforma

- **Docker:** despliega Sebastian HR y aloja ambas bases de datos en una misma instancia.
- **Aplicación instalada:** instala Sebastian HR como aplicación y ábrela desde la dirección de inicio configurada.
- **Modo de mantenimiento:** activa un modo de mantenimiento en la aplicación.
- **Cursos por WebAPI:** crea cursos mediante nuevas operaciones de la WebAPI. [Más información](../integraciones/web-api.es.md)

### Fichajes

- **Gestión diaria:** ignora o reactiva varios fichajes a la vez desde la lista diaria.
- **Vista agrupada:** reúne los avisos e identifica y filtra los cierres automáticos de turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Punto de Acceso:** consulta el código de acceso del empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes y gastos

- **Informes de fichajes:** genéralos desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Libro de Registro de Jornada:** distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** crea y consulta partes con una experiencia mejorada en dispositivos móviles. [Más información](../informes/catalogo-de-informes.es.md)

### Aprobaciones y procesos

- **Flujos de aprobación:** cada tipo de vacaciones o ausencia usa automáticamente el flujo que le corresponde. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Conversaciones:** la conversación de una instancia se mantiene unificada entre la validación y la revisión. [Más información](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md)
- **Correos de vacaciones y ausencias:** incluyen la fecha y distinguen el tipo en el asunto. [Más información](../documentos-y-comunicacion/configuracion-de-notificaciones.es.md)

### Interfaz y navegación

- **Avisos y ventanas:** adapta el estilo de avisos, alertas, confirmaciones y solicitudes de datos a Sebastian HR; también renueva la pantalla de inicio de sesión.
- **Asistente de inicio de sesión:** adopta los colores de Sebastian HR.
- **Procesos:** muestran el término «Entrada» en el idioma disponible.

### Turnos y planificación

- **Colores de turno:** los turnos muestran colores asignados por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** la lista de validación respeta los tipos seleccionados y la gestión de solicitudes e instancias funciona también con varios validadores. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
    - **Ausencias:** vuelve a funcionar el borrado de ausencias pasadas sin restricciones; las cancelaciones sin días seleccionados no dejan avisos pendientes y el modo LITE evita avisos incorrectos de descanso. [Más información](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)
    - **Empleados:** se corrigen la edición masiva de contratos, la aplicación de excepciones de teletrabajo y la visualización de fotografías, estados y opciones de QR; también vuelven a funcionar cursos, inscripciones y documentos para firmar. [Más información](../empleados-y-organizacion/modificacion-masiva-de-empleados.es.md)
    - **Fichajes:** se corrigen fechas, duplicados, fichajes en días libres y festivos, ubicación, turnos nocturnos, jornadas de 24 horas, zonas horarias y comentarios; los cambios actualizan jornadas e incidencias correctamente. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/casos-de-uso-de-fichajes.es.md)
    - **Informes:** vuelven a mostrarse correctamente los periodos, festivos y ausencias; también funcionan los filtros de empleados y la agrupación de ausencias por día. [Más información](../informes/catalogo-de-informes.es.md)
    - **Instalación e integraciones:** Docker vuelve a cargar imágenes y permite iniciar sesión como administrador tras el primer arranque; se corrigen las comprobaciones de conexión y licencia de las integraciones. [Más información](../introduccion/requisitos-de-instalacion.es.md)
    - **Jornadas y planificación:** vuelve a funcionar la resolución de incidencias en lote y se corrigen los descansos, las horas trabajadas, la duración de turnos, la navegación por patrones y las horas previstas durante permisos. [Más información](../turnos-y-planificacion/turnos.es.md)
    - **Navegación y procesos:** vuelven a abrirse los menús desplegables en paneles y móviles; los formularios largos mantienen accesible el botón de acción, las notificaciones no requieren un usuario activo y las sugerencias anónimas se envían sin errores.
    - **Importación y WebAPI:** las plantillas de fichajes de Excel se reconocen correctamente y las solicitudes de ausencia simultáneas se procesan sin problemas. [Más información](../integraciones/web-api.es.md)
