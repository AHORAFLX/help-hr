# Asignación de Turno y Fecha de Jornada

## Introducción

Cada vez que un empleado ficha, Sebastian HR guarda dos datos clave:

- **Hora del fichaje** (`CheckTime`): la fecha y hora en que se ficha.
- **Fecha de jornada** (`DateJourney`): la jornada laboral a la que pertenece el fichaje. Puede coincidir con la fecha natural del fichaje o ser anterior (por ejemplo, en jornadas nocturnas que cruzan la medianoche).

Además, a cada fichaje se le asigna un turno. Este artículo explica cómo decide el sistema la jornada y el turno de cada fichaje.

## La ventana del turno

Un fichaje está "dentro del turno" cuando cae en su ventana: desde el inicio del turno menos los **minutos de límite** configurados en el turno hasta el fin del turno más esos minutos (o los límites inferior y superior, si el turno los tiene separados). No basta con el horario del turno: los minutos de límite determinan qué fichajes se consideran dentro.

## Empleados planificados

Son los que tienen un turno planificado para ese día.

- **Fichaje dentro de la ventana del turno**: se asigna el turno planificado y la fecha de ese día. En este caso no se aplican los parámetros de separación de jornadas.
- **Fichaje fuera de la ventana del turno**: el sistema lo trata como un fichaje sin planificación (ver el apartado siguiente). Si continúa una jornada ya abierta, toma su fecha y su turno. Si abre una jornada nueva, queda con el turno especial **Sin Planificación** (turno -1).

!!! example "Ejemplo"
    Un empleado tiene un turno de 08:00 a 16:00 el 31/07/2025, con 30 minutos de límite.

    - Ficha a las 08:15: está dentro de la ventana (07:30–16:30), así que se le asigna el turno planificado y la jornada del 31/07/2025.
    - Ficha a las 18:00 sin ningún fichaje anterior abierto: está fuera de la ventana y abre una jornada nueva con el turno Sin Planificación.

## Empleados sin planificación

Son los que tienen **Sin Planificar** en el campo **Tipo de gestión de fichaje** de su ficha, o los planificados que no tienen turno ese día.

Sus fichajes reciben el turno **Sin Planificación** (turno -1), salvo que ese día tengan un turno puesto en el planificador de empleados, una regla de modificación de horario o un turno cambiado en la propia jornada. En esos casos, los fichajes que caen dentro de la ventana de ese turno lo reciben.

La fecha de jornada se calcula con las reglas de separación de jornadas que se explican a continuación.

## Parámetros que controlan la asignación de la fecha de jornada

Los dos parámetros están en `Mantenimiento > Parámetros > Configuración`.

| Parámetro | Etiqueta | Valor por defecto |
| --- | --- | --- |
| `MinBreakBetweenWorkingDays` | Descanso mínimo entre días laborables (en horas) | 10 |
| `HoursUntilNewWorkday` | Define el número máximo de horas que puede durar una jornada laboral antes de considerarse el inicio de una nueva | 0 (desactivado) |

### MinBreakBetweenWorkingDays

Es el descanso mínimo, en horas, entre un fichaje y el inmediatamente anterior para que el fichaje actual empiece una jornada nueva.

- Se compara con el fichaje inmediatamente anterior, estén o no en el mismo día natural.
- Se abre jornada nueva si el descanso es **igual o superior** al valor configurado.
- El tiempo entre una entrada y su salida no cuenta como descanso: es tiempo trabajado. Por eso una salida nunca abre jornada nueva por este parámetro.

!!! example "Ejemplo con MinBreakBetweenWorkingDays = 8 horas"
    - Entrada el 29/07/2025 a las 08:00 y salida a las 20:30 (12,5 horas después): la salida sigue en la jornada del 29/07/2025, porque el tiempo entre una entrada y su salida no es descanso.
    - Salida el 29/07/2025 a las 22:00 y entrada el 30/07/2025 a las 12:00 (14 horas de descanso): 14 ≥ 8, así que la entrada abre la jornada del 30/07/2025.
    - Salida el 29/07/2025 a las 22:00 y entrada el 30/07/2025 a las 02:00 (4 horas de descanso): 4 < 8, así que la entrada sigue en la jornada del 29/07/2025.

