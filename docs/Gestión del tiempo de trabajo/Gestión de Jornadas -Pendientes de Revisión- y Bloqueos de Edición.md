# Gestión de Jornadas "Pendientes de Revisión" y Bloqueos de Edición

### 1\. Introducción y Contexto Legal

La normativa española de registro de jornada exige un control estricto sobre la validación de las horas laborales. Para cumplir con la ley, el sistema debe garantizar:

  1. Inmutabilidad: Una jornada validada no puede modificarse "silenciosamente".

  2. Trazabilidad: Cualquier cambio posterior que afecte al cálculo de horas debe quedar registrado.

  3. Seguridad Jurídica: No se deben permitir modificaciones de datos estructurales fuera de un plazo razonable.

Para ello, Sebastian HR incorpora dos mecanismos de seguridad:

  * Jornadas Pendientes de Revisión: Marca las jornadas existentes que deben ser verificadas tras un cambio.

  * Bloqueos por Antigüedad: Impide la edición de datos antiguos que afectarían a periodos cerrados.



### 2\. ¿Qué es una Jornada "Pendiente de Revisión"?

Una jornada pasa al estado Pendiente de Revisión cuando cumple tres condiciones obligatorias:

  1. Existe un registro de jornada con fichajes (el empleado trabajó ese día).

  2. Ese registro había sido validado previamente.

  3. Se realiza una modificación posterior (ej: añadir una ausencia parcial o cambiar el turno) que altera el cálculo de horas.

Cuando esto ocurre, el sistema elimina la validación, marca la jornada visualmente como "Pendiente" y exige un recálculo.

 

### 3\. Sistema de Bloqueos por Antigüedad (Settings)

Para evitar modificaciones en periodos cerrados, el sistema verifica la fecha del cambio. Existen 5 configuraciones (Settings) que definen el límite de días para editar información:

<table><tbody><tr class="table-header ng-star-inserted"><td class="ng-star-inserted"><span class="ng-star-inserted">Tipo de Dato</span></td><td class="ng-star-inserted"><span class="ng-star-inserted">Setting Configurable</span></td><td class="ng-star-inserted"><span class="ng-star-inserted">Días recomendados (Default)</span></td></tr><tr class="ng-star-inserted"><td class="ng-star-inserted"><strong class="ng-star-inserted"><span class="ng-star-inserted">Vacaciones</span></strong></td><td class="ng-star-inserted"><span class="inline-code ng-star-inserted">DirtyDaysBack_Vacaciones</span></td><td class="ng-star-inserted"><span class="ng-star-inserted">30 días</span></td></tr><tr class="ng-star-inserted"><td class="ng-star-inserted"><strong class="ng-star-inserted"><span class="ng-star-inserted">Ausencias</span></strong></td><td class="ng-star-inserted"><span class="inline-code ng-star-inserted">DirtyDaysBack_Ausencias</span></td><td class="ng-star-inserted"><span class="ng-star-inserted">30 días</span></td></tr><tr class="ng-star-inserted"><td class="ng-star-inserted"><strong class="ng-star-inserted"><span class="ng-star-inserted">Turnos</span></strong></td><td class="ng-star-inserted"><span class="inline-code ng-star-inserted">DirtyDaysBack_Turnos</span></td><td class="ng-star-inserted"><span class="ng-star-inserted">7 días</span></td></tr><tr class="ng-star-inserted"><td class="ng-star-inserted"><strong class="ng-star-inserted"><span class="ng-star-inserted">Festivos</span></strong></td><td class="ng-star-inserted"><span class="inline-code ng-star-inserted">DirtyDaysBack_Festivos</span></td><td class="ng-star-inserted"><span class="ng-star-inserted">365 días</span></td></tr><tr class="ng-star-inserted"><td class="ng-star-inserted"><strong class="ng-star-inserted"><span class="ng-star-inserted">Bajas (IT)</span></strong></td><td class="ng-star-inserted"><span class="inline-code ng-star-inserted">DirtyDaysBack_Bajas</span></td><td class="ng-star-inserted"><span class="ng-star-inserted">90 días</span></td></tr></tbody></table>

 

  * DENTRO del plazo: Se permite el cambio. Si afecta a una jornada trabajada, esta pasará a "Pendiente de Revisión".

  * FUERA del plazo: El sistema bloquea la acción si detecta que afectaría a una jornada validada antigua.

 

