# Versión 10.0

Permite registrar permisos por horas, integrar terminales NFC, crear reservas recurrentes para varios recursos, consultar ayuda y segmentar noticias; además, mejora la detección de incidencias de jornada.

## Novedades

### Ausencias

- **Puedes registrar permisos por horas, que también aparecen en el calendario y el planificador del empleado.** Estos permisos no descuentan días del saldo. Sus horas retribuidas y no retribuidas se incluyen en la exportación de nómina y en el cómputo de jornada; además, se consideran al gestionar ausencias no planificadas.
- **Puedes establecer un mínimo y un máximo de días para cada solicitud de ausencia.** Los límites se configuran en cada tipo de ausencia. La aplicación los comprueba al revisar la solicitud.

### Fichajes

- **Puedes integrar terminales Kapri/Kimaldi para gestionar fichajes con identificadores NFC.** Puedes asociar identificadores NFC a empleados y procesar eventos de los terminales, además de configurar opciones relacionadas. La integración también incorpora mejoras en sus pantallas e imágenes para los estados sin contenido. Desde la lista puedes borrar identificadores NFC.
- **Puedes ignorar o reactivar varios fichajes a la vez desde la lista diaria.** Para aplicar el cambio, debes indicar un motivo. El motivo queda guardado en el comentario de cada fichaje.

### Navegación

- **La aplicación incorpora un espacio de ayuda accesible desde la navegación.** Puedes consultar la ayuda desde el propio entorno de la aplicación.
- **Puedes limitar la visibilidad de las noticias por área, empresa, empleado, oficina o equipo.** Configura el acceso en cada categoría para que las noticias se muestren a las personas correspondientes.
- **La aplicación instalada se abre desde la dirección de inicio configurada.** Al abrirla, se utiliza la dirección definida para iniciar la aplicación.

### Planificación

- **Puedes crear reservas recurrentes para varios recursos a la vez.** Configura la repetición cada cierto número de días, semanas, meses o años, y excluye fines de semana y festivos. Si alguna fecha está ocupada, no se crea ninguna reserva y puedes corregir la selección.

### Despliegue

- **Puedes desplegar Sebastian HR con Docker y mantener ambas bases de datos en una misma instancia.** La configuración inicial reúne las dos bases de datos en una misma instancia para que funcionen las referencias entre ellas. Puedes usarla para desplegar la aplicación con Docker.

### Informes

- **Puedes generar informes desde la gestión agrupada mensual o semanal de fichajes.** Tienes disponibles los mismos informes que en la vista diaria. Puedes generarlos para los empleados seleccionados o para todos, dentro del periodo que estés consultando.

### Instalación

- **Puedes instalar Sebastian HR como una aplicación.** La instalación incluye la configuración necesaria para ofrecer esta modalidad.

### Integración con ERP

- **Nueva integración con Kapri.** Kapri pasa a estar disponible entre las integraciones con ERP.

### Plataforma

- **La aplicación incorpora un modo de mantenimiento.** Este modo permite indicar que la aplicación está en mantenimiento mientras no está disponible para su uso habitual.

## Mejoras

### Jornadas

- **La detección de incidencias de jornada contempla tolerancias, pausas, descansos y límites de horas, y evita avisos cuando no hay horario previsto.** Se tienen en cuenta las tolerancias del turno para detectar fichajes fuera de sus límites y jornadas con más o menos horas de las previstas. También se identifican pausas y descansos entre jornadas, y los límites semanales, mensuales y anuales se calculan en el día en que se superan. Si un turno no tiene horario previsto para un día, no se genera una incidencia por falta de fichajes.
- **Los turnos muestran colores asignados por defecto.** Puedes distinguir visualmente los tipos de turno desde el principio, sin tener que configurar sus colores previamente.

### Aprobaciones

- **Los tipos de vacaciones y ausencias usan automáticamente el flujo de aprobación que les corresponde.** Los grupos de vacaciones se asignan al flujo de vacaciones y los demás tipos, al de ausencias. Así, cada solicitud sigue el proceso previsto según su tipo.
- **La conversación de una instancia se mantiene unificada entre validación y revisión.** El mismo hilo está disponible en ambas vistas. Así puedes consultar el contexto de una instancia sin cambiar de conversación.

### Ausencias

