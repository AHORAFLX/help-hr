# Versión 10.0

La versión 10.0 amplía la gestión de permisos, noticias y reservas, y abre nuevas formas de conectar Sebastian HR con asistentes y aplicaciones. También renueva la plataforma y mejora la gestión diaria de ausencias, fichajes, jornadas e informes.

## Lo más destacado

### Permisos por horas

Ahora puedes configurar cada tipo de permiso para que se solicite por días, por horas o de ambas formas. Las horas no descuentan días de permiso; además, las horas retribuidas y no retribuidas aparecen en la exportación de nómina y cuentan para calcular la jornada.

[Más información: restricciones de ausencias](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Ayuda dentro de la aplicación

Puedes abrir la guía desde el botón de ayuda de la barra superior y consultarla sin salir de Sebastian HR. El contenido se adapta a tu perfil: verás la información dirigida a empleados o la destinada a RR. HH. y responsables.

[Más información: guía de ayuda](../index.es.md)

### Visibilidad de las noticias

Puedes decidir quién ve las noticias de cada categoría según su área, empresa, oficina, equipo o persona. Las categorías sin reglas siguen siendo visibles para todo el mundo; si una categoría tiene reglas, solo verá sus noticias quien cumpla al menos una.

### Reservas repetidas de recursos

Puedes reservar varios recursos a la vez y repetir las reservas por días, semanas, meses o años. En las repeticiones mensuales y anuales eliges una fecha o una posición, como el último viernes, y puedes excluir fines de semana y festivos; si hay conflictos, consulta las fechas y corrígelas sin rehacer el formulario.

### Asistentes de IA y Web API

Conecta Sebastian HR con asistentes compatibles con MCP para consultar datos y realizar gestiones con tus propias palabras, según los permisos de tu perfil. Un administrador activa el acceso y elige quién puede usarlo; también puedes conectar la app móvil y otras aplicaciones mediante la nueva Web API.

[Más información: Web API](../integraciones/web-api.es.md)

### Actualización de la plataforma

Sebastian HR funciona ahora sobre Flexygo 10. Entre otros cambios, se renuevan los calendarios anuales de vacaciones y ausencias, y se incorpora la posibilidad de conectar asistentes de IA mediante MCP.

## Otras novedades

### Ausencias y vacaciones

- **Ausencias no planificadas:** registra directamente a los empleados de la lista con el tipo de ausencia que elijas.
- **Horas teóricas:** excluye del cómputo las ausencias no remuneradas de los tipos que selecciones.
- **Duración de solicitudes:** establece un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Correos de solicitudes:** los avisos de vacaciones y ausencias incluyen las fechas solicitadas y el tipo de solicitud.

### Fichajes y control horario

- **Descansos fichados:** una nueva incidencia avisa si superan los descansos previstos en el turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)
- **Gestión diaria:** ignora o reactiva varios fichajes a la vez, e identifica y filtra los días con fin de turno automático.
- **Terminales Kapri:** permite fichar con tarjeta NFC o código QR mediante terminales Kapri de Kimaldi. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Punto de acceso:** muestra el código que estás escribiendo aunque esté configurado como oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes de jornada

- **Informes de fichajes:** genera informes desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-control-horario.es.md)
- **Libro de Registro de Jornada:** incluye el detalle diario de ausencias y permisos y un resumen por tipo. [Más información](../informes/informes-de-control-horario.es.md)

### Solicitudes y gastos

- **Flujos de aprobación:** los grupos de tipos de ausencia que no tengan uno reciben un flujo predeterminado al instalar o actualizar. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Partes de gastos en el móvil:** añade líneas desde un formulario y adjunta sus justificantes.

### Jornadas y planificación

- **Incidencias de jornada:** las alertas por retrasos, salidas anticipadas y límites de turno respetan las tolerancias; las incidencias de descanso aparecen antes de validar.
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Acceso y plataforma

- **Modo de mantenimiento:** los administradores pueden activarlo desde el menú superior.
- **Aplicación instalable:** instala Sebastian HR en el ordenador o el móvil desde el navegador.
- **Inicio de sesión:** la pantalla tiene un diseño renovado.
- **Avisos y cuadros:** las alertas, confirmaciones y peticiones de datos tienen un diseño nuevo, con color e icono según su tipo.
- **Web API:** cambia la forma de llamar a sus procesos y se ajustan el acceso a los datos y las acciones disponibles. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se guardan los flujos de todos los tipos de solicitud; los comentarios y filtros coinciden entre vistas, y las solicitudes se resuelven correctamente al aceptar o denegar. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
    - **Ausencias y vacaciones:** vuelven a funcionar los descuentos de horas, las solicitudes y cancelaciones, la edición de días pasados y las acciones de las listas; se evitan solicitudes vacías o inválidas.
    - **Empleados:** se corrigen la edición masiva de contratos, los cursos, las inscripciones, la firma de documentos, las notificaciones, las sugerencias y la foto de la ficha.
    - **Fichajes:** se corrigen las zonas horarias, la actualización tras fichar, las solicitudes y modificaciones, la planificación y los controles para registrar entradas y salidas.
    - **Jornadas:** se corrigen el cálculo y la validación de jornadas, turnos, festivos, descansos, fichajes en días libres y empleados sin planificación.
    - **Planificación:** vuelven a funcionar los patrones y la selección múltiple; se actualizan las duraciones de los turnos y se corrigen los datos de la planificación semanal.
    - **Informes, importación e instalación:** se corrigen las fechas, los filtros y los resultados de informes, las importaciones desde Excel y el contenido de los paquetes de instalación y actualización.
    - **Navegación y traducciones:** se corrigen los botones, formularios y menús en móviles, y las traducciones de tipos de solicitud y fichaje.
    - **Integraciones y Web API:** vuelven a funcionar la consulta de licencias y la conexión con AHORA ERP; las sugerencias incluyen la reacción del usuario actual.