### 4\. Acciones que generan "Pendiente de Revisión"

Las siguientes acciones marcan la jornada como pendiente solo si existe un registro de fichajes previo en ese día:

### 4.1. Ausencias Parciales

Si se inserta, modifica o elimina una ausencia de unas horas (ej: "Visita médica 2 horas") en un día donde el empleado ha fichado y validado su jornada.

### 4.2. Modificación de Turnos

Cualquier cambio en la estructura del turno (hora inicio/fin, descansos, tolerancia) afecta a los empleados que hayan validado jornada usando ese turno.

### 4.3. Cambios en Festivos

Si un día trabajado y validado se convierte posteriormente en festivo (o viceversa), la jornada se marca para revisión.

### 4.4. Superposición de datos sobre días trabajados

Si se inserta una ausencia de día completo o unas vacaciones sobre un día que, por error, el empleado había trabajado y validado.



### 5\. Acciones que NO generan "Pendiente de Revisión"

Es fundamental entender qué acciones no activan este estado:

### 5.1. Ausencias de Día Completo (Sin fichajes previos)

Si se crea una ausencia de día completo (Vacaciones, Baja IT, Asuntos Propios) en una fecha donde el empleado no tiene fichajes , no se genera ninguna marca de "Pendiente de Revisión".

> Motivo: Al no haber fichajes, no existe un registro de jornada (Employees_Assistence) que se pueda "ensuciar" o invalidar. Simplemente se crea la ausencia en el calendario.

### 5.2. Cambios en la Planificación Diaria

La planificación diaria (Employees_Schedule) está bloqueada si la jornada está validada. Por tanto, no es posible generar inconsistencias por esta vía.

### 5.3. Ausencias No Retribuidas (No computables)

Las ausencias que no suman horas computables generalmente no requieren revalidar el cálculo horario de fichajes existentes.



### 6\. Cómo resolver una Jornada Pendiente

Si el sistema marca una jornada como pendiente, proceda así:

### Opción A: Recálculo Automático (Recomendado)

  1. Ejecute el recálculo desde la jornada o mediante procesos masivos.

  2. El sistema actualiza horas teóricas y trabajadas con los nuevos datos.

  3. Si el resultado es correcto, limpie la marca y valide de nuevo.

### Opción B: Revisión Manual

  1. Revise el motivo del cambio registrado en la jornada.

  2. Verifique el total de horas.

  3. Pulse Validar.



### 7\. Ejemplos Prácticos

Caso 1: Ausencia de día completo (Caso estándar)

  * Acción: RRHH asigna vacaciones del 1 al 15 de agosto. El empleado no trabajó esos días (no hay fichajes).

  * Resultado: NO se genera "Pendiente de Revisión". El sistema simplemente registra las vacaciones en el calendario.

Caso 2: Ausencia parcial (Caso que ensucia)

  * Acción: El empleado trabajó y validó el lunes. Hoy se añade una ausencia de 2 horas para ese lunes.

  * Resultado: La jornada pasa a "Pendiente de Revisión" porque el cálculo de horas trabajadas vs. teóricas ha cambiado.

Caso 3: Intento de modificación antigua

  * Acción: Se intenta borrar un festivo de hace 2 años que tiene jornadas validadas asociadas.

  * Resultado: Bloqueo. El sistema impide la acción por seguridad (DirtyDaysBack).



### 8\. Preguntas Frecuentes

¿Por qué al poner vacaciones no se marcan las jornadas como pendientes?  
Si el empleado no ha fichado esos días, no hay ninguna "jornada de trabajo" que revisar. Las vacaciones se aplican directamente. Solo se marcaría como pendiente si, por error, el empleado hubiera fichado en un día de vacaciones.

¿Puedo desactivar los bloqueos de antigüedad?  
No se recomienda para garantizar la seguridad jurídica y el cierre de nóminas, pero los administradores pueden ampliar los días en las Settings si es necesario.

¿Cómo busco todas las jornadas pendientes?  
Existe un filtro en el listado de asistencias y un proceso masivo para recalcular todas las que tengan la marca de revisión activa.