# Versión 10.0

La versión 10.0 amplía la gestión de ausencias, la planificación y las reservas, y añade nuevas opciones de acceso e integración. También mejora la visibilidad de la información y corrige problemas en fichajes, jornadas y procesos habituales.

## Lo más destacado

### Permisos por horas

Registra permisos parciales y consúltalos en el calendario y en el planificador del empleado. No descuentan días del saldo, y sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada; también se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: informes de ausencias](../informes/informes-de-ausencias-y-vacaciones.es.md)

### Ayuda desde la aplicación

Consulta la ayuda sin salir del entorno de Sebastian HR: ahora tienes un espacio de ayuda accesible desde la navegación. Así puedes buscar orientación mientras trabajas en la aplicación.

[Más información: ayuda de Sebastian](../index.es.md)

### Noticias para cada audiencia

Limita quién puede ver las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura la visibilidad de cada categoría para que la información llegue a las personas correspondientes.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Crea reservas recurrentes para varios recursos a la vez, con repeticiones cada cierto número de días, semanas, meses o años. Puedes excluir fines de semana y festivos; si alguna fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección antes de intentarlo de nuevo.

[Más información: planificación de recursos](../turnos-y-planificacion/cuadrantes.es.md)

## Otras novedades

### Ausencias y vacaciones

- **Ausencias no planificadas:** elige también tipos de jornada parcial al insertar una ausencia.
- **Fichajes diarios:** registra ausencias aprobadas de día completo para las personas seleccionadas o para toda la lista.
- **Solicitudes:** establece un mínimo y un máximo de días, y excluye tipos de ausencia del cómputo de horas teóricas.

### Fichajes y control horario

- **Gestión diaria:** ignora o reactiva varios fichajes a la vez y filtra los días con cierres automáticos. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Informes:** genera informes desde la gestión agrupada mensual o semanal de fichajes. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Punto de Acceso:** consulta el código de acceso del empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Turnos y planificación

- **Incidencias de jornada:** se detectan más casos y se tienen en cuenta las tolerancias y los límites del turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Turnos:** tienen colores asignados por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Instalación y despliegue

- **Docker:** despliega Sebastian HR y configura ambas bases de datos en una misma instancia.
- **Aplicación instalada:** instala Sebastian HR como una aplicación y ábrela desde la dirección de inicio configurada.
- **Modo de mantenimiento:** activa el modo de mantenimiento de la aplicación.

### Integraciones y WebAPI

- **Kapri/Kimaldi:** gestiona fichajes con identificadores NFC desde la integración con terminales. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **WebAPI:** consulta detalles de instancias y conversaciones, y elimina justificantes de gastos. [Más información](../integraciones/web-api.es.md)
- **WebAPI:** consulta incidencias anuales, adjunta justificantes a gastos cerrados y crea cursos. [Más información](../integraciones/web-api.es.md)

### Aprobaciones y solicitudes

- **Flujos de aprobación:** los tipos de vacaciones y ausencias reciben automáticamente su flujo correspondiente. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Conversaciones:** la conversación de una instancia se mantiene unificada durante la validación y la revisión. [Más información](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md)

### Informes y gastos

- **Libro de Registro de Jornada:** distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** crea y consulta partes con una experiencia mejorada en dispositivos móviles. [Más información](../informes/catalogo-de-informes.es.md)

### Empleados y comunicación

- **Lista NFC:** muestra a todos los empleados que no están bloqueados. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/dispositivos-rfid.es.md)
- **Procesos:** los correos de vacaciones y ausencias muestran la fecha y distinguen el tipo en el asunto.

### Interfaz y configuración

- **Inicio de sesión:** renueva la imagen y los estilos de la pantalla; el asistente de configuración adopta los colores de Sebastian HR.
- **Avisos y cuadros de diálogo:** alertas, confirmaciones y solicitudes de datos adoptan un estilo adaptado a Sebastian HR.
- **Procesos:** muestran el término «Entrada» en el idioma disponible.

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se muestran solo las solicitudes de los tipos seleccionados y se completan correctamente los pasos y acciones asociados.
    - **Ausencias:** se corrigen la gestión de solicitudes y cancelaciones, las fechas, los fichajes planificados y las incidencias asociadas a ausencias y permisos.
    - **Empleados:** vuelven a mostrarse las fotos y los indicadores; se corrigen la edición de contratos, el teletrabajo, los cursos, las inscripciones, los documentos y la opción de QR.
    - **Fichajes:** se corrigen la zona horaria, la selección, la actualización y el cálculo de fichajes, además de los duplicados, días libres, festivos y turnos nocturnos. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/fichaje-con-zonas-horarias.es.md)
    - **Jornadas y planificación:** vuelven a calcularse correctamente turnos, horas, saldos y descansos; se corrigen incidencias, patrones y horas previstas durante permisos.
    - **Informes e importaciones:** se corrigen periodos, calendarios, saldos de vacaciones, resúmenes de jornada y la lectura de hojas y plantillas de fichajes. [Más información](../informes/catalogo-de-informes.es.md)
    - **Instalación e integraciones:** se corrigen la publicación con SQL Server 2016, el inicio y los recursos visuales de Docker, y las comprobaciones de licencia y conexión ERP.
    - **Navegación y móvil:** vuelven a funcionar los menús desplegables en paneles y móviles, y se muestran correctamente los menús laterales y los botones de formularios largos.
    - **Procesos:** se corrigen informes y gestiones de vacaciones, compensaciones y fichajes; también funcionan las notificaciones y el envío de sugerencias anónimas.
    - **WebAPI:** las solicitudes de ausencia se procesan correctamente aunque lleguen varias al mismo tiempo. [Más información](../integraciones/web-api.es.md)
