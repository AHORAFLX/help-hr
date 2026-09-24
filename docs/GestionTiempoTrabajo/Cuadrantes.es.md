# Cuadrantes

El cuadrante es una herramienta para planificar, gestionar y controlar la jornada laboral de los empleados. Permite comparar lo previsto con lo realmente trabajado, detectar desviaciones y garantizar el cumplimiento de convenios laborales.

![](../docs_assets/images/s9-Ftl6LSce-8eQ7bybotJPtevl0d-JRpg.png)

## Estructura del cuadrante

### Información del contrato

Esta sección muestra los datos contractuales del empleado durante el periodo del cuadrante:

- **Fechas del contrato**: rango de días en los que el contrato está activo dentro del cuadrante.
- **Max Horas (máximas a realizar)**: desglosadas en dos líneas:
    - **Línea Superior**: horas que marca el convenio como obligación estándar. Variables que la afectan:
        - Duración del contrato (si < 365 días)
        - % de jornada (si < 100%)
    - **Línea Inferior**: cálculo: `Horas Planificadas Totales - Horas de Vacaciones Pendientes de Solicitar`
- **Vacaciones Pendientes de Solicitar**: se calcula multiplicando los días de vacaciones no solicitados por las horas/día según convenio.

### Detalle de horas

Muestra el desglose de las horas asignadas, trabajadas, ajustadas y ausentes:

| Campo | Descripción |
| --- | --- |
| Planificado | Turnos asignados al empleado menos vacaciones aceptadas y festivos del calendario. |
| Teórico | Resultado de: `Planificado - Ausencias Remuneradas - Permisos - Bajas` |
| Presencia | Tiempo real fichado por el empleado. |
| Extra | Horas extra validadas por el responsable. |
| Ajustes | Modificaciones manuales aplicadas (por regularización, correcciones, etc.). |
| Neto | Cálculo: `Presencia - Extras + Ajustes` |
| Ausencias | Horas de ausencias justificadas o injustificadas (parciales o completas). |
| Bajas | Horas en días donde el empleado ha estado de baja médica. |
| Vacaciones | Horas correspondientes a vacaciones aprobadas y registradas. |
| Balance | Diferencia entre lo que se esperaba y lo que realmente se ha realizado: `Neto - Teórico` |

## ¿Para qué sirve el cuadrante?

- Controlar el cumplimiento de horarios.

- Validar si se han cubierto las horas obligatorias según el convenio.

- Gestionar las ausencias y bajas de forma clara.

- Validar horas extra o compensaciones.

- Detectar desviaciones en planificación vs. realidad.

- Obtener un resumen fiable para nóminas, informes y auditorías internas.
