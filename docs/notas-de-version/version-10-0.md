# Versión 10.0

Sebastian HR 10.0 amplía la gestión de ausencias y la planificación, y añade opciones para instalar, desplegar y conectar la aplicación. También mejora el acceso a la ayuda y la experiencia de uso, y corrige problemas en fichajes, jornadas y procesos.

## Lo más destacado

### Permisos por horas

Registra permisos parciales y consúltalos en el calendario y el planificador del empleado. No descuentan días del saldo, y sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada; también se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: ausencias y vacaciones](../informes/informes-de-ausencias-y-vacaciones.es.md)

### Ayuda en la aplicación

Consulta la ayuda desde la navegación, sin salir del entorno de Sebastian HR. Así puedes acceder a la información de ayuda desde la propia aplicación mientras trabajas.

[Más información: página de inicio](../index.es.md)

### Visibilidad de noticias

Decide quién puede ver las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para que cada noticia llegue a las personas que correspondan.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Crea reservas para varios recursos a la vez y repítelas cada cierto número de días, semanas, meses o años. Puedes excluir fines de semana y festivos; si una fecha está ocupada, no se crea ninguna reserva, para que puedas corregir la selección y volver a intentarlo.

[Más información: cuadrantes](../turnos-y-planificacion/cuadrantes.es.md)

## Otras novedades

### Ausencias y aprobaciones

- **Gestión de ausencias:** puedes insertar tipos de jornada parcial desde ausencias no planificadas y registrar ausencias aprobadas de día completo desde la página de fichajes. [Más información](../informes/informes-de-ausencias-y-vacaciones.es.md)
- **Solicitudes:** establece mínimos y máximos de días y excluye tipos de ausencia del cómputo de horas teóricas. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Aprobaciones y cancelaciones:** los tipos de ausencia y vacaciones reciben su flujo correspondiente; las cancelaciones se gestionan según el tipo y los correos indican la fecha y el tipo. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)

### Instalación y despliegue

- **Docker:** despliega Sebastian HR y configura las dos bases de datos en una misma instancia. [Más información](../introduccion/requisitos-de-instalacion.es.md)
- **Aplicación instalada:** instala Sebastian HR como una aplicación; se abrirá desde la dirección de inicio configurada. [Más información](../introduccion/configuracion-inicial.es.md)
- **Modo de mantenimiento:** activa un modo para la aplicación; los documentos subidos por los usuarios ya no se incluyen en los paquetes de publicación.

### Fichajes y terminales

- **Gestión diaria:** ignora o reactiva varios fichajes a la vez y localiza los días con cierres automáticos. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Terminales Kapri/Kimaldi:** gestiona fichajes con identificadores NFC. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Punto de Acceso:** consulta el código de acceso aunque esté oculto; la lista NFC incluye a todos los empleados no bloqueados. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes

- **Fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Registro de jornada:** distingue las ausencias por tipo, muestra sus colores y un resumen; también vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** crea y consulta partes con una experiencia adaptada a dispositivos móviles. [Más información](../informes/catalogo-de-informes.es.md)

### Jornadas y planificación

- **Incidencias de jornada:** se detectan más incidencias y se aplican las tolerancias y los límites del turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Turnos:** tienen colores asignados por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Interfaz y navegación

- **Inicio de sesión:** se renuevan la imagen y los estilos; el asistente de configuración adopta los colores de Sebastian HR. [Más información](../introduccion/configuracion-inicial.es.md)
- **Avisos y cuadros:** los avisos, las alertas y los cuadros de confirmación o solicitud de datos adoptan un estilo adaptado a Sebastian HR.
- **Procesos:** el término «Entrada» se muestra en el idioma disponible.

### WebAPI e integraciones

- **Kapri:** se incorpora una nueva integración con este sistema. [Más información](../integraciones/kapri.es.md)
- **WebAPI:** añade operaciones para gestionar empresas e instancias, crear noticias y cursos, consultar incidencias anuales y detalles de instancias, y gestionar justificantes de gastos. [Más información](../integraciones/web-api.es.md)
- **Asistentes de IA:** pueden ejecutar procesos de la WebAPI mediante MCP, también si tienen parámetros opcionales. [Más información](../integraciones/web-api.es.md)
- **Permisos y descripciones:** la WebAPI y los asistentes respetan los permisos de cada perfil; sus procesos, parámetros y vistas tienen descripciones más completas. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se muestran solo las solicitudes seleccionadas y se completan correctamente las acciones y los pasos pendientes. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
    - **Ausencias:** vuelven a funcionar correctamente las solicitudes, cancelaciones, fichajes planificados y fechas; se evitan incidencias y bloqueos incorrectos. [Más información](../informes/informes-de-ausencias-y-vacaciones.es.md)
    - **Despliegue:** la publicación vuelve a funcionar con SQL Server 2016 y las instalaciones Docker cargan sus recursos e inician correctamente. [Más información](../introduccion/requisitos-de-instalacion.es.md)
    - **Empleados:** se corrigen la edición de contratos, las fotografías y los estados; también vuelven a funcionar cursos, documentos, teletrabajo y opciones de acceso. [Más información](../empleados-y-organizacion/modificacion-masiva-de-empleados.es.md)
    - **Fichajes:** se corrigen la zona horaria, los duplicados, las fechas, la selección y el cálculo; los cambios se actualizan al momento y se puede fichar cuando corresponde. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/fichaje-con-zonas-horarias.es.md)
    - **Informes e importaciones:** se corrigen las fechas, los filtros, los resúmenes y los calendarios; las plantillas de fichajes de Excel vuelven a reconocerse. [Más información](../informes/catalogo-de-informes.es.md)
    - **Jornadas y planificación:** se actualizan los cálculos y turnos, se evitan incidencias incorrectas y vuelven a funcionar la resolución en lote y la navegación por patrones. [Más información](../turnos-y-planificacion/turnos.es.md)
    - **Interfaz y procesos:** vuelven a funcionar los menús en paneles y móviles; se corrigen los formularios, informes, notificaciones y acciones de solicitudes.
    - **Integraciones y WebAPI:** se corrigen las conexiones y el procesamiento simultáneo de solicitudes de ausencia, y se resuelve un problema de seguridad. [Más información](../integraciones/web-api.es.md)
