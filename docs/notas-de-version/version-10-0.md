# Versión 10.0

La versión 10.0 amplía la gestión de ausencias, reservas y jornadas, y añade nuevas opciones de acceso y configuración. También mejora la navegación, las integraciones y el trabajo diario con fichajes e informes.

## Lo más destacado

### Permisos por horas

Ya puedes registrar permisos por horas, además de permisos de día completo. Los permisos parciales no descuentan días del saldo: sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y el cómputo de jornada, y se muestran en el calendario y el planificador.

[Más información: restricciones de ausencias](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Ayuda desde la aplicación

Tienes un espacio de ayuda accesible desde la navegación de Sebastian HR. Puedes consultar la documentación desde el propio entorno de la aplicación, sin salir de tu espacio de trabajo.

[Más información: página de inicio](../index.es.md)

### Noticias por audiencia

Puedes limitar quién ve las noticias según el área, la empresa, el empleado, la oficina o el equipo. Configura el acceso en cada categoría para mostrar cada noticia solo a las personas a las que corresponde.

[Más información: ámbitos de visibilidad](../empleados-y-organizacion/ambitos-de-visibilidad.es.md)

### Reservas recurrentes

Puedes crear reservas recurrentes para varios recursos a la vez y repetirlas cada cierto número de días, semanas, meses o años. También puedes excluir fines de semana y festivos; si alguna fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección.

[Más información: cuadrantes de planificación](../turnos-y-planificacion/cuadrantes.es.md)

### Incidencias de jornada más precisas

La detección de incidencias tiene en cuenta las tolerancias del turno, las pausas y los descansos, además de los límites de horas. Calcula los límites semanales, mensuales y anuales el día en que se superan, y no avisa de fichajes ausentes cuando no hay horario previsto.

[Más información: incidencias de jornada](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md)

## Otras novedades

### Ausencias

- **Cómputo de horas:** puedes excluir determinados tipos de ausencia del cálculo de horas teóricas.
- **Duración de solicitudes:** puedes definir un mínimo y un máximo de días para cada solicitud de ausencia. [Más información](../ausencias-y-vacaciones/restricciones-de-ausencias.es.md)

### Instalación y plataforma

- **Docker:** puedes desplegar Sebastian HR y configurar las dos bases de datos en una misma instancia.
- **Aplicación instalada:** puedes instalar Sebastian HR y abrirla desde la dirección de inicio configurada.
- **Modo de mantenimiento:** la aplicación incorpora una opción para activar este modo.
- **Paquetes publicados:** los documentos que subes a la aplicación ya no se incluyen en ellos.

### Fichajes

- **Gestión en lote:** puedes ignorar o reactivar varios fichajes desde la lista diaria.
- **Cierres automáticos:** la vista agrupada muestra los días con fin de turno automático y permite filtrarlos. [Más información](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/cierre-automatico-de-fichajes-pendientes.es.md)
- **Punto de Acceso:** puedes consultar el código de acceso del empleado aunque esté oculto. [Más información](../fichajes-y-jornadas/donde-fichan-los-empleados/punto-de-acceso.es.md)

### Informes y gastos

- **Informes de fichajes:** puedes generarlos desde la gestión agrupada mensual o semanal. [Más información](../informes/catalogo-de-informes.es.md)
- **Libro de Registro de Jornada:** distingue las ausencias por tipo, muestra sus colores y un resumen. [Más información](../informes/informes-de-control-horario.es.md)
- **Partes de gastos:** puedes crearlos y consultarlos con una experiencia mejorada en dispositivos móviles.

### Integraciones y WebAPI

- **Kapri/Kimaldi:** la integración con terminales admite fichajes mediante identificadores NFC. [Más información](../integraciones/kapri.es.md)
- **Integración con Kapri:** Sebastian HR incorpora una nueva integración con este sistema. [Más información](../integraciones/kapri.es.md)
- **Lista NFC:** muestra a todos los empleados que no están bloqueados.
- **WebAPI:** puedes consultar incidencias anuales, gestionar justificantes de gastos incluso en gastos cerrados y crear cursos; también ofrece descripciones más completas. [Más información](../integraciones/web-api.es.md)

### Aprobaciones y procesos

- **Flujos de aprobación:** los tipos de vacaciones y ausencias reciben automáticamente el flujo correspondiente. [Más información](../solicitudes-e-instancias/flujos-de-aprobacion.es.md)
- **Conversaciones:** la conversación de una instancia se mantiene unificada entre la validación y la revisión. [Más información](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md)
- **Correos de ausencias:** muestran la fecha y especifican el tipo en el asunto.

### Interfaz y acceso

- **Inicio de sesión:** se renuevan la imagen y los estilos de la pantalla, y el asistente de configuración adopta los colores de Sebastian HR.
- **Procesos:** muestran el término «Entrada» en el idioma disponible.
- **Avisos y cuadros de diálogo:** adoptan un estilo adaptado a Sebastian HR.

### Turnos y planificación

- **Colores de turnos:** los turnos muestran colores asignados por defecto. [Más información](../turnos-y-planificacion/turnos.es.md)
- **Modo LITE:** puedes consultar los tipos de patrón desde el menú Mantenimiento. [Más información](../introduccion/ediciones-lite-y-pro.es.md)

## Correcciones

??? note "Ver las correcciones de esta versión"

    - **Aprobaciones:** se conservan los validadores configurados, se muestran las solicitudes de los tipos seleccionados y se completan correctamente las acciones y pasos pendientes.
    - **Ausencias:** las cancelaciones pendientes dejan de bloquearse o duplicarse; también vuelven a funcionar el borrado de ausencias pasadas y la detección de descansos.
    - **Empleados y formación:** se corrigen la edición de contratos, las fotos y estados, las excepciones de teletrabajo, la gestión de cursos, la firma de documentos y la visibilidad del botón QR.
    - **Fichajes:** vuelven a funcionar la selección y edición de fichajes, su actualización inmediata, las fechas y zonas horarias, y los casos de días libres, turnos nocturnos y jornadas de 24 horas.
    - **Informes e importación:** se corrigen la lectura de plantillas Excel, las fechas de los periodos, los festivos, las ausencias agrupadas y los saldos de vacaciones.
    - **Instalación e integración:** Docker vuelve a cargar imágenes y permite completar el primer inicio; también se corrigen las comprobaciones de licencia y conexión con el ERP.
    - **Jornadas y planificación:** se pueden resolver incidencias en lote, se respetan los descansos y se corrigen el cálculo de horas, la duración de turnos y la navegación por patrones.
    - **Navegación móvil:** los desplegables de las barras, el menú superior y el menú lateral vuelven a mostrarse correctamente en paneles y dispositivos móviles.
    - **Procesos y WebAPI:** se corrigen los informes y las solicitudes, vuelven a verse los botones al final de formularios largos y las notificaciones y sugerencias se gestionan sin errores.
