# Versión 10.0

Sebastian HR 10.0 amplía la gestión de ausencias y la planificación, y añade nuevas opciones para fichajes, instalación e integraciones. También mejora los flujos de aprobación, la experiencia de uso y la estabilidad de tareas habituales.

## Lo más destacado

### Permisos por horas

Ya puedes registrar permisos por horas y consultarlos en el calendario y el planificador del empleado. No descuentan días del saldo, y sus horas retribuidas y no retribuidas cuentan en la exportación de nómina, el cómputo de jornada y la gestión de ausencias no planificadas.

[Más información: horas de vacaciones](../horas/horas-de-vacaciones.es.md)

### Ayuda desde la aplicación

La aplicación incorpora un espacio de ayuda al que puedes acceder desde la navegación, sin salir de Sebastian HR. Así puedes consultar la documentación desde el propio entorno de trabajo cuando necesites resolver una duda.

[Más información: ayuda de Sebastian HR](../index.es.md)

### Visibilidad de las noticias

Puedes limitar quién ve las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para que cada noticia llegue solo a las personas a las que corresponde.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Puedes crear reservas recurrentes para varios recursos a la vez y definir si se repiten cada cierto número de días, semanas, meses o años. También puedes excluir fines de semana y festivos; si alguna fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección.

## Otras novedades

### Ausencias y vacaciones

- **Ausencias no planificadas:** regístralas desde la página de fichajes diarios y elige el tipo de ausencia.
- **Cómputo de horas:** excluye determinados tipos de ausencia del cálculo de horas teóricas.
- **Límites de solicitud:** establece un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Fichajes, jornadas y planificación

- **Gestión diaria de fichajes:** ignora o reactiva varios fichajes a la vez desde la lista diaria.
- **Fichajes NFC:** la integración con terminales Kapri/Kimaldi admite identificadores NFC, y la lista muestra a los empleados que no están bloqueados. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Cierre automático de turnos:** identifica y filtra los fichajes de salida automáticos y los días con cierre automático desde la vista agrupada. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Control de jornada:** se detectan más incidencias teniendo en cuenta las tolerancias y los límites del turno; los turnos reciben colores por defecto. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Planificación LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)
- **Punto de Acceso:** consulta el código de acceso del empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Instalación y despliegue

- **Docker:** despliega Sebastian HR y configura las dos bases de datos en una misma instancia.
- **Aplicación instalada:** instala Sebastian HR como una aplicación; al abrirla, usa la dirección de inicio configurada.
- **Modo de mantenimiento:** activa un modo de mantenimiento en la aplicación.
- **Publicaciones:** los documentos subidos por los usuarios ya no se incluyen en los paquetes de publicación.

### Interfaz y navegación

- **Inicio de sesión:** se renuevan la imagen y los estilos de la pantalla, y el asistente de configuración adopta los colores de Sebastian HR.
- **Avisos y confirmaciones:** los avisos, las alertas y los cuadros de confirmación o solicitud de datos adoptan el estilo de Sebastian HR.
- **Procesos:** el término «Entrada» aparece en el idioma disponible.

### Aprobaciones y procesos

- **Flujos de aprobación:** los tipos de vacaciones y ausencias reciben automáticamente el flujo correspondiente, y la conversación se mantiene unificada entre validación y revisión. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Correos de ausencias:** incluyen la fecha y distinguen el tipo de solicitud en el asunto.

### Informes y gastos

- **Informes de fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Libro de Registro de Jornada:** diferencia las ausencias por tipo, muestra sus colores y añade un resumen; además, vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** crea y consulta partes con una experiencia mejorada en dispositivos móviles.

### Integraciones y WebAPI

- **Kapri:** Sebastian HR incorpora una integración con Kapri. [Más información](../integraciones/kapri.es.md)
- **WebAPI:** consulta incidencias anuales, gestiona justificantes de gastos incluso en gastos cerrados y crea cursos. [Más información](../integraciones/web-api.es.md)
- **Documentación de la WebAPI:** sus procesos, parámetros y vistas cuentan con descripciones más completas. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se muestran solo las solicitudes de los tipos elegidos y se completan correctamente las acciones y los pasos pendientes.
    - **Ausencias:** las fechas se interpretan correctamente y las cancelaciones pendientes ya no se bloquean, duplican ni afectan a días denegados; también puedes borrar ausencias pasadas sin límite.
    - **Empleados:** vuelven a mostrarse las fotografías y los colores de estado; la edición de contratos, el teletrabajo, los cursos, las vigilancias de salud, los documentos y la opción de QR funcionan según lo configurado.
    - **Fichajes:** se corrigen la selección, actualización y edición de fichajes, los turnos nocturnos, la ubicación y los cálculos de días libres y jornadas de 24 horas; también se evitan duplicados.
    - **Jornadas y planificación:** los turnos, las horas, los saldos y las incidencias se recalculan correctamente; también se respetan horarios, descansos y duraciones, y puedes resolver incidencias en lote.
    - **Informes e importaciones:** se corrigen las fechas, los periodos y los resultados de los informes de ausencias, jornada y vacaciones; las importaciones de Excel reconocen la hoja y la plantilla de fichajes.
    - **Instalación e integraciones:** la publicación vuelve a funcionar con SQL Server 2016, Docker inicia correctamente y carga sus imágenes, y las comprobaciones de licencia y conexión con el ERP funcionan.
    - **Navegación:** los menús desplegables y el menú lateral vuelven a mostrarse correctamente en paneles deslizantes y dispositivos móviles.
    - **Procesos y WebAPI:** se corrigen fallos en informes, vacaciones, compensaciones, fichajes y formularios móviles; las notificaciones llegan sin exigir un usuario activo y las solicitudes de ausencia simultáneas se procesan correctamente.
