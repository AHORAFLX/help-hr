# Guía de Incidencias de Jornada

##   

### 1\. ¿Qué es una Incidencia?

Una incidencia es cualquier situación o error que impide el cálculo correcto de la jornada laboral de un empleado. El sistema las detecta automáticamente para avisarte de que algo requiere tu atención.

Ejemplos comunes:

  * Errores de fichaje: Olvidar fichar a la salida, fichar dos veces la entrada.
  * Errores de planificación: Trabajar en un día festivo no planificado, o faltar un día laborable.
  * Alertas de integridad: Cambios realizados en días que ya estaban "Cerrados" y validados.



### 2\. Tipos de Incidencias que verás

El sistema clasifica las incidencias en 3 grupos para ayudarte a priorizar:

### ? Incidencias Críticas (Integridad)

Son las más importantes. Indican que se ha modificado información en días que ya se daban por "cerrados".

  * Ejemplo: Añadir manual un fichaje en una nómina ya cerrada.
  * Acción requerida: Revisar urgentemente y volver a calcular el día.

### ? Incidencias de Fichaje (Marking)

Problemas con los datos que vienen del reloj o app de fichaje.

  * Ejemplo: "Entrada duplicada", "Secuencia ilógica" (Entrada → Entrada).
  * Acción requerida: Corregir los fichajes manualmente.

### ? Incidencias de Jornada (Workday)

El sistema ha calculado el día y ha encontrado discrepancias.

  * Ejemplo: "Faltan fichajes" (día incompleto), "Trabajo en festivo".
  * Acción requerida: Justificar la ausencia o corregir el turno.



### 3\. ¿Cómo resolver una incidencia?

El proceso general es muy sencillo: Corregir y Recalcular.

### Paso 1: Identificar el problema

En tu panel de control o en la ficha del empleado, verás un icono de alerta (⚠️) junto a la fecha. Pasa el ratón por encima para leer el problema (ej. "Fichaje impar").

### Paso 2: Corregir la causa

  * Si faltan fichajes, añádelos manualmente.
  * Si el horario es incorrecto, cambia el turno.
  * Si es una alerta de integridad, verifica que el cambio es autorizado.

### Paso 3: Recalcular (¡Importante!)

Una vez corregido el dato, el sistema necesita "darse cuenta".

  1. Pulsa el botón Recalcular (a veces aparece como una flecha circular ?).
  2. El sistema procesará de nuevo el día.
  3. Si todo está bien, la incidencia desaparecerá automáticamente.

NOTE

No necesitas "borrar" la incidencia. Al corregir el error y recalcular, el sistema la elimina sola.



### 4\. Preguntas Frecuentes

P: He corregido el fichaje pero la alerta sigue ahí.

R: ¿Has pulsado "Recalcular"? El sistema no adivina cuándo has terminado. Necesitas forzar el recálculo para que limpie la alerta.

P: Me aparece "Fichaje en día Consolidado". ¿Qué es?

R: Significa que alguien ha tocado un día que ya estaba enviado a nómina. Esta es una alerta de seguridad para que sepas que la nómina podría estar mal calculada en esa fecha.

P: ¿Puedo ignorar una incidencia?

R: Las incidencias informativas (azules) no afectan al cálculo. Las naranjas y rojas sí, y si no las arreglas, el saldo de horas del empleado será incorrecto.