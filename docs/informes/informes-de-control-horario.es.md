---
title: Control horario
---
# Informes de control horario

Informes de los grupos **Control de tiempos** y **Planificación y turnos** del botón **Informes** de la lista de empleados (`Menú lateral > Empleados`). Todos se calculan sobre los empleados que muestra la lista con los filtros que tengas aplicados. Consulta el [catálogo de informes](catalogo-de-informes.es.md) para ver cómo se lanzan.

## Informe de registro de horas

PDF con todos los fichajes del periodo, agrupados por empleado y por día de jornada. Sirve para revisar en detalle qué ha fichado cada empleado.

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Obligatorio. Último día del periodo. |

Por cada fichaje se muestran la fecha, la hora, el tipo (entrada, salida o ausencia), la ubicación y la nota que haya añadido el empleado, con el total de cada día.

Este informe también se puede lanzar desde la [gestión mensual](informes-de-la-gestion-mensual.es.md).

## Análisis de la pausa

PDF apaisado que compara los descansos que han hecho los empleados con los planificados en su turno, durante un mes.

| Filtro | Descripción |
| --- | --- |
| Periodo (Mes) | Obligatorio. Mes que se analiza. |

El informe tiene tres partes:

- **Resumen ejecutivo**: total de descansos, empleados, jornadas con descansos, minutos planificados y reales, desviación media y número de descansos excedidos (en rojo si hay alguno) y por debajo del plan.
- **Resumen por tipo de descanso**: para cada tipo, cuántos descansos hay, la media planificada y real en minutos y la desviación media.
- **Detalle por empleado**: cada descanso con fecha, inicio y fin planificados, inicio y fin reales, minutos planificados y reales, desviación, si es computable y el turno.

Un descanso se considera excedido cuando dura más de lo planificado.

## Informe de jornadas diarias

PDF con la jornada consolidada de cada empleado y día: turno, horas y estado de validación.

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Obligatorio. Último día del periodo. |

Por cada día se muestran la fecha, el día de la semana, el estado de la jornada (abierta o validada, o si es festivo o día libre), el turno, las entradas y salidas, las horas teóricas, trabajadas y de ausencia, el saldo y los detalles, con los totales al final.

Este informe también se puede lanzar desde la [gestión mensual](informes-de-la-gestion-mensual.es.md).

## Cumplimiento del teletrabajo

PDF que comprueba, mes a mes, si los empleados cumplen las reglas de teletrabajo que tienen asignadas. Las reglas se configuran en las [reglas de control de localizaciones](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/reglas-de-control-de-localizaciones.es.md).

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Obligatorio. Último día del periodo. |

!!! note "Solo empleados con incidencias"
    El informe solo muestra los empleados que tienen algún incumplimiento en el periodo.

El informe tiene dos partes:

- **Resumen ejecutivo**: por empleado, el departamento, el porcentaje de cumplimiento del periodo, los meses incumplidos y el estado anual (*Cumple* o *Revisión requerida* si ha incumplido algún mes).
- **Detalle por empleado**: por cada mes controlado, los días programados, los días incumplidos, el porcentaje de cumplimiento, el estado (*Cumple* o *Incumplido*) y la regla aplicada.

## Horas mensuales de los empleados

PDF con las horas computables de cada empleado en un mes, desglosadas por semana, con espacio para la firma del empleado.

| Filtro | Descripción |
| --- | --- |
| Mes | Obligatorio. Mes del informe. |
| ¿Incluir detalles de fichajes? | Si está activado, cada día incluye también los fichajes reales del empleado. |

Por cada empleado se muestra una tabla por día con el inicio y el fin, las horas computables y las pausas, con un subtotal por semana y el total de horas computables del mes. Al final hay un bloque de firma del empleado y otro de notas.

## Informe de desviación de marcas <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span> { #informe-de-desviacion-de-marcas }

PDF con los fichajes que se apartan del horario del turno: entradas y salidas antes o después de lo previsto y, opcionalmente, desviaciones en los descansos.

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Obligatorio. Último día del periodo. |
| Entrada anticipada, Entrada tardía, Salida anticipada, Salida tardía | Interruptores. Activa los tipos de desviación que quieres ver. |
| Tolerancia (para cada tipo) | Minutos de desviación a partir de los cuales se incluye el fichaje. Con 0 se incluye cualquier desviación. Por defecto: entrada anticipada 5, entrada tardía 0, salida anticipada 0 y salida tardía 5. |
| Descansos | Interruptor. Incluye las desviaciones en el inicio y el fin de los descansos. |
| Tolerancias de descansos | Minutos de tolerancia para el inicio y el fin de los descansos, antes o después de lo previsto. Por defecto, 5 en todos. |

La entrada que se compara es la primera del día, y la salida, la última. Por cada desviación se muestran la fecha, el tipo, la hora prevista, la hora fichada, la diferencia en minutos y el turno.

## Horas por turno y semana <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span> { #horas-por-turno-y-semana }

Excel con las horas agregadas por turno y por semana. Sirve para ver qué turnos cumplen las horas teóricas.

| Filtro | Descripción |
| --- | --- |
| Mes | Opcional. Si no se indica, se incluyen todos los periodos. |

| Columna | Descripción |
| --- | --- |
| Año, Mes, Semana | Periodo de la fila. |
| Turno, Alias | Turno al que corresponden las jornadas. |
| Empresa, Oficina | Organización de los empleados. |
| Nº Empleados, Nº Jornadas | Cuántos empleados y jornadas hay en ese turno y semana. |
| H. Trabajadas, H. Teóricas, H. Ausencia, Saldo (min) | Totales de horas y saldo. |
| Min. Trabajo, Min. Teóricos, Min. Ausencia | Los mismos totales en minutos. |
| H. Disponibilidad | Horas de disponibilidad. |
| Ratio Ef.% | Porcentaje de horas trabajadas sobre las teóricas. Se colorea en verde si es 100 % o más, en blanco entre 90 % y 99 % y en rojo por debajo de 90 %. |

## Planificación mensual de empleados

Excel con el calendario de un mes: una fila por empleado y una columna por día, con el alias del turno o de la ausencia de cada día y su color.

| Filtro | Descripción |
| --- | --- |
| Período | Obligatorio. Mes del calendario. |

La leyenda del informe usa estos códigos:

| Código | Significado |
| --- | --- |
| VAC | Vacaciones |
| BAJ | Baja |
| FES | Festivo |
| AUS | Ausencia |
| PER | Permiso |
| LIBRE | Día libre |

Los días de trabajo muestran el alias del turno planificado.
