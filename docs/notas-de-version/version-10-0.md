# Versión 10.0

La versión 10.0 amplía la gestión de ausencias y la planificación, y facilita el acceso a la ayuda y a las noticias. También incorpora cambios en fichajes, informes, instalación e integraciones.

## Lo más destacado

### Permisos por horas

Registra permisos por horas y consúltalos en el calendario y el planificador del empleado. No descuentan días del saldo; sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada, y se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: informes de ausencias](../informes/informes-de-ausencias-y-vacaciones.es.md)

### Ayuda desde la aplicación

Consulta la ayuda sin salir del entorno de Sebastian HR: ahora tienes un espacio de ayuda accesible desde la navegación. Así puedes buscar orientación mientras trabajas en la aplicación.

### Noticias según visibilidad

Limita quién puede ver las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para que cada noticia llegue a las personas correspondientes.

### Reservas recurrentes

Crea reservas recurrentes para varios recursos a la vez y elige si se repiten cada cierto número de días, semanas, meses o años. Puedes excluir fines de semana y festivos; si una fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección.

## Otras novedades

### Ausencias y vacaciones

- Al registrar ausencias no planificadas, puedes elegir tipos de jornada parcial.
- Desde los fichajes diarios, registra ausencias aprobadas de día completo para las personas seleccionadas o toda la lista.
- Excluye tipos de ausencia del cómputo de horas teóricas y establece mínimos y máximos de días por solicitud. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- Las solicitudes de cancelación se gestionan según sean de vacaciones o ausencias, incluso si no indican fechas; los tipos se ordenan en listas y menús.

### Fichajes y jornadas

- Ignora o reactiva varios fichajes a la vez desde la lista diaria, y genera informes desde la gestión agrupada mensual o semanal.
- Identifica y filtra los días con cierres automáticos desde la vista agrupada y la gestión diaria. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- El Punto de Acceso muestra el código del empleado aunque esté oculto; la lista NFC incluye a todos los empleados no bloqueados. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)
- El Libro de Registro de Jornada distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- La detección de incidencias de jornada tiene en cuenta más casos, así como las tolerancias y los límites del turno.

### Planificación y turnos

- Los turnos reciben colores por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- En modo LITE, consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Aprobaciones y procesos

- Los tipos de vacaciones y ausencias reciben automáticamente el flujo de aprobación correspondiente. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- La conversación de una instancia se mantiene unificada entre la validación y la revisión. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- Los correos sobre vacaciones y ausencias muestran la fecha y distinguen el tipo en el asunto.

### Informes y gastos

- Crea y consulta partes de gastos con una experiencia mejorada en móviles.

### Instalación y despliegue

- Instala Sebastian HR como una aplicación; se abrirá desde la dirección de inicio configurada.
- Despliega Sebastian HR con Docker y configura las dos bases de datos en una misma instancia. [Más información](../introduccion/requisitos-de-instalacion.es.md)
- Los documentos subidos por los usuarios ya no se incluyen en los paquetes de publicación.
- La aplicación incorpora un modo de mantenimiento.

### Integraciones y WebAPI

- La integración con terminales Kapri/Kimaldi permite gestionar fichajes con identificadores NFC; también se incorpora la integración con Kapri. [Más información](../integraciones/kapri.es.md)
- La WebAPI permite consultar el detalle de instancias y conversaciones, y eliminar justificantes de gastos. [Más información](../integraciones/web-api.es.md)
- La WebAPI permite consultar el total anual de incidencias, adjuntar justificantes a gastos cerrados y crear cursos. [Más información](../integraciones/web-api.es.md)
- La API de ubicaciones incluye el dato `InstancesDisabled` para la aplicación, y la documentación describe mejor procesos, parámetros y vistas. [Más información](../integraciones/web-api.es.md)

### Interfaz y navegación

- Se renuevan la imagen y los estilos de inicio de sesión, y el asistente de configuración adopta los colores de Sebastian HR.
- Los avisos, alertas y cuadros de confirmación y solicitud de datos adoptan un estilo adaptado a Sebastian HR.
- Los procesos muestran el término «Entrada» en el idioma disponible.

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se muestran solo las solicitudes de los tipos elegidos y se completan correctamente las acciones pendientes.
    - **Ausencias:** funcionan correctamente el registro y la cancelación de solicitudes, los fichajes planificados y la gestión de límites, fechas y descansos.
    - **Empleados:** vuelven a mostrarse fotos e indicadores; funcionan las ediciones de contratos, el teletrabajo, los cursos, los documentos y las opciones de QR.
    - **Fichajes:** se corrigen problemas de zona horaria, duplicados, fechas, ubicación y actualización de la pantalla, además de errores al fichar y editar. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/fichaje-con-zonas-horarias.es.md)
    - **Jornadas:** se corrigen los cálculos de horas, descansos y turnos, y vuelven a funcionar la resolución de incidencias y las actualizaciones de la planificación.
    - **Informes e importaciones:** vuelven a funcionar las fechas de los informes, los resúmenes de jornada, los calendarios y los filtros; Excel reconoce las hojas y plantillas de fichajes.
    - **Instalación e integraciones:** se corrigen el inicio y los recursos visuales de Docker, la publicación con SQL Server 2016 y las comprobaciones de conexión y licencia.
    - **Navegación y procesos:** vuelven a funcionar los menús en paneles y móviles, y los formularios, notificaciones e informes respetan su comportamiento esperado.
    - **Planificación y WebAPI:** se corrigen la generación de marcajes desde ausencias, los cambios de turno y la navegación por patrones; las solicitudes simultáneas de ausencia se procesan correctamente.
