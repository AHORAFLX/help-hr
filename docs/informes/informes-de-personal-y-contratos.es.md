---
title: Personal y contratos
---
# Informes de personal y contratos

Informes de los grupos **Personal** y **Contratos** del botón **Informes** de la lista de empleados (`Menú lateral > Empleados`). Todos se calculan sobre los empleados que muestra la lista con los filtros que tengas aplicados. Consulta el [catálogo de informes](catalogo-de-informes.es.md) para ver cómo se lanzan.

## Directorio de empleados

Excel con una fila por empleado activo y sus datos personales, de contacto y organizativos. Sirve como listado maestro de la plantilla.

No tiene filtros propios: incluye los empleados activos de la lista a fecha de hoy. Para limitarlo a una empresa, oficina o departamento, filtra antes la lista de empleados.

| Bloque | Columnas |
| --- | --- |
| Identificación | ID, Código, Nombre completo, Nombre, Apellidos, Número ID, NSS |
| Datos personales | Fecha de nacimiento, Edad, Sexo, Estado civil, Nacionalidad |
| Contacto | Email corporativo, Email personal, Tel. trabajo, Tel. personal, Dirección, Ciudad, Provincia, Código postal |
| Organización | Empresa, Oficina, Unidad, Grupo, Departamento, Área, Puesto, Categoría |
| Situación | Fecha antigüedad, Años antigüedad, Fecha baja, Estado |

## Distribución del personal por estructura

PDF con el número de empleados activos en cada unidad de la estructura organizativa. No muestra datos individuales, solo recuentos.

| Filtro | Descripción |
| --- | --- |
| Agrupar por | Obligatorio. Nivel por el que se agrupa la plantilla. Por defecto, empresa. En PRO se puede agrupar por unidad organizativa, oficina, departamento, área, grupo, puesto, categoría o empresa; en LITE, por oficina, departamento, área o empresa. |

Para cada valor del nivel elegido, el informe muestra:

| Columna | Descripción |
| --- | --- |
| Total | Número de empleados activos. |
| H. / M. | Número de hombres y de mujeres. |
| % Plantilla | Porcentaje sobre el total de empleados del informe. |
| Edad media | Edad media en años. |
| Antigüedad media | Antigüedad media en años. |
| Temp. Año+1 | Empleados con fecha de fin de contrato en el año actual o el siguiente. |

## Exportación de datos de empleados (RGPD) <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span> { #exportacion-de-datos-de-empleados-rgpd }

Excel con varias hojas que reúne todos los datos que Sebastian HR guarda de un empleado. Está pensado para atender una solicitud de portabilidad de datos (art. 20 del RGPD).

No tiene filtros propios: exporta los empleados de la lista. Para atender la solicitud de una persona, filtra la lista hasta que solo aparezca ese empleado y lanza el informe.

El libro contiene estas hojas:

- **Datos personales**: identificación, datos personales y de contacto.
- **Datos laborales**: empresa, oficina, departamento, puesto, categoría, antigüedad y fechas del contrato actual.
- **Contratos**: histórico de contratos con tipo, estado, fechas y porcentaje de jornada.
- **Ausencias y bajas**: ausencias, permisos y bajas con su tipo, duración y motivo.
- **Saldos de vacaciones**: días generados, disfrutados y pendientes por año, días de años anteriores, compensación y ajustes.
- **Detalle de vacaciones**: cada periodo de vacaciones disfrutado.
- **Fichajes**: cada fichaje con fecha de jornada, hora, tipo, turno, localización, origen, si fue manual y comentarios.
- **Registro de jornada**: resumen diario con horas teóricas, saldo, primera entrada y última salida.
- **Resumen de nóminas**: periodos de nómina con salario base, importes, ajustes, horas extra y estado.
- **Documentos**: listado de los documentos del empleado (nombre, carpeta, idioma y fechas).
- **Evaluaciones de desempeño**: fecha, tipo, resultado, áreas de mejora y evaluador.

!!! warning "Los documentos no se incluyen"
    La hoja *Documentos* solo lista los metadatos. Los ficheros de los documentos hay que entregarlos por separado.

## Relación de contratos <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span> { #relacion-de-contratos }

Excel con los contratos de los empleados de la lista, ordenados por empresa, estado y nombre.

| Filtro | Descripción |
| --- | --- |
| Estado | Opcional. Todos (por defecto), Activo (contratos vigentes) o Futuro (contratos que aún no han empezado). |

| Columna | Descripción |
| --- | --- |
| ID contrato, ID empleado, Código, Nombre completo | Identificación del contrato y del empleado. |
| Empresa, Oficina | Dónde está contratado el empleado. |
| Estado | Estado del contrato. La fila se colorea en verde si está vigente, en amarillo si es futuro y en gris si ha vencido. |
| Tipo contrato | Tipo de contrato. |
| Indefinido | Sí o No. |
| Agencia (ETT) | Empresa de trabajo temporal, si la hay. |
| Fecha inicio, Fecha fin, Fecha fin inicial | Fechas del contrato. La fecha fin inicial es la prevista antes de cualquier prórroga. |
| Fin período prueba | Fecha en que termina el periodo de prueba. |
| % Jornada | Porcentaje de jornada del contrato. |

## Contratos que vencen pronto <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span> { #contratos-que-vencen-pronto }

PDF con los contratos vigentes cuya fecha de fin cae entre hoy y el horizonte indicado. Sirve para decidir a tiempo renovaciones y finalizaciones.

| Filtro | Descripción |
| --- | --- |
| Horizonte (días) | Opcional. Número de días a partir de hoy. Por defecto, 90. |

Los contratos se ordenan por urgencia y se marcan con un semáforo según los días que faltan para su vencimiento:

| Nivel | Días hasta el vencimiento |
| --- | --- |
| Crítico | 30 o menos |
| Aviso | De 31 a 60 |
| Próximo | Más de 60, hasta el horizonte |

De cada contrato se muestran el empleado, la empresa y oficina, el tipo de contrato, las fechas de inicio y fin, los días que faltan y la jornada.

## Periodos de prueba próximos a vencer <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span> { #periodos-de-prueba-proximos-a-vencer }

PDF con los contratos vigentes cuyo periodo de prueba termina entre hoy y el horizonte indicado. Funciona igual que [Contratos que vencen pronto](#contratos-que-vencen-pronto), pero con la fecha de fin del periodo de prueba: mismo filtro *Horizonte (días)* (por defecto 90) y mismo semáforo (crítico hasta 30 días, aviso de 31 a 60 y próximo a partir de 61).

En la app, el botón aparece como "El período de prueba expira pronto.".

## Antigüedad del empleado <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span> { #antiguedad-del-empleado }

Excel con la antigüedad de cada empleado de la lista en cada empresa. Solo incluye empleados que tienen fecha de antigüedad informada. No tiene filtros.

| Columna | Descripción |
| --- | --- |
| ID empleado, Nombre completo | Identificación del empleado. |
| Empresa, Departamento | Empresa en la que se calcula la antigüedad y departamento del empleado. |
| Fecha antigüedad | Fecha desde la que se cuenta la antigüedad. |
| Total días | Días transcurridos desde la fecha de antigüedad. |
| Antigüedad | La misma antigüedad expresada en años y meses. |
