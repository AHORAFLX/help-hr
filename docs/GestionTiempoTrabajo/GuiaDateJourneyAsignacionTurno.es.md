# Guía de Asignación de Turno y Fecha de Jornada (DateJourney)

## 1\. Introducción

En Sebastian HR, cada vez que un empleado realiza un fichaje, el sistema registra esta acción en la tabla de fichajes con dos campos fundamentales:

  * CheckTime : La fecha y hora exacta en la que se realiza el fichaje (dato real del momento del registro).
  * DateJourney : La fecha de la jornada laboral a la que se asigna el fichaje. Este campo puede coincidir con la fecha natural de CheckTime o corresponder a una fecha anterior (generalmente el día anterior, en casos como jornadas nocturnas que cruzan medianoche).

El objetivo de esta asignación es agrupar correctamente los fichajes en la jornada laboral correspondiente, respetando la planificación del empleado y las reglas de descanso configuradas en el sistema. La lógica depende de:

  * Si el empleado tiene un turno planificado o no.
  * Dos parámetros configurables: MinBreakBetweenWorkingDays y HoursUntilNewWorkday.

Este documento explica paso a paso cómo Sebastian HR asigna el turno (ShiftId) y la DateJourney a cada fichaje, con ejemplos prácticos para garantizar una comprensión clara.

## 2\. Tipos de Empleados y Asignación de Turnos

Los empleados en Sebastian HR se dividen en dos categorías según su planificación:

### 2.1. Empleados Planificados

Son aquellos que tienen un turno predefinido en la planificación para un día específico.

  * Lógica de asignación del turno :
    * Si el CheckTime del fichaje cae dentro de los límites horarios del turno planificado para ese día, se asigna el turno planificado y la DateJourney corresponde a la fecha planificada.
    * Si el CheckTime está fuera de los límites del turno planificado, se asigna igualmente el turno planificado, pero la DateJourney se calcula según las reglas de descanso definidas por los parámetros MinBreakBetweenWorkingDays y HoursUntilNewWorkday.
  * Ejemplo : Un empleado tiene un turno planificado de 08:00 a 16:00 el 31/07/2025.
    * Fichaje a las 08:15 → Turno planificado asignado, DateJourney = 31/07/2025.
    * Fichaje a las 18:00 → Turno planificado asignado, pero DateJourney se calcula según las reglas de descanso (ver sección 3).

### 2.2. Empleados Sin Planificación

Son aquellos que no tienen un turno asignado para el día.

  * Lógica de asignación del turno :
    * Todos los fichajes se asignan al turno especial -1 , que indica ausencia de planificación.
    * La DateJourney se calcula exclusivamente según las reglas de descanso, sin considerar límites de turno.
  * Ejemplo : Un empleado sin planificación ficha el 31/07/2025 a las 10:00.
    * Turno asignado: -1.
    * DateJourney: Calculada según MinBreakBetweenWorkingDays o HoursUntilNewWorkday.

## 3\. Parámetros que Controlan la Asignación de DateJourney

La asignación de DateJourney se basa en dos parámetros configurables que determinan cuándo un fichaje pertenece a una nueva jornada o continúa en la jornada anterior.

### 3.1. MinBreakBetweenWorkingDays

