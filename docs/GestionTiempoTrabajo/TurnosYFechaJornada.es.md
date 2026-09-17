# Asignación de turnos y fecha de jornada en Fichajes.

## 1\. Introducción

En Sebastian HR, cada fichaje que realiza un empleado se guarda en la tabla de fichajes con dos campos clave:

  * CheckTime : Fecha y hora exacta en que el empleado ficha (dato real del fichaje).

  * DateJourney : Fecha de la jornada laboral a la que se asigna ese fichaje.  
Esta fecha puede coincidir con la de CheckTime o ser anterior (normalmente el día anterior cuando la jornada cruza medianoche).

La asignación de DateJourney y turno depende de si el empleado tiene planificación o no, y de dos parámetros configurables:  
`MinBreakBetweenWorkingDays` y `HoursUntilNewWorkday`.

## 2\. Tipos de empleados y su tratamiento

### 2.1 Empleados planificados

Estos empleados tienen asignado un turno para el día.

  * Si el fichaje está dentro de los límites del turno planificado → se asigna ese turno y la DateJourney planificada.

  * Si el fichaje está fuera de esos límites → igualmente se asigna el turno planificado, pero la DateJourney se calcula aplicando las reglas de separación de fichajes.

### 2.2 Empleados sin planificación

No tienen turno definido.

  * Siempre se asigna turno especial -1.

  * La DateJourney se calcula exclusivamente según las reglas  de separación de fichajes , sin comprobar límites de turno.

## 3\. Parámetros que influyen en la asignación

### 3.1 `MinBreakBetweenWorkingDays`

Este parámetro define el descanso mínimo en horas entre dos fichajes consecutivos para que el sistema considere que comienza una nueva jornada laboral.

Aspectos importantes:

  * No importa si los fichajes están en el mismo día natural o en días distintos: este parámetro se aplica siempre entre fichajes consecutivos.

  * No genera nueva jornada si:

    1. Ambos fichajes tienen la misma fecha en CheckTime.

    2. Esa fecha de CheckTime es la misma que la DateJourney del fichaje anterior (f‑1).

  * Solo genera nueva jornada si:

    1. La fecha natural de CheckTime del nuevo fichaje es distinta a la DateJourney del fichaje anterior.

    2. Y la diferencia de horas entre ambos fichajes es mayor o igual al valor configurado.

Este parámetro sirve para detectar descansos largos dentro de un mismo ciclo laboral.

### 3.2 `HoursUntilNewWorkday`

Este parámetro controla cuándo un fichaje debe considerarse como parte de una nueva jornada laboral después de un cambio de fecha natural.

Características clave:

  * Solo se aplica si hay cambio de fecha natural entre el fichaje actual y el primer fichaje de la jornada anterior.

  * El valor debe ser mayor que 0 para que la regla se aplique.

  * Compara el CheckTime del fichaje actual con el CheckTime del primer fichaje de la jornada anterior.

  * Si la diferencia en horas es mayor o igual al valor configurado:

    * El fichaje actual inicia una nueva jornada (DateJourney = fecha natural de CheckTime).

  * Si la diferencia es menor:

    * El fichaje actual se asigna a la misma DateJourney que el de la jornada anterior, aunque haya cambio de fecha natural.

Este parámetro es el que permite que, aunque un fichaje ocurra pasada la medianoche, se siga considerando parte de la jornada anterior si todavía no ha pasado el tiempo mínimo configurado desde el primer fichaje de esa jornada.

## 4\. Lógica de decisión para asignar DateJourney

Cada vez que se inserta un fichaje, el sistema:

  1. Comprueba si es el primer fichaje del empleado en la ventana de cálculo:

     * Si lo es → la DateJourney será la fecha natural del CheckTime.

  2. Si no es el primer fichaje:

     * Si hay cambio de fecha natural :

       * Aplica la regla de HoursUntilNewWorkday comparando con el primer fichaje de la jornada anterior.

       * Si se supera el umbral → nueva jornada con fecha natural del fichaje.

       * Si no se supera → se mantiene la DateJourney de la jornada anterior.

     * Haya o nocambio de fecha natural :

       * Aplica la regla de MinBreakBetweenWorkingDays comparando con el fichaje anterior.

       * Si se supera el umbral y las fechas de CheckTime y DateJourney no son iguales → nueva jornada.

       * Si no se cumplen las condiciones → se mantiene la DateJourney de la jornada anterior.

## 5\. Resumen

  * Empleados planificados : Turno planificado siempre, fecha de jornada calculada según límites de turno o reglas de descanso.

  * Empleados sin planificación : Turno -1 siempre, fecha de jornada calculada exclusivamente por reglas de descanso.

  * MinBreakBetweenWorkingDays : Evalúa descansos largos entre fichajes consecutivos, independientemente del cambio de día natural, pero solo crea nueva jornada si la fecha de CheckTime es distinta a la DateJourney anterior.

  * HoursUntilNewWorkday : Solo con cambio de fecha natural y parámetro > 0; compara con primer fichaje de jornada anterior para decidir si iniciar nueva jornada.