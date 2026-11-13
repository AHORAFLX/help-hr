# Versión 10.0

La versión 10.0 amplía la gestión de ausencias y la planificación, y añade opciones para instalar y usar Sebastian HR. También mejora la navegación, los informes y la gestión diaria de fichajes y jornadas.

## Lo más destacado

### Permisos por horas

Registra permisos por horas y consúltalos en el calendario y el planificador del empleado. No descuentan días del saldo, y sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada; también se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: restricciones de ausencias](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Ayuda desde la aplicación

Consulta la ayuda desde el propio entorno de Sebastian HR, sin tener que salir de la aplicación para buscar orientación. Así tienes a mano la información de ayuda mientras trabajas.

### Noticias para cada grupo

Limita quién ve las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para que cada noticia llegue a las personas correspondientes.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Crea reservas recurrentes para varios recursos a la vez y elige si se repiten cada cierto número de días, semanas, meses o años. Puedes excluir fines de semana y festivos; si alguna fecha está ocupada, no se crea ninguna reserva, para que corrijas la selección antes de volver a intentarlo.

## Otras novedades

### Ausencias y vacaciones

- Al insertar una ausencia no planificada, puedes elegir también tipos de jornada parcial.
- Desde la página de fichajes diarios, registra ausencias aprobadas de día completo para las personas seleccionadas o para toda la lista.
- Configura qué tipos de ausencia se excluyen de las horas teóricas y establece límites mínimos y máximos de días por solicitud. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- Las cancelaciones siguen el proceso correspondiente a vacaciones o ausencias; puedes gestionar las solicitudes de cancelación de vacaciones aunque no tengan fechas. [Más información](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)

### Solicitudes y aprobaciones

- Los tipos de vacaciones y ausencias reciben automáticamente el flujo de aprobación correspondiente. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- La conversación de cada solicitud se mantiene unificada entre la validación y la revisión. [Más información](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md)

### Fichajes y planificación

- Ignora o reactiva varios fichajes a la vez desde la lista diaria.
- Genera informes desde la gestión agrupada mensual o semanal de fichajes. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- Identifica y filtra los días con cierre automático de fichajes en las vistas agrupada y diaria. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- El Libro de Registro de Jornada distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- Se detectan más incidencias de jornada, teniendo en cuenta las tolerancias y los límites del turno; los turnos tienen colores por defecto. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

### Instalación y despliegue

- Despliega Sebastian HR con Docker y configura ambas bases de datos en una misma instancia.
- Instala Sebastian HR como una aplicación; se abrirá desde la dirección de inicio configurada.
- Los documentos subidos por los usuarios ya no se incluyen en los paquetes de publicación.

### Informes y gastos

- Crea y consulta partes de gastos con una experiencia mejorada en dispositivos móviles.
- El Libro de Registro de Jornada muestra las ausencias por tipo, sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)

### Interfaz y navegación

- La pantalla de inicio de sesión renueva su imagen y sus estilos; el asistente de configuración adopta los colores de Sebastian HR.
- Los avisos, alertas y cuadros de confirmación y solicitud de datos tienen un estilo adaptado a Sebastian HR.
- Los procesos muestran «Entrada» en el idioma disponible. En modo LITE, puedes consultar los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Integraciones y WebAPI

- La integración con terminales Kapri/Kimaldi permite gestionar fichajes con identificadores NFC; la lista NFC incluye a todos los empleados no bloqueados. [Más información](../integraciones/kapri.es.md)
- La WebAPI permite consultar incidencias anuales, gestionar justificantes de gastos —incluso en gastos cerrados— y crear cursos. [Más información](../integraciones/web-api.es.md)
- La WebAPI ofrece descripciones más completas de sus procesos, parámetros y vistas. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se muestran las solicitudes de los tipos seleccionados y se completan correctamente las acciones y los pasos pendientes. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
    - **Ausencias:** vuelven a funcionar el registro de fichajes planificados y las cancelaciones; las fechas y los límites se gestionan correctamente y no se crean solicitudes vacías ni incidencias improcedentes. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
    - **Empleados:** se muestran correctamente fotos e indicadores; funcionan la edición de contratos, el teletrabajo, los cursos, las vigilancias de salud y el envío de documentos a firmar.
    - **Fichajes:** se corrigen la zona horaria, la selección, la actualización y el cálculo de fichajes; se evitan duplicados e incidencias incorrectas y se puede fichar en los casos previstos. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/fichaje-con-zonas-horarias.es.md)
    - **Jornadas y planificación:** se recalculan los turnos y saldos al cambiar la planificación, funcionan la resolución en lote y la navegación por patrones, y se respetan horarios, descansos y duraciones. [Más información](../turnos-y-planificacion/metodos-de-planificacion.es.md)
    - **Informes e importaciones:** se corrigen las fechas de los periodos, los festivos y las ausencias agrupadas; los informes de saldo y las plantillas de fichajes se generan y reconocen correctamente. [Más información](../informes/catalogo-de-informes.es.md)
    - **Instalación e integraciones:** se recupera la publicación con SQL Server 2016, se corrigen el inicio y la carga de recursos en Docker y funcionan las comprobaciones de conexión y licencia. [Más información](../introduccion/requisitos-de-instalacion.es.md)
    - **Navegación:** los menús desplegables y laterales se muestran correctamente en paneles y dispositivos móviles.
    - **Procesos y WebAPI:** se respetan las fechas de los informes, vuelven a verse los botones en formularios móviles, se envían notificaciones sin usuario activo y se procesan correctamente solicitudes simultáneas y sugerencias anónimas. [Más información](../integraciones/web-api.es.md)
