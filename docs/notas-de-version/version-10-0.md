# Versión 10.0

La versión 10.0 amplía la gestión de ausencias, la planificación y la integración con otros sistemas. También incorpora mejoras en fichajes, informes, instalación y navegación, junto con correcciones en distintos procesos.

## Lo más destacado

### Permisos por horas

Ahora puedes registrar permisos por horas y consultarlos en el calendario y en el planificador del empleado. No descuentan días del saldo; sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y en el cómputo de jornada, y se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: gestión de vacaciones](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)

### Ayuda en la aplicación

Puedes consultar la ayuda desde el propio entorno de Sebastian HR, sin salir de la aplicación. Así tienes a mano la información que necesitas mientras trabajas. El nuevo espacio de ayuda está disponible desde la navegación.

[Más información: ayuda de Sebastian HR](../index.es.md)

### Visibilidad de noticias

Puedes limitar quién ve las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para que cada noticia llegue a las personas correspondientes.

### Reservas recurrentes

Puedes crear reservas recurrentes para varios recursos a la vez y elegir que se repitan cada cierto número de días, semanas, meses o años. También puedes excluir fines de semana y festivos. Si una fecha está ocupada, no se crea ninguna reserva, para que puedas corregir la selección y volver a intentarlo.

[Más información: planificación de turnos](../turnos-y-planificacion/cuadrantes.es.md)

## Otras novedades

### Ausencias y vacaciones

- **Ausencias no planificadas:** puedes insertar también tipos de jornada parcial.
- **Registro desde fichajes:** puedes registrar ausencias aprobadas de día completo para las personas seleccionadas o para toda la lista.
- **Cómputo de horas:** puedes excluir determinados tipos de ausencia de las theoretical hours calculation.
- **Límites de solicitud:** puedes definir un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Fichajes y jornadas

- **Gestión diaria:** puedes ignorar o reactivar varios fichajes a la vez y generar informes desde la gestión agrupada semanal o mensual. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Terminales Kapri/Kimaldi:** puedes gestionar fichajes con identificadores NFC. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Cierres automáticos:** puedes identificar y filtrar los días con cierres automáticos en las vistas agrupada y diaria. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Punto de Acceso:** puedes consultar el código de acceso del empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Turnos y planificación

- **Tipos de patrón:** en modo LITE, puedes consultarlos desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)
- **Turnos:** ahora tienen colores asignados por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Incidencias de jornada:** se detectan más casos y se tienen en cuenta las tolerancias y los límites del turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

### Informes

- **Libro de Registro de Jornada:** distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** puedes crearlos y consultarlos con una experiencia mejorada en dispositivos móviles.

### Empleados y procesos

- **Lista NFC:** muestra a todos los empleados que no están bloqueados.
- **Vacaciones y ausencias:** los tipos reciben automáticamente su flujo de aprobación y las solicitudes de cancelación se encaminan según corresponda. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Cancelaciones de vacaciones:** puedes gestionar solicitudes aunque no indiquen fechas de inicio y fin.
- **Correos de vacaciones y ausencias:** muestran la fecha y distinguen el tipo en el asunto.

### Instalación y despliegue

- **Docker:** puedes desplegar Sebastian HR y configurar ambas bases de datos en una misma instancia. [Más información](../introduccion/requisitos-de-instalacion.es.md)
- **Aplicación instalada:** puedes instalar Sebastian HR como una aplicación y abrirla desde la dirección de inicio configurada.
- **Paquetes de publicación:** los documentos subidos por los usuarios ya no se incluyen.

### Navegación e interfaz

- **Modo de mantenimiento:** la aplicación incorpora un modo para realizar tareas de mantenimiento.
- **Inicio de sesión:** se renuevan la imagen y los estilos, y el asistente de configuración adopta los colores de Sebastian HR.
- **Avisos y confirmaciones:** los avisos, alertas y cuadros para confirmar o solicitar datos tienen un estilo adaptado a Sebastian HR.

### Integraciones y WebAPI

- **Kapri:** se incorpora una integración con Kapri. [Más información](../integraciones/kapri.es.md)
- **WebAPI y MCP:** los asistentes de IA pueden ejecutar procesos de la WebAPI, incluso cuando tienen parámetros opcionales. [Más información](../integraciones/web-api.es.md)
- **Empresas e instancias:** la WebAPI incorpora operaciones para gestionar empresas, eliminar instancias y consultar sus detalles y conversaciones. [Más información](../integraciones/web-api.es.md)
- **Solicitudes, noticias y gastos:** puedes consultar solicitudes denegadas, crear noticias y eliminar justificantes de gastos mediante la WebAPI. [Más información](../integraciones/web-api.es.md)
- **Incidencias, gastos y cursos:** puedes consultar incidencias anuales, adjuntar justificantes a gastos cerrados y crear cursos mediante la WebAPI. [Más información](../integraciones/web-api.es.md)
- **Información de la WebAPI:** puedes consultar descripciones más completas de procesos, parámetros y vistas. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se muestran las solicitudes de los tipos seleccionados y se completan correctamente las acciones y los pasos pendientes. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
    - **Ausencias:** vuelven a funcionar correctamente los formularios, las cancelaciones, la inserción de fichajes planificados y la gestión de solicitudes y días pasados.
    - **Empleados:** se corrigen la edición de contratos, las fotografías, los indicadores, el control de teletrabajo, los cursos, los documentos y las opciones de QR.
    - **Fichajes:** se corrigen el registro y la edición, las zonas horarias, la actualización de la pantalla, los duplicados y los errores de selección y cálculo. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/fichaje-con-zonas-horarias.es.md)
    - **Informes e importación:** vuelven a funcionar las plantillas de Excel y se corrigen las fechas, los resúmenes de jornada y los informes de ausencias y vacaciones. [Más información](../informes/catalogo-de-informes.es.md)
    - **Instalación e integraciones:** se corrigen el inicio y los recursos visuales de Docker, la publicación con SQL Server 2016 y las comprobaciones de conexión y licencia.
    - **Jornadas:** se corrigen los recálculos, la resolución en lote de incidencias, los descansos y la detección de fichajes pendientes.
    - **Navegación y procesos:** los menús funcionan en paneles y móviles, y se corrigen formularios, notificaciones y procesos de vacaciones, compensaciones e informes.
    - **Planificación y WebAPI:** se corrigen la creación de marcajes, los cambios de turno, la navegación por patrones y el procesamiento simultáneo de solicitudes de ausencia.