- **La cancelación de vacaciones y ausencias sigue su grupo de tipos, que aparecen ordenados en listas y menús desplegables.** El flujo de cancelación de ausencias queda diferenciado del de vacaciones. En las listas, los tipos propios del producto aparecen antes que los añadidos en cada instalación.
- **Puedes gestionar cancelaciones de vacaciones aunque no tengan fechas de inicio y fin.** Las solicitudes de cancelación pueden tener vacías ambas fechas. Por tanto, no es necesario indicar una fecha para este tipo de solicitud.

### Empleados

- **La lista NFC muestra a todos los empleados que no están bloqueados.** Los empleados solo se excluyen de la lista cuando están bloqueados. No quedan fuera por otros motivos.

### Fichajes

- **La vista agrupada de fichajes reúne avisos y permite identificar y filtrar los cierres automáticos de turno.** La columna «Avisos» reúne días con incidencias, cierres automáticos o elementos pendientes de revisión. Un icono distingue las salidas generadas automáticamente de las registradas manualmente. El filtro de incidencias también incluye los días con más de una incidencia.
- **Puedes ver el código de acceso del empleado en el Punto de Acceso aunque esté oculto.** El código queda disponible para consultarlo desde el Punto de Acceso. Así puedes comprobarlo cuando necesites acceder a él.

### Informes

- **El Libro de Registro de Jornada distingue las ausencias por tipo, muestra sus colores y un resumen, y vuelve a estar traducido.** También puedes filtrar por empleados activos o empresa, y el informe vuelve a funcionar con ambos criterios. El código de empleado se muestra como EmployeeId y el informe se genera en el idioma de quien lo consulta.
- **Puedes crear y consultar partes de gastos con una experiencia mejorada en dispositivos móviles.** La mejora está disponible tanto al introducir los partes como al consultarlos desde el móvil.

### Inicio de sesión

- **Se renuevan la imagen y los estilos de la pantalla de inicio de sesión.** El nuevo fondo se muestra al acceder a Sebastian HR. La presentación visual de la pantalla también se actualiza.
- **El asistente de configuración del inicio de sesión adopta los colores de Sebastian HR.** Así, su apariencia queda alineada con la identidad visual de la aplicación.

### Navegación

- **Los procesos muestran el término «Entrada» en el idioma disponible.** La traducción se incorpora al propio contenido de los procesos.
- **Los avisos, alertas y cuadros de confirmación y solicitud de datos tienen un estilo adaptado a Sebastian HR.** También se adaptan al modo claro u oscuro y al idioma del perfil. Los iconos siguen el estilo de Sebastian HR y, si el contenido de una alerta es largo, puedes desplazarte para leerlo completo.

### Planificación

- **En el modo LITE, puedes consultar los tipos de patrón desde el menú Mantenimiento.** La consulta de los tipos de patrón está disponible en Mantenimiento al utilizar el modo LITE.

### Procesos

- **Los correos de vacaciones y ausencias muestran la fecha y diferencian el tipo en el asunto.** La fecha correspondiente aparece en el correo de la instancia. Además, el asunto permite distinguir si se trata de vacaciones o de una ausencia.

## Correcciones

### Aprobaciones

- **La lista de validación muestra únicamente las solicitudes de los tipos seleccionados.** El panel lateral y la lista muestran ahora los mismos tipos de solicitudes. Así puedes revisar las instancias correspondientes a tu selección sin que aparezcan solicitudes de otros tipos.
- **Se corrigen fallos en la gestión de instancias y solicitudes, incluidos los procesos con varios validadores.** Al aprobar una instancia, se ejecuta la acción asociada. Al aceptar o denegar una solicitud, también se procesa el objeto relacionado y se cierran los pasos y validadores pendientes, para que el proceso no quede incompleto ni falle sin aviso.

### Ausencias

- **Puedes borrar vacaciones y ausencias pasadas cuando el límite de días está configurado sin restricciones.** La opción sin límite vuelve a permitir eliminar registros pasados. Esta posibilidad queda disponible igual que con otras comprobaciones.
- **Al cancelar ausencias sin días seleccionados, ya no se crea un aviso pendiente imposible de gestionar.** La aplicación avisa si no hay vacaciones o ausencias que cancelar. Así, no genera una instancia vacía.
- **En el modo LITE, ya no se señalan como falta de descanso algunas bajas, vacaciones o días sin planificación.** La corrección evita que esos casos se marquen como incidencias cuando no corresponde.

### Empleados

