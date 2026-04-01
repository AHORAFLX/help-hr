# Documentación Técnica: Sistema de Gestión de Incidencias

##   

### 1\. Descripción General

El sistema de gestión de incidencias centraliza la detección y resolución de anomalías en el control de presencia. Utiliza un Modelo Unificado donde cualquier error (fichaje, jornada o integridad) se trata como una Incidencia tipificada en el catálogo maestro `WorkdayIncidenceType`.

El sistema está diseñado para ofrecer información en tiempo real , combinando datos persistidos en base de datos con cálculos al vuelo para garantizar que la información mostrada siempre esté actualizada.



### 2\. Arquitectura de Datos (Las 4 Fuentes)

La vista unificada de incidencias agrega datos de 4 fuentes distintas :

### Fuente 1: Incidencias de Fichaje (Persistidas)

  * Origen: Tabla `Markings` (columna `MarkingIncidentTypeId`).
  * Rango IDs: 1–20.
  * Descripción: Errores detectados en el momento de la inserción del fichaje (ej. "Empleado no identificado", "Sin turno asignado").
  * Persistencia: Se graban físicamente en la tabla `Markings`.

### Fuente 2: Incidencias de Fichaje (Tiempo Real)

  * Origen: Función `fvMarkings_EmployeesWithIncidents_Mode1`.
  * Rango IDs: 1–20.
  * Descripción: Errores de coherencia lógica calculados dinámicamente al consultar.
  * Secuencia ilógica (Entrada seguida de Entrada).
  * Entrada tardía / Salida anticipada.
  * Fichajes fuera de rango.

Comportamiento: Estas incidencias NO se guardan en base de datos. Se recalculan en cada consulta para reflejar el estado exacto de los fichajes en ese instante.

### Fuente 3: Incidencias de Jornada (Persistidas)

  *Origen: Tabla `Employees_Assistence_Incidences`.
  *Rango IDs: 21–27.
  *Descripción: Problemas a nivel de día completo detectados durante el cálculo de la jornada.
  * Día sin fichajes.
  * Trabajo en festivo / no laborable.
  * Ausencias no justificadas.

Persistencia: Se calculan y guardan mediante el procedimiento `pEmployees_Assistence_RecalcMetrics`.

### Fuente 4: Incidencias de Integridad (Tiempo Real)

  * Origen: Estado de `Employees_Assistence` (`DirtyFlag`).
  * Rango IDs: 28–35.
  * Descripción: Violaciones de reglas de negocio en días ya cerrados (Validados o Consolidados).
  * Fichaje añadido a día consolidado.
  * Modificación en día validado.

Detección: Si `DirtyFlag = 1` y `StatusId > 0`, el sistema genera automáticamente una incidencia de tipo 28 o 29 en tiempo real, sin necesidad de inserción en tabla.

 

### 3\. Flujo de Información

### 3.1. Detección y Visualización

Para consumir las incidencias, el sistema utiliza la función `fEmployeeDate_GetAllIncidences_ForView`, que actúa como un agregador único realizando un UNION de las 4 fuentes.
    
    

```sql
SELECT * 
    FROM fEmployeeDate_GetAllIncidences_ForView(@EmployeeId, @Date)
    
    -- Retorna:
    -- 1. Incidencias Marking (Tabla Markings)
    -- 2. Incidencias Marking RT (fvMarkings... excluyendo las ya persistidas)
    -- 3. Incidencias Workday (Tabla Incidences)
    -- 4. Incidencias Integrity (Calculadas vía DirtyFlag)
```

Esta información alimenta tanto las vistas de detalle (Grids) como los Dashboards (`vIncidences_Unified`, `vIncidences_Active`).

### 3.2. Resolución

El ciclo de vida de una incidencia termina con el Recálculo.

  1. Acción Correctiva: El usuario corrige el dato origen (ej. añade el fichaje faltante).
  2. Recálculo: Se ejecuta `pEmployees_Assistence_RecalcMetrics`.

  * Elimina incidencias de jornada antiguas.
  * Recalcula métricas y genera nuevas incidencias si persisten problemas.
  * Resetea `DirtyFlag = 0`, haciendo desaparecer instantáneamente las incidencias de integridad.



### 4\. Estructura de Base de Datos Clave

### Tablas

  * WorkdayIncidenceType: Catálogo maestro (IDs 1–35). Define Código, Severidad (Info / Warning / Critical) y Categoría.
  * Employees_Assistence_Incidences: Almacena únicamente incidencias de tipo JORNADA (IDs 21–27).
  * Employees_Assistence: Gestiona el estado de integridad mediante `DirtyFlag` y `DirtyReason`.

### Funciones Core

  * fvMarkings_EmployeesWithIncidents_Mode1: Motor de reglas de negocio para validar la coherencia de fichajes en tiempo real.
  * fEmployeeDate_GetDayType: Motor de clasificación de jornada (detecta festivos, libres y laborables).

 *

### 5\. Resumen de Tipos

<table style="width:100%; border-collapse:collapse;"><thead><tr><th style="border-bottom:2px solid #ddd; text-align:left; padding:6px;">Categoría</th><th style="border-bottom:2px solid #ddd; text-align:left; padding:6px;">IDs</th><th style="border-bottom:2px solid #ddd; text-align:left; padding:6px;">Origen</th><th style="border-bottom:2px solid #ddd; text-align:left; padding:6px;">Naturaleza</th></tr></thead><tbody><tr><td style="padding:6px;">MARKING</td><td style="padding:6px;">1–20</td><td style="padding:6px;">Markings / fvMarkings...</td><td style="padding:6px;">Híbrida (DB + RealTime)</td></tr><tr><td style="padding:6px;">WORKDAY</td><td style="padding:6px;">21–27</td><td style="padding:6px;">Employees_Assistence_Incidences</td><td style="padding:6px;">Persistida (DB)</td></tr><tr><td style="padding:6px;">INTEGRITY</td><td style="padding:6px;">28–35</td><td style="padding:6px;">DirtyFlag</td><td style="padding:6px;">RealTime</td></tr></tbody></table>