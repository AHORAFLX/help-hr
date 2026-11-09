# Versión 10.0

Sebastian HR 10.0 amplía las opciones para gestionar ausencias, planificar recursos y controlar jornadas. También incorpora cambios en la navegación, el despliegue y las integraciones, además de mejoras en informes y aprobaciones.

## Lo más destacado

### Permisos por horas

Registra permisos por horas y consúltalos en el calendario y el planificador del empleado. No descuentan días del saldo, pero sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada, y cuentan al gestionar ausencias no planificadas.

### Ayuda desde la aplicación

Consulta la ayuda desde el propio entorno de Sebastian HR, sin salir de la aplicación. Así tienes a mano la información de apoyo mientras trabajas.

### Noticias según su ámbito

Limita quién puede ver las noticias por área, empresa, empleado, oficina o equipo. Configura la visibilidad en cada categoría para que cada noticia llegue a las personas correspondientes.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Crea reservas para varios recursos a la vez y repítelas cada cierto número de días, semanas, meses o años. Puedes excluir fines de semana y festivos; si alguna fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección.

### Detección de incidencias

La detección de incidencias tiene en cuenta las tolerancias del turno, las pausas, los descansos y los límites de horas. Calcula los límites en el día en que se superan y evita avisos por falta de fichajes cuando no hay horario previsto.

[Más información: incidencias de jornada](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

## Otras novedades

### Instalación y despliegue

- **Docker:** puedes desplegar Sebastian HR y configurar las dos bases de datos en una misma instancia.
- **Aplicación instalada:** instala Sebastian HR como aplicación y ábrela desde la dirección de inicio configurada.
- **Paquetes publicados:** los documentos que subas a la aplicación ya no se incluyen en los paquetes.
- **Modo de mantenimiento:** la aplicación incorpora un modo de mantenimiento.

### Ausencias y aprobaciones

- **Duración de solicitudes:** establece un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)
- **Flujos de aprobación:** los tipos de vacaciones y ausencias reciben automáticamente su flujo de aprobación correspondiente. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Conversaciones:** la conversación de una instancia se mantiene unificada entre la validación y la revisión.
- **Cancelaciones:** se ordenan los tipos de vacaciones y ausencias por grupo, y puedes gestionar cancelaciones aunque no tengan fechas de inicio y fin.
- **Correos:** los mensajes sobre vacaciones y ausencias muestran la fecha y distinguen el tipo en el asunto.

### Fichajes

- **Gestión diaria:** ignora o reactiva varios fichajes desde la lista diaria; los ignorados no afectan al cálculo de ubicación del día.
- **Terminales Kapri/Kimaldi:** gestiona fichajes con identificadores NFC. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/terminales-kapri.es.md)
- **Lista NFC:** muestra a todos los empleados que no están bloqueados.
- **Cierres automáticos:** identifica y filtra los días con fin de turno automático y los fichajes de salida generados al cerrar un turno. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Punto de Acceso:** puedes ver el código de acceso del empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes y gastos

- **Informes de fichajes:** genéralos desde la gestión agrupada mensual o semanal. [Más información](../informes/informes-de-la-gestion-mensual.es.md)
- **Libro de Registro de Jornada:** distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** créalos y consúltalos con una experiencia mejorada en dispositivos móviles.

### Turnos y planificación

- **Colores de turnos:** los turnos muestran colores asignados por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Modo LITE:** consulta los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

### Interfaz y navegación

- **Inicio de sesión:** se renuevan la imagen y los estilos de la pantalla.
- **Asistente de configuración:** adopta los colores de Sebastian HR.
- **Procesos:** muestran el término «Entrada» en el idioma disponible.
- **Avisos y confirmaciones:** los avisos, alertas y cuadros para confirmar o solicitar datos tienen un estilo adaptado a Sebastian HR.

### Integraciones y WebAPI

- **Kapri:** se incorpora una integración con Kapri. [Más información](../integraciones/kapri.es.md)
- **WebAPI:** consulta el total anual de incidencias y sube justificantes de gastos cerrados. [Más información](../integraciones/web-api.es.md)
- **Cursos:** crea cursos mediante nuevas operaciones de la WebAPI. [Más información](../integraciones/web-api.es.md)
- **Documentación de la WebAPI:** incluye descripciones más completas de procesos, parámetros y vistas. [Más información](../integraciones/web-api.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se guardan los validadores, se muestran las solicitudes de los tipos seleccionados y se completan correctamente las acciones y pasos pendientes.
    - **Ausencias:** puedes borrar solicitudes pasadas sin restricciones, y cancelar ausencias sin días seleccionados no deja avisos pendientes imposibles de gestionar.
    - **Empleados:** vuelven a funcionar la edición de contratos, las fotos, los controles de teletrabajo, los indicadores de estado, los cursos, la firma de documentos y la opción de QR.
    - **Fichajes:** se corrigen la actualización, las fechas, los duplicados, las incidencias y los cálculos; también funcionan el fichaje móvil, los turnos nocturnos y la edición de horas.
    - **Importación e informes:** Excel reconoce las hojas y plantillas de fichajes, y los informes muestran fechas, festivos, ausencias y saldos correctamente.
    - **Instalación e integraciones:** Docker carga sus recursos, arranca correctamente y permite el acceso de administrador; también se comprueban bien las conexiones y licencias.
    - **Jornadas y planificación:** vuelven a funcionar la resolución de incidencias en lote, los descansos, los turnos planificados y las horas previstas durante permisos.
    - **Navegación y móvil:** los menús desplegables y laterales se muestran correctamente en paneles deslizantes y dispositivos móviles; el botón de los formularios largos vuelve a estar visible.
    - **Procesos y WebAPI:** se corrigen los informes y procesos de vacaciones, compensaciones y fichajes, las notificaciones, las sugerencias anónimas y el procesamiento de solicitudes de ausencia; también se soluciona una vulnerabilidad de seguridad.
