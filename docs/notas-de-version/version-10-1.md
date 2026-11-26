# Versión 10.1

Sebastian HR 10.1 facilita la consulta de las vacaciones y los permisos del equipo, y amplía las notificaciones y las opciones de la WebAPI. También incorpora ajustes en la plataforma y corrige aspectos de fichajes, jornadas, ausencias y nóminas.

## Lo más destacado

### Vacaciones y permisos del equipo

Consulta con el asistente las vacaciones y los permisos de las personas a tu cargo y de tu equipo. Para las personas a tu cargo, puedes ver el motivo y el saldo; para tus compañeros, las solicitudes aceptadas y pendientes.

[Más información: gestión de vacaciones](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)

## Otras novedades

### Notificaciones y plataforma

- **Notificaciones push:** la aplicación incorpora notificaciones push con las personalizaciones necesarias. [Más información](../documentos-y-comunicacion/configuracion-de-notificaciones.es.md)
- **Mensajes:** al leer un mensaje en la aplicación, su notificación también queda marcada como leída.
- **Página de mantenimiento:** ofrece temas y juegos estacionales, y permite a los administradores configurar las temporadas.

### Fichajes y acceso

- **Resumen mensual:** identifica con el indicador «A» los días en que la salida se ha generado automáticamente. [Más información](../informes/informes-de-control-horario.es.md)
- **Acceso con QR:** el acceso mediante códigos QR de empleados es más seguro y ya no depende de terminales Kapri.

### WebAPI: consultas y datos

- **Teletrabajo:** consulta el cumplimiento de las reglas por empleado y mes. [Más información](../integraciones/web-api.es.md)
- **Resumen anual de jornada:** ofrece los mismos datos que el resumen de Sebastian HR. [Más información](../integraciones/web-api.es.md)

### WebAPI: opciones y accesos

- **Opciones disponibles:** las aplicaciones pueden consultar qué opciones están disponibles. [Más información](../integraciones/web-api.es.md)
- **Usuarios de puntos de acceso:** gestiona mediante la WebAPI usuarios con permisos limitados. [Más información](../integraciones/web-api.es.md)
- **Documentación:** describe las ausencias no planificadas y los parámetros de MCP. [Más información](../integraciones/web-api.es.md)

### WebAPI y asistentes de IA

- **Fichajes pendientes:** los asistentes de IA pueden identificar quién debía fichar y no lo hizo. [Más información](../integraciones/web-api.es.md)
- **Inserción de fichajes:** la WebAPI gestiona su cancelación cuando corresponde. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se corrigen la actualización de datos solicitados, la gestión masiva, la asignación de responsables y la aprobación de solicitudes y cambios de fichaje.
    - **Ausencias:** se corrigen la eliminación de adjuntos, los procesos no planificados, la aprobación con justificantes, las vacaciones, las compensaciones y el cálculo del derecho anual.
    - **Empleados y contratos:** se conservan las fechas de fin, la visibilidad de empleados y la prioridad del contrato más antiguo en caso de empate.
    - **Fichajes:** se corrigen las restricciones por IP y ubicación, las horas extra, los turnos nocturnos, la asignación de turnos y jornada, y la carga masiva y simultánea.
    - **Jornadas y balances:** se corrigen los límites semanales, los cálculos con varios contratos, las horas extra y nocturnas, el standby, las solicitudes pendientes y las bolsas de horas.
    - **Nóminas:** se corrigen la limpieza de datos, los balances y compensaciones, los finiquitos, las horas extra, los embargos, los suplementos y la valoración de ausencias.
    - **Planificación:** se aplican los descansos elegidos y se reconocen correctamente los días libres, especiales y los turnos y reglas que cruzan la medianoche.
    - **Importaciones e informes:** se conservan los registros ignorados y se interpretan bien las fechas ISO; también se corrigen las semanas de fin de año y la validación de NIE.
    - **Plataforma e integraciones:** se corrigen textos traducidos, listas de días, coordenadas, identificadores y motivos con comillas, y consultas de la WebAPI.

## Obsoleto

- Se retira el botón «Recalcular precios» de fichajes; la acción ya no estaba disponible.
- Se retira del balance el botón «Modificación masiva de horas».
