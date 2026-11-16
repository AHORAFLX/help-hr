# Versión 10.0

La versión 10.0 amplía la gestión de ausencias y reservas, y facilita el acceso a la ayuda desde la aplicación. También incorpora mejoras en fichajes, planificación, informes e integración con otros sistemas.

## Lo más destacado

### Permisos por horas

Registra permisos por horas y consúltalos en el calendario y en el planificador del empleado. No descuentan días del saldo; sus horas retribuidas y no retribuidas cuentan en la exportación de nómina y en el cómputo de jornada, y se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: restricciones de ausencias](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Ayuda desde la aplicación

Consulta la ayuda sin salir del entorno de Sebastian HR. El nuevo espacio está disponible desde la navegación, para que puedas encontrar información mientras trabajas en la aplicación.

[Más información: inicio de la ayuda](../index.es.md)

### Noticias para cada grupo

Limita quién puede ver las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para mostrar las noticias solo a las personas a quienes van dirigidas.

### Reservas recurrentes

Crea reservas recurrentes para varios recursos a la vez, con repeticiones cada cierto número de días, semanas, meses o años. Puedes excluir fines de semana y festivos; si una fecha ya está ocupada, no se crea ninguna reserva y puedes corregir la selección antes de intentarlo de nuevo.

## Otras novedades

### Ausencias y vacaciones

- **Solicitudes:** establece un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Ausencias no planificadas:** al insertar una ausencia, puedes elegir tipos de jornada parcial.
- **Ausencias aprobadas:** registra ausencias de día completo para las personas seleccionadas o para toda la lista desde la página de fichajes diarios.
- **Cómputo de horas:** excluye determinados tipos de ausencia de las horas teóricas.

### Instalación y despliegue

- **Docker:** despliega Sebastian HR y configura las dos bases de datos en una misma instancia.
- **Aplicación instalada:** instala Sebastian HR como una aplicación; se abrirá desde la dirección de inicio configurada.
- **Modo de mantenimiento:** activa un modo de mantenimiento en la aplicación.
- **Publicaciones:** los documentos que suben los usuarios ya no se incluyen en los paquetes de publicación.

### Fichajes y terminales

- **Gestión diaria:** ignora o reactiva varios fichajes a la vez desde la lista diaria.
- **Terminales Kapri/Kimaldi:** gestiona fichajes con identificadores NFC. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Lista NFC:** muestra a todos los empleados que no están bloqueados.
- **Cierres automáticos:** identifica y filtra los días con cierres automáticos en la vista agrupada y en la gestión diaria. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Punto de Acceso:** consulta el código de acceso del empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes y gastos

- **Informes de fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/catalogo-de-informes.es.md)
- **Libro de Registro de Jornada:** distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** crea y consulta partes con una experiencia mejorada en dispositivos móviles.

### Acceso e interfaz

- **Inicio de sesión:** se renuevan la imagen y los estilos de la pantalla.
- **Configuración del inicio de sesión:** el asistente adopta los colores de Sebastian HR.
- **Avisos y cuadros de diálogo:** adoptan un estilo adaptado a Sebastian HR.
- **Procesos:** muestran el término «Entrada» en el idioma disponible.

### Aprobaciones y solicitudes

- **Flujos de aprobación:** los tipos de vacaciones y ausencias reciben automáticamente el flujo correspondiente. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Conversaciones:** la conversación de una instancia se mantiene unificada entre la validación y la revisión. [Más información](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md)
- **Cancelaciones:** se gestionan según sean de vacaciones o de ausencias, y los tipos se ordenan en listas y menús.
- **Cancelación de vacaciones:** gestiona solicitudes aunque no indiquen fechas de inicio y fin. [Más información](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)
- **Correos:** los mensajes sobre vacaciones y ausencias muestran la fecha y distinguen el tipo en el asunto.

### Jornadas y planificación

- **Incidencias de jornada:** se detectan más casos y se tienen en cuenta las tolerancias y los límites del turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Turnos:** tienen colores asignados por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### WebAPI e integraciones

- **Operaciones WebAPI:** crea noticias y cursos, elimina justificantes de gastos, adjunta justificantes a gastos cerrados y consulta incidencias anuales. [Más información](../integraciones/web-api.es.md)
- **Asistentes de IA:** pueden ejecutar procesos de la WebAPI mediante MCP, también cuando incluyen parámetros opcionales. [Más información](../integraciones/web-api.es.md)
- **Instancias:** consulta mediante la WebAPI sus detalles y conversaciones; la API de ubicaciones también indica si están desactivadas para la aplicación. [Más información](../integraciones/web-api.es.md)
- **Documentación WebAPI:** amplía las descripciones de procesos, parámetros y vistas. [Más información](../integraciones/web-api.es.md)
- **Kapri:** se añade una integración con Kapri. [Más información](../integraciones/kapri.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se muestran las solicitudes de los tipos seleccionados y se completan correctamente las resoluciones y acciones pendientes.
    - **Ausencias:** se corrigen incidencias y fechas al gestionar permisos, insertar fichajes planificados y cancelar o borrar solicitudes; también se evitan bloqueos, duplicados y avisos incorrectos.
    - **Empleados:** vuelven a mostrarse las fotos y los indicadores de estado; se corrigen la edición de contratos, el teletrabajo, los cursos, las vigilancias de salud, los documentos y la opción de QR.
    - **Fichajes:** se corrigen la zona horaria, la actualización tras fichar, los duplicados, los turnos nocturnos, los festivos y el cálculo de jornadas; también funcionan correctamente la edición, los filtros y la inserción de fichajes. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/fichaje-con-zonas-horarias.es.md)
    - **Jornadas y planificación:** se recalculan los datos al cambiar la planificación, se corrigen las incidencias y los descansos, y vuelven a funcionar la resolución en lote y la navegación por patrones.
    - **Informes e importaciones:** se corrigen las fechas, los filtros y los resúmenes; los calendarios y saldos de vacaciones se generan correctamente y Excel reconoce las hojas y plantillas de fichajes.
    - **Instalación e integraciones:** se recupera la publicación con SQL Server 2016; Docker carga sus recursos y permite iniciar sesión como administrador, y las integraciones comprueban correctamente las licencias y la conexión.
    - **Navegación y móvil:** los menús desplegables y laterales vuelven a mostrarse correctamente, también en paneles deslizantes y dispositivos móviles.
    - **Procesos y WebAPI:** se corrigen los informes y formularios móviles, las notificaciones a empleados sin usuario activo y el envío de sugerencias anónimas; las solicitudes de ausencia por API se procesan en paralelo y se corrige un problema de seguridad. [Más información](../integraciones/web-api.es.md)
