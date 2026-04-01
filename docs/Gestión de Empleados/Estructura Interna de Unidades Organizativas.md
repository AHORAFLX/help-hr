# Estructura Interna de Unidades Organizativas

## (doc. técnico no publicar como ayuda a usuarios)

##   

##  Guía de Unidades Organizativas, Grupos y Empleados

> Objetivo: documentar la estructura de datos y los procesos para gestionar Unidades Organizativas , Grupos , Puestos y Planificación de empleados; detallar reglas de integridad, funciones de lectura canónica y operaciones habituales. Incluye notas de coherencia, validaciones y elementos a revisar/deprecar.

 

### 1) Visión general

  * Unidades (OU) definen el árbol organizativo (UnitId ← UnitId_Parent) y parámetros de control de presencia.

  * Grupos pertenecen a una unidad y pueden cambiar de unidad en el tiempo (histórico de modificaciones).

  * Asignaciones del empleado :

    * Organizational_Units_Positions (OUP) : tramo de empleado→unidad (y posición) con fechas (StartDate/EndDate) y `RegId` como identificador lógico del tramo.

    * Employees_Groups_Historic (EGH) : cortes de grupo por empleado, enlazados al tramo OUP mediante `UnitRegId`.

    * Employees_PositionsUO_Historic (EPUH) : cortes de posición dentro del tramo OUP.

    * Employees_UnitGroup_Planning (PLN) : planificación futura de cambios (unidad/grupo/posición).

> Clave conceptual: el `RegId` del tramo en OUP es la columna vertebral ; sobre él cuelgan los históricos de grupo y posición.

 

### 2) Modelo de datos (resumen)
    
    
    Organizational_Units (UnitId, UnitId_Parent, ScopeId, TypeId, ...)  ├─< Groups (GroupId, UnitId actual, LeaderId, SupervisorId, ...)  │     └─< Groups_ModHistoric (GroupId, DateFrom, UnitId, ...)  └─< Organizational_Units_Positions (RegId, EmployeeId, UnitId, PositionId, StartDate, EndDate, StatusId)         ├─< Employees_Groups_Historic (HistoricId, EmployeeId, NewGroup, OldGroup, DateStart, UnitRegId)         └─< Employees_PositionsUO_Historic (PositionId, DateStart, UnitRegId) 
    Employees_UnitGroup_Planning (RegId, EmployeeId, DateFrom, UnitId | GroupId | PositionId)
    

### 2.1 Tablas soporte relevantes del contexto recibido

  * Scopes_Position : intersección Scope↔Position (permite restringir qué puestos son válidos por ámbito). Ojo: en el script aparece duplicada (ver §10.1).

  * vistas

    * `vOrganizationalUnits_Employees`: foto “hoy” basada en `fGiveMe_tbl_UnitEmployeeID(GETDATE())`.

    * `vOrganizationalUnitsPositions`: vista enriquecida de OUP con metadatos (empleado, contrato, oficina…).

  * Calendario/turnos de grupos

    * `Groups_Schedule` (turnos por día y grupo) + trigger IU de validación básica.

    * `Groups_Shifts_Periods` (periodos de turnos por grupo) + trigger IU de integridad de rangos.

 

### 3) Reglas de integridad y validaciones

### 3.1 Rangos temporales (OUP)

  * No deben existir solapes de tramos para un mismo empleado (rango cerrado con `EndDate` o abierto con `EndDate IS NULL`).

  * Adyacencia permitida (fin D y siguiente inicio D+1).

  * Recomendado : trigger `trg_OUP_NoOverlaps_IU` (ver §8.2) para bloquear solapes en INSERT/UPDATE.

### 3.2 Planificación (PLN)

  * Debe aceptar solo futuro (`DateFrom > GETDATE()`), con trigger.

### 3.3 Borrados seguros en históricos

  * EGH y EPUH: permitir borrar solo el último corte por clave lógica (empleado o `UnitRegId`). Triggers de delete para proteger continuidad.

### 3.4 Relaciones

  * `EGH.UnitRegId` debe apuntar a un `OUP.RegId` válido; antes de cerrar/eliminar un tramo OUP verificar que no queden hijos colgantes.

  * `Groups.UnitId` = unidad “actual por defecto”; `Groups_ModHistoric` registra cambios por fecha. Funciones/vistas deben resolver UnitId efectivo en fecha.

 

### 4) Lectura canónica (funciones)

### 4.1 `fn_GroupUnitIdAtDate(GroupId, Date)`

Devuelve la unidad efectiva de un grupo en una fecha, consultando primero `Groups_ModHistoric` y, si no hay corte ≤ fecha, devolviendo la `Groups.UnitId` actual.

### 4.2 `fEmployeeOrgState(EmployeeId, Date, ApplyPlanning BIT=1)`