Este parámetro define el descanso mínimo en horas que debe existir entre dos fichajes consecutivos (f-1 y f) para que el fichaje actual (f) inicie una nueva jornada.

  * Características clave :
    * Se aplica entre el CheckTime del fichaje actual (f) y el CheckTime del fichaje inmediatamente anterior (f-1), independientemente de si están en el mismo día natural o en días distintos.
    * Para que se inicie una nueva jornada:
      * La diferencia horaria entre los CheckTime de f y f-1 debe ser mayor o igual al valor configurado.
      * La fecha natural del CheckTime de f debe ser distinta a la DateJourney del fichaje anterior (f-1).
    * Si ambos fichajes tienen la misma fecha natural en CheckTime y esa fecha coincide con la DateJourney de f-1, no se inicia una nueva jornada, incluso si la separación horaria supera el parámetro.
  * Ejemplo práctico : Supongamos que MinBreakBetweenWorkingDays = 8 horas.
    * Caso 1: Fichajes en el mismo día natural, misma DateJourney.
      * f-1: CheckTime = 29/07/2025 08:00, DateJourney = 29/07/2025.
      * f: CheckTime = 29/07/2025 20:30 (12,5 horas de diferencia).
      * Resultado: No se inicia nueva jornada porque CheckTime de f (29/07/2025) coincide con DateJourney de f-1 (29/07/2025). DateJourney de f = 29/07/2025.
    * Caso 2: Fichajes en días distintos, DateJourney distinta.
      * f-1: CheckTime = 29/07/2025 22:00, DateJourney = 29/07/2025.
      * f: CheckTime = 30/07/2025 12:00 (14 horas de diferencia).
      * Resultado: Se inicia nueva jornada porque la diferencia es ≥ 8 horas y CheckTime de f (30/07/2025) es distinta a DateJourney de f-1 (29/07/2025). DateJourney de f = 30/07/2025.
    * Caso 3: Fichajes en días distintos, sin suficiente descanso.
      * f-1: CheckTime = 29/07/2025 22:00, DateJourney = 29/07/2025.
      * f: CheckTime = 30/07/2025 02:00 (4 horas de diferencia).
      * Resultado: No se inicia nueva jornada porque la diferencia es < 8 horas. DateJourney de f = 29/07/2025.

### 3.2. HoursUntilNewWorkday

Este parámetro define el máximo tiempo en horas que puede transcurrir desde el primer fichaje de una jornada hasta un fichaje posterior para que este siga perteneciendo a la misma jornada.

  * Características clave :
    * Solo se aplica cuando hay un cambio de fecha natural entre el CheckTime del fichaje actual y el primer fichaje de la jornada anterior.
    * Requiere que el parámetro esté configurado con un valor mayor que 0.
    * Compara el CheckTime del fichaje actual con el CheckTime del primer fichaje de la jornada anterior (no con el fichaje inmediatamente anterior).
    * Si la diferencia horaria es mayor o igual al valor configurado, el fichaje actual inicia una nueva jornada (DateJourney = fecha natural de CheckTime).
    * Si la diferencia es menor, el fichaje actual se asigna a la DateJourney de la jornada anterior, incluso si su CheckTime está en un día diferente.

  * Ejemplo práctico : Supongamos que HoursUntilNewWorkday = 12 horas.
    * Caso 1: Jornada larga con cambio de fecha.
      * Primer fichaje de la jornada: CheckTime = 31/07/2025 08:00, DateJourney = 31/07/2025.
      * Fichaje actual: CheckTime = 01/08/2025 02:00 (18 horas de diferencia).
      * Resultado: Se inicia nueva jornada porque 18 horas ≥ 12 horas. DateJourney = 01/08/2025.
    * Caso 2: Jornada nocturna sin superar el límite.
      * Primer fichaje de la jornada: CheckTime = 31/07/2025 20:00, DateJourney = 31/07/2025.
      * Fichaje actual: CheckTime = 01/08/2025 05:00 (9 horas de diferencia).
      * Resultado: No se inicia nueva jornada porque 9 horas < 12 horas. DateJourney = 31/07/2025.

## 4\. Proceso de Asignación de DateJourney

