# Versión 10.0

Sebastian HR 10.0 amplía la gestión de ausencias, los fichajes y la planificación, y mejora la detección de incidencias de jornada. También incorpora opciones de despliegue, una aplicación instalable y cambios en la navegación, los informes y las integraciones.

## Lo más destacado

### Permisos por horas

Registra permisos por horas y consúltalos en el calendario y el planificador del empleado. No descuentan días del saldo; sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada, y se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: gestión de vacaciones](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)

### Terminales Kapri/Kimaldi

Integra terminales Kapri/Kimaldi para gestionar fichajes con identificadores NFC. Puedes asociar identificadores a empleados, procesar los eventos de los terminales y configurar opciones relacionadas; también puedes borrar identificadores desde la lista.

[Más información: terminales Kapri](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)

### Ayuda en la aplicación

Consulta la ayuda desde la navegación de Sebastian HR, sin salir del entorno de la aplicación. Así tienes a mano la información que necesitas mientras trabajas.

[Más información: inicio de la ayuda](../index.es.md)

### Noticias según visibilidad

Limita quién puede ver las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para que cada noticia llegue a las personas correspondientes.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Crea reservas recurrentes para varios recursos a la vez y elige si se repiten cada cierto número de días, semanas, meses o años. Puedes excluir fines de semana y festivos; si alguna fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección.

[Más información: cuadrantes de planificación](../turnos-y-planificacion/cuadrantes.es.md)

### Detección de incidencias

La detección de incidencias de jornada tiene en cuenta las tolerancias del turno, las pausas, los descansos y los límites de horas. Los límites semanales, mensuales y anuales se señalan el día en que se superan, y no se avisa de fichajes ausentes cuando no hay horario previsto.

[Más información: incidencias de jornada](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

## Otras novedades

### Ausencias y aprobaciones

- **Límites de solicitud:** establece un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Flujos y cancelaciones:** los tipos de vacaciones y ausencias aplican su flujo de aprobación; las cancelaciones siguen su grupo de tipos y pueden gestionarse aunque no tengan fechas de inicio y fin. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Conversaciones:** la conversación de una instancia se mantiene unificada entre la validación y la revisión. [Más información](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md)

### Fichajes y empleados

- **Gestión agrupada:** puedes ignorar o reactivar varios fichajes desde la lista diaria, y generar informes desde la gestión semanal o mensual. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Cierres automáticos:** la vista agrupada reúne los avisos y permite identificar y filtrar los cierres automáticos de turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Identificadores NFC:** la lista incluye a todos los empleados que no están bloqueados. [Más información](../integraciones/kapri.es.md)
- **Punto de Acceso:** puedes consultar el código de acceso de un empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Turnos y planificación

- **Colores de turno:** los turnos muestran colores asignados por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Informes y gastos

- **Libro de Registro de Jornada:** distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** crea y consulta partes con una experiencia mejorada en dispositivos móviles. [Más información](../informes/catalogo-de-informes.es.md)

### Instalación y despliegue

- **Docker:** despliega Sebastian HR y mantén ambas bases de datos en una misma instancia. [Más información](../introduccion/requisitos-de-instalacion.es.md)
- **Aplicación instalable:** instala Sebastian HR como una aplicación; se abre desde la dirección de inicio configurada.
- **Modo de mantenimiento:** activa un modo que permite mantener la aplicación en mantenimiento.

### Navegación e interfaz

- **Inicio de sesión:** se renuevan la imagen y los estilos de la pantalla, y el asistente de configuración adopta los colores de Sebastian HR. [Más información](../introduccion/configuracion-inicial.es.md)
- **Avisos y ventanas:** los avisos, las alertas y los cuadros de confirmación y solicitud de datos adoptan un estilo adaptado a Sebastian HR.
- **Procesos:** se muestra «Entrada» en el idioma disponible.

### Integraciones y WebAPI

- **Kapri y ERP:** se incorpora una integración con Kapri. [Más información](../integraciones/kapri.es.md)
- **Cursos:** crea cursos mediante nuevas operaciones de la WebAPI. [Más información](../integraciones/web-api.es.md)
- **Documentación de la WebAPI:** consulta descripciones más completas de sus procesos, parámetros y vistas. [Más información](../integraciones/web-api.es.md)

### Comunicaciones

- **Correos de ausencias:** los mensajes de vacaciones y ausencias muestran la fecha y diferencian el tipo en el asunto. [Más información](../documentos-y-comunicacion/configuracion-de-notificaciones.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** las listas respetan los tipos seleccionados y vuelven a funcionar correctamente las instancias, las solicitudes y los procesos con varios validadores.
    - **Ausencias:** se corrigen la eliminación de solicitudes pasadas sin restricciones, las cancelaciones sin días seleccionados y algunas incidencias de descanso en modo LITE.
    - **Empleados:** se recuperan las fotos y los colores de estado, y se corrigen la edición masiva de contratos, el teletrabajo, los cursos, las vigilancias de salud, los documentos y la opción de QR.
    - **Fichajes:** se corrigen la visualización y edición, los duplicados, las incidencias, la ubicación y los fichajes desde la aplicación o durante turnos nocturnos.
    - **Informes e importación:** se corrigen la lectura de plantillas de Excel, las fechas de los informes, el recuento de festivos, los calendarios de ausencias y los filtros de empleados.
    - **Docker:** vuelven a cargarse las imágenes y fuentes, y se corrige el primer inicio para que puedas acceder como administrador.
    - **Integraciones:** se corrigen la consulta de licencia del Canal de Denuncias y la comprobación de conexión con la base de datos del ERP.
    - **Jornadas y planificación:** vuelven a funcionar la resolución de incidencias en lote, el cálculo de descansos y horas trabajadas, los cambios de turno y la navegación por patrones.
    - **Navegación y procesos:** se corrigen los menús en móviles y paneles deslizantes, y los formularios largos y las notificaciones vuelven a funcionar correctamente.
    - **WebAPI:** las solicitudes de ausencia se procesan correctamente aunque se reciban varias a la vez.