Devuelve la foto canónica del empleado en una fecha: `UnitRegId, UnitId/Name/Code, GroupId (+UnitId efectivo del grupo), PositionId, fechas del tramo, PlanningApplied`.

  * Con `ApplyPlanning=1` combina histórico + primer cambio en `Planning ≥ Date`.

  * Con `ApplyPlanning=0` usa solo histórico.

> Estas funciones ya están preparadas con cabecera y están pensadas para depósitos, reporting y APIs.

 

### 5) Operaciones típicas (escritura)

  * Asignar unidad/grupo/puesto “ya” : `POrganizational_Units_Positions_I` (cierra tramo previo si cambia de unidad, inserta/merge de OUP, añade cortes en EGH/EPUH según cambios).

  * Programar cambio futuro : mismo proc con `@StartDate` futuro → escribe en Planning.

  * Cambio de unidad del grupo (reorg): actualizar `Groups` o `Groups_ModHistoric` y ejecutar `pUpdateEmployeesHistoricForGroupUnitChanges(@UnitId, @GroupId, @CurrentDate, …)` para reencajar los empleados.

 

### 6) Vistas incluidas (y uso sugerido)

  * `vOrganizationalUnits_Employees` : foto a hoy (usa `fGiveMe_tbl_UnitEmployeeID(GETDATE())`).

    * Sugerencia : crear `vEmployeeOrgState_Today` basada en `fEmployeeOrgState(EmployeeId, CAST(GETDATE() AS date), 1)` para homologar el cálculo con planificación.

  * `vOrganizationalUnitsPositions` : matriz de tramos (con contrato, oficina, scope…). Útil para auditoría y paneles.

 

### 7) Jerarquía de unidades

  * `fGetUnitAncestors(StartUnitId)` : devuelve la línea ascendente (UnitId, LevelOrder). Útil para filtrar por subtree o para herencia de políticas.

  * `fGiveMe_UNIT_HIERARCHY_SCOPE(UnitId)` : CTE recursiva que recorre ancestros con mismo ScopeId ; válida para resolver restricciones por ámbito.

> Para jerarquías profundas, documentar `OPTION (MAXRECURSION N)` en consultas consumidoras.

 

### 8) Validaciones y triggers propuestos

### 8.1 Planning solo futuro (PLN)

  * Trigger AFTER INSERT/UPDATE en `Employees_UnitGroup_Planning` que rechace `DateFrom <= GETDATE()`.

### 8.2 No solapes en OUP

  * Trigger AFTER INSERT/UPDATE (sin CTE) que compare:

    * `inserted` ↔ filas existentes (mismo EmployeeId, RegId distinto, rangos solapados).

    * intra-inserted (dos filas en el mismo batch).

  * Mensajes claros y `ROLLBACK` en conflicto.

### 8.3 Delete solo último corte

  * EGH: máximo `DateStart` por `EmployeeId`.

  * EPUH: máximo `DateStart` por `UnitRegId`.

 

### 9) Buenas prácticas e índices

  * Sentinel : usar `'2079-06-06'` para `EndDate IS NULL` en todas las consultas de rango.

  * Índices sugeridos :

    * `OUP(EmployeeId, StartDate) INCLUDE (EndDate, UnitId, PositionId, StatusId, RegId)`

    * `EGH(EmployeeId, DateStart) INCLUDE (NewGroup, OldGroup, UnitRegId)`

    * `Groups_ModHistoric(GroupId, DateFrom) INCLUDE (UnitId)`

    * `EPUH(UnitRegId, DateStart) INCLUDE (PositionId)`

 

### 10) Elementos a revisar / posibles obsolescencias

### 10.1 Duplicación de `Scopes_Position`

En el script aparece dos veces la creación completa de la tabla y sus FKs con el mismo nombre de PK y FKs. Esto puede fallar en despliegue o inducir confusión. Acción: eliminar duplicado y conservar una única definición.

### 10.2 Activación de trigger en tabla equivocada

Se define `CREATE TRIGGER [dbo].[Groups_Schedule_IUTrig] ON [dbo].[Groups_Schedule] ...`, pero acto seguido se ejecuta:  
`ALTER TABLE [dbo].[Employees_Schedule] ENABLE TRIGGER [Groups_Schedule_IUTrig]`.

Ese `ALTER TABLE` apunta a Employees_Schedule en lugar de `Groups_Schedule`. Acción: cambiar a `ALTER TABLE [dbo].[Groups_Schedule] ENABLE TRIGGER [Groups_Schedule_IUTrig]`.

### 10.3 Vista `vOrganizationalUnits_Employees` usa función antigua

La vista usa `fGiveMe_tbl_UnitEmployeeID(EmployeeId, GETDATE())`, por lo que no aplica planificación y no garantiza coherencia con `Groups_ModHistoric`. Acción: crear nueva vista basada en `fEmployeeOrgState` o actualizar ésta si es viable.

### 10.4 Unicidad en `Groups_Schedule`

