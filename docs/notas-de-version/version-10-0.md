# Versión 10.0

La versión 10.0 amplía las opciones para gestionar ausencias, noticias y reservas, y facilita el acceso a la ayuda y el uso de asistentes de IA. También renueva la plataforma y mejora la gestión de fichajes, solicitudes e informes.

## Lo más destacado

### Permisos por horas

Puedes configurar cada tipo de permiso para que se solicite por días, por horas o de ambas formas. Las horas no se descuentan como días y, tanto si son retribuidas como si no, aparecen en la exportación de nómina y se tienen en cuenta al calcular la jornada.

[Más información: gestión de vacaciones](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)

### Ayuda dentro de la aplicación

Abre la guía desde el botón de ayuda de la barra superior sin salir de Sebastian HR. El contenido se adapta a tu perfil: verás la información para empleados o la destinada a RR. HH. y responsables.

### Visibilidad de noticias

Decide quién puede ver las noticias de cada categoría según el área, la empresa, la oficina, el equipo o el empleado. Si una categoría no tiene reglas, seguirá siendo visible para todos; si las configuras, la verá quien cumpla al menos una.

### Reservas repetidas

Reserva varios recursos a la vez y repite las reservas cada cierto número de días, semanas, meses o años. Puedes fijar fechas mensuales o anuales, excluir fines de semana y festivos y revisar los conflictos; si una fecha está ocupada, no se crea ninguna reserva.

### Asistentes de IA y WebAPI

Conecta Sebastian HR a asistentes compatibles con MCP para consultar datos y realizar gestiones con tus propias palabras, según los permisos de tu perfil. Un administrador activa MCP y autoriza a los usuarios; después, cada usuario conecta el asistente a la dirección de la aplicación terminada en /mcp e inicia sesión.

[Más información: WebAPI](../integraciones/web-api.es.md)

### Actualización de plataforma

Sebastian HR funciona ahora sobre Flexygo 10. Entre los cambios, se renuevan los calendarios anuales de vacaciones y ausencias; la conexión de asistentes de IA mediante MCP se explica por separado.

## Otras novedades

### Ausencias

- **Ausencias no planificadas:** puedes asignar a sus empleados una ausencia del tipo que elijas.
- **Ausencias no remuneradas:** puedes decidir si sus horas cuentan en las horas teóricas.
- **Duración de las solicitudes:** fija un mínimo y un máximo de días para cada solicitud de ausencia.

### Solicitudes y aprobaciones

- **Flujos de aprobación:** los grupos de tipos de ausencia que no tengan uno reciben un flujo por defecto al instalar o actualizar. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Cancelaciones:** tienen un tipo de solicitud propio, «Cancelar ausencias», separado del de vacaciones.
- **Correos de solicitudes:** indican las fechas solicitadas y si se trata de vacaciones o de una ausencia.

### Fichajes y jornadas

- **Descansos:** una nueva incidencia avisa si el descanso fichado supera el previsto en el turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Gestión diaria:** puedes ignorar o reactivar varios fichajes a la vez.
- **Terminales Kapri:** conecta terminales de Kimaldi para fichar con una tarjeta NFC o un código QR. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Fin de turno automático:** puedes ver y filtrar estos días en la gestión diaria y agrupada de fichajes. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Punto de acceso:** puedes mostrar el código mientras lo tecleas, aunque esté configurado como oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)
- **Incidencias de jornada:** las de entrada retrasada, salida anticipada y límites del turno respetan sus tolerancias. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Validación de jornada:** las incidencias por descanso entre jornadas o por más de seis horas sin pausa aparecen antes de validar. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

### Gastos e informes

- **Justificantes de gastos:** el asistente puede adjuntar la foto de un ticket a una línea de gasto.
- **Informes de fichajes:** puedes generarlos desde la gestión agrupada mensual o semanal. [Más información](../informes/catalogo-de-informes.es.md)
- **Gastos desde el móvil:** añade líneas a un parte mediante un formulario y adjunta sus justificantes.
- **Libro de Registro de Jornada:** incluye el desglose diario de ausencias y permisos, con un resumen por tipo. [Más información](../informes/informes-de-control-horario.es.md)

### Aplicación y planificación

- **Modo de mantenimiento:** los administradores pueden activarlo desde el menú superior.
- **Aplicación instalable:** instala Sebastian HR en un ordenador o móvil desde el navegador.
- **Inicio de sesión:** la pantalla tiene un diseño renovado.
- **Avisos y ventanas:** las alertas, confirmaciones y peticiones de datos usan un diseño nuevo con color e icono propios.
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### WebAPI

- **Justificantes de ausencia:** el asistente puede adjuntar un justificante al registrar una ausencia. [Más información](../integraciones/web-api.es.md)
- **Solicitudes:** el asistente puede consultar el detalle de una solicitud. [Más información](../integraciones/web-api.es.md)
- **Notificaciones:** la WebAPI permite consultar las notificaciones disponibles en la aplicación. [Más información](../integraciones/web-api.es.md)
- **Noticias:** la WebAPI permite marcarlas como leídas y consultar su estado de lectura. [Más información](../integraciones/web-api.es.md)
- **Permisos:** la WebAPI ejecuta procesos de otra forma y limita las operaciones y los datos según los permisos del usuario. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** vuelve a funcionar la configuración de los flujos, la coherencia de los comentarios y filtros, y la resolución de solicitudes al aceptar o denegar. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
    - **Ausencias y vacaciones:** se corrigen los cálculos de horas, las cancelaciones y sus motivos, las solicitudes vacías y las acciones de las listas.
    - **Empleados:** vuelven a funcionar la edición de contratos, festivos, habilidades, cursos y fichas; también se corrigen permisos, avisos, inscripciones y documentos para firmar.
    - **Fichajes:** se corrigen el acceso al punto de fichaje, las solicitudes de cambio, las zonas horarias, la actualización de pantalla y los fichajes en turnos nocturnos. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/fichaje-con-zonas-horarias.es.md)
    - **Jornadas:** se corrigen el cálculo de horas y descansos, las incidencias, la planificación y la resolución de avisos, también en días libres y sin planificación. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
    - **Informes e integraciones:** vuelven a funcionar las importaciones de Excel, los informes respetan periodos y filtros, y se recuperan las conexiones con los servicios integrados. [Más información](../informes/catalogo-de-informes.es.md)
    - **Navegación móvil:** se corrigen la posición de los botones y las listas desplegables, y la visualización del menú lateral en móviles y tabletas.
    - **Noticias y planificación:** vuelven a abrirse correctamente las noticias y los documentos, se registran las lecturas y se corrigen acciones de reservas y turnos.
    - **Instalación y traducciones:** se corrigen los archivos incluidos en los paquetes y las traducciones de tipos de solicitud y fichaje; la WebAPI vuelve a incluir los datos de reacción. [Más información](../integraciones/web-api.es.md)
