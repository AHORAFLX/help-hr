# Versión 10.0

La versión 10.0 amplía la gestión de ausencias, los fichajes y la planificación, y añade nuevas opciones de integración e instalación. También mejora la detección de incidencias y la experiencia de uso.

## Lo más destacado

### Permisos por horas

Puedes registrar permisos por horas y consultarlos en el calendario y el planificador del empleado. No descuentan días del saldo, pero sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y en el cómputo de jornada, y se tienen en cuenta al gestionar ausencias no planificadas.

### Terminales Kapri/Kimaldi

Integra terminales Kapri/Kimaldi para gestionar fichajes con identificadores NFC. Puedes asociar identificadores a empleados, procesar los eventos de los terminales y configurar opciones de la integración; además, puedes borrar identificadores desde la lista.

[Más información: terminales Kapri](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)

### Ayuda en la aplicación

Ahora puedes consultar la ayuda desde la navegación de Sebastian HR, sin salir del entorno de trabajo. Así tienes a mano la información de uso mientras utilizas la aplicación.

[Más información: página de inicio](../index.es.md)

### Visibilidad de noticias

Puedes limitar quién ve las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso para cada categoría y muestra cada noticia solo a las personas a las que corresponde.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Crea reservas recurrentes para varios recursos a la vez y elige si se repiten cada cierto número de días, semanas, meses o años. Puedes excluir fines de semana y festivos; si una fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección.

### Detección de incidencias

La detección de incidencias de jornada tiene en cuenta las tolerancias del turno, las pausas, los descansos y los límites de horas. Calcula los límites semanales, mensuales y anuales el día en que se superan, y no avisa de fichajes ausentes si ese día no hay horario previsto.

[Más información: incidencias de jornada](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

## Otras novedades

### Ausencias y aprobaciones

- **Límites de solicitud:** establece un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Flujos de aprobación:** cada tipo de vacaciones o ausencia utiliza automáticamente su flujo correspondiente. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Conversaciones:** la conversación de una instancia se mantiene unificada durante la validación y la revisión. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Cancelaciones:** siguen el grupo de tipos correspondiente, cuyos tipos aparecen ordenados; también puedes gestionarlas aunque falten fechas de inicio y fin. [Más información](../ausencias-y-vacaciones/gestion-de-vacaciones.es.md)

### Instalación y despliegue

- **Docker:** despliega Sebastian HR y mantén ambas bases de datos en una misma instancia.
- **Aplicación instalada:** instala Sebastian HR como aplicación y ábrela desde la dirección de inicio configurada.
- **Modo de mantenimiento:** activa un modo de mantenimiento en la aplicación.

### Fichajes e integraciones

- **Gestión diaria:** ignora o reactiva varios fichajes a la vez desde la lista diaria.
- **Informes:** genera informes desde la gestión agrupada mensual o semanal de fichajes. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Vista agrupada:** reúne los avisos e identifica y filtra los cierres automáticos de turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Punto de Acceso:** consulta el código de acceso del empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)
- **Integración con Kapri:** conecta Sebastian HR con Kapri. [Más información](../integraciones/kapri.es.md)

### Informes y gastos

- **Libro de Registro de Jornada:** distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** crea y consulta partes con una experiencia mejorada en dispositivos móviles.

### Jornadas y planificación

- **Colores de turnos:** los turnos muestran colores asignados por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento.

### Interfaz y comunicación

- **Inicio de sesión:** renueva la imagen y los estilos de la pantalla; el asistente de configuración adopta los colores de Sebastian HR.
- **Avisos y diálogos:** adapta a Sebastian HR el estilo de avisos, alertas y cuadros de confirmación o solicitud de datos.
- **Correos de ausencias:** muestran la fecha y distinguen el tipo de ausencia en el asunto.

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** las listas respetan los tipos seleccionados y se corrigen fallos en solicitudes e instancias, incluidos los flujos con varios validadores.
    - **Ausencias:** vuelven a funcionar el borrado de solicitudes pasadas sin restricciones y la cancelación sin días; en LITE se evitan avisos incorrectos de descanso.
    - **Empleados:** se corrigen la edición masiva de contratos, la visualización de fotos y estados, el control de teletrabajo, cursos, vigilancias de salud, documentos y el botón de QR.
    - **Fichajes:** se corrigen fechas, actualizaciones de jornada, duplicados, incidencias en días libres, festivos, ubicación, jornadas de 24 horas, comentarios, turnos nocturnos, zonas horarias y filtros.
    - **Importaciones e informes:** se recupera el reconocimiento de hojas y plantillas de fichajes, y se corrigen fechas, resúmenes de jornada y calendarios y saldos de ausencias.
    - **Instalación e integraciones:** Docker vuelve a cargar imágenes y fuentes, arranca correctamente y permite el acceso de administración; también se corrigen las comprobaciones de licencia y conexión.
    - **Jornadas:** vuelven a funcionar la resolución de incidencias en lote, el redondeo de descansos y el cálculo de horas con descansos computables no fichados.
    - **Navegación y formularios:** se corrigen los menús desplegables en paneles y móviles, el menú lateral y el acceso a los botones de formularios largos en móvil.
    - **Planificación:** al cambiar un turno se actualiza su duración, puedes navegar por patrones sin abrir el planificador desde la unidad organizativa y se muestran las horas previstas durante permisos.
    - **Procesos y API:** se corrigen las notificaciones a empleados sin usuario activo, el envío de sugerencias anónimas y el procesamiento simultáneo de solicitudes de ausencia.
