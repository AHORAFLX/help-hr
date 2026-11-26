# Versión 10.1

Sebastian HR 10.1 facilita la consulta de vacaciones y permisos del equipo y amplía las opciones de la WebAPI. También incorpora ajustes en la página de mantenimiento y mejora el seguimiento de fichajes y notificaciones.

## Lo más destacado

### Vacaciones y permisos del equipo

Consulta con el asistente las vacaciones y los permisos de tu equipo y de las personas a tu cargo. Para estas últimas, también puedes ver el motivo y el saldo; para tus compañeros de equipo, puedes consultar las solicitudes aceptadas o pendientes.

[Más información: gestión de vacaciones](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)

## Otras novedades

### Plataforma y acceso

- **Página de mantenimiento:** incluye temas y juegos estacionales; los administradores pueden configurar las temporadas.
- **Acceso con QR:** el acceso mediante códigos QR de empleados es más seguro y ya no depende de terminales Kapri.

### Fichajes y notificaciones

- **Resumen mensual:** el indicador «A» señala los días con una salida generada automáticamente.
- **Noticias:** al leer un mensaje en la aplicación, su notificación también queda marcada como leída.

### WebAPI: consultas

- **Teletrabajo:** consulta el cumplimiento de las reglas por empleado y mes. [Más información](../integraciones/web-api.es.md)
- **Resumen anual de jornada:** ofrece los mismos datos que el resumen de Sebastian HR. [Más información](../integraciones/web-api.es.md)

### WebAPI: aplicaciones y usuarios

- **Opciones disponibles:** las aplicaciones pueden consultar qué opciones tienen disponibles. [Más información](../integraciones/web-api.es.md)
- **Usuarios de puntos de acceso:** gestiona usuarios con permisos limitados. [Más información](../integraciones/web-api.es.md)

### WebAPI: fichajes y asistentes

- **Fichajes pendientes:** los asistentes de IA pueden identificar quién debía fichar y no lo hizo. [Más información](../integraciones/web-api.es.md)
- **Inserción de fichajes:** el servidor gestiona la cancelación cuando corresponde. [Más información](../integraciones/web-api.es.md)
- **Documentación:** describe las ausencias no planificadas y los parámetros de MCP. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se corrigen la actualización parcial de datos, la gestión masiva, la asignación de responsables y la aprobación de solicitudes.
    - **Ausencias y vacaciones:** se corrigen los permisos de gestión, los adjuntos, la aprobación con justificantes, los saldos y el cálculo de derechos y compensaciones.
    - **Empleados y contratos:** se conservan las fechas de fin, se muestran los empleados según los permisos y se prioriza el contrato más antiguo en caso de empate.
    - **Fichajes:** se corrigen las restricciones por IP y ubicación, las horas nocturnas y extra, la asignación de turnos, las cargas y el registro simultáneo.
    - **Importaciones e integraciones:** se conservan los registros ignorados en Excel y se gestionan correctamente las fechas, identificadores y motivos con comillas.
    - **Jornadas y horas:** se corrigen los cálculos con varios contratos, los límites semanales, los balances, las bolsas y las horas planificadas.
    - **Planificación y turnos:** se aplican los descansos elegidos y se reconocen los días libres y especiales, también en turnos que cruzan la medianoche.
    - **Nóminas:** se corrigen los balances, las compensaciones, los finiquitos, las horas extra, los embargos y los suplementos.
    - **Informes y plataforma:** se muestran correctamente las semanas ISO y los NIE, vuelven a funcionar las traducciones y se corrigen los periodos y las coordenadas.
    - **WebAPI:** se corrigen la visibilidad de vacaciones de equipos privados y la consulta del control anual de incumplimientos de ubicación.

## Obsoleto

- **Recalcular precios:** se retira el botón porque la acción ya no estaba disponible; no se indica una alternativa.
- **Modificación masiva de horas:** se retira el botón del balance; no se indica una alternativa.
