# Versión 10.0

La versión 10.0 amplía las opciones para gestionar ausencias, reservas y noticias, y facilita el acceso a la ayuda y la conexión con otras aplicaciones. También renueva la plataforma y mejora la gestión diaria de fichajes, jornadas e informes.

## Lo más destacado

### Permisos por horas

Ahora puedes configurar cada tipo de permiso para solicitarlo por días, por horas o de ambas formas. Los permisos por horas no descuentan días y sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y en el cálculo de la jornada.

[Más información: horas de vacaciones](../horas/horas-de-vacaciones.es.md)

### Ayuda dentro de la aplicación

Abre la ayuda de Sebastian HR desde el botón de la barra superior y consulta la guía sin salir de la aplicación. El contenido se adapta a tu perfil: verás la información para empleados o la dirigida a RR. HH. y responsables.

[Más información: ayuda de Sebastian HR](../index.es.md)

### Visibilidad de noticias

Puedes definir quién ve las noticias de cada categoría según su área, empresa, oficina, equipo o empleado. Si una categoría no tiene reglas, sigue siendo visible para todo el mundo; si las tiene, solo la verá quien cumpla alguna de ellas.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas repetidas

Reserva varios recursos a la vez y programa repeticiones cada cierto número de días, semanas, meses o años. Para las repeticiones mensuales o anuales, puedes elegir una fecha o una posición, excluir fines de semana y festivos y resolver los conflictos de ocupación sin volver a completar el formulario.

### Asistentes de IA y Web API

Conecta asistentes compatibles con MCP para consultar datos y pedir gestiones con tus propias palabras, según los permisos de tu perfil. Un administrador activa el acceso; además, la nueva Web API permite conectar la app móvil y otras aplicaciones con Sebastian HR.

[Más información: Web API](../integraciones/web-api.es.md)

### Actualización de plataforma

Sebastian HR funciona ahora sobre Flexygo 10. La actualización renueva, entre otros elementos, los calendarios anuales de vacaciones y ausencias.

## Otras novedades

### Ausencias y permisos

- **Gestión de ausencias:** puedes registrar ausencias para empleados de la lista de no planificadas, establecer límites de días por solicitud y excluir ciertos tipos de ausencia no remunerada del cómputo de horas teóricas. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Solicitudes:** los grupos de ausencias sin flujo reciben uno por defecto; cancelar ausencias tiene un tipo de solicitud propio y los correos incluyen las fechas solicitadas. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)

### Fichajes

- **Gestión diaria:** puedes ignorar o reactivar varios fichajes a la vez y consultar o filtrar los días con cierre automático de turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Terminales Kapri:** conecta terminales de Kimaldi para que los empleados fichen con una tarjeta NFC o un código QR. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Punto de acceso:** puedes mostrar el código que estás escribiendo aunque esté configurado como oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Turnos y jornadas

- **Incidencias de turno:** las incidencias por entrada retrasada, salida anticipada o fichaje fuera de límites respetan las tolerancias configuradas. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Revisión de jornada:** las incidencias por descanso entre jornadas y por más de seis horas sin pausa aparecen antes de validar la jornada. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Informes y gastos

- **Informes de fichajes:** genera informes desde la gestión mensual o semanal agrupada de fichajes. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Gastos desde el móvil:** añade líneas a un parte desde un formulario y adjunta los justificantes.
- **Libro de Registro de Jornada:** consulta el desglose diario de ausencias y permisos y el resumen por tipo. [Más información](../informes/informes-de-control-horario.es.md)

### Acceso e interfaz

- **Modo de mantenimiento:** los administradores pueden activarlo desde el menú superior.
- **Aplicación instalable:** instala Sebastian HR en un ordenador o móvil desde el navegador.
- **Inicio y avisos:** se renueva el diseño de inicio de sesión y de los avisos, las confirmaciones y las peticiones de datos.

### Conexiones e integraciones

- **Web API:** cambia la forma de llamar a sus procesos y se ajustan los datos y las acciones disponibles. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** vuelven a guardarse los pasos de todos los tipos de solicitud; comentarios, filtros y resolución de solicitudes funcionan de forma coherente.
    - **Ausencias y vacaciones:** se corrigen listas, fichajes planificados, formularios, cancelaciones, motivos de denegación y edición de días pasados; también se evitan solicitudes vacías o en días no laborables.
    - **Empleados:** se corrigen la edición masiva de contratos, los cursos, las inscripciones, el envío de documentos a firmar, los avisos, las sugerencias y la foto de la ficha.
    - **Fichajes:** vuelven a funcionar las acciones de selección y planificación; se corrigen horarios, zonas horarias, actualización de pantalla, ubicación, solicitudes y fichajes en turnos nocturnos.
    - **Informes e importación:** se corrigen las importaciones desde Excel, los periodos y fechas de los informes, los filtros de empleados y la presentación de ausencias por grupo.
    - **Instalación e integraciones:** los paquetes ya no incluyen archivos de documentos subidos y vuelven a funcionar las consultas de licencias y la conexión con AHORA ERP.
    - **Jornadas:** se corrigen el cálculo y la agrupación de jornadas, las incidencias, los descansos, los festivos trabajados y la conservación de nombres y colores personalizados.
    - **Navegación móvil:** los botones de formularios largos, las listas desplegables y el menú lateral vuelven a mostrarse correctamente en móviles y tabletas.
    - **Planificación:** se actualiza la duración al cambiar un turno y vuelven a funcionar los patrones y la planificación semanal de permisos.
    - **Plataforma y Web API:** se corrigen las traducciones de tipos de solicitud y fichaje, y la lista de sugerencias incluye la reacción del usuario actual.