- **Al cambiar la empresa en una edición masiva de contratos, debes elegir una oficina para la nueva empresa.** Así, el contrato queda asociado a una oficina de la empresa seleccionada. Se evita que conserve por error la oficina de la empresa anterior.
- **La fotografía de cada empleado vuelve a mostrarse en la lista y en su página.** Puedes ver la imagen tanto al consultar la lista de empleados como al abrir la página de cada persona. Esto facilita reconocer a cada empleado en ambos lugares.
- **El control de teletrabajo aplica las excepciones de oficina aunque el empleado se incorporase después.** Así se evitan incumplimientos incorrectos en los periodos consultados. El control tiene en cuenta la fecha de incorporación al aplicar estas excepciones.
- **Los indicadores de estado de la lista de empleados vuelven a mostrarse en sus colores correspondientes.** Los estados de éxito, aviso y error se distinguen visualmente. Así puedes interpretar los indicadores sin que aparezcan todos en negro.
- **Ya puedes guardar cursos indicando un tipo de coste.** El formulario acepta el tipo de coste introducido como texto. Así puedes guardar el curso sin que se produzca un error de formato.
- **Ya no puedes inscribirte a cursos o vigilancias de salud después de que venza el plazo.** La aplicación comprueba la fecha límite antes de aceptar la solicitud. De este modo, no se admiten inscripciones fuera del plazo establecido.
- **Ya puedes vincular documentos y enviarlos a firmar sin recibir un error desconocido.** Si se produce un error durante el proceso, aparece un mensaje que ayuda a identificar qué ha ocurrido. Esto permite distinguir los problemas que puedan surgir al vincular o enviar los documentos.
- **El botón de QR ya no aparece cuando la opción está desactivada.** La aplicación oculta el botón si la función QR no está habilitada. Así, no se muestra una opción que no está disponible.

### Fichajes

- **Las fechas de los fichajes se muestran correctamente al abrir un día desde el calendario de inicio del Manager.** Se corrige el error que aparecía al acceder a los fichajes desde ese calendario.
- **Al aceptar la inserción de un fichaje, la jornada afectada y sus incidencias se actualizan de inmediato.** Ya no es necesario esperar a que los procesos automáticos revisen la jornada para que aparezcan los cambios.
- **La aplicación evita fichajes duplicados cuando los datos de fichaje están desactualizados.** Si el tipo de fichaje no corresponde con el último fichaje válido, muestra un aviso y actualiza la información de fichaje.
- **Los fichajes en días libres ya no generan incidencias incorrectas de entrada retrasada o salida anticipada.** Estas incidencias solo se evalúan cuando el empleado tiene un turno real ese día.
- **Puedes marcar o desmarcar un festivo como trabajado sin que se altere su fecha.** Antes de guardar el cambio, la aplicación verifica que el día sea festivo en el calendario del empleado.
- **Puedes fichar desde la aplicación sin activar la ubicación cuando no se solicita para el fichaje.** La aplicación gestiona esta situación correctamente desde el móvil. Si la opción de solicitar ubicación está desactivada, no exige que la ubicación del dispositivo esté activada.
- **Se corrige el cálculo de jornadas de 24 horas en empleados sin planificación.** Al recalcular los fichajes, la jornada vuelve a agruparse correctamente. También se corrige la asignación del turno y la detección de los descansos entre jornadas.
- **Los comentarios largos ya no hacen fallar el guardado del fichaje ni estropean el enlace a la instancia.** Si el comentario no cabe completo en el fichaje, se acorta allí para conservar el enlace correctamente formado. El comentario original de la instancia se mantiene íntegro.
- **Ya puedes fichar durante un turno nocturno iniciado el día anterior cuando se exige planificación previa.** El cambio de día ya no impide registrar el fichaje correspondiente al turno planificado.
- **Al editar un fichaje, se actualizan también su hora UTC y su zona horaria.** El recálculo se aplica tanto a las modificaciones manuales como a la aceptación de una instancia de modificación. Así, los datos horarios quedan sincronizados con la hora editada.
- **El filtro de fichajes al modificar una instancia funciona correctamente.** La lista asociada a la instancia vuelve a aplicar el filtro esperado.
- **Si se ignoran todos los fichajes de un día, la localización deja de influir en el cálculo.** Cuando todos los fichajes del día están ignorados, la localización del empleado ya no se tiene en cuenta para ese día.

### Importación

