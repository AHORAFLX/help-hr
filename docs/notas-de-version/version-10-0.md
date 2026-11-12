# Versión 10.0

Sebastian HR 10.0 amplía la gestión de ausencias, la planificación de recursos y el acceso a la información. También incorpora novedades en la navegación, los fichajes, los informes y las opciones de instalación e integración.

## Lo más destacado

### Permisos por horas

Registra permisos parciales y consúltalos en el calendario y en el planificador del empleado. No descuentan días del saldo; sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada, y se consideran al gestionar ausencias no planificadas.

[Más información: restricciones de ausencias](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Ayuda integrada

Consulta la ayuda desde la propia aplicación, sin salir del entorno de Sebastian HR. El nuevo espacio reúne la información de apoyo para que puedas encontrar orientación mientras trabajas.

[Más información: página de inicio](../index.es.md)

### Noticias según destinatarios

Limita quién puede ver las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para que la información llegue a las personas a las que corresponde.

### Reservas recurrentes

Crea reservas repetidas para varios recursos a la vez, con intervalos de días, semanas, meses o años. Puedes excluir fines de semana y festivos; si alguna fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección.

## Otras novedades

### Ausencias y aprobaciones

- **Ausencias no planificadas:** regístralas desde la página de fichajes diarios y elige el tipo de ausencia.
- **Cómputo y solicitudes:** excluye tipos de ausencia de las horas teóricas y define los días mínimos y máximos de cada solicitud. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Flujos de aprobación:** los tipos de vacaciones y ausencias reciben automáticamente el flujo correspondiente, y la conversación se mantiene unificada entre validación y revisión. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Cancelaciones:** siguen el grupo de tipos correspondiente, aparecen ordenadas y se pueden gestionar aunque no tengan fechas de inicio y fin.

### Instalación y despliegue

- **Docker:** despliega Sebastian HR y configura las dos bases de datos en una misma instancia. [Más información](../introduccion/requisitos-de-instalacion.es.md)
- **Aplicación instalada:** instala Sebastian HR como aplicación y ábrela desde la dirección de inicio configurada.
- **Modo de mantenimiento:** activa un modo específico para el mantenimiento de la aplicación.
- **Publicación:** los documentos que suben los usuarios ya no se incluyen en los paquetes de publicación.

### Fichajes y terminales

- **Gestión diaria:** ignora o reactiva varios fichajes a la vez y localiza los días con cierres automáticos. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Terminales Kapri/Kimaldi:** gestiona fichajes con identificadores NFC. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Punto de Acceso:** consulta el código de acceso del empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes y gastos

- **Informes de fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Libro de Registro de Jornada:** distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** crea y consulta informes de gastos con una experiencia mejorada en dispositivos móviles.

### Empleados y organización

- **Lista NFC:** muestra a todos los empleados que no están bloqueados. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/dispositivos-rfid.es.md)
- **Kapri:** incorpora una integración con Kapri. [Más información](../integraciones/kapri.es.md)

### Jornadas y planificación

- **Incidencias de jornada:** detecta más incidencias y aplica las tolerancias y los límites del turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Turnos:** asigna colores por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Interfaz y comunicación

- **Inicio de sesión:** renueva la imagen y los estilos; el asistente de configuración adopta los colores de Sebastian HR.
- **Avisos y cuadros:** adapta avisos, alertas y cuadros de confirmación o solicitud de datos al estilo de Sebastian HR.
- **Procesos:** muestra «Entrada» en el idioma disponible.
- **Correos de ausencias:** incluyen la fecha y distinguen el tipo en el asunto.

### WebAPI

- **Incidencias y gastos:** consulta incidencias anuales y gestiona justificantes de gastos, también en gastos cerrados. [Más información](../integraciones/web-api.es.md)
- **Cursos:** crea cursos mediante nuevas operaciones de la WebAPI. [Más información](../integraciones/web-api.es.md)
- **Documentación:** consulta descripciones más completas de procesos, parámetros y vistas. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se filtran las solicitudes por tipo y se completan correctamente los pasos y acciones pendientes.
    - **Ausencias:** vuelven a funcionar las fechas, cancelaciones, borrados y avisos pendientes; también se corrige el cálculo de descansos en modo LITE.
    - **Empleados:** se corrigen la edición de contratos, la visibilidad de fotos e indicadores, las excepciones de teletrabajo, los cursos, las vigilancias de salud y el envío de documentos a firmar.
    - **Fichajes:** se corrigen la zona horaria, la selección y edición, la actualización tras fichar, los duplicados, los festivos, los días libres y los turnos nocturnos.
    - **Jornadas y planificación:** vuelven a calcularse correctamente turnos, horas, saldos y descansos; también se resuelven incidencias en lote y se corrigen errores de planificación.
    - **Informes e importaciones:** se corrigen las fechas de los periodos, los festivos, los saldos de vacaciones y los calendarios de ausencias; las plantillas de fichajes de Excel vuelven a reconocerse.
    - **Instalación e integraciones:** se recuperan la publicación con SQL Server 2016, las imágenes de Docker y el primer inicio; las comprobaciones de conexión y licencia vuelven a funcionar.
    - **Navegación y procesos:** se corrige la visualización de menús en paneles y móviles, vuelven a verse los botones de formularios largos y se evitan errores al enviar sugerencias anónimas.
    - **WebAPI:** las solicitudes de ausencia se procesan correctamente aunque se reciban varias a la vez. [Más información](../integraciones/web-api.es.md)
