---
title: Auditoría y cumplimiento
---
# Informes de auditoría y cumplimiento

Informes del grupo **Auditoría y cumplimiento** del botón **Informes** de la lista de empleados (`Menú lateral > Empleados`). Sirven para acreditar ante la Inspección de Trabajo y Seguridad Social (ITSS) el registro de jornada que exige el art. 34.9 del Estatuto de los Trabajadores y que ese registro no se ha manipulado. Todos se calculan sobre los empleados que muestra la lista con los filtros que tengas aplicados. Consulta el [catálogo de informes](catalogo-de-informes.es.md) para ver cómo se lanzan.

!!! tip "Recomendación"
    Si recibes un requerimiento de la Inspección para un mes concreto, el [Paquete de inspección integral](#paquete-de-inspeccion-integral) reúne en un solo PDF el registro de jornada, la trazabilidad de los cambios, las reaperturas y las incidencias.

## Libro de registro de horas de trabajo

PDF con el registro diario de jornada de un mes, con una hoja por empleado agrupada por empresa. Es el documento que se entrega como registro de jornada.

| Filtro | Descripción |
| --- | --- |
| Período | Obligatorio. Mes del registro. |
| ¿Solo validado? | Si está activado, solo incluye las jornadas validadas. Por defecto, desactivado. |

Cada hoja incluye:

- **Cabecera**: datos de la empresa con el título "REGISTRO DE JORNADA LABORAL" y la referencia "Art. 34.9 ET · Real Decreto-Ley 8/2019".
- **Datos del trabajador**: nombre y apellidos, código de empleado, número de contrato y fecha de generación.
- **Tabla diaria**: día, semana, tipo de día, entrada y salida del turno, entrada y salida reales, horas teóricas, horas trabajadas, saldo y observaciones. El fondo de cada fila cambia según el tipo de día.
- **Totales** del mes, con los días trabajados.
- **Firmas**: espacio para la firma del trabajador y para el sello y la firma de la empresa.
- **Nota legal**: "Documento generado automáticamente según Art. 34.9 del Estatuto de los Trabajadores (RDL 8/2019). Datos sometidos a RGPD (UE) 2016/679. Conservar 4 años."

## Trazabilidad de modificaciones de fichajes

Excel con todas las altas, modificaciones y eliminaciones de fichajes hechas en un periodo. Demuestra que cualquier cambio en el registro queda identificado.

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Obligatorio. Último día del periodo. |
| Tipo de operación | Opcional. Todas (por defecto), Inserción, Modificación o Eliminación. |

| Columna | Descripción |
| --- | --- |
| ID auditoría | Identificador del cambio. |
| ID emp., Nombre completo, Código, Empresa, Oficina | Empleado afectado. |
| ID fichaje, Hora fichaje original | Fichaje modificado y su hora original. |
| Tipo op., Descripción op. | Inserción, modificación o eliminación. |
| Hora anterior, Tipo ant. | Hora y tipo (entrada o salida) antes del cambio. |
| Hora nueva, Tipo nuevo | Hora y tipo después del cambio. |
| Fecha modificación (UTC) | Cuándo se hizo el cambio, en hora UTC. |
| ID usuario, Nombre usuario, IP | Quién hizo el cambio y desde qué dirección IP. |

La cabecera muestra el total de inserciones, modificaciones y eliminaciones del periodo.

## Historial de reapertura de jornadas

Excel con las jornadas que se han reabierto o desvalidado en un periodo, con el motivo y el usuario. Ante una inspección justifica por qué se cambió una jornada ya cerrada.

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Obligatorio. Último día del periodo. |

| Columna | Descripción |
| --- | --- |
| ID | Identificador de la reapertura. |
| ID emp., Nombre completo, Código, Empresa, Oficina | Empleado afectado. |
| Fecha jornada | Jornada reabierta. |
| Estado anterior, Estado nuevo | Estado de la jornada antes y después de la reapertura. |
| Motivo | Motivo indicado al reabrir. |
| ID usuario, Nombre usuario | Quién reabrió la jornada. |
| Fecha reapertura (UTC) | Cuándo se reabrió, en hora UTC. |
| Nº reaperturas, Alerta | Veces que se ha reabierto esa jornada. Si es más de una, se marca como MÚLTIPLE. |

## Clasificación del tiempo de trabajo

PDF apaisado de auditoría interna que reparte el tiempo registrado por tipo de actividad: trabajo efectivo, disponibilidad, descanso, ausencias, etc.

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Obligatorio. Último día del periodo. |
| Agrupar por | Opcional. Empleado (por defecto), departamento o empresa. |

El informe muestra primero los totales del periodo y después una fila por empleado, departamento o empresa con los días, la jornada teórica, el trabajo efectivo, el porcentaje de eficiencia, las ausencias computables y no computables, la disponibilidad, otros tiempos y el saldo. Incluye una leyenda con las clases de tiempo.

## Incidentes de cumplimiento por período

PDF con las incidencias de cumplimiento detectadas en un periodo y su estado de resolución. Demuestra que las irregularidades se controlan y se resuelven.

| Filtro | Descripción |
| --- | --- |
| Fecha de inicio | Obligatorio. Primer día del periodo. |
| Fecha Fin | Obligatorio. Último día del periodo. |
| Categoría | Opcional. Todas (por defecto), Cumplimiento o Integridad. |
| Gravedad mínima | Opcional. Información (por defecto, incluye todas), Advertencia o Crítico. |
| Estado | Opcional. Todos (por defecto), Pendiente, Resuelto o Ignorado. |

El informe empieza con un resumen ejecutivo (total de incidencias, críticas, advertencias, resueltas, pendientes y días medios de resolución) y sigue con el detalle agrupado por categoría: fecha, empleado, incidencia, gravedad, estado y días que tardó en resolverse, con un subtotal por categoría.

## Paquete de inspección integral

PDF único con toda la documentación de registro de jornada de un mes, preparado para entregarlo a la Inspección. Si los empleados de la lista pertenecen a varias empresas, genera un bloque completo para cada una.

| Filtro | Descripción |
| --- | --- |
| Mes (1-12) | Obligatorio. Mes de la inspección. Por defecto, el mes actual. |
| Motivo de la inspección (opcional) | Texto que aparece en la portada. Si se deja vacío, se usa "Inspección de cumplimiento normativo". |

El documento contiene:

- **Portada**: empresa, CIF, periodo, motivo, número de empleados, fecha de generación y referencia legal (Art. 34.9 ET · RDL 8/2019 · Criterio Técnico ITSS 101/2019), seguida de un índice.
- **Sección 1 — Registro de jornada**: el mismo registro diario que el [libro de registro](#libro-de-registro-de-horas-de-trabajo), con firma del trabajador y de la empresa en cada hoja.
- **Sección 2 — Trazabilidad de modificaciones de fichajes**: empleado, hora original, operación, valores antes y después, fecha del cambio (UTC), usuario e IP.
- **Sección 3 — Reaperturas y desvalidaciones**: empleado, fecha de la jornada, estado anterior y nuevo, motivo, usuario y fecha de reapertura.
- **Sección 4 — Incidencias de cumplimiento**: empleado, fecha, incidencia, gravedad, estado y resolución.
- **Sección 5 — Declaración de conformidad**: declaración de la empresa de que el documento es el registro fiel y completo de las jornadas del periodo, según el art. 34.9 ET y el Criterio Técnico 101/2019 de la ITSS, y de que se conservará durante al menos cuatro años. Termina con los bloques de firma.

El pie de cada página indica "Documento estrictamente confidencial · Datos sujetos a RGPD (UE) 2016/679".
