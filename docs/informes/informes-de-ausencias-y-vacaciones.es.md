---
title: Ausencias y vacaciones
---
# Informes de ausencias y vacaciones

Informes del grupo **Ausencias y vacaciones** del botón **Informes** de la lista de empleados (`Menú lateral > Empleados`). Todos se calculan sobre los empleados que muestra la lista con los filtros que tengas aplicados. Consulta el [catálogo de informes](catalogo-de-informes.es.md) para ver cómo se lanzan.

## Saldos de vacaciones

Excel con el saldo de vacaciones de cada empleado en un año.

| Filtro | Descripción |
| --- | --- |
| Año | Obligatorio. Año del saldo, entre 2000 y 2099. |

| Columna | Descripción |
| --- | --- |
| ID empleado, Código, Nombre completo | Identificación del empleado. |
| Empresa, Oficina, Unidad, Grupo, Puesto | Organización del empleado. |
| Días generados | Días de vacaciones que corresponden al empleado en el año. |
| Días disfrutados | Días ya disfrutados. |
| Días pendientes | Días que le quedan por disfrutar. |
| Años anteriores | Días que arrastra de años anteriores. |
| Bolsa comp. (d), Bolsa comp. (h) | Compensación desde la bolsa de horas, en días y en horas. |
| Ajuste | Ajustes manuales del saldo. |
| Reconocimiento festivos | Días reconocidos por festivos. |
| Sin disfrutar año ant. | Días no disfrutados del año anterior. |
| Otros días | Otros días que suman al saldo. |

La última fila muestra los totales.

## Calendario de ausencias por grupo

Excel con el calendario de un mes: los empleados agrupados por grupo o departamento en filas y los días del mes en columnas. Cada celda muestra el código de la ausencia de ese día. Sirve para ver de un vistazo quién falta cada día en cada equipo.

| Filtro | Descripción |
| --- | --- |
| Mes | Obligatorio. Mes del calendario. |

| Código | Significado |
| --- | --- |
| VAC | Vacaciones |
| IT | Baja médica |
| PR | Permiso retribuido |
| PNR | Permiso no retribuido |
| AUS | Ausencia |

## Horas de ausencia según horario

Excel con las horas de ausencia de cada empleado en un periodo, calculadas según su horario.

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Obligatorio. Último día del periodo. |

!!! warning "Solo jornadas validadas"
    El informe solo incluye las ausencias de jornadas validadas. Si no aparecen datos, valida primero las jornadas de los empleados.

Por cada empleado y tipo de ausencia se muestran los días, las horas parciales y las horas totales. Al final hay un resumen por tipo de ausencia.

## Detalle de ausencias por período <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span> { #detalle-de-ausencias-por-periodo }

Excel con todas las ausencias de un periodo, con subtotales por empleado y un resumen por tipo de ausencia. Está pensado para analizar el absentismo.

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Obligatorio. Último día del periodo. |
| Mostrar vacaciones, Mostrar ausencias, Mostrar permisos, Mostrar bajas por enfermedad | Interruptores. Tipos de registro que se incluyen. Por defecto, todos activados. |

El informe tiene dos partes:

- **Resumen por tipo de ausencia**: registros, días totales, horas totales y porcentaje sobre el total de horas teóricas de cada tipo.
- **Detalle**: cada ausencia con el empleado, las fechas de inicio y fin, los días, las horas, el porcentaje de la jornada, el tipo, el grupo y la categoría de ausencia, si está pendiente de aprobación, la oficina, el departamento, el puesto y el motivo. Si una ausencia empieza o termina fuera del periodo, se indica hasta cuándo continúa. Cada empleado tiene su subtotal.

## Permisos de empleados <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span> { #permisos-de-empleados }

PDF con las bajas de los empleados en un periodo.

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Opcional. Último día del periodo. |

El informe empieza con un resumen (total de bajas, en curso y cerradas) y sigue con el detalle de cada baja: empleado, fechas de inicio y fin, días totales, causa y tipo de baja.

<!-- PENDIENTE: el botón se llama "Permisos de empleados" pero el informe que genera es "Informe de Bajas de Empleados". Confirmar con desarrollo el nombre correcto. -->
