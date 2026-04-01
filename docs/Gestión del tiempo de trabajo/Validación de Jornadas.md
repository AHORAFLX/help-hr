# Validación de Jornadas

### Por qué es importante y cómo afecta al cálculo de tiempos y reportes



### ¿Qué significa validar una jornada?

Cada día, el sistema registra automáticamente la actividad de cada empleado:

  * • Fichajes de entrada y salida
  * • Ausencias o permisos
  * • Planificación del turno
  * • Pausas u otras incidencias

Mientras la jornada no está validada, permanece abierta , lo que significa que el sistema recalcula las horas en tiempo real cada vez que se consulta un listado o informe.

✔ Validar una jornada confirma que los datos del día son correctos y los deja como definitivos.



### ⚙ ¿Qué ocurre al validar una jornada?

Cuando se valida una jornada:

  1. ? El sistema guarda los cálculos (horas trabajadas, teóricas, ausencias, balances, etc.).
  2. ? Los informes dejan de recalcular y leen los valores ya guardados.
  3. ⚡ El rendimiento mejora: las consultas se vuelven mucho más rápidas.



### ? Beneficio principal: más velocidad y estabilidad

Cuando una jornada está abierta , el sistema recalcula todo cada vez (fichajes, ausencias, planificación y pausas).  
Cuando está validada , los valores ya están almacenados.

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;"><thead><tr style="background:#f2f2f2;"><th>Tipo de jornada</th><th>Jornadas procesadas</th><th>Tiempo medio</th></tr></thead><tbody><tr><td>Abiertas (sin validar)</td><td>1.000</td><td>15–20 segundos</td></tr><tr><td>Validadas</td><td>1.000</td><td>1–2 segundos</td></tr></tbody></table>

 


### ? ¿Qué pasa si modifico datos después de validar?

Una vez validada, la jornada se considera cerrada y consolidada.  
Por tanto:

⚠ Los cambios realizados después de validar no se reflejarán automáticamente.

Ejemplos de cambios que no se aplican de forma inmediata:

  * ➕ Añadir o modificar una ausencia o permiso
  * • Cambiar datos del turno
  * • Ajustar la planificación diaria

→ Estos cambios no afectarán a las jornadas validadas hasta ejecutar un proceso de recálculo.



### ? ¿Qué es el proceso de recálculo?

El recálculo actualiza las jornadas validadas cuando se han hecho cambios relevantes.

Durante este proceso:

  1. • El sistema relee los nuevos datos (fichajes, ausencias y planificación).
  2. • Recalcula las horas teóricas, trabajadas y computables.
  3. • Actualiza los valores almacenados en la jornada validada.

? Utiliza el recálculo solo cuando se hayan realizado modificaciones importantes (por ejemplo, una ausencia añadida en un día ya validado).

 

### ? Beneficios de validar jornadas

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;"><thead><tr style="background:#f2f2f2;"><th>Beneficio</th><th>Descripción</th></tr></thead><tbody><tr><td>⚡ Rendimiento</td><td>Los informes se generan más rápido.</td></tr><tr><td>✔ Fiabilidad</td><td>Los datos quedan cerrados y estables.</td></tr><tr><td>? Trazabilidad</td><td>Se conserva el registro exacto de cada jornada.</td></tr><tr><td>? Control</td><td>Evita cambios accidentales en jornadas cerradas.</td></tr><tr><td>? Flexibilidad</td><td>Permite recalcular manualmente si es necesario.</td></tr></tbody></table>

 

 *

### ? Buenas prácticas recomendadas

  * ? Validar las jornadas periódicamente (diario o semanal).
  * ? Revisar fichajes y permisos antes de validar.
  * ? Evitar cambios en jornadas ya validadas, salvo que sea imprescindible.
  * ? Si hay cambios, ejecutar el proceso de recálculo.
  * ? Usar reportes de jornadas abiertas para controlar qué falta por validar.

 

### ? En resumen

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;"><thead><tr style="background:#f2f2f2;"><th>Estado</th><th>Cálculo</th><th>Rendimiento</th><th>Cambios posteriores</th></tr></thead><tbody><tr><td>Abierta</td><td>En tiempo real</td><td>Más lento</td><td>Se actualiza automáticamente</td></tr><tr><td>Validada</td><td>Datos guardados</td><td>Muy rápido</td><td>Requiere recálculo</td></tr></tbody></table>

 



### ? Conclusión

Validar las jornadas no solo confirma que los datos del día son correctos,  
sino que mejora el rendimiento del sistema y garantiza la coherencia de los informes.

  * ? Los cálculos quedan almacenados.
  * ⚙ Los listados y reportes se generan al instante.
  * ? Cualquier cambio posterior requiere un recálculo controlado.

✔ Validar es asegurar y acelerar.