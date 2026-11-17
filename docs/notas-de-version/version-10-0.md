# Versión 10.0

Sebastian HR 10 amplía las opciones para gestionar permisos, noticias, reservas y fichajes, y permite conectar asistentes de IA compatibles con MCP. También renueva la plataforma y reúne mejoras en la planificación, los informes y el uso desde móviles.

## Lo más destacado

### Permisos por horas

Puedes configurar cada tipo de permiso para que se solicite por días, por horas o de ambas formas. Las horas no descuentan días de permiso y, tanto si son retribuidas como si no, aparecen en la exportación de nómina y cuentan para calcular la jornada.

[Más información: horas de vacaciones](../horas/horas-de-vacaciones.es.md)

### Ayuda desde la aplicación

Abre la ayuda desde el botón de la barra superior sin salir de Sebastian HR. La guía que ves se adapta a tu perfil: encontrarás la información para empleados o la destinada a RR. HH. y responsables.

[Más información: guía de ayuda](../index.es.md)

### Visibilidad de noticias

Decide quién puede ver las noticias de cada categoría según su área, empresa, oficina, equipo o empleado. Las categorías sin reglas siguen siendo visibles para todos; las noticias de una categoría restringida no aparecen para quien no cumpla ninguna de sus reglas.

### Reservas repetidas

Reserva varios recursos a la vez y repite las reservas cada cierto número de días, semanas, meses o años. Para las repeticiones mensuales y anuales puedes elegir una fecha o una posición, como el último viernes, y excluir fines de semana y festivos.

### Asistentes de IA y WebAPI

Conecta Sebastian HR con asistentes de IA compatibles con MCP para consultar datos y realizar gestiones con instrucciones escritas en tus propias palabras. Un administrador activa MCP y autoriza a los usuarios; cada usuario conecta su asistente e inicia sesión, con los permisos de su perfil.

[Más información: configuración de WebAPI](../integraciones/web-api.es.md)

### Actualización a Flexygo 10

Sebastian HR funciona ahora sobre Flexygo 10. La actualización renueva, entre otros elementos, los calendarios anuales de vacaciones y ausencias.

## Otras novedades

### Ausencias y solicitudes

- **Gestión de ausencias:** registra ausencias del tipo que elijas desde la lista de ausencias no planificadas y establece límites mínimos y máximos de días por solicitud.
- **Cómputo de horas:** configura los tipos de ausencia no remunerada para que no cuenten en las horas teóricas.
- **Solicitudes y avisos:** las cancelaciones tienen un tipo de solicitud propio y los correos indican las fechas solicitadas y el tipo de solicitud. [Más información](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md)
- **Aprobaciones:** los grupos de tipos de ausencia sin un flujo reciben uno por defecto al instalar o actualizar. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)

### Fichajes y jornadas

- **Descansos:** una nueva incidencia avisa cuando los descansos fichados superan los previstos en el turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Gestión diaria:** puedes ignorar o reactivar varios fichajes a la vez y filtrar los días con cierre automático de turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Punto de acceso:** puedes conectar terminales Kapri de Kimaldi para fichar con tarjeta NFC o código QR. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Código de fichaje:** en el punto de acceso puedes mostrar el código mientras lo escribes, aunque esté configurado como oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Planificación y turnos

- **Informes de fichajes:** genera informes desde la gestión mensual o semanal agrupada. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Tipos de patrón:** en modo LITE, consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Informes y gastos

- **Libro de Registro de Jornada:** consulta el desglose diario de ausencias y permisos y su resumen por tipo. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos en el móvil:** añade líneas desde un formulario y adjunta sus justificantes.

### Plataforma e interfaz

- **Modo mantenimiento:** los administradores pueden activarlo desde el menú superior.
- **Aplicación instalable:** instala Sebastian HR en el ordenador o el móvil desde el navegador.
- **Inicio de sesión y avisos:** se renueva el diseño de acceso y el de los avisos y cuadros de alerta, confirmación y petición de datos.

### WebAPI

- **Notificaciones:** la WebAPI permite consultar las notificaciones de la aplicación. [Más información](../integraciones/web-api.es.md)
- **Noticias:** la WebAPI permite marcar noticias como leídas y consultar su estado de lectura. [Más información](../integraciones/web-api.es.md)
- **Acceso y datos:** cambian las llamadas a procesos, los permisos y los datos disponibles para cada usuario. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** los flujos se guardan correctamente, las listas y comentarios son coherentes y las solicitudes se resuelven según la decisión del validador.
    - **Vacaciones y ausencias:** vuelven a funcionar el cómputo de horas, las cancelaciones, las ediciones de días pasados y las opciones de las listas; se evitan solicitudes vacías o duplicadas.
    - **Empleados y formación:** se corrigen la edición de contratos, los cursos, las inscripciones, la firma de documentos, las notificaciones y la visualización de fichas.
    - **Fichajes:** se corrigen la fecha y hora, la actualización tras fichar, las acciones en lote y los marcajes desde la app, los turnos nocturnos y el control de ubicación.
    - **Jornadas:** vuelven a calcularse correctamente las horas, los descansos, los festivos y las incidencias, tanto con planificación como sin ella.
    - **Planificación:** se corrigen los cambios de turno, el uso de patrones y la visualización de horas en días de permiso.
    - **Informes:** los informes respetan los periodos seleccionados y los filtros de empleados, y muestran correctamente las fechas y ausencias.
    - **Navegación en móviles:** los formularios, menús, listas desplegables y el menú lateral se muestran y funcionan correctamente.
    - **Instalación e integraciones:** se corrigen los paquetes de instalación y actualización, las traducciones y las conexiones con AHORA ERP y el Canal de Denuncias.
    - **WebAPI:** la lista de sugerencias incluye la reacción del usuario. [Más información](../integraciones/web-api.es.md)
