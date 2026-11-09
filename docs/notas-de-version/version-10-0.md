# Versión 10.0

La versión 10.0 amplía las opciones para gestionar ausencias y reservas, y mejora la detección de incidencias de jornada. También incorpora cambios en fichajes, informes, instalación y navegación.

## Lo más destacado

### Permisos por horas

Ahora puedes registrar permisos por horas y consultarlos en el calendario y el planificador del empleado. No descuentan días del saldo, y las horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada. También se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: restricciones de ausencias](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Ayuda integrada

Tienes un espacio de ayuda disponible desde la navegación de la aplicación. Así puedes consultar información de apoyo sin salir del entorno de Sebastian HR.

[Más información: ayuda de Sebastian HR](../index.es.md)

### Noticias según visibilidad

Puedes decidir quién ve las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso para cada categoría y las noticias se mostrarán a las personas que correspondan.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Puedes crear reservas recurrentes para varios recursos a la vez, con repetición cada cierto número de días, semanas, meses o años. También puedes excluir fines de semana y festivos; si alguna fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección.

[Más información: planificación de turnos](../turnos-y-planificacion/cuadrantes.es.md)

### Incidencias de jornada

La detección de incidencias tiene en cuenta las tolerancias del turno, las pausas, los descansos y los límites de horas. Los límites se señalan el día en que se superan y no se avisa de fichajes ausentes cuando no hay horario previsto para ese día.

[Más información: incidencias de jornada](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

## Otras novedades

### Ausencias y aprobaciones

- **Duración de solicitudes:** puedes establecer un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Flujos de aprobación:** los tipos de vacaciones y ausencias reciben su flujo automáticamente, y la conversación se mantiene unificada entre validación y revisión. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Cancelaciones:** siguen el grupo de tipos correspondiente, aparecen ordenadas en listas y menús, y se pueden gestionar aunque no tengan fechas de inicio y fin.

### Instalación y despliegue

- **Docker:** puedes desplegar Sebastian HR y configurar las dos bases de datos en una misma instancia. [Más información](../introduccion/requisitos-de-instalacion.es.md)
- **Paquetes publicados:** los documentos que subes a la aplicación ya no se incluyen en los paquetes.
- **Aplicación instalada:** puedes instalar Sebastian HR como aplicación y abrirla desde la dirección de inicio configurada.

### Fichajes y terminales

- **Gestión diaria:** puedes ignorar o reactivar varios fichajes desde la lista diaria; los ignorados no afectan al cálculo de ubicación del día.
- **Terminales Kapri/Kimaldi:** puedes gestionar fichajes con identificadores NFC; la lista NFC incluye a todos los empleados que no están bloqueados. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Cierre automático:** la vista agrupada permite mostrar y filtrar los días con fin de turno automático, e identificar esos fichajes de salida. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Punto de Acceso:** puedes consultar el código de acceso del empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes y gastos

- **Informes de fichajes:** puedes generarlos desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Libro de Registro de Jornada:** distingue las ausencias por tipo y color, e incluye un resumen; además, vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** puedes crearlos y consultarlos con una experiencia mejorada en dispositivos móviles.

### Interfaz y navegación

- **Inicio de sesión:** se renuevan la imagen y los estilos, y el asistente de configuración adopta los colores de Sebastian HR.
- **Avisos y cuadros:** los avisos, las alertas y los cuadros de confirmación y solicitud de datos tienen un estilo adaptado a Sebastian HR.

### Integraciones y WebAPI

- **Kapri:** se incorpora una integración con Kapri. [Más información](../integraciones/kapri.es.md)
- **WebAPI:** puedes consultar incidencias anuales, gestionar justificantes de gastos incluso en gastos cerrados y crear cursos; sus descripciones de procesos, parámetros y vistas son más completas. [Más información](../integraciones/web-api.es.md)

### Mantenimiento y comunicaciones

- **Modo de mantenimiento:** la aplicación incorpora un modo de mantenimiento.
- **Correos de ausencias:** los mensajes sobre vacaciones y ausencias muestran la fecha y distinguen el tipo en el asunto.

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se muestran solo las solicitudes de los tipos elegidos y se completan correctamente las acciones pendientes.
    - **Ausencias:** puedes borrar solicitudes pasadas sin límites; las cancelaciones sin días seleccionados no generan avisos imposibles de gestionar y se corrigen incidencias de descanso en LITE.
    - **Empleados:** vuelven a funcionar las fotos, los indicadores de estado, el control de teletrabajo, la edición masiva de contratos, los cursos, la firma de documentos y la opción de QR.
    - **Fichajes:** se corrigen la actualización y visualización de fichajes, las fechas y zonas horarias, los duplicados, los días libres, los festivos, la ubicación, los turnos nocturnos y las jornadas de 24 horas.
    - **Importaciones e informes:** se reconocen las hojas y plantillas de fichajes de Excel, y se corrigen fechas, festivos, ausencias y saldos en los informes.
    - **Instalación e integraciones:** Docker vuelve a cargar imágenes y fuentes, inicia correctamente y permite acceder como administrador; también se corrigen las comprobaciones de licencia y conexión del ERP.
    - **Jornadas y planificación:** funcionan la resolución en lote de incidencias, el cálculo de descansos y horas trabajadas, la duración de turnos modificados, las horas previstas durante permisos y la navegación por patrones.
    - **Navegación:** los menús desplegables y el menú lateral vuelven a mostrarse correctamente en paneles deslizantes y dispositivos móviles.
    - **Procesos:** se respetan las fechas de los informes, vuelven a verse los botones en formularios largos móviles y se corrigen avisos a empleados y sugerencias anónimas.
    - **WebAPI:** las solicitudes de ausencia se procesan correctamente cuando se reciben varias a la vez.
