# Versión 10.1

Sebastian HR 10.1 facilita la consulta de vacaciones y permisos del equipo y amplía las opciones de notificación y acceso. También incorpora nuevas consultas y gestiones en la WebAPI, y corrige aspectos del control horario, las jornadas y las nóminas.

## Lo más destacado

### Vacaciones y permisos del equipo

Pregunta al asistente por las vacaciones y los permisos de tu equipo y de las personas a tu cargo. Para estas últimas, consulta también el motivo y el saldo; para tus compañeros, verás las solicitudes aceptadas y las que siguen pendientes.

[Más información: gestión de vacaciones](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)

## Otras novedades

### Ausencias y fichajes

- **Ausencias no planificadas:** los procesos quedan limitados a los gestores y a los empleados seleccionados que tienen permiso para verlos. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Resumen mensual:** identifica los días en los que se generó automáticamente una hora de salida. [Más información](../informes/informes-de-control-horario.es.md)

### Notificaciones y mensajes

- **Notificaciones push:** la aplicación incorpora notificaciones push con las personalizaciones necesarias. [Más información](../documentos-y-comunicacion/configuracion-de-notificaciones.es.md)
- **Noticias:** al leer un mensaje en la aplicación, su notificación también queda marcada como leída.

### Plataforma y acceso

- **Página de mantenimiento:** ofrece temas y juegos estacionales, y permite a los administradores configurar las temporadas.
- **Acceso con códigos QR:** el acceso mediante códigos QR de empleados es más seguro y ya no depende de terminales Kapri. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### WebAPI: cumplimiento y asistencia

- **Teletrabajo:** consulta mediante la WebAPI el cumplimiento de las reglas por empleado y mes. [Más información](../integraciones/web-api.es.md)
- **Asistentes de IA:** pueden identificar quién debía fichar y no lo hizo. [Más información](../integraciones/web-api.es.md)

### WebAPI: opciones y usuarios

- **Opciones disponibles:** las aplicaciones pueden consultar mediante la WebAPI qué opciones tienen disponibles. [Más información](../integraciones/web-api.es.md)
- **Usuarios de puntos de acceso:** gestiona mediante la WebAPI usuarios con permisos limitados. [Más información](../integraciones/web-api.es.md)

### WebAPI: jornada y documentación

- **Resumen anual de jornada:** ofrece los mismos datos que el resumen de Sebastian HR. [Más información](../integraciones/web-api.es.md)
- **Inserción de fichajes:** al insertar fichajes mediante la WebAPI, el servidor gestiona su cancelación cuando corresponde. [Más información](../integraciones/web-api.es.md)
- **Documentación:** describe las ausencias no planificadas y los parámetros de MCP. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se corrigen la actualización de datos personales, la gestión masiva, la asignación de responsables y la aprobación de solicitudes y cambios de fichaje.
    - **Ausencias:** vuelven a funcionar correctamente los adjuntos, los permisos de borrado, las compensaciones de horas y los cálculos de vacaciones.
    - **Contratos y empleados:** se conservan las fechas de fin, se mantiene correctamente el estado del empleado y vuelve a funcionar la visibilidad según los permisos.
    - **Fichajes:** se corrigen el redondeo, los turnos, las horas nocturnas y extra, la localización, los bloqueos, las cargas y los cambios de jornada; también vuelven a funcionar las importaciones y las integraciones.
    - **Jornadas y horas:** vuelven a calcularse correctamente los límites, las horas extra, los días de standby y los balances; también se corrigen los traspasos y las bolsas de horas.
    - **Nóminas:** se corrigen la limpieza de datos, los balances, los finiquitos, el cálculo de horas, los embargos, los suplementos y la valoración de ausencias.
    - **Planificación:** vuelven a aplicarse correctamente los descansos, los días libres y especiales, los días de la semana y los turnos que cruzan la medianoche.
    - **Documentos, informes y plataforma:** se corrigen la eliminación de recibos, las semanas ISO, la validación de NIE, las traducciones, las listas de días y la visualización de coordenadas.
    - **WebAPI:** vuelven a respetarse la privacidad de los equipos y la consulta anual de incumplimientos de ubicación en SQL Server 2016. [Más información](../integraciones/web-api.es.md)

## Obsoleto

- Se retira el botón «Recalcular precios», porque la acción ya no estaba disponible; no se indica una alternativa.
- Se retira del balance el botón «Modificación masiva de horas»; no se indica una alternativa.
