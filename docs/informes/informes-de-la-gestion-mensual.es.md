# Informes de la gestión mensual

En `Menú lateral > Gestión Mensual`, al abrir un día se muestra la gestión de fichajes de esa jornada. Su botón **Informes** agrupa los informes en dos bloques, **PDF** y **EXCEL**. Los informes incluyen los empleados que muestra la pantalla, con los filtros que tengas aplicados.

A diferencia de los informes de la lista de empleados, estos informes están disponibles también para el rol *Manager*.

## Informes en PDF

| Informe | Descripción |
| --- | --- |
| Informe de registro de horas | Todos los fichajes, agrupados por empleado y día. Es el mismo informe que se describe en [Informes de control horario](informes-de-control-horario.es.md#informe-de-registro-de-horas). |
| Informe de jornadas diarias | Jornada consolidada de cada empleado y día. Es el mismo informe que se describe en [Informes de control horario](informes-de-control-horario.es.md#informe-de-jornadas-diarias). |

En estos dos informes, las fechas de inicio y fin se rellenan con el día abierto, y puedes cambiarlas antes de lanzar el informe.

## Informes en Excel

Los informes en Excel toman directamente las fechas de la pantalla y no piden ningún filtro. No incluyen los días libres del empleado. Todos tienen las columnas de identificación y organización (ID emp., Nombre completo, Código, Empresa, Oficina, Unidad y Grupo) y las de la jornada (Fecha, Día, Turno, Estado, Primera entrada y Última salida), además de las columnas propias de cada informe.

<!-- PENDIENTE: confirmar qué periodo toman los informes Excel ({{StartDate}} y {{EndDate}} de la página) cuando se abre un único día desde la gestión mensual. -->

| Informe | Columnas propias |
| --- | --- |
| Horas trabajadas | Horas teóricas, trabajadas y de ausencia, y saldo en minutos. |
| Horas trabajadas y extras | Horas teóricas, trabajadas, extra y de ausencia, y saldo en minutos. |
| Horas trabajadas (por día incluyendo exceso) | Horas teóricas, trabajadas, computables, de exceso y de ausencia, y saldo en minutos. |
| Horario no cumplido | Inicio y fin del turno, horas teóricas, trabajadas y que faltan, y minutos que faltan. Solo incluye los días en que el empleado ha trabajado menos horas de las teóricas. |
| Total horas presencia por periodo | Una fila por empleado con el número de días y el total de horas de presencia, trabajadas, teóricas y de ausencia, y el saldo total en minutos. |

El botón *Horas presencia diarias* aparece en el menú pero está deshabilitado.

!!! note "Informes anteriores"
    Estos informes sustituyen a los antiguos *Horas trabajadas (por día)*, *Horas trabajadas (por periodo)* y *Vacaciones (por período)*. Para los saldos y periodos de vacaciones, usa los [informes de ausencias y vacaciones](informes-de-ausencias-y-vacaciones.es.md).
