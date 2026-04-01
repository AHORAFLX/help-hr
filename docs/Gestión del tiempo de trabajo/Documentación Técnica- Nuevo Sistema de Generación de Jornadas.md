# Documentación Técnica: Nuevo Sistema de Generación de Jornadas

##   

### 1\. Resumen Ejecutivo

El sistema de generación de jornadas ha sido rediseñado para proporcionar una cobertura completa de todos los días activos de un empleado, no solo aquellos con fichajes. Esta actualización permite:

  * Registro de días sin fichajes (vacaciones, bajas, festivos, días libres)
  * Detección y logging de conflictos en jornadas cerradas
  * Auditoría completa de cambios de estado
  * Soporte explícito para modos LITE y PRO

 

### 2\. Comparativa: Sistema Anterior vs Nuevo

### 2.1 Creación de Registros en Employees_Assistence

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;"><thead><tr><th>Aspecto</th><th>Sistema Anterior</th><th>Sistema Nuevo</th></tr></thead><tbody><tr><td><strong>Momento de creación</strong></td><td>Solo al recibir un fichaje</td><td>Al fichar + al cerrar periodo + cron retroactivo (opcional)</td></tr><tr><td><strong>Días sin fichajes</strong></td><td>No existían registros</td><td>Sí existen (vacaciones, bajas, festivos)</td></tr><tr><td><strong>Días futuros</strong></td><td>No aplicaba</td><td>No se generan (cálculo en tiempo real)</td></tr><tr><td><strong>Campos poblados al crear</strong></td><td>Solo EmployeeId, Date, ShiftId</td><td>Todos: Office, Company, Contract, Calendar, métricas</td></tr><tr><td><strong>Recálculo de métricas</strong></td><td>Manual o al validar</td><td>Automático al crear (@RecalcMetrics=1)</td></tr></tbody></table>

 

### 2.2 Triggers de Markings

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;"><thead><tr><th>Trigger</th><th>Sistema Anterior</th><th>Sistema Nuevo</th></tr></thead><tbody><tr><td><strong>Markings_ITrig</strong></td><td>Crea EA si no existe</td><td>Crea EA + marca DirtyFlag si StatusId &gt; 0 + log conflicto</td></tr><tr><td><strong>Markings_DTrig</strong></td><td>Elimina EA si no quedan fichajes</td><td>Elimina EA solo si StatusId = 0 (protege validados)</td></tr></tbody></table>

 

### 2.3 Manejo de Estados

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;"><thead><tr><th>Transición</th><th>Sistema Anterior</th><th>Sistema Nuevo</th></tr></thead><tbody><tr><td>0 → 1 (Validar)</td><td>pDateEmployee_Validate_Period</td><td>Sin cambios</td></tr><tr><td>1 → 2 (Consolidar)</td><td>pEmployeeDate_Generate_Balance</td><td>Sin cambios</td></tr><tr><td>2 → 1 (Deshacer consolidación)</td><td>pEmployeeDate_Balance_Undo</td><td>+ Logging en ReopenLog + Resolución de conflictos</td></tr><tr><td>1 → 0 (Deshacer validación)</td><td>pDateEmployee_Validate_Undo_Batch</td><td>+ DirtyFlag = 1 + Logging en DirtyLog</td></tr></tbody></table>

 

### 2.4 Gestión de Conflictos

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;"><thead><tr><th>Escenario</th><th>Sistema Anterior</th><th>Sistema Nuevo</th></tr></thead><tbody><tr><td>Fichaje en día validado</td><td>Permitido sin control</td><td>DirtyFlag = 1 + Warning en ConflictLog</td></tr><tr><td>Fichaje en día consolidado</td><td>Permitido sin control</td><td>DirtyFlag = 1 + Critical en ConflictLog</td></tr><tr><td>Eliminar fichaje en día validado</td><td>EA se borraba</td><td>EA se mantiene (StatusId &gt; 0)</td></tr></tbody></table>

 



### 3\. Arquitectura del Sistema Nuevo

