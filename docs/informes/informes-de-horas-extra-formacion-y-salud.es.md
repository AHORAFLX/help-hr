# Informes de horas extra, formación y salud

Informes de los grupos **Horas extra y banco de horas**, **Capacitación** y **Salud ocupacional** del botón **Informes** de la lista de empleados (`Menú lateral > Empleados`). Todos se calculan sobre los empleados que muestra la lista con los filtros que tengas aplicados. Consulta el [catálogo de informes](catalogo-de-informes.es.md) para ver cómo se lanzan.

## Registro de horas extras <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span> { #registro-de-horas-extras }

Excel con las horas extra registradas en un periodo y su estado de validación. Más información sobre cómo se generan en [Gestión de tiempo extra](../horas/gestion-de-tiempo-extra.es.md).

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Obligatorio. Último día del periodo. |

| Columna | Descripción |
| --- | --- |
| ID emp., Nombre completo, Código | Identificación del empleado. |
| Empresa, Oficina | Organización del empleado. |
| Fecha | Día de la jornada. |
| Tipo de hora extra | Tipo de hora extra aplicado. |
| ¿Adicional? | Indica si son horas adicionales. |
| Horas extra, Horas cómputo, Horas adicionales | Horas registradas, horas que computan y horas adicionales. |
| Validado, Validado por, Fecha validación | Si las horas están validadas, quién las validó y cuándo. |

La última fila muestra los totales.

## Estado de bolsas de horas <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span> { #estado-de-bolsas-de-horas }

Excel con las bolsas de horas de los empleados y su saldo. Más información en [Bolsa de horas](../horas/bolsa-de-horas.es.md).

| Filtro | Descripción |
| --- | --- |
| Estado de Bolsa | Opcional. Limita el informe a las bolsas en un estado concreto. Si se deja vacío, se incluyen todas. |

| Columna | Descripción |
| --- | --- |
| ID bolsa | Identificador de la bolsa. |
| ID emp., Código, Nombre completo | Identificación del empleado. |
| Empresa, Oficina | Organización del empleado. |
| Fecha bolsa | Fecha de la bolsa. |
| Horas acumuladas | Horas que han entrado en la bolsa. |
| Horas disfrutadas | Horas ya disfrutadas. |
| Saldo pendiente | Horas que quedan por compensar. En verde si es positivo y en rojo si es negativo. |
| Horas directas, Días disfrutados, Horas en días | Detalle de cómo se han disfrutado las horas: directamente en horas o en días completos. |
| Estado, Comentario | Estado de la bolsa y observaciones. |

## Cursos y asistentes

Excel con los cursos de formación y los empleados que asisten a cada uno.

| Filtro | Descripción |
| --- | --- |
| Año (opcional) | Si se indica, solo incluye los cursos que empiezan ese año. |

Por cada curso y asistente se muestran el ID y el nombre del curso, la categoría, el tipo, el estado, las fechas de inicio y fin, el empleado (ID, código y nombre), si ha confirmado, si ha aprobado, si ha sido evaluado, la puntuación, la empresa y el departamento.

## Historial de capacitación por empleado

PDF con la formación que ha recibido cada empleado de la lista, con una ficha por empleado.

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Obligatorio. Último día del periodo. |

Incluye los cursos que empiezan dentro del periodo. En la ficha de cada empleado se listan sus cursos con la fecha de inicio, el nombre del curso, la categoría, el tipo, el estado, si lo ha aprobado y la calificación.

Para sacar el historial de un solo empleado, filtra antes la lista de empleados.

## Vigilancia de la salud

Excel con los reconocimientos médicos de los empleados y su resultado.

| Filtro | Descripción |
| --- | --- |
| Horizonte de alerta (días) | Opcional. Por defecto, 90. |

Por cada reconocimiento se muestran el empleado (ID, código y nombre), la empresa, la oficina, el tipo de vigilancia, el resultado, la fecha de realización, si está confirmado y la fecha de confirmación. Las filas se colorean según el resultado: verde si el empleado es apto, amarillo si es apto con restricciones y rojo si no es apto.

<!-- PENDIENTE: la fecha de próxima revisión no se calcula (el informe la deja siempre vacía), así que el horizonte de alerta no tiene efecto. Además, en PRO el grupo "Salud ocupacional" está deshabilitado y el informe solo aparece en LITE. Confirmar con desarrollo. -->
