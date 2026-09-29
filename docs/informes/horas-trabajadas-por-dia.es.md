# Horas trabajadas (por día)

Este informe proporciona un **excel** con información detallada sobre las horas trabajadas por cada empleado, agrupadas por día, dentro del periodo seleccionado.

![](../docs_assets/images/S2tglS7vA3bqw8bd5_tUbKlqtgAsArGAhA.png)

## Parámetros

| Parámetro | Descripción |
| --- | --- |
| Fecha de inicio | Primer día del periodo a consultar |
| Fecha final | Último día del periodo a consultar |

## Campos del informe

| Campo | Descripción |
| --- | --- |
| Id | Identificación única del empleado |
| Nombre del empleado | Nombre con apellidos del empleado |
| Fecha jornada | Jornada a la que pertenecen los fichajes. Es posible que fichajes de dos días diferentes pertenezcan a la misma jornada (por ejemplo, entrada a las 22:00 y salida a las 06:00 del día siguiente). |
| Horas computadas | Suma de las horas trabajadas más las horas de ausencias computables. |
| Horas planificadas | Horas planificadas para ese día, incluyendo las horas teóricas de trabajo más las ausencias computables. |
| Horas computadas y horas planificadas (decimal) | Lo mismo que los campos anteriores, pero expresado en formato decimal. |
| Porcentaje | Proporción de horas computadas sobre las horas planificadas, expresada en porcentaje. |
| Localización | Ubicación con mayor prevalencia en ese día. |
| Estado | Estado de los fichajes para ese día, con posibles valores: **Generado** (datos registrados pero no validados), **Validado** (datos revisados) o **En balance** (datos aprobados y en el balance diario). |

## Ejemplo

![](../docs_assets/images/V9nEIi-Ljfc0lQiaZSwD5e94l9NzMXdqHg.png)
