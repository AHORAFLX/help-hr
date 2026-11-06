# Versión 10.0

Sebastian HR 10.0 amplía la gestión de ausencias y la planificación, y mejora el control de jornada. También incorpora cambios en la navegación, la instalación y las integraciones.

## Lo más destacado

### Permisos por horas

Registra permisos por horas y consúltalos en el calendario y en el planificador del empleado. No descuentan días del saldo: las horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada, y se tienen en cuenta al gestionar ausencias no planificadas.

[Más información: informes de ausencias](../informes/informes-de-ausencias-y-vacaciones.es.md)

### Ayuda desde la aplicación

Consulta la ayuda desde el propio entorno de Sebastian HR, sin salir de la aplicación. Así tienes a mano la información de apoyo mientras trabajas.

### Noticias para cada público

Limita quién puede ver las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para mostrar las noticias a las personas que corresponden.

### Reservas recurrentes

Crea reservas repetidas para varios recursos a la vez, con una frecuencia en días, semanas, meses o años. Puedes excluir fines de semana y festivos; si alguna fecha ya está ocupada, no se crea ninguna reserva y puedes corregir la selección.

### Incidencias de jornada más precisas

La detección de incidencias tiene en cuenta las tolerancias del turno, las pausas, los descansos y los límites de horas. También evita avisos por falta de fichajes cuando no hay horario previsto, y señala los límites semanales, mensuales o anuales el día en que se superan.

[Más información: incidencias de jornada](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

## Otras novedades

### Ausencias y aprobaciones

- **Límites de solicitud:** establece un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Flujos y cancelaciones:** asigna automáticamente flujos de aprobación a los tipos de ausencia y gestiona cancelaciones según el grupo, incluso sin fechas de inicio y fin. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Conversaciones:** mantiene unificada la conversación de una solicitud durante su validación y revisión. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)

### Fichajes y acceso

- **Gestión de fichajes:** ignora o reactiva varios fichajes desde la lista diaria sin alterar el cálculo de ubicación del día. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/casos-de-uso-de-fichajes.es.md)
- **Fichajes automáticos:** muestra y filtra en la vista agrupada los días con fin de turno automático y los fichajes de salida que genera. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Terminales y NFC:** gestiona fichajes NFC con terminales Kapri/Kimaldi y consulta en la lista NFC a todos los empleados que no están bloqueados. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Punto de Acceso:** consulta el código de acceso del empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes y gastos

- **Informes de fichajes:** genera informes desde la gestión agrupada mensual o semanal de fichajes. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Libro de Registro de Jornada:** distingue las ausencias por tipo, muestra sus colores y añade un resumen. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** crea y consulta partes con una experiencia mejorada en móviles.

### Instalación y despliegue

- **Docker:** despliega Sebastian HR y mantiene sus dos bases de datos en una misma instancia. [Más información](../introduccion/requisitos-de-instalacion.es.md)
- **Aplicación instalada:** instala Sebastian HR como una aplicación y ábrela desde la dirección de inicio configurada.
- **Modo de mantenimiento:** activa un modo de mantenimiento en la aplicación.

### Integraciones y WebAPI

- **Kapri:** conecta Sebastian HR con Kapri. [Más información](../integraciones/kapri.es.md)
- **Cursos por WebAPI:** crea cursos mediante nuevas operaciones de la WebAPI. [Más información](../integraciones/web-api.es.md)
- **Documentación de WebAPI:** consulta descripciones más completas de los procesos, parámetros y vistas. [Más información](../integraciones/web-api.es.md)

### Interfaz y navegación

- **Inicio de sesión:** renueva la imagen y los estilos de la pantalla y adapta el asistente de configuración a los colores de Sebastian HR.
- **Avisos y cuadros:** adapta a Sebastian HR el estilo de los avisos, las alertas y los cuadros de confirmación y solicitud de datos.
- **Procesos:** muestra el término «Entrada» en el idioma disponible.

### Turnos y planificación

- **Colores de turnos:** muestra los turnos con colores asignados por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** conserva el validador configurado, filtra las solicitudes por tipo y completa correctamente las acciones y los pasos pendientes.
    - **Ausencias:** permite borrar ausencias pasadas sin restricciones, evita avisos de cancelación imposibles de gestionar y corrige incidencias de descanso en LITE.
    - **Empleados:** corrige la edición masiva de contratos, la foto, las excepciones de teletrabajo, los indicadores, los cursos, las vigilancias de salud, los documentos y la opción de QR.
    - **Fichajes:** corrige la actualización tras fichar, las fechas, las inserciones, los duplicados, los días libres, festivos, ubicación, turnos nocturnos, zonas horarias, filtros y jornadas de 24 horas.
    - **Importaciones e informes:** reconoce las hojas y plantillas de fichajes, muestra bien los periodos y ausencias, y corrige los informes de jornada y saldo de vacaciones.
    - **Instalación e integraciones:** restaura imágenes en Docker, corrige el primer inicio y el acceso de administrador, y repara las comprobaciones de licencia y conexión.
    - **Jornadas:** permite resolver incidencias en lote y corrige el redondeo de descansos y el cómputo de descansos computables no fichados.
    - **Planificación:** actualiza la duración al cambiar un turno, permite navegar por patrones y muestra las horas previstas durante un permiso.
    - **Navegación:** corrige los menús desplegables en paneles deslizantes y dispositivos móviles, y mantiene accesible el menú lateral.
    - **Procesos y WebAPI:** mantiene accesibles los botones en formularios largos, permite notificar a empleados sin usuario activo, corrige sugerencias anónimas y procesa solicitudes de ausencia simultáneas.
