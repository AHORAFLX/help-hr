# Versión 10.0

Sebastian HR 10.0 incorpora nuevas formas de gestionar ausencias, noticias y reservas, además de conectar la aplicación con asistentes de IA. También renueva la experiencia de uso y mejora la gestión de fichajes, jornadas y solicitudes.

## Lo más destacado

### Permisos por horas

Ahora puedes configurar cada tipo de permiso para solicitarlo por días, por horas o de ambas formas. Las horas no descuentan días de permiso y, tanto si son retribuidas como si no, aparecen en la exportación de nómina y cuentan en el cálculo de la jornada.

[Más información: restricciones de ausencias](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Ayuda dentro de la aplicación

Puedes abrir la ayuda desde el botón de la barra superior sin salir de Sebastian HR. La guía se adapta a tu perfil y muestra la información para empleados o para el equipo de RR. HH. y responsables, según corresponda.

### Visibilidad de noticias

Puedes decidir quién ve las noticias de cada categoría mediante reglas por área, empresa, oficina, equipo o empleado. Si no configuras ninguna regla, la categoría seguirá siendo visible para todos; si las configuras, bastará con cumplir una para verla.

### Reservas recurrentes

Puedes reservar varios recursos a la vez y repetir las reservas cada cierto número de días, semanas, meses o años. En las repeticiones mensuales y anuales puedes elegir un día o una posición concreta, excluir fines de semana y festivos, y revisar los conflictos antes de corregirlos.

### Asistentes de IA y WebAPI

Con MCP, puedes conectar un asistente compatible para consultar datos y hacer gestiones con instrucciones en lenguaje natural, como pedir vacaciones, fichar o aprobar solicitudes. Un administrador activa MCP y autoriza a los usuarios; cada asistente solo puede consultar y realizar acciones permitidas por el perfil de quien lo usa.

[Más información: web api](../integraciones/web-api.es.md)

### Nueva base de plataforma

Sebastian HR funciona ahora sobre Flexygo 10. Entre otros cambios, se renuevan los calendarios anuales de vacaciones y ausencias y se añade la posibilidad de conectar asistentes de IA mediante MCP.

## Otras novedades

### Ausencias

- **Ausencias no planificadas:** asigna desde su lista el tipo de ausencia que corresponda.
- **Horas teóricas:** excluye de su cálculo las ausencias no remuneradas que elijas.
- **Límites de solicitud:** establece un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Fichajes y jornadas

- **Descansos:** una nueva incidencia avisa si el descanso fichado supera el previsto en el turno.
- **Gestión diaria:** ignora o reactiva varios fichajes a la vez y filtra los días con fin de turno automático.
- **Terminales Kapri:** conecta terminales Kimaldi para fichar con tarjeta NFC o código QR. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Punto de acceso:** muestra el código que estás tecleando aunque esté configurado como oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)
- **Control de jornadas:** las incidencias de entrada retrasada, salida anticipada y límites de turno respetan las tolerancias; otras incidencias aparecen antes de validar.

### Gastos e informes

- **Justificantes de gastos:** el asistente puede adjuntar la foto de un ticket; desde el móvil también puedes añadir líneas y adjuntar justificantes.
- **Informes de fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Libro de Registro de Jornada:** incluye el detalle diario de ausencias y permisos y un resumen por tipo. [Más información](../informes/informes-de-control-horario.es.md)

### Solicitudes y aprobaciones

- **Flujos de ausencia:** los grupos sin flujo de aprobación reciben uno por defecto al instalar o actualizar. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Cancelaciones:** tienen su propio tipo de solicitud, separado del de vacaciones. [Más información](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md)
- **Correos de solicitudes:** indican las fechas solicitadas y el tipo de solicitud.

### WebAPI e integraciones

- **Notificaciones:** la WebAPI permite consultar su lista y marcarlas como leídas desde una integración. [Más información](../integraciones/web-api.es.md)
- **Noticias:** consulta desde la WebAPI si una noticia se ha leído y márcala como leída. [Más información](../integraciones/web-api.es.md)
- **Solicitudes:** el asistente puede consultar su detalle y adjuntar justificantes de ausencia para obtener las fechas y horas que falten. [Más información](../integraciones/web-api.es.md)
- **Procesos:** las llamadas requieren indicar la colección y aplican los permisos del usuario. [Más información](../integraciones/web-api.es.md)

### Plataforma y experiencia de uso

- **Modo de mantenimiento:** los administradores pueden activarlo desde el menú superior.
- **Aplicación instalable:** instala Sebastian HR en el ordenador o el móvil desde el navegador.
- **Inicio de sesión:** se renueva el diseño de la pantalla.
- **Avisos y cuadros:** las alertas, confirmaciones y peticiones de datos muestran un nuevo diseño con color e icono según su tipo.
- **Planificación LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se guardan los pasos de los flujos, coinciden los comentarios y filtros, y las solicitudes se resuelven correctamente al aceptar o denegar. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
    - **Ausencias y vacaciones:** vuelven a funcionar las listas y acciones; se corrigen los cálculos de horas, las cancelaciones, los borrados y las solicitudes vacías o en días no laborables.
    - **Empleados y contratos:** se corrigen permisos, edición y borrado, inscripciones y avisos, cursos, documentos, sugerencias y fotos; también se muestran bien los salarios.
    - **Fichajes:** se corrigen el acceso, las solicitudes, las zonas horarias, los turnos nocturnos, la ubicación y los cálculos; la pantalla y las acciones vuelven a actualizarse correctamente.
    - **Jornadas y turnos:** se corrigen incidencias, descansos, festivos, planificación y recálculos; los fichajes sin planificación y los turnos personalizados se gestionan correctamente.
    - **Informes e importaciones:** las plantillas de Excel cargan datos y los informes respetan los periodos, filtros, fechas y agrupaciones seleccionados.
    - **Navegación y traducciones:** se corrigen los formularios y menús en móviles, las acciones sin proceso asociado y las traducciones de tipos de solicitud y fichaje.
    - **Instalación e integraciones:** los paquetes ya no incluyen archivos de documentos subidos y vuelven a funcionar las consultas de licencias y la conexión con AHORA ERP. [Más información](../integraciones/integracion-con-ahora-erp.es.md)
    - **Noticias y WebAPI:** la lectura de noticias y documentos vuelve a registrarse; la lista de sugerencias incluye el dato de reacción del usuario. [Más información](../integraciones/web-api.es.md)
