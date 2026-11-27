# Versión 10.1

Sebastian HR 10.1 facilita la consulta de ausencias del equipo y amplía las opciones de la WebAPI y las notificaciones. También mejora el control horario, la gestión de jornadas y nóminas, y corrige incidencias en distintas áreas.

## Lo más destacado

### Ausencias del equipo

Consulta con el asistente las vacaciones y los permisos de tu equipo y de las personas a tu cargo. Para estas últimas, puedes ver el motivo y el saldo; para tus compañeros de equipo, las solicitudes aceptadas o pendientes.

[Más información: gestión de vacaciones](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)

## Otras novedades

### Ausencias y control horario

- **Procesos de ausencias:** limita los procesos no planificados a los gestores y a los empleados seleccionados que pueden verlos.
- **Resumen mensual:** identifica los días en que la salida se ha generado automáticamente.

### Acceso y plataforma

- **Acceso con QR:** los códigos QR de empleados ofrecen un acceso más seguro y ya no dependen de terminales Kapri. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Usuarios de puntos de acceso:** la WebAPI permite gestionarlos con permisos limitados. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Notificaciones y plataforma

- **Notificaciones push:** la aplicación incorpora notificaciones push con las personalizaciones necesarias. [Más información](../documentos-y-comunicacion/configuracion-de-notificaciones.es.md)
- **Temas estacionales:** la página de mantenimiento ofrece temas y juegos de temporada, que los administradores pueden configurar.
- **Noticias:** al leer un mensaje en la aplicación, su notificación también se marca como leída.

### WebAPI: consultas

- **Teletrabajo:** consulta mediante la WebAPI el cumplimiento de las reglas por empleado y mes. [Más información](../integraciones/web-api.es.md)
- **Opciones disponibles:** las aplicaciones pueden consultar qué opciones están disponibles mediante la WebAPI. [Más información](../integraciones/web-api.es.md)
- **Resumen anual de jornada:** la WebAPI ofrece los mismos datos que el resumen de Sebastian HR. [Más información](../integraciones/web-api.es.md)

### WebAPI: gestión

- **Fichajes:** al insertarlos mediante la WebAPI, el servidor gestiona su cancelación cuando corresponde. [Más información](../integraciones/web-api.es.md)
- **Documentación:** explica las ausencias no planificadas y los parámetros de MCP. [Más información](../integraciones/web-api.es.md)

### Asistentes y automatización

- **Asistentes de IA:** pueden identificar quién debía fichar y no lo hizo. [Más información](../integraciones/web-api.es.md)
- **Cancelación de fichajes:** al añadir fichajes mediante la WebAPI, se gestiona automáticamente su cancelación cuando corresponde. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** las solicitudes se asignan y validan correctamente; la gestión masiva respeta tus permisos y solo actualiza los datos solicitados.
    - **Ausencias y vacaciones:** vuelven a funcionar correctamente los justificantes, los borrados, los permisos, las compensaciones y el cálculo del derecho anual.
    - **Empleados y contratos:** la edición conserva las fechas de fin, mantiene correctamente el estado del empleado y muestra los empleados según los permisos de acceso.
    - **Fichajes:** vuelven a funcionar correctamente el redondeo, las restricciones, la asignación de turnos, el registro simultáneo y los cálculos de horas.
    - **Importaciones e integraciones:** la importación desde Excel conserva los registros e interpreta las fechas correctamente; también se gestionan bien identificadores y motivos con comillas.
    - **Informes y plataforma:** vuelven a mostrarse correctamente las semanas ISO, los NIE y los textos traducidos; las listas de días y las coordenadas ya no provocan errores.
    - **Jornadas:** se corrigen los cálculos de límites, turnos nocturnos, horas extra, descansos y saldos, así como la validación y el recálculo de jornadas.
    - **Nóminas:** vuelven a funcionar la limpieza de datos, los balances, los finiquitos, las horas extra, los embargos y los suplementos.
    - **Planificación:** se aplican correctamente los descansos elegidos y se reconocen los días libres y especiales, incluso en turnos que cruzan la medianoche.
    - **WebAPI:** el asistente respeta la privacidad de los equipos y vuelve a funcionar la consulta del control anual de incumplimientos de ubicación.

## Obsoleto

- **Recalcular precios:** se retira el botón porque la acción ya no estaba disponible; no se indica una alternativa.
- **Modificación masiva de horas:** se retira el botón del balance; no se indica una alternativa.
