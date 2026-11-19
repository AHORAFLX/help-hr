# Versión 10.0

Sebastian HR 10.0 amplía la gestión de ausencias y reservas, y facilita el acceso a la ayuda y la conexión con asistentes de IA. También renueva la plataforma y mejora el control horario, los informes y la experiencia de uso.

## Lo más destacado

### Permisos por horas

Ahora puedes configurar cada tipo de permiso para solicitarlo por días, por horas o de ambas formas. Las horas no se descuentan como días y, tanto si son retribuidas como si no, se incluyen en la exportación de nómina y en el cálculo de la jornada.

[Más información: horas de vacaciones](../horas/horas-de-vacaciones.es.md)

### Ayuda dentro de la aplicación

Abre la ayuda desde el botón de la barra superior y consulta las instrucciones sin salir de la pantalla en la que estás. La guía adapta el contenido a tu perfil: empleado, o personal de RR. HH. y responsable.

### Visibilidad de noticias

Decide quién puede ver las noticias de cada categoría mediante reglas por área, empresa, oficina, equipo o empleado. Si una categoría no tiene reglas, seguirá siendo visible para todos; si las tiene, bastará con cumplir una de ellas.

### Reservas periódicas de recursos

Reserva varios recursos en una sola operación y repite la reserva cada cierto número de días, semanas, meses o años. Puedes elegir fechas concretas o una posición del mes, excluir fines de semana y festivos, y revisar los conflictos antes de corregirlos sin volver a rellenar el formulario.

### Conexión con asistentes de IA

Conecta un asistente compatible con MCP para consultar datos y realizar gestiones con instrucciones en lenguaje natural, siempre dentro de los permisos de tu perfil. Un administrador debe habilitar MCP en la WebAPI y autorizar a los usuarios; después, cada persona conecta su asistente e inicia sesión.

[Más información: WebAPI e integraciones](../integraciones/web-api.es.md)

### Actualización de la plataforma

Sebastian HR funciona ahora sobre Flexygo 10. Esta actualización renueva, entre otros elementos, los calendarios anuales de vacaciones y ausencias, para que puedas seguir gestionando estos periodos en una plataforma actualizada.

## Otras novedades

### Ausencias y solicitudes

- **Gestión de ausencias:** asigna desde la lista de ausencias no planificadas el tipo de ausencia que corresponda.
- **Límites de solicitud:** establece un mínimo y un máximo de días para cada solicitud de ausencia.
- **Horas teóricas:** indica si una ausencia no remunerada debe descontarse de las horas teóricas.
- **Cancelaciones:** las cancelaciones de ausencias tienen su propio tipo de solicitud, separado del de vacaciones.
- **Avisos de solicitud:** los correos de vacaciones y ausencias incluyen las fechas solicitadas y el tipo de solicitud.

### Fichajes y jornadas

- **Descansos:** una nueva incidencia avisa si el descanso fichado supera el previsto en el turno.
- **Gestión diaria:** ignora o reactiva varios fichajes a la vez y filtra los días con fin de turno automático.
- **Terminales Kapri:** conecta terminales Kapri de Kimaldi para fichar con tarjetas NFC o códigos QR. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Inserciones de fichaje:** al aceptar una inserción, se actualizan al momento la jornada y sus incidencias.
- **Punto de acceso:** puedes mostrar el código que estás escribiendo aunque normalmente aparezca oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Turnos y planificación

- **Incidencias de turno:** respetan las tolerancias y permiten comparar las horas trabajadas con las previstas. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Detección de descansos:** los descansos entre jornadas y las pausas tras más de seis horas se detectan sin esperar a validar la jornada. [Más información](../turnos-y-planificacion/descanso-minimo-de-turno.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Gastos e informes

- **Justificantes de gastos:** desde el móvil, añade líneas a un parte de gastos con un formulario y adjunta los justificantes.
- **Foto de ticket:** el asistente puede adjuntar la foto de un ticket a una línea de gasto.
- **Informes de fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/catalogo-de-informes.es.md)
- **Libro de Registro de Jornada:** incluye un desglose diario de ausencias y permisos, con un resumen por tipo. [Más información](../informes/informes-de-control-horario.es.md)

### Plataforma y experiencia de uso

- **Modo mantenimiento:** los administradores pueden activarlo desde el menú superior.
- **Aplicación instalable:** instala Sebastian HR en el ordenador o el móvil desde el navegador.
- **Inicio de sesión:** la pantalla de acceso tiene un diseño renovado.
- **Avisos y cuadros de diálogo:** muestran un diseño nuevo con un color y un icono para cada tipo.

### WebAPI

- **Notificaciones:** las integraciones pueden consultar el listado y marcar notificaciones como leídas. [Más información](../integraciones/web-api.es.md)
- **Noticias:** las integraciones pueden marcar una noticia como leída y consultar su estado de lectura. [Más información](../integraciones/web-api.es.md)
- **Permisos de procesos:** las llamadas a procesos requieren la colección y aplican los permisos del usuario. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se guardan los flujos para todos los tipos de solicitud, se unifican los comentarios y las listas filtran por tipo; también se resuelven correctamente las validaciones.
    - **Ausencias y vacaciones:** vuelven a funcionar los cálculos de horas, las solicitudes y cancelaciones, la inserción de fichajes planificados y las opciones de cada fila.
    - **Empleados:** se corrigen la edición de empleados y contratos, los permisos de acceso, los cursos, las notificaciones, los documentos y la información visible en las fichas.
    - **Fichajes:** vuelven a funcionar el punto de acceso y las acciones de gestión; se corrigen las solicitudes, las zonas horarias, los turnos nocturnos y la actualización de pantalla.
    - **Incidencias y jornadas:** se corrigen el cálculo de jornadas, los descansos, los días libres, la planificación, los festivos y la resolución de incidencias.
    - **Informes:** vuelven a respetarse los periodos y filtros elegidos, y se muestran correctamente las fechas y las ausencias en los informes y calendarios.
    - **Navegación:** se corrigen los formularios y menús en ventanas deslizantes y en dispositivos móviles, y vuelve a funcionar la apertura de acciones disponibles.
    - **Instalación e integraciones:** funcionan las importaciones de Excel y las conexiones con AHORA ERP y el Canal de Denuncias; los paquetes ya no incluyen documentos subidos.
    - **Contratos y nóminas:** la lista de contratos muestra correctamente todos los salarios.
    - **WebAPI y traducciones:** se corrigen los datos de las sugerencias y las traducciones de tipos de solicitud y fichaje.
