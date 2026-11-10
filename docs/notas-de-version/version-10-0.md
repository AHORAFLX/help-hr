# Versión 10.0

Sebastian HR 10.0 amplía la gestión de ausencias y reservas y mejora el seguimiento de la jornada. También incorpora cambios en la instalación, la navegación y las integraciones.

## Lo más destacado

### Permisos por horas

Ya puedes registrar permisos parciales, además de permisos de día completo. No descuentan días del saldo y aparecen en el calendario y el planificador del empleado. Sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y en el cómputo de jornada.

[Más información: restricciones de ausencias](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Ayuda integrada

La ayuda está disponible desde la navegación de la aplicación, para que puedas consultar sus contenidos sin salir del entorno de Sebastian HR. Así tienes a mano la información de apoyo mientras utilizas la aplicación.

[Más información: página de inicio](../index.es.md)

### Visibilidad de noticias

Puedes limitar quién ve las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso para cada categoría y muestra las noticias solo a las personas a las que corresponden.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Crea reservas recurrentes para varios recursos a la vez y elige que se repitan cada cierto número de días, semanas, meses o años. Puedes excluir fines de semana y festivos; si una fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección.

### Incidencias de jornada

La detección de incidencias tiene en cuenta las tolerancias del turno, las pausas y los descansos, además de los límites de horas semanales, mensuales y anuales. También evita avisos por falta de fichajes cuando el turno no prevé horario para ese día.

[Más información: incidencias de jornada](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

## Otras novedades

### Ausencias y aprobaciones

- **Gestión de ausencias:** registra ausencias aprobadas de día completo desde la página de fichajes diarios y excluye tipos concretos del cómputo de horas teóricas.
- **Solicitudes:** establece un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Flujos de aprobación:** los tipos de vacaciones y ausencias reciben su flujo correspondiente, y la conversación de cada instancia se mantiene unificada entre validación y revisión. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Cancelaciones:** siguen el grupo de tipos correspondiente, se ordenan en listas y menús, y pueden gestionarse aunque no tengan fechas de inicio y fin.

### Instalación y plataforma

- **Docker:** despliega Sebastian HR y configura ambas bases de datos en una misma instancia. [Más información](../introduccion/requisitos-de-instalacion.es.md)
- **Aplicación instalada:** instala Sebastian HR como una aplicación y ábrela desde la dirección de inicio configurada.
- **Modo de mantenimiento:** activa un modo de mantenimiento en la aplicación.
- **Publicación:** los documentos subidos a la aplicación ya no se incluyen en los paquetes publicados.

### Fichajes y terminales

- **Gestión diaria:** ignora o reactiva varios fichajes a la vez desde la lista diaria. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/casos-de-uso-de-fichajes.es.md)
- **Terminales Kapri/Kimaldi:** gestiona fichajes con identificadores NFC; la lista muestra a todos los empleados que no están bloqueados. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Cierres automáticos:** identifica y filtra los días y fichajes de salida generados automáticamente al cerrar un turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Punto de Acceso:** consulta el código de acceso del empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes y gastos

- **Informes de fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Libro de Registro de Jornada:** distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** crea y consulta partes con una experiencia mejorada en dispositivos móviles. [Más información](../informes/catalogo-de-informes.es.md)

### Integraciones y WebAPI

- **Kapri:** incorpora una integración con Kapri. [Más información](../integraciones/kapri.es.md)
- **WebAPI:** consulta incidencias anuales y gestiona justificantes de gastos, incluso en gastos cerrados. [Más información](../integraciones/web-api.es.md)
- **Cursos y documentación:** crea cursos con nuevas operaciones de la WebAPI y consulta descripciones más completas de procesos, parámetros y vistas. [Más información](../integraciones/web-api.es.md)

### Interfaz y navegación

- **Inicio de sesión:** renueva la imagen y los estilos de la pantalla; el asistente de configuración adopta los colores de Sebastian HR.
- **Avisos y cuadros:** adapta a Sebastian HR el estilo de avisos, alertas y cuadros de confirmación y solicitud de datos.
- **Procesos y turnos:** muestra «Entrada» en el idioma disponible y asigna colores por defecto a los turnos. [Más información](../turnos-y-planificacion/turnos.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se muestran solo las solicitudes de los tipos seleccionados y se completan correctamente las acciones y pasos pendientes.
    - **Ausencias:** vuelven a funcionar correctamente las cancelaciones, el borrado de solicitudes pasadas y la gestión de avisos; también se evitan falsas incidencias de descanso en modo LITE.
    - **Empleados:** se corrigen la edición masiva de contratos, las fotografías y los indicadores de estado, las excepciones de teletrabajo, los cursos, las vigilancias de salud, los documentos y la opción de QR.
    - **Fichajes:** se corrigen la selección, el registro, la edición y el cálculo de fichajes y jornadas, incluidas las jornadas nocturnas, los días libres, la ubicación y los datos de hora y zona horaria.
    - **Informes e importaciones:** se corrigen las plantillas de Excel, las fechas de los periodos, los festivos, los calendarios de ausencias y los informes de saldo de vacaciones.
    - **Instalación e integraciones:** Docker vuelve a cargar imágenes y permite completar el primer inicio; también se corrigen las comprobaciones de licencia y conexión del ERP.
    - **Jornadas:** vuelven a funcionar la resolución en lote de incidencias, el redondeo de descansos y el cálculo de horas con descansos computables no fichados.
    - **Navegación y planificación:** se corrigen los menús en móviles y paneles, los cambios de turno, la navegación por patrones y las horas previstas durante permisos.
    - **Procesos y WebAPI:** se corrigen fechas de informes, formularios largos en móviles, notificaciones, sugerencias anónimas y el procesamiento simultáneo de solicitudes de ausencia.