La `UNIQUE` actual es `(GroupId, Date)` (con `ShiftId` comentado). Esto impone un único turno por grupo y día. Si el negocio admite múltiples turnos/fragmentos por día (mañana/tarde), habría que incluir`ShiftId` (o un ordinal de bloque) en la clave única. Confirmar con negocio.

### 10.5 Validación de solapes en `Groups_Shifts_Periods`

El trigger IU valida solapes por `GroupId` sin segregar por `ShiftId`. Si un grupo puede tener varios shifts en paralelo (distintos), la condición actual bloquea esos casos. Si se desea permitir paralelismo por `ShiftId`, añadir `AND p.ShiftId = i.ShiftId` a la comprobación de solape.

### 10.6 Consistencia Scope↔Position

Con `Scopes_Position` puedes validar que una posición sea compatible con el scope de la unidad. Hoy no hay una validación explícita en OUP. Acción sugerida: trigger en OUP que, en INSERT/UPDATE, valide que `(Unit.ScopeId, PositionId)` exista en `Scopes_Position` (o permitir NULL = sin restricción).

### 10.7 Funciones de jerarquía

  * `fGetUnitAncestors` y `fGiveMe_UNIT_HIERARCHY_SCOPE` no exponen `MAXRECURSION`; si tu árbol puede superar 100 niveles, documentar consumo con hint.

 

### 11) API/Contratos internos recomendados

  * Lectura puntual: `SELECT * FROM dbo.fEmployeeOrgState(@EmployeeId, @Date, @ApplyPlanning)`

  * Lectura masiva: vista parametrizada o función table-valued multistatement que itere `Employees` y `CROSS APPLY` a `fEmployeeOrgState`.

  * Escritura inmediata: `EXEC dbo.POrganizational_Units_Positions_I @EmployeeId, @CurrentReference, @UnitId, @PositionId, @StartDate, @GroupId`.

  * Cambio de unidad de grupo: actualizar `Groups_ModHistoric` \+ `EXEC dbo.pUpdateEmployeesHistoricForGroupUnitChanges @UnitId, @GroupId, @CurrentDate, @CurrentReference`.

 

### 12) Ejemplos de uso

### 12.1 Foto canónica hoy (con planning)
    
    

```sql
SELECT s.* FROM dbo.Employees e CROSS APPLY dbo.fEmployeeOrgState(e.EmployeeId, CAST(GETDATE() AS date), 1) s;
```

### 12.2 Validar que la posición es apta para el Scope de la unidad (consulta diagnóstica)
    
    

```sql
SELECT o.EmployeeId, o.UnitId, u.ScopeId, o.PositionId FROM dbo.Organizational_Units_Positions o JOIN dbo.Organizational_Units u ON u.UnitId = o.UnitId LEFT JOIN dbo.Scopes_Position sp ON sp.ScopeId = u.ScopeId AND sp.PositionId = o.PositionId WHERE sp.PositionId IS NULL;  -- candidatos a incoherencia
 ```   

### 12.3 Resolver unidad efectiva del grupo en fecha
    
 ```sql  
    SELECT g.GroupId,       dbo.fn_GroupUnitIdAtDate(g.GroupId, '2025-10-01') AS UnitIdAtDate FROM dbo.Groups g;
```    

 

### 13) Checklist de despliegue

  1. Eliminar duplicados de `Scopes_Position` (mantener una definición).

  2. Corregir `ALTER TABLE ... ENABLE TRIGGER` para `Groups_Schedule_IUTrig`.

  3. Crear/activar triggers de integridad:

     * No solapes en OUP.

     * Planning solo futuro.

     * Delete solo último corte en EGH y EPUH.

  4. Crear/actualizar índices recomendados (§9).

  5. Publicar funciones `fn_GroupUnitIdAtDate` y `fEmployeeOrgState` con cabeceras.

  6. (Opcional) Nueva vista `vEmployeeOrgState_Today` con planificación aplicada.

  7. (Opcional) Trigger en OUP para validar compatibilidad Scope↔Position.

 

### 14) FAQ

¿Qué objeto determina la continuidad histórica?  
`Organizational_Units_Positions.RegId`. Todo histórico de grupo y posición cuelga de él.

¿Puedo borrar un tramo intermedio?  

No. Hay trigger para impedirlo y romperías la integridad de EGH/EPUH.

¿Cómo calculo el estado en una fecha futura con planificaciones?  
Usa `fEmployeeOrgState(@EmployeeId, @DateFutura, 1)`.

¿Dónde se guarda el cambio de unidad para un grupo?  
En `Groups_ModHistoric` (y `Groups.UnitId` es el valor por defecto/actual).

 

> Estado del documento: 28/10/2025. Mantener sincronizado con cambios de esquema y procs. Añadir ejemplos unit-test SQL cuando se incorporen nuevas validaciones.