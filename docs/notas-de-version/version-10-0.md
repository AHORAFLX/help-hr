# Versión 10.0

La versión 10.0 amplía la gestión de ausencias y la planificación, y facilita el acceso a la ayuda y a las noticias relevantes. También incorpora mejoras en fichajes, instalación, informes e integración con otros sistemas.

## Lo más destacado

### Permisos por horas

Registra permisos parciales y consúltalos en el calendario y el planificador del empleado. No descuentan días del saldo; sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada, y también se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: gestión de ausencias](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Ayuda integrada

Consulta la ayuda desde la propia aplicación, sin salir de tu entorno de trabajo. Así tienes a mano la información que necesitas mientras utilizas Sebastian HR.

[Más información: ayuda de Sebastian HR](../index.es.md)

### Noticias para cada ámbito

Decide quién puede ver las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura la visibilidad en cada categoría para que cada persona consulte solo la información que le corresponde.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Crea reservas recurrentes para varios recursos en una sola operación, con repeticiones por días, semanas, meses o años. Puedes excluir fines de semana y festivos; si alguna fecha está ocupada, no se crea ninguna reserva, para que puedas corregir la selección y volver a intentarlo.

[Más información: planificación de recursos](../turnos-y-planificacion/cuadrantes.es.md)

## Otras novedades

### Ausencias y vacaciones

- **Ausencias no planificadas:** puedes insertar también tipos de jornada parcial y registrar ausencias aprobadas de día completo desde la página de fichajes diarios.
- **Cómputo de horas:** excluye determinados tipos de ausencia de las horas teóricas y establece límites mínimos y máximos de días para cada solicitud. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Solicitudes y cancelaciones:** los tipos de ausencia y vacaciones reciben el flujo de aprobación adecuado; puedes gestionar cancelaciones de vacaciones aunque no indiquen fechas. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Gestión de ausencias:** las cancelaciones se tramitan según sean de vacaciones o de otro tipo, y los tipos aparecen ordenados en listas y menús.

### Fichajes y jornadas

- **Gestión diaria:** puedes ignorar o reactivar varios fichajes a la vez e identificar los días con cierres automáticos. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Terminales Kapri/Kimaldi:** la integración permite gestionar fichajes con identificadores NFC y consultar a todos los empleados no bloqueados en la lista NFC. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Informes de fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-control-horario.es.md)
- **Incidencias de jornada:** se detectan más incidencias y se aplican las tolerancias y los límites del turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Códigos de acceso:** puedes consultar el código del empleado en el Punto de Acceso aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Turnos y planificación

- **Turnos:** se asignan colores por defecto para distinguirlos mejor. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Patrones en LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Empleados y formación

- **Formación y salud:** puedes crear cursos mediante la WebAPI. [Más información](../integraciones/web-api.es.md)

### Informes y comunicación

- **Libro de Registro de Jornada:** distingue las ausencias por tipo y color, incluye un resumen y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** crea y consulta informes de gastos con una experiencia mejorada en dispositivos móviles. [Más información](../informes/catalogo-de-informes.es.md)
- **Correos de vacaciones y ausencias:** muestran la fecha y diferencian el tipo en el asunto.

### Instalación y despliegue

- **Docker:** puedes desplegar Sebastian HR y configurar las dos bases de datos en una misma instancia. [Más información](../introduccion/requisitos-de-instalacion.es.md)
- **Aplicación instalable:** instala Sebastian HR como una aplicación y ábrela desde la dirección de inicio configurada.
- **Paquetes de publicación:** los documentos subidos por los usuarios ya no se incluyen en ellos.

### Interfaz y aprobaciones

- **Inicio de sesión:** se renuevan la imagen y los estilos, y el asistente de configuración adopta los colores de Sebastian HR. [Más información](../introduccion/configuracion-inicial.es.md)
- **Avisos y confirmaciones:** los avisos, las alertas y los cuadros para confirmar o pedir datos adoptan el estilo de Sebastian HR.
- **Procesos:** se muestra «Entrada» en el idioma disponible y la conversación de cada instancia se mantiene unificada entre validación y revisión.

### Integraciones y WebAPI

- **Kapri:** se incorpora una nueva integración con este sistema. [Más información](../integraciones/kapri.es.md)
- **Acceso a la WebAPI:** los permisos siguen el perfil del usuario y las operaciones de gestión quedan reservadas a RR. HH. [Más información](../integraciones/web-api.es.md)
- **Operaciones de la WebAPI:** gestiona empresas e instancias, consulta sus detalles y conversaciones, y elimina instancias y justificantes de gastos. [Más información](../integraciones/web-api.es.md)
- **Noticias y gastos:** crea noticias, consulta incidencias anuales y adjunta justificantes a gastos cerrados; las respuestas explican denegaciones e incluyen el identificador creado. [Más información](../integraciones/web-api.es.md)
- **Asistentes de IA:** pueden ejecutar procesos de la WebAPI mediante MCP, también cuando incluyen parámetros opcionales. [Más información](../integraciones/web-api.es.md)
- **Documentación de la WebAPI:** consulta descripciones más completas de procesos, parámetros y vistas; la API de ubicaciones también añade el dato `InstancesDisabled`. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se muestran las solicitudes de los tipos elegidos y se completan correctamente las acciones y los pasos pendientes.
    - **Ausencias y vacaciones:** vuelven a funcionar la inserción de fichajes planificados, las cancelaciones y el borrado de solicitudes; se corrigen formularios, fechas y avisos de jornada.
    - **Empleados:** se corrigen la edición masiva de contratos, las fotografías y los indicadores de estado; también vuelven a funcionar la gestión de cursos, documentos y firmas.
    - **Fichajes:** se corrigen zonas horarias, selección, visualización y guardado, se evitan duplicados y se actualizan las jornadas y las incidencias tras los cambios.
    - **Jornadas:** vuelven a calcularse correctamente turnos, horas, saldos e incidencias; también se corrigen la resolución en lote y el cálculo de descansos.
    - **Informes:** se corrigen periodos, resúmenes y calendarios de ausencias, y vuelve a generarse correctamente el informe de saldo de vacaciones.
    - **Instalación y despliegue:** Docker vuelve a cargar imágenes, permite el primer inicio y el acceso de administrador; también se recupera la publicación con SQL Server 2016.
    - **Navegación y móvil:** vuelven a mostrarse correctamente los menús desplegables y laterales, y los formularios largos mantienen visibles sus botones en dispositivos móviles.
    - **Planificación y procesos:** se corrigen fechas, turnos y duraciones, y vuelven a funcionar la navegación por patrones, los informes y varias acciones de vacaciones, compensaciones y fichajes.
    - **Integraciones e importación:** se corrigen las comprobaciones de conexión y licencia, la lectura de plantillas de Excel y el procesamiento simultáneo de solicitudes de ausencia por API.
