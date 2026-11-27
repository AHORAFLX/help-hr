# Versión 10.1

Sebastian HR 10.1 facilita la consulta de vacaciones y permisos, y amplía las notificaciones y las opciones de la WebAPI. También mejora los fichajes, la planificación y los cálculos de jornada y nómina.

## Lo más destacado

### Vacaciones y permisos del equipo

Consulta con el asistente las vacaciones y los permisos de tu equipo y de las personas a tu cargo. Para estas últimas, también puedes ver el motivo y el saldo; para tus compañeros, aparecen las solicitudes aceptadas y pendientes.

[Más información: gestión de vacaciones](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)

## Otras novedades

### Notificaciones

- **Notificaciones push:** la aplicación incorpora avisos push con las personalizaciones necesarias. [Más información](../documentos-y-comunicacion/configuracion-de-notificaciones.es.md)
- **Mensajes:** al leer un mensaje en la aplicación, su notificación también se marca como leída. [Más información](../documentos-y-comunicacion/configuracion-de-notificaciones.es.md)

### Plataforma y acceso

- **Página de mantenimiento:** ofrece temas y juegos de temporada, y permite a los administradores configurar las temporadas.
- **Acceso con QR:** el acceso mediante códigos QR de empleados es más seguro y ya no depende de terminales Kapri.

### Teletrabajo e informes

- **Cumplimiento del teletrabajo:** consulta mediante la WebAPI el cumplimiento de las reglas por empleado y mes. [Más información](../integraciones/web-api.es.md)
- **Resumen anual de jornada:** la WebAPI ofrece los mismos datos que el resumen de Sebastian HR. [Más información](../integraciones/web-api.es.md)

### Opciones de la WebAPI

- **Opciones disponibles:** las aplicaciones pueden consultar mediante la WebAPI qué opciones tienen disponibles. [Más información](../integraciones/web-api.es.md)
- **Documentación:** la guía de la WebAPI describe las ausencias no planificadas y los parámetros de MCP. [Más información](../integraciones/web-api.es.md)

### Accesos e inserción de fichajes

- **Usuarios de puntos de acceso:** la WebAPI permite gestionar usuarios con permisos limitados. [Más información](../integraciones/web-api.es.md)
- **Inserción de fichajes:** al insertar fichajes mediante la WebAPI, el servidor gestiona su cancelación cuando corresponde. [Más información](../integraciones/web-api.es.md)

### Asistencia y fichajes

- **Asistentes de IA:** pueden identificar quién debía fichar y no lo hizo. [Más información](../integraciones/web-api.es.md)
- **Resumen mensual:** el resumen de fichajes señala los días con una salida generada automáticamente.

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se corrigen la actualización de datos, la gestión masiva, la asignación de responsables, los tipos de solicitud y la aprobación de fichajes.
    - **Ausencias:** vuelven a funcionar correctamente los adjuntos, la gestión de ausencias no planificadas, los justificantes, las vacaciones, las compensaciones y el cálculo de derechos.
    - **Empleados y contratos:** se corrigen la fecha de fin de contrato, la visibilidad de empleados y la prioridad aplicada cuando hay contratos empatados.
    - **Fichajes:** se corrigen los avisos, las restricciones de IP y ubicación, las horas extra, los turnos nocturnos, la asignación de turnos y el registro simultáneo.
    - **Importación e integraciones:** la importación desde Excel conserva los registros y lee las fechas correctamente; Kapri y los correos de aprobación gestionan bien identificadores y motivos.
    - **Informes y plataforma:** se corrigen las semanas ISO, la validación de NIE, las traducciones, los periodos largos y la visualización de coordenadas.
    - **Jornadas y horas:** se corrigen los límites semanales, el cálculo de turnos y horas nocturnas, las horas extra, los balances, las bolsas y la validación de días.
    - **Nóminas:** se corrigen la limpieza de datos, los balances y compensaciones, los finiquitos, las horas extra, los embargos, los suplementos y la valoración de horas.
    - **Planificación:** se aplican los descansos elegidos y se reconocen correctamente los días libres, los días especiales y los turnos que cruzan la medianoche.
    - **WebAPI:** se corrigen la consulta de vacaciones de equipos privados y el control anual de incumplimientos de ubicación. [Más información](../integraciones/web-api.es.md)

## Obsoleto

- Se retira el botón «Recalcular precios» de fichajes; la acción ya no está disponible y no se indica una alternativa.
- Se retira del balance el botón «Modificación masiva de horas»; no se indica una alternativa.
