# CLASIFICACIÓN DE FICHAJES Y GESTIÓN DE TIEMPO NO EFECTIVO

### BORRADOR A FALTA DE REVISION

  

A partir de esta actualización, la aplicación incorpora un sistema avanzado para clasificar los fichajes según el tipo de actividad realizada.  
Este cambio permite mejorar el control horario, separar el tiempo realmente trabajado del tiempo no efectivo y reflejarlo correctamente en informes, jornadas y visualizaciones.



## 1\. ¿Qué es la clasificación de fichajes?

Cuando un empleado realiza un fichaje (entrada o salida), ahora puede quedar asociado a una categoría de trabajo.

  
Cada clase identifica el tipo de tiempo registrado.

Hay dos grandes grupos:

### ✔️ Tiempo efectivo

Tiempo que se considera trabajo real y computa directamente para:

  * Horas trabajadas

  * Cálculo de jornada

  * Informes laborales

  * Retribución / coste

Ejemplos:

  * Trabajo normal

  * Horas nocturnas

  * Horas extra

  * Guardia activa

### ❌ Tiempo no efectivo

Tiempo que se registra dentro de la jornada pero no cuenta como tiempo trabajado.

Ejemplos:

  * Esperas no productivas

  * Tiempo muerto

  * Pausas no retribuidas

  * Viajes sin actividad laboral

  * Formación no computable

 *

## 2\. ¿Qué aporta esta nueva funcionalidad?

Ahora la aplicación permite:

### Separar claramente tiempo efectivo y no efectivo

El sistema diferencia automáticamente ambos tipos de horas al generar:

  * Pares (entrada/salida)

  * Horas calculadas

  * Informes

  * Resúmenes diarios

### Visibilidad total en la jornada

Aunque no computen como tiempo efectivo, los fichajes no efectivos siguen asignados a la jornada , para mantener:

  * Coherencia cronológica

  * Trazabilidad

  * Visualización correcta en el día del empleado

### Cálculos de horas más precisos

El tiempo no efectivo ya no suma en:

  * Horas trabajadas

  * Productividad

  * Retribuciones

  * Cómputos de turnos

 

## 3\. ¿Cómo funciona para el usuario?

### ➤ No tienes que hacer nada nuevo

Los fichajes se siguen registrando exactamente igual:

  * Desde la app

  * Desde terminales

  * Desde API

  * Desde carga masiva

La clasificación se asigna de manera:

  * Automática (según reglas internas)

  * Por dispositivo o sistema externo (si lo envía)

  * Editando el fichaje (si el usuario tiene permisos)

 

## 4\. ¿Cómo puedo ver la clasificación de un fichaje?

En las pantallas de asistencia aparecerá un nuevo campo:

### “Clase de fichaje” o “Tipo de actividad”

Se mostrará con etiquetas como:

  * Trabajo efectivo

  * Tiempo no efectivo

  * Formación

  * Desplazamiento

  * Pausa no retribuida

  * Guardia inactiva  
  según la configuración de tu empresa.

 

## 5\. Cómo afecta a la jornada del empleado

### ✔ Se asigna siempre a una jornada

El sistema sigue determinando la jornada (datejourney) igual que antes.  
Incluso para los fichajes "no efectivos", el sistema necesita saber a qué día/jornada pertenecen.

Esto permite:

  * Consultar la línea temporal del día

  * Revisar todos los fichajes en orden

  * Identificar pausas o tiempos inactivos

### ✔ Se crean pares Entrada–Salida igualmente

Si un fichaje de entrada es no efectivo, su salida también quedará en la misma categoría para mantener consistencia.

 

## ⛔ 6\. Cómo NO afecta esta clasificación

Los fichajes de tiempo no efectivo NO afectan a:

  * Total de horas trabajadas

  * Horas extra

  * Cálculo de productividad

  * Cálculo de coste

  * Balance mensual

Solo se usan para documentar el día, no para computar horas laborales.

 

## 7\. ¿Dónde se refleja en los informes?

En resúmenes de jornada:

  * Se muestran todos los fichajes

  * Se separan visualmente los no efectivos

En informes de horas trabajadas:

  * Solo se suman los efectivos

  * Los no efectivos aparecen aparte (si el informe los contempla)

En auditoría:

  * Se ve su clasificación original



## 8\. Ejemplos prácticos

### Ejemplo 1: Entrada no efectiva

  * 08:00 — Entrada (Tiempo No Efectivo – Espera)

  * 08:15 — Salida  
Resultado:  
El sistema registra la pausa, pero no suma 15 minutos al tiempo trabajado.



### Ejemplo 2: Mezcla de fichajes

<table><thead><tr><th>Hora</th><th>Tipo</th><th>Clasificación</th><th>Cuenta en horas</th></tr></thead><tbody><tr><td>09:00</td><td>Entrada</td><td>Trabajo</td><td>✔ Sí</td></tr><tr><td>11:00</td><td>Salida</td><td>Trabajo</td><td>✔ Sí</td></tr><tr><td>11:15</td><td>Entrada</td><td>No efectivo</td><td>✖ No</td></tr><tr><td>11:45</td><td>Salida</td><td>No efectivo</td><td>✖ No</td></tr><tr><td>12:00</td><td>Entrada</td><td>Trabajo</td><td>✔ Sí</td></tr><tr><td>15:00</td><td>Salida</td><td>Trabajo</td><td>✔ Sí</td></tr></tbody></table>

 

Resultado:

  * Total trabajado: 5 horas

  * Tiempo no efectivo: 30 minutos (se muestra, pero no suma)



## 9\. ¿Qué cambia para ti?

Para el usuario final:

  * Nada se complica

  * Los fichajes se siguen registrando igual

  * La app muestra más información útil

  * Las horas se calculan de forma más justa y detallada

 

## Si tienes permisos de administrador…

Ahora puedes:

  * Ver qué fichajes son efectivos y cuáles no

  * Editar su clasificación

  * Controlar el tiempo no productivo

  * Generar informes más completos

 

## Conclusión

La nueva funcionalidad mejora la precisión del control horario sin cambiar la forma en que los empleados fichan.  
Permite diferenciar claramente el tiempo productivo del no productivo, mejora los informes y da más claridad a la gestión laboral.

