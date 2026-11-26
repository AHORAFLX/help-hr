# Versión 10.1

Incluye consultas de vacaciones con el asistente, el envío de horas extra validadas a la bolsa y nuevas consultas en la WebAPI sobre teletrabajo y fichajes pendientes.

## Novedades

### Fichajes

- **Ya puedes enviar a la bolsa de horas las horas extra validadas, aunque el convenio no las calcule.** Puedes hacerlo tanto con horas extra solicitadas como con las introducidas manualmente. También se ha corregido el aviso que aparecía aunque hubiera registros seleccionados.

### Plataforma

- **La página de mantenimiento ofrece temas y juegos de temporada en el idioma del usuario; los administradores pueden ajustar las fechas y activar o desactivar las temporadas.** El contenido está disponible en inglés, español, catalán, francés e italiano; si no se puede determinar el idioma de la aplicación, se usa el del navegador. Las temporadas y sus opciones también se muestran en el idioma del usuario. Desde Parámetros > Juegos del modo de mantenimiento, los administradores pueden definir las fechas y previsualizar los juegos; los nombres, juegos y modos de fecha son fijos. En Pascua se puede guiar una cometa con el ratón, un dedo o las teclas de dirección; en verano, controlar una gaviota para robar aperitivos; y en Halloween, asustar a quienes piden caramelos. También se incluye un tema navideño con un juego de Papá Noel.

### WebAPI

- **La WebAPI permite consultar el cumplimiento mensual de las reglas de teletrabajo por empleado.** La información incluye los días de teletrabajo, los que cuentan para el límite y los meses con incumplimientos. Cada empleado puede consultar sus datos, mientras que Recursos Humanos, responsables y administradores pueden consultar los de las personas a su cargo.
- **La WebAPI permite consultar qué opciones están disponibles para una aplicación.** Las aplicaciones que se integran con Sebastian HR pueden identificar las opciones posibles. Esto les permite conocer qué opciones tienen disponibles al usar la WebAPI.
- **La WebAPI permite gestionar usuarios de puntos de acceso con permisos limitados.** Puedes gestionar estos usuarios mediante la WebAPI. Sus permisos están restringidos para impedir el acceso a funciones no autorizadas.
- **Los asistentes de IA pueden identificar quién debía fichar y no lo hizo.** Para detectar los fichajes que faltan, consultan los fichajes, las jornadas y la planificación. Así pueden identificar si una persona no ha realizado un fichaje previsto.

## Mejoras

### Ausencias

- **Consulta con el asistente las vacaciones y los permisos de tu equipo y de las personas a tu cargo.** Para las personas a tu cargo, el asistente muestra el motivo y el saldo. Para tus compañeros de equipo, indica las vacaciones y los permisos, tanto aceptados como pendientes.

### Fichajes

- **El resumen mensual de fichajes identifica los días con una salida generada automáticamente.** El icono «A» señala estos casos y, al pasar el cursor sobre él, se explica que la salida se generó por el fin automático de jornada.

### Inicio de sesión

- **El acceso mediante códigos QR de empleados es más seguro y ya no depende de terminales Kapri.** Puedes utilizar el acceso por QR sin depender de esos terminales. Además, se ha reforzado la seguridad de este comportamiento.

### Noticias

- **Al leer un mensaje en la aplicación, su notificación también queda marcada como leída.** La notificación asociada refleja que ya has leído el mensaje. Así puedes distinguir las notificaciones pendientes de las ya atendidas.

### WebAPI

- **El resumen anual de jornada de la WebAPI ofrece los mismos datos que el disponible en Sebastian HR.** Las integraciones pueden consultar mediante la API el mismo contenido que aparece en el resumen anual de jornada de Sebastian HR. Así, ambos canales ofrecen los mismos datos.
- **Al insertar fichajes mediante la WebAPI, el servidor se encarga de cancelar la operación cuando corresponda.** Ya no es necesario que la aplicación que envía los fichajes gestione esa cancelación. El servidor la realiza cuando la operación debe interrumpirse.
- **La documentación de la WebAPI incluye información sobre las ausencias no planificadas y los parámetros de MCP.** La información está disponible tanto en la colección de Postman como en la referencia de la API. La documentación detalla los parámetros de MCP.

## Correcciones

### Ausencias

- **Al eliminar una solicitud o días de ausencia, también se eliminan sus documentos adjuntos.** Así, los documentos borrados no aparecen en solicitudes posteriores ni cuentan como justificantes al validar una ausencia. La eliminación se aplica desde las listas de ausencias, el grupo de ausencias y el calendario del empleado.

### Empleados

- **Al editar un contrato, la fecha de fin ya no se pierde ni mantiene activo al empleado por error.** La fecha inicial de fin se conserva al crear el contrato y no se modifica durante una edición. Al finalizar, ampliar o reabrir el contrato, la fecha correspondiente queda guardada correctamente.

### Plataforma

- **Los textos traducidos vuelven a mostrar correctamente los acentos y el signo de advertencia.** El aviso del formulario de ausencias vuelve a mostrar sus acentos y el signo de advertencia. También se corrigen «Descripción» en las páginas offline y el prefijo «??» del título «Weekly Trend» en Climate Pulse.

### WebAPI

- **La WebAPI puede consultar el control anual de incumplimientos de ubicación en SQL Server 2016.** La consulta devuelve los meses con incumplimientos en el formato esperado. También funciona cuando no hay ningún incumplimiento.