### HoursUntilNewWorkday

Es la duración máxima, en horas, de una jornada: cuenta desde el **primer fichaje de la jornada**, no desde el fichaje anterior.

- Solo se aplica si su valor es mayor que 0.
- Solo se aplica a fichajes de un día natural distinto al de la jornada en curso.
- Se abre jornada nueva si han pasado **más** horas que el valor configurado desde el primer fichaje de la jornada.

!!! example "Ejemplo con HoursUntilNewWorkday = 12 horas"
    - Primer fichaje de la jornada el 31/07/2025 a las 08:00 y fichaje actual el 01/08/2025 a las 02:00 (18 horas): 18 > 12, así que el fichaje abre la jornada del 01/08/2025.
    - Primer fichaje de la jornada el 31/07/2025 a las 20:00 y fichaje actual el 01/08/2025 a las 05:00 (9 horas): 9 < 12, así que el fichaje sigue en la jornada del 31/07/2025 (si tampoco se cumple el descanso mínimo).

## Cómo se decide la jornada de un fichaje

Las reglas no se evalúan en secuencia, sino que basta con que se cumpla una. Un fichaje fuera de la ventana de un turno abre jornada nueva si se cumple **cualquiera** de estas condiciones:

- no hay ningún fichaje anterior abierto (si la jornada anterior está validada, sus fichajes están cerrados y el siguiente fichaje siempre abre jornada nueva);
- desde el fichaje anterior hay un descanso igual o superior a `MinBreakBetweenWorkingDays` (salvo entre una entrada y su salida);
- `HoursUntilNewWorkday` es mayor que 0, el fichaje es de otro día y han pasado más horas que ese valor desde el primer fichaje de la jornada.

Si no se cumple ninguna, el fichaje se asigna a la jornada en curso, con su turno.

## Ejemplo completo con ambos parámetros

Parámetros: `MinBreakBetweenWorkingDays` = 8 horas y `HoursUntilNewWorkday` = 12 horas. Un empleado sin planificación realiza estos fichajes:

| Fichaje | Qué pasa | Jornada |
| --- | --- | --- |
| 31/07/2025 08:00 Entrada | Primer fichaje: abre jornada. | 31/07/2025 |
| 31/07/2025 10:00 Salida | Salida tras una entrada: no es descanso. | 31/07/2025 |
| 31/07/2025 10:20 Entrada | 20 minutos de descanso < 8 horas. | 31/07/2025 |
| 31/07/2025 22:00 Salida | Salida tras una entrada: no es descanso. | 31/07/2025 |
| 01/08/2025 02:00 Entrada | Descanso de 4 horas < 8, pero es otro día y han pasado 18 horas > 12 desde el primer fichaje (08:00). | 01/08/2025 |

El fichaje de las 02:00 abre una jornada nueva por `HoursUntilNewWorkday`, aunque el descanso respecto al fichaje anterior (4 horas) sea menor que `MinBreakBetweenWorkingDays`.

## Resumen y notas importantes

- **Empleados planificados**: los fichajes dentro de la ventana del turno reciben el turno y la fecha planificados. Los que caen fuera se tratan como fichajes sin planificación.
- **Empleados sin planificación**: turno Sin Planificación, salvo que el día tenga un turno en el planificador de empleados, una regla de modificación de horario o un turno cambiado en la jornada.
- **MinBreakBetweenWorkingDays**: descanso entre fichajes consecutivos, sin contar el tiempo entre una entrada y su salida.
- **HoursUntilNewWorkday**: duración máxima de la jornada desde su primer fichaje. Con valor 0 no se aplica, y la fecha de jornada depende solo de `MinBreakBetweenWorkingDays`.
- La [reasignación automática de turnos](../../turnos-y-planificacion/reasignacion-automatica-de-turnos.es.md) <span class="fh-version-tag hr-pro-mode no-margin margin-right-s" title="Disponible en modo pro">Pro</span>, si está activada en la ficha del empleado, puede cambiar después el turno de la jornada por el que mejor encaje con sus fichajes.
