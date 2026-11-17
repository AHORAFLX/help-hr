# Versión 10.0

Sebastian HR 10.0 incorpora nuevas formas de gestionar permisos, noticias y reservas, y amplía las posibilidades de conexión con otras aplicaciones. También renueva la experiencia diaria de uso y ajusta la gestión de fichajes, jornadas e informes.

## Lo más destacado

### Permisos por horas

Ahora puedes configurar cada tipo de permiso para que se solicite por días, por horas o de ambas formas. Las horas no descuentan días de permiso y, tanto si son retribuidas como si no, se reflejan en la exportación de nómina y en el cálculo de la jornada.

[Más información: horas de vacaciones](../horas/horas-de-vacaciones.es.md)

### Ayuda dentro de la aplicación

Puedes abrir la guía de Sebastian HR desde el botón de ayuda de la barra superior, sin salir de la aplicación. El contenido se adapta a tu perfil y muestra la información dirigida a empleados o a personal de RR. HH. y responsables.

### Visibilidad de las noticias

Puedes decidir quién ve las noticias de cada categoría según su área, empresa, oficina, equipo o persona. Configura las reglas en «Visibilidad de la categoría»; si una categoría no tiene reglas, las noticias siguen siendo visibles para todo el mundo.

### Reservas repetidas de recursos

Puedes reservar varios recursos a la vez y repetir las reservas cada cierto número de días, semanas, meses o años. En las repeticiones mensuales o anuales puedes elegir un día o una posición, como el último viernes, y excluir fines de semana y festivos.

### Conexión con asistentes de IA

Puedes conectar asistentes de IA compatibles con MCP y usar la Web API desde la app móvil y otras aplicaciones. El asistente puede consultar datos y realizar gestiones con tus instrucciones, siempre según los permisos de tu perfil; un administrador debe habilitar MCP y autorizar el acceso.

[Más información: Web API](../integraciones/web-api.es.md)

### Actualización de plataforma

Sebastian HR funciona ahora sobre Flexygo 10, con cambios que renuevan, entre otras cosas, los calendarios anuales de vacaciones y ausencias. Esta versión también permite conectar asistentes de IA mediante MCP.

## Otras novedades

### Ausencias y solicitudes

- **Registro de ausencias:** asigna un tipo de ausencia a los empleados desde la lista de ausencias no planificadas.
- **Tipos de ausencia:** decide si las ausencias no remuneradas cuentan en las horas teóricas y fija los días mínimos y máximos por solicitud. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Solicitudes:** las cancelaciones de ausencias tienen un tipo propio, y los correos indican las fechas solicitadas y el tipo de solicitud.

### Fichajes y jornadas

- **Descansos fichados:** una incidencia avisa cuando los descansos registrados superan los previstos en el turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Gestión diaria:** puedes ignorar o reactivar varios fichajes a la vez e identificar y filtrar los días con fin de turno automático.
- **Tolerancias del turno:** las incidencias por entrada tardía, salida anticipada o límites del turno tienen en cuenta las tolerancias configuradas.
- **Incidencias de jornada:** los avisos por descanso entre jornadas y por más de seis horas sin pausa aparecen antes de validar la jornada. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

### Terminales y puntos de acceso

- **Terminales Kapri:** conecta terminales de Kimaldi para que los empleados fichen con tarjeta NFC o código QR. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Punto de acceso:** puedes mostrar el código mientras lo tecleas aunque esté configurado para aparecer oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes y gastos

- **Informes de fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Partes de gastos:** desde el móvil, añade líneas al formulario y adjunta los justificantes.
- **Libro de Registro de Jornada:** consulta el desglose diario de ausencias y permisos, con un resumen por tipo. [Más información](../informes/informes-de-control-horario.es.md)

### Plataforma y experiencia de uso

- **Modo mantenimiento:** los administradores pueden activarlo desde el menú superior.
- **Aplicación instalable:** instala Sebastian HR en el ordenador o en el móvil desde el navegador.
- **Pantallas y avisos:** se renuevan el inicio de sesión y el diseño de los avisos y cuadros de alerta, confirmación y petición de datos.

### Web API

- **Noticias:** puedes marcar noticias como leídas y consultar su estado de lectura desde la Web API. [Más información](../integraciones/web-api.es.md)
- **Procesos:** las llamadas de la Web API requieren cambios y respetan los permisos y los datos visibles para cada usuario. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** vuelve a funcionar el guardado y filtrado de flujos y solicitudes; los comentarios coinciden y las solicitudes se resuelven correctamente. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
    - **Ausencias y vacaciones:** se corrigen los cálculos de horas y las solicitudes de cancelación, edición y días no laborables; también vuelven a funcionar las acciones de las listas. [Más información](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)
    - **Empleados y formación:** se corrigen las ediciones de contratos, cursos, inscripciones, documentos para firma, avisos, sugerencias y fotos de empleados.
    - **Fichajes:** se corrigen el registro y la modificación de fichajes, los horarios nocturnos y las zonas horarias, además de varias acciones y vistas de la gestión diaria. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/fichaje-con-zonas-horarias.es.md)
    - **Jornadas:** se corrigen el cálculo de horas y descansos, las incidencias, los festivos, las jornadas sin planificación y la actualización de la jornada tras cambios. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/empleados-sin-planificacion.es.md)
    - **Planificación:** vuelven a funcionar la selección, el arrastre de turnos y el relleno de patrones; cambiar un turno también actualiza su duración. [Más información](../turnos-y-planificacion/metodos-de-planificacion.es.md)
    - **Informes e importaciones:** se corrigen los periodos y fechas de los informes, los filtros de empleados, los calendarios de ausencias y las importaciones desde Excel. [Más información](../informes/catalogo-de-informes.es.md)
    - **Navegación móvil:** los formularios largos, las listas desplegables y el menú lateral vuelven a mostrarse correctamente en móviles y tabletas.
    - **Instalación e integraciones:** se corrigen los archivos de los paquetes de instalación y actualización, y vuelven a funcionar las consultas de licencias y la conexión con AHORA ERP. [Más información](../integraciones/integracion-con-ahora-erp.es.md)
    - **Plataforma y Web API:** se corrigen las traducciones de tipos de solicitud y fichaje, y la respuesta de sugerencias incluye la reacción del usuario. [Más información](../integraciones/web-api.es.md)