Cuando se registra un nuevo fichaje, el sistema sigue esta secuencia para determinar su DateJourney:

  1. Comprobar si es el primer fichaje :
     * Si el fichaje es el primero en la ventana de cálculo (no hay fichajes previos en la jornada), se asigna DateJourney = fecha natural de CheckTime.
  2. Evaluar si hay cambio de fecha natural :
     * Si el CheckTime del fichaje actual tiene una fecha natural distinta al primer fichaje de la jornada anterior:
       * Se aplica HoursUntilNewWorkday :
         * Compara el CheckTime del fichaje actual con el CheckTime del primer fichaje de la jornada anterior.
         * Si la diferencia es ≥ HoursUntilNewWorkday → DateJourney = fecha natural de CheckTime (nueva jornada).
         * Si la diferencia es < HoursUntilNewWorkday → DateJourney = DateJourney de la jornada anterior.
  3. Si no hay cambio de fecha o tras evaluar HoursUntilNewWorkday :
     * Se aplica MinBreakBetweenWorkingDays :
       * Compara el CheckTime del fichaje actual con el CheckTime del fichaje inmediatamente anterior.
       * Si la diferencia es ≥ MinBreakBetweenWorkingDays y la fecha natural de CheckTime del fichaje actual es distinta a la DateJourney del fichaje anterior → DateJourney = fecha natural de CheckTime (nueva jornada).
       * Si no se cumplen ambas condiciones → DateJourney = DateJourney del fichaje anterior.

## 5\. Ejemplo Completo con Ambos Parámetros

Supongamos los siguientes parámetros:

  * MinBreakBetweenWorkingDays = 8 horas.
  * HoursUntilNewWorkday = 12 horas

Escenario : Un empleado sin planificación realiza los siguientes fichajes:

  * 31/07/2025 08:00 (Entrada): Es el primer fichaje, por lo que DateJourney = 31/07/2025, turno = -1.
  * 31/07/2025 10:00 (Salida): Diferencia con el anterior = 2 horas < 8 horas, misma fecha natural y DateJourney anterior = 31/07/2025 → DateJourney = 31/07/2025, turno = -1.
  * 31/07/2025 10:20 (Entrada): Diferencia con el anterior = 20 minutos < 8 horas, misma fecha natural y DateJourney anterior = 31/07/2025 → DateJourney = 31/07/2025, turno = -1.
  * 31/07/2025 22:00 (Salida): Diferencia con el anterior = 11,67 horas ≥ 8 horas, pero CheckTime (31/07/2025) coincide con DateJourney anterior (31/07/2025) → DateJourney = 31/07/2025, turno = -1.
  * 01/08/2025 02:00 (Salida): Hay cambio de fecha natural, por lo que se aplica HoursUntilNewWorkday:
    * Diferencia con el primer fichaje de la jornada (31/07/2025 08:00) = 18 horas ≥ 12 horas → DateJourney = 01/08/2025 (nueva jornada), turno = -1.

Conclusión del ejemplo : El fichaje del 01/08/2025 a las 02:00 inicia una nueva jornada porque supera el límite de HoursUntilNewWorkday respecto al primer fichaje de la jornada anterior, a pesar de que la diferencia con el fichaje inmediatamente anterior (31/07/2025 22:00) es solo 4 horas, menor que MinBreakBetweenWorkingDays.

## 6\. Resumen y Notas Importantes

  * Asignación de turnos :
    * Empleados planificados: Siempre se asigna el turno planificado, independientemente de si el fichaje está dentro o fuera de los límites del turno.
    * Empleados sin planificación: Siempre se asigna turno -1.
  * Asignación de DateJourney :
    * MinBreakBetweenWorkingDays : Evalúa la separación horaria entre fichajes consecutivos. Solo genera nueva jornada si la fecha natural de CheckTime es distinta a la DateJourney del fichaje anterior y la diferencia horaria es suficiente.
    * HoursUntilNewWorkday : Solo se aplica con cambio de fecha natural y si el parámetro es > 0\. Compara el fichaje actual con el primer fichaje de la jornada anterior para decidir si continuar en la misma jornada o iniciar una nueva.
  * Notas adicionales :
    * Si HoursUntilNewWorkday está configurado en 0, esta regla no se aplica, y la asignación de DateJourney depende exclusivamente de MinBreakBetweenWorkingDays.
    * El sistema garantiza que los fichajes se agrupen correctamente en jornadas laborales coherentes, respetando las normativas de descanso y los horarios planificados.