- **Las importaciones de Excel reconocen correctamente la hoja y la plantilla de fichajes.** La corrección afecta a varias importaciones, entre ellas empleados, contratos y fichajes. Así se evitan errores al procesar los datos de las plantillas.

### Informes

- **Los informes de detalle y horas de ausencia muestran correctamente las fechas del periodo en servidores en español.** El idioma configurado en el servidor ya no provoca que las fechas del periodo aparezcan incorrectamente.
- **El resumen de jornada ya no cuenta como falta un festivo no trabajado.** Los festivos no trabajados aparecen en una fila específica del resumen, separados de las faltas.
- **El calendario de ausencias por grupo muestra juntas las ausencias de un empleado en el mismo día.** Así, el informe se genera correctamente cuando un empleado tiene varias ausencias en una misma fecha.
- **El informe de saldo de vacaciones se genera correctamente al filtrar por empleados activos.** El filtro por empleados activos ya no impide obtener el informe.

### Instalación

- **En las instalaciones Docker, vuelven a cargarse el logo, las fuentes de la skin y otras imágenes.** El logo se muestra en el inicio de sesión y en el menú. También se corrigen las imágenes del asistente y de ayuda, y deja de aparecer el aviso de archivos no encontrados tras iniciar sesión.
- **Las instalaciones Docker ya no fallan al iniciarse por primera vez y permiten acceder como administrador al terminar.** La configuración desatendida se completa sin el error que intentaba actualizar una base de datos que ya estaba al día. Esta instalación utiliza SQL Server Express.

### Integración con ERP

- **La integración con el Canal de Denuncias consulta correctamente la licencia.** Así se evitan errores al comprobar la licencia durante el uso de la integración.
- **La integración con el ERP comprueba correctamente la conexión con la base de datos.** La comprobación de conexión durante la integración deja de ofrecer resultados incorrectos.

### Jornadas

- **Ya puedes resolver en lote las incidencias de jornada seleccionadas.** La acción aplica la resolución a todas las incidencias que selecciones. Así, al resolverlas en lote, los cambios se aplican correctamente.
- **La parada mínima del turno se respeta al redondear los descansos.** La duración que se muestra tiene en cuenta el mínimo configurado, aunque el horario aplique redondeos. Los descansos que superan ese mínimo conservan su duración.
- **Los descansos computables no fichados se incluyen en el cálculo de las horas trabajadas.** El total de horas trabajadas refleja estos descansos aunque no se hayan fichado.

### Navegación

- **Los desplegables de las barras de herramientas ya se abren correctamente dentro de paneles deslizantes.** Además, los paneles ya no ocultan otros elementos emergentes, como tooltips y galerías.
- **El menú superior ya no oculta los menús desplegables en dispositivos móviles.** Se corrige la superposición para que puedas ver y utilizar las opciones desplegables desde el móvil.
- **El menú lateral se muestra correctamente en dispositivos móviles.** Así puedes consultar y utilizar la navegación lateral con normalidad desde pantallas móviles.

### Planificación

- **Al cambiar un turno ya planificado, también se actualiza su duración.** El cambio se aplica tanto al modificar el día desde el planificador como al hacerlo mediante patrones. Así, no se conserva la duración del turno anterior.
- **Puedes navegar por los patrones aunque no abras el planificador desde la unidad organizativa.** No es necesario iniciar la navegación desde una unidad organizativa para consultar los patrones.
- **La planificación de la página de inicio muestra correctamente las horas previstas durante un permiso.** En los días de permiso, la información sobre las horas que tienes previstas deja de mostrarse de forma incorrecta.

### Procesos

- **En formularios largos vistos desde el móvil, el botón para solicitar o aceptar permanece accesible.** Al desplazarte por la página, el pie del formulario no queda oculto bajo la barra del navegador.
- **Las notificaciones al empleado ya no requieren que tenga un usuario activo.** Al seleccionar la opción de notificar al empleado, se envía la notificación aunque la persona no tenga una cuenta activa en la aplicación.
- **Al enviar una sugerencia anónima no pública, el formulario se cierra sin provocar errores de seguridad.** El cierre evita que se intente acceder a una vista que no está disponible para esa sugerencia.

### WebAPI

- **Las solicitudes de ausencia por API se procesan correctamente incluso cuando llegan varias a la vez.** También se corrige una vulnerabilidad que podía permitir inyecciones SQL en estas llamadas.
