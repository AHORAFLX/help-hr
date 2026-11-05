# Versión 10.0

Sebastian HR 10.0 amplía la gestión de ausencias, fichajes y planificación, y facilita la instalación y el acceso a la ayuda. También incorpora nuevas posibilidades de integración y mejoras en la WebAPI, junto con ajustes en la experiencia diaria.

## Lo más destacado

### Permisos por horas

Registra permisos por horas y consúltalos en el calendario y el planificador del empleado. No descuentan días del saldo; sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada, y se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: restricciones de ausencias](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Terminales Kapri/Kimaldi

Integra terminales Kapri/Kimaldi para gestionar fichajes mediante identificadores NFC. Puedes asociar identificadores a empleados, procesar los eventos de los terminales y configurar sus opciones; también puedes borrar identificadores desde la lista y consultar pantallas con mejoras visuales.

[Más información: terminales Kapri](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)

### Ayuda integrada

Consulta la ayuda desde el propio entorno de Sebastian HR, sin salir de la aplicación. El nuevo espacio está disponible desde la navegación para que puedas encontrar orientación mientras trabajas.

[Más información: inicio de la ayuda](../index.es.md)

### Visibilidad de noticias

Limita quién puede ver las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para que cada noticia llegue a las personas que corresponden.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Crea reservas recurrentes para varios recursos a la vez y define si se repiten cada cierto número de días, semanas, meses o años. Puedes excluir fines de semana y festivos; si una fecha ya está ocupada, no se crea ninguna reserva y puedes corregir la selección.

### Incidencias de jornada

La detección de incidencias tiene en cuenta las tolerancias del turno, las pausas, los descansos y los límites de horas semanales, mensuales y anuales. Los límites se señalan el día en que se superan, y no se avisa de fichajes ausentes si ese día no tiene un horario previsto.

[Más información: incidencias de jornada](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

## Otras novedades

### Ausencias y aprobaciones

- **Límites de solicitud:** establece un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Flujos y cancelaciones:** cada tipo de ausencia o vacaciones usa su flujo de aprobación; las cancelaciones siguen el grupo de tipos y pueden gestionarse aunque no tengan fechas de inicio y fin. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Conversaciones:** la conversación de una instancia se mantiene unificada durante la validación y la revisión.

### Instalación y acceso

- **Docker:** despliega Sebastian HR con Docker y mantén ambas bases de datos en una misma instancia. [Más información](../introduccion/requisitos-de-instalacion.es.md)
- **Aplicación instalada:** instala Sebastian HR como una aplicación; al abrirla, usa la dirección de inicio configurada.
- **Modo de mantenimiento:** activa un modo de mantenimiento para la aplicación.

### Fichajes e informes

- **Gestión diaria:** ignora o reactiva varios fichajes a la vez desde la lista diaria.
- **Lista NFC:** muestra a todos los empleados que no están bloqueados. [Más información](../integraciones/kapri.es.md)
- **Vista agrupada:** reúne los avisos de fichajes e identifica y filtra los cierres automáticos de turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Informes de fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-la-gestion-mensual.es.md)

### Turnos y gastos

- **Colores de turno:** los turnos muestran colores asignados por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Patrones LITE:** consulta los tipos de patrón desde el menú Mantenimiento en el modo LITE. [Más información](../introduccion/ediciones-lite-y-pro.es.md)
- **Partes de gastos:** crea y consulta partes de gastos con una experiencia mejorada en dispositivos móviles.

### Interfaz y procesos

- **Inicio de sesión:** se renuevan la imagen y los estilos de la pantalla, y el asistente de configuración adopta los colores de Sebastian HR.
- **Avisos y cuadros:** avisos, alertas y cuadros de confirmación o solicitud de datos adoptan un estilo adaptado a Sebastian HR.
- **Correos de ausencia:** los correos de vacaciones y ausencias muestran la fecha y diferencian el tipo en el asunto. [Más información](../documentos-y-comunicacion/configuracion-de-notificaciones.es.md)
- **Libro de Registro de Jornada:** distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Procesos:** muestran el término «Entrada» en el idioma disponible.

### WebAPI

- **Empleados y documentos:** consulta y gestiona empleados y su información personal, documentos y adjuntos, códigos QR, fichajes y configuración de fichajes. [Más información](../integraciones/web-api.es.md)
- **Contratos y equipos:** consulta contratos e historial, equipos y sus miembros, cursos e inscripciones, documentos y vigilancias de salud. [Más información](../integraciones/web-api.es.md)
- **Jornadas y ausencias:** consulta tiempo trabajado, balances de jornada mensuales y anuales, días de trabajo a distancia, bajas, vacaciones, turnos y planificación. [Más información](../integraciones/web-api.es.md)
- **Control horario:** consulta fichajes, festivos, informes de fichajes y datos mensuales de control de ubicaciones; también puedes importar fichajes reales con retraso sin aplicar el control antifraude. [Más información](../integraciones/web-api.es.md)
- **Gestión y participación:** consulta, crea o gestiona sugerencias y reacciones, reservas y bloqueos de recursos, gastos y líneas, noticias y categorías, e instancias. [Más información](../integraciones/web-api.es.md)
- **Acceso y documentación:** la WebAPI queda activada de forma predeterminada; su documentación incluye las consultas disponibles, información sobre solicitudes rechazadas y una colección de Postman para probarlas. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** las listas muestran las solicitudes de los tipos seleccionados y se corrigen errores en instancias y solicitudes, también con varios validadores.
    - **Ausencias:** vuelven a funcionar el borrado de ausencias pasadas sin límites, las cancelaciones sin días seleccionados y la detección de descansos en el modo LITE.
    - **Empleados:** se corrigen la edición masiva de contratos, las fotos e indicadores, las excepciones de teletrabajo, los cursos, las inscripciones, los documentos y la visibilidad del botón QR.
    - **Fichajes:** se corrigen la visualización de fechas, la actualización de jornadas e incidencias, duplicados, festivos, ubicación, turnos nocturnos, zonas horarias, comentarios y filtros.
    - **Informes e importación:** se corrigen las plantillas de Excel, las fechas de informes, el cómputo de festivos, los calendarios de ausencias y los saldos de vacaciones.
    - **Instalación e integraciones:** Docker vuelve a cargar imágenes y permite completar el primer inicio; también se corrigen las comprobaciones de licencia y conexión con el ERP.
    - **Jornadas y planificación:** se corrigen la resolución masiva de incidencias, el redondeo de descansos, el cómputo de horas y la duración y visualización de turnos planificados.
    - **Navegación y procesos:** los menús desplegables y laterales vuelven a funcionar en paneles y móviles; los formularios largos y las notificaciones también funcionan correctamente.
    - **WebAPI:** las solicitudes de ausencia enviadas a la vez se procesan correctamente. [Más información](../integraciones/web-api.es.md)