### 3.1 Diagrama de Flujo General
    
    
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                           FLUJO DE JORNADAS v4.0                            │
    ├─────────────────────────────────────────────────────────────────────────────┤
    │                                                                             │
    │  ╔═══════════════════════════════════════════════════════════════════════╗  │
    │  ║  DÍAS FUTUROS: Cálculo en tiempo real (NO hay registro en EA)        ║  │
    │  ║  └── vEmployees_Assistence_Consolidated + fHR_Employee_Daydate_Lite  ║  │
    │  ╚═══════════════════════════════════════════════════════════════════════╝  │
    │                                                                             │
    │  ╔═══════════════════════════════════════════════════════════════════════╗  │
    │  ║  DÍAS PASADOS: Registro físico en Employees_Assistence               ║  │
    │  ╠═══════════════════════════════════════════════════════════════════════╣  │
    │  ║                                                                       ║  │
    │  ║  [1] FICHAJE ────► Markings_ITrig ────► INSERT EA (si no existe)    ║  │
    │  ║                                    └──► DirtyFlag + ConflictLog     ║  │
    │  ║                                         (si StatusId > 0)            ║  │
    │  ║                                                                       ║  │
    │  ║  [2] CIERRE PERIODO ────► pEmployees_PeriodValidation_Close         ║  │
    │  ║                           └──► pEmployees_Assistence_EnsureInit     ║  │
    │  ║                               └──► pEmployees_Assistence_RecalcMetrics║ │
    │  ║                                                                       ║  │
    │  ║  [3] CRON RETROACTIVO (opcional) ────► pCron_Generate_Yesterday     ║  │
    │  ║      └──► Solo día anterior, para detectar ausencias                ║  │
    │  ║                                                                       ║  │
    │  ╚═══════════════════════════════════════════════════════════════════════╝  │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘

### 3.2 Ciclo de Vida del StatusId
    
    
                        pDateEmployee_Validate_Period
                                  │
                                  ▼
        ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
        │   GENERADO   │ ───► │   VALIDADO   │ ───► │ CONSOLIDADO  │
        │  StatusId=0  │      │  StatusId=1  │      │  StatusId=2  │
        └──────────────┘      └──────────────┘      └──────────────┘
               ▲                     │                     │
               │                     │                     │
               │   pDateEmployee_    │   pEmployeeDate_    │
               │   Validate_Undo     │   Balance_Undo      │
               │   ◄─────────────────┘◄────────────────────┘
               │                     
        Nueva jornada            
        sin fichajes             

### 3.3 Flujo Detallado: Inserción de Fichaje
    
    
    [Nuevo Fichaje]
          │
          ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    Markings_ITrig                            │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │  1. Asignar DateJourney y ShiftId (lógica existente)        │
    │                                                              │
    │  2. ¿Existe Employees_Assistence para esa fecha?            │
    │     ├── NO ─► INSERT en Employees_Assistence (StatusId=0)   │
    │     │                                                        │
    │     └── SÍ ─► ¿StatusId > 0?                                │
    │               ├── SÍ ─► UPDATE DirtyFlag = 1                │
    │               │         INSERT en ConflictLog               │
    │               │         (MARKING_ON_VALIDATED/CONSOLIDATED) │
    │               │                                              │
    │               └── NO ─► Sin acción adicional                │
    │                                                              │
    │  3. Continuar con lógica de MarkingsPair...                 │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘

### 3.4 Flujo Detallado: Cierre de Periodo
    
    
    [Cierre de Periodo]
          │
          ▼
    ┌─────────────────────────────────────────────────────────────┐
    │              pEmployees_PeriodValidation_Close               │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │  1. pEmployees_Assistence_EnsureInit                        │
    │     └── Genera registros para días SIN fichajes             │
    │         └── Días con vacaciones, bajas, festivos, libres    │
    │                                                              │
    │  2. pDateEmployee_Validate_Period                           │
    │     ├── pEmployees_Assistence_RecalcMetrics                 │
    │     │   └── Usa fHR_Employee_Daydate_Lite (fuente verdad)   │
    │     │                                                        │
    │     ├── UPDATE StatusId = 1                                 │
    │     │                                                        │
    │     └── Cerrar Markings y MarkingsPair (Closed = 1)         │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘

 

