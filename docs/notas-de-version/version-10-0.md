# Versión 10.0

La versión 10.0 amplía la gestión de ausencias, la planificación y las conexiones con asistentes de IA. También mejora el control horario y reúne ajustes para que las tareas habituales funcionen con más claridad.

## Lo más destacado

### Permisos por horas

Ahora puedes configurar cada tipo de permiso para que se solicite por días, por horas o de ambas formas. Las horas no descuentan días de permiso y las retribuidas y no retribuidas aparecen en la exportación de nómina y cuentan en el cálculo de la jornada.

[Más información: horas de vacaciones](../horas/horas-de-vacaciones.es.md)

### Ayuda dentro de la aplicación

Abre la ayuda desde el botón de la barra superior y consulta la guía sin salir de Sebastian HR. El contenido se adapta a tu perfil: verás la información para empleados o para el equipo de RR. HH. y responsables.

[Más información: guía de ayuda](../index.es.md)

### Visibilidad de las noticias

Decide quién puede ver las noticias de cada categoría según su área, empresa, oficina, equipo o empleado. Configura las reglas en «Visibilidad de la categoría»: si no hay reglas, la categoría sigue siendo visible para todo el mundo; si las hay, basta con cumplir una.

[Más información: visibilidad por categoría](../documentos-y-comunicacion/visibilidad-de-documentos-por-categoria.es.md)

### Reservas repetidas de recursos

Reserva varios recursos a la vez y repite las reservas cada cierto número de días, semanas, meses o años. Puedes elegir fechas concretas o posiciones como el último viernes, y excluir fines de semana y festivos. Si hay conflictos, consulta las fechas afectadas y corrígelas sin volver a rellenar el formulario.

[Más información: métodos de planificación](../turnos-y-planificacion/metodos-de-planificacion.es.md)

### Asistentes de IA y WebAPI

Con el MCP de Sebastian, puedes consultar datos y hacer gestiones con tus propias palabras desde un asistente compatible; el acceso se limita a los permisos de tu perfil. Un administrador activa MCP en la configuración de la WebAPI y autoriza a los usuarios, que conectan el asistente a la dirección de la aplicación terminada en /mcp e inician sesión.

[Más información: webapi](../integraciones/web-api.es.md)

### Actualización de plataforma

Sebastian HR funciona ahora sobre Flexygo 10. La actualización renueva, entre otros elementos, los calendarios anuales de vacaciones y ausencias, y permite conectar asistentes de IA mediante MCP.

## Otras novedades

### Ausencias y solicitudes

- **Gestión de ausencias:** registra ausencias desde la lista de no planificadas, excluye ciertos tipos no remunerados de las horas teóricas y establece límites de días por solicitud. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Aprobaciones:** los grupos de tipos de ausencia sin flujo reciben uno predeterminado al instalar o actualizar. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Solicitudes y correos:** las cancelaciones tienen un tipo propio y los avisos de vacaciones y ausencias indican las fechas y el tipo de solicitud. [Más información](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md)

### Fichajes y jornadas

- **Descansos:** una nueva incidencia avisa si el descanso fichado supera el previsto en el turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Gestión diaria:** ignora o reactiva varios fichajes a la vez y filtra los días con cierre automático de turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Incidencias de jornada:** las tolerancias del turno se aplican a las entradas tardías, salidas anticipadas y límites; algunas incidencias aparecen antes de validar la jornada. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Punto de acceso:** ahora puedes mostrar el código que estás escribiendo aunque esté configurado como oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Dispositivos y planificación

- **Terminales Kapri:** conecta terminales de Kimaldi para que el personal fiche con una tarjeta NFC o un código QR. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Gastos e informes

- **Partes de gastos:** adjunta la foto de un ticket desde el asistente y añade líneas y justificantes desde el móvil.
- **Informes de fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Libro de Registro de Jornada:** consulta el desglose diario de ausencias y permisos, con un resumen por tipo. [Más información](../informes/informes-de-control-horario.es.md)

### Plataforma y acceso

- **Modo mantenimiento:** los administradores pueden activarlo desde el menú superior.
- **Aplicación instalable:** instala Sebastian HR en un ordenador o móvil desde el navegador.
- **Inicio y avisos:** la pantalla de inicio de sesión y los cuadros de alerta, confirmación y petición de datos tienen un diseño renovado.

### WebAPI

- **Solicitudes y notificaciones:** consulta el detalle de una solicitud y las notificaciones disponibles; el asistente también puede adjuntar justificantes al registrar ausencias. [Más información](../integraciones/web-api.es.md)
- **Noticias:** marca una noticia como leída y consulta su estado de lectura desde la WebAPI. [Más información](../integraciones/web-api.es.md)
- **Permisos:** las operaciones y los datos de la WebAPI se ajustan a los permisos del usuario. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** vuelven a guardarse los flujos y a coincidir los comentarios y filtros; las solicitudes se resuelven correctamente cuando un validador decide. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
    - **Ausencias:** vuelven a funcionar los descuentos de jornada, las listas y los formularios; las solicitudes y cancelaciones evitan duplicados y fechas vacías, y respetan las horas y días laborables.
    - **Empleados:** se aplican correctamente los permisos, cambios masivos, inscripciones, avisos, cursos y sugerencias; también vuelven a mostrarse las fotos y se aclaran los errores al firmar PDFs.
    - **Fichajes:** se corrigen el acceso, las zonas horarias, las solicitudes de cambio y la actualización de jornadas; vuelven a funcionar las acciones de planificación y se evitan registros duplicados.
    - **Jornadas:** se calculan correctamente turnos, descansos, horas y festivos, y dejan de aparecer incidencias incorrectas en días libres, sin planificación o cubiertos por ausencias.
    - **Informes, importación e integraciones:** los informes respetan periodos y filtros, las plantillas de Excel cargan los datos y vuelven a funcionar las conexiones y consultas de licencias.
    - **Instalación y plataforma:** los paquetes ya no incluyen archivos de documentos subidos y se conservan las traducciones, los colores y los nombres personalizados al actualizar.
    - **Navegación y noticias:** los formularios y menús se muestran bien en móviles; se corrigen los accesos a noticias y documentos y el registro de lectura.
    - **Planificación y WebAPI:** vuelven a funcionar las reservas, los patrones y los cambios de turno, y la API incluye la información de reacción a sugerencias. [Más información](../integraciones/web-api.es.md)