### 4\. Nuevos Componentes

### 4.1 Tablas de Catálogo

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;"><thead><tr><th>Tabla</th><th>Descripción</th></tr></thead><tbody><tr><td>Employees_Assistence_ConflictType</td><td>8 tipos de conflicto predefinidos</td></tr><tr><td>Employees_Assistence_ResolutionType</td><td>5 tipos de resolución</td></tr></tbody></table>

 

### 4.2 Tablas de Log

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;"><thead><tr><th>Tabla</th><th>Propósito</th></tr></thead><tbody><tr><td>Employees_Assistence_ConflictLog</td><td>Registro de conflictos con FK a tipos</td></tr><tr><td>Employees_Assistence_ReopenLog</td><td>Auditoría de reaperturas de jornadas</td></tr></tbody></table>

 

### 4.3 Stored Procedures Nuevos

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;"><thead><tr><th>Procedimiento</th><th>Función</th></tr></thead><tbody><tr><td>pEmployees_Assistence_EnsureComplete_All</td><td>Generación masiva para todos los empleados</td></tr><tr><td>pCron_Generate_Yesterday_Workdays</td><td>Cron retroactivo (opcional)</td></tr><tr><td>pEmployees_Assistence_Backfill</td><td>Migración de datos históricos</td></tr></tbody></table>

 

### 4.4 Stored Procedures Modificados

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;"><thead><tr><th>Procedimiento</th><th>Cambios</th></tr></thead><tbody><tr><td>pEmployees_Assistence_EnsureInit</td><td>@RecalcMetrics, LITE/PRO mode, ShiftId automático</td></tr><tr><td>pEmployeeDate_Balance_Undo</td><td>@UserId, @Reason, logging</td></tr><tr><td>pDateEmployee_Validate_Undo_Batch</td><td>DirtyFlag, logging</td></tr></tbody></table>

 



### 5\. Modos LITE vs PRO

### 5.1 Diferencias en Obtención de Datos

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;"><thead><tr><th>Campo</th><th>Modo LITE</th><th>Modo PRO</th></tr></thead><tbody><tr><td>Office</td><td>Employees.Office</td><td>fGet_Priority_EmployeeContract.Office</td></tr><tr><td>CompanyId</td><td>Offices.CompanyId</td><td>fGet_Priority_EmployeeContract.CompanyId</td></tr><tr><td>ContractId</td><td>NULL</td><td>ID del contrato prioritario</td></tr><tr><td>CalendarId</td><td>Offices.CalendarId</td><td>Offices.CalendarId del contrato</td></tr></tbody></table>

 

### 5.2 Código de Detección
    
    

```sql
DECLARE @Mode VARCHAR(5);
    SELECT @Mode = Mode FROM SetApplication WHERE Id = 1;
    
    CASE WHEN @Mode = 'LITE' THEN E.Office ELSE V.Office END
```
 

### 6\. Tipos de Conflicto

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;"><thead><tr><th>ID</th><th>Código</th><th>Severidad</th><th>Requiere Reapertura</th></tr></thead><tbody><tr><td>1</td><td>MARKING_ON_VALIDATED</td><td>WARNING</td><td>No</td></tr><tr><td>2</td><td>MARKING_ON_CONSOLIDATED</td><td>CRITICAL</td><td>Sí</td></tr><tr><td>3</td><td>MODIFY_CLOSED_MARKING</td><td>WARNING</td><td>No</td></tr><tr><td>4</td><td>DELETE_CLOSED_MARKING</td><td>CRITICAL</td><td>Sí</td></tr><tr><td>5</td><td>DATEJOURNEY_CHANGE_VALIDATED</td><td>WARNING</td><td>No</td></tr><tr><td>6</td><td>DATEJOURNEY_CHANGE_CONSOLIDATED</td><td>CRITICAL</td><td>Sí</td></tr><tr><td>7</td><td>ABSENCE_ON_CONSOLIDATED</td><td>CRITICAL</td><td>Sí</td></tr><tr><td>8</td><td>LEAVE_ON_CONSOLIDATED</td><td>CRITICAL</td><td>Sí</td></tr></tbody></table>

