# Sistema de Consolidación de Jornadas y Cierre de Periodos

##   

### Documentación Técnica para Desarrolladores de Interfaz

 

### 1\. Contexto y Problema

### Situación Anterior

  * `Employees_Assistence` solo contenía registros de días con fichajes.
  * Días sin fichajes (vacaciones, bajas, permisos, festivos) no existían en la tabla.
  * Al consolidar datos para informes, había huecos que requerían cálculo en tiempo real.

### Objetivo

Garantizar que `Employees_Assistence` contenga un registro por cada día del año mientras el empleado esté activo, independientemente de si fichó o no.

 

### 2\. Arquitectura de la Solución
    
    
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                         FLUJOS DE TRABAJO                                │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                          │
    │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐     │
    │  │  FICHAJE (E/S)  │───▶│  Markings       │───▶│ Employees_      │     │
    │  │  (Trigger)      │    │  MarkingsPair   │    │ Assistence      │     │
    │  └─────────────────┘    └─────────────────┘    └────────┬────────┘     │
    │                                                          │              │
    │  ┌─────────────────┐                           ┌────────▼────────┐     │
    │  │ CRON DIARIO     │──────────────────────────▶│ Días faltantes  │     │
    │  │ (02:00)         │  pCron_Generate_          │ generados       │     │
    │  └─────────────────┘  Yesterday_Workdays       └────────┬────────┘     │
    │                                                          │              │
    │  ┌─────────────────┐                           ┌────────▼────────┐     │
    │  │ VALIDACIÓN      │──────────────────────────▶│ StatusId: 0→1   │     │
    │  │ DIARIA          │  pDateEmployee_           │ (Validado)      │     │
    │  └─────────────────┘  Validate_Period          └─────────────────┘     │
    │                                                                          │
    │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐     │
    │  │ CIERRE DE       │───▶│ EnsureInit      │───▶│ Validate        │     │
    │  │ PERIODO         │    │ (genera huecos) │    │ + Registra      │     │
    │  └─────────────────┘    └─────────────────┘    └─────────────────┘     │
    │  pEmployees_PeriodValidation_Close              			              │
    │                                                 					        │
    └─────────────────────────────────────────────────────────────────────────┘

 

### 3\. Componentes de Base de Datos

### 3.1 Tablas

<table border="1" cellpadding="6" cellspacing="0"><thead><tr><th>Tabla</th><th>Propósito</th></tr></thead><tbody><tr><td><code>Employees_Assistence</code></td><td>Registro diario de cada empleado (fichado o no)</td></tr></tbody></table>

 


### 3.2 Stored Procedures

<table border="1" cellpadding="6" cellspacing="0"><thead><tr><th>SP</th><th>Uso</th><th>Cuándo Llamarlo</th></tr></thead><tbody><tr><td><code>pDateEmployee_Validate_Period</code></td><td>Validación diaria/semanal</td><td>Desde UI: "Validar seleccionados"</td></tr><tr><td><code>pEmployees_PeriodValidation_Close</code></td><td>Cierre mensual completo</td><td>Desde UI: "Cerrar Periodo"</td></tr><tr><td><code>pEmployees_Assistence_EnsureInit</code></td><td>Genera días para UN empleado</td><td>Interno (no llamar desde UI)</td></tr><tr><td><code>pEmployees_Assistence_EnsureComplete_All</code></td><td>Genera días para TODOS</td><td>Interno / Cron</td></tr><tr><td><code>pCron_Generate_Yesterday_Workdays</code></td><td>Genera día anterior automáticamente</td><td>Tarea programada (Cron)</td></tr></tbody></table>

 

 *

### 4\. APIs para la Interfaz

### 4.1 Validar Días Seleccionados (sin cambios)
    
    

```sql
EXEC pDateEmployee_Validate_Period 
        @CurrentReference = {UserId},
        @StartDate = '2025-11-01',
        @EndDate = '2025-11-30';
```    

  * Comportamiento: Valida registros existentes con `StatusId = 0`.
  * No genera días faltantes.
  * Uso UI: Botón "Validar Seleccionados" en cuadrante.

### 4.2 Cerrar Periodo (NUEVO)
    
```sql    
    -- Un empleado específico
    EXEC pEmployees_PeriodValidation_Close 
        @EmployeeId = 123,
        @EndDate = '2025-11-30',
        @UserId = {CurrentUserId};
    
    -- Todos los empleados
    EXEC pEmployees_PeriodValidation_Close 
        @EmployeeId = NULL,
        @EndDate = '2025-11-30',
        @UserId = {CurrentUserId};
    
```
  * Genera días faltantes (vacaciones, bajas, etc.)
  * Valida todos los días
  * Actualiza `Employees_PeriodValidation`
  * Uso UI: Botón "Cerrar Periodo" / "Cerrar Mes".

### 4.3 Consultar Estado de Cierre
    
```sql    
    SELECT 
        E.EmployeeId,
        E.FullName,
        P.LastValidatedDate,
        P.ValidationDate,
        P.ValidatedBy
    FROM Employees E
    LEFT JOIN Employees_PeriodValidation P ON E.EmployeeId = P.EmployeeId
    WHERE E.Discharge IS NULL;
```

### 5\. Cambios Sugeridos en Interfaz

### 5.1 Cuadrante / Gestión de Jornadas

Añadir botón "Cerrar Periodo":
    
    
    ┌─────────────────────────────────────────────────────────────┐
    │  Noviembre 2025                     [Cerrar Mes ▼]          │
    ├─────────────────────────────────────────────────────────────┤
    │  [✓] Validar Seleccionados    [Recalcular]    [Exportar]    │
    └─────────────────────────────────────────────────────────────┘

Comportamiento del botón:

  1. Confirmar: “¿Cerrar el periodo hasta {fecha}? Esto generará días faltantes y validará todo.”
  2. Llamar a `pEmployees_PeriodValidation_Close`.
  3. Mostrar resultado: “Cerrado. X empleados procesados.”

### 5.2 Indicador Visual de Estado
    
    
    ┌──────────────────────────────────────────────────────────────┐
    │ Empleado          │ Último Cierre  │ Estado Noviembre        │
    ├───────────────────┼────────────────┼─────────────────────────┤
    │ Juan Pérez        │ 2025-10-31     │ Pendiente               │
    │ María García      │ 2025-11-30     │ Cerrado                 │
    │ Carlos López      │ NULL           │ Nunca cerrado           │
    └──────────────────────────────────────────────────────────────┘

### 5.3 Vista de Empleado Individual
    
    
    ┌────────────────────────────────────────┐
    │ Estado de Consolidación                │
    ├────────────────────────────────────────┤
    │ Último periodo cerrado: 31/10/2025     │
    │ Cerrado por: Admin                     │
    │ Fecha de cierre: 05/11/2025 09:30      │
    └────────────────────────────────────────┘

 

### 6\. Flujo de Trabajo Recomendado

### Operación Mensual (Cierre de Nómina)
    
    
    1. Usuario accede a "Gestión de Periodos" o "Cuadrante"
    2. Selecciona mes a cerrar (ej: Noviembre 2025)
    3. Click en "Cerrar Periodo"
    4. Sistema ejecuta pEmployees_PeriodValidation_Close
    5. Se generan días faltantes → Se validan → Se registra cierre
    6. Usuario puede exportar datos consolidados

### Operación Diaria (Validación Normal)
    
    
    1. Gestor revisa jornadas del día/semana
    2. Corrige incidencias si las hay
    3. Click en "Validar Seleccionados"
    4. Sistema ejecuta pDateEmployee_Validate_Period
    5. Solo valida lo existente (sin generar días)

 

### 7\. Notas Importantes

### El cierre NO bloquea modificaciones

  * Los datos cerrados pueden seguir editándose.
  * El sistema `DirtyFlag` sigue funcionando.
  * `Employees_PeriodValidation` es solamente informativo.

### Generación retroactiva automática

  * El Cron `pCron_Generate_Yesterday_Workdays` genera días pasados cada noche.
  * No es necesario cerrar periodos para que aparezcan días.
  * El cierre es para consolidación formal (reporting, nómina).

### Re-cierre de periodos

  * Se puede ejecutar el cierre varias veces.
  * Actualiza fecha y genera días faltantes si existen.

 

### 8\. Resumen de Cambios Backend

<table border="1" cellpadding="6" cellspacing="0"><thead><tr><th>Archivo</th><th>Acción</th><th>Descripción</th></tr></thead><tbody><tr><td><code>Employees_PeriodValidation.sql</code></td><td>NUEVO</td><td>Tabla de control de cierres</td></tr><tr><td><code>pEmployees_PeriodValidation_Close.sql</code></td><td>NUEVO</td><td>SP de cierre de periodo</td></tr><tr><td><code>pEmployees_Assistence_EnsureInit.sql</code></td><td>EXISTENTE</td><td>Genera días para un empleado</td></tr><tr><td><code>pEmployees_Assistence_EnsureComplete_All.sql</code></td><td>EXISTENTE</td><td>Genera días para todos</td></tr><tr><td><code>pEmployeeDate_Refresh_Target.sql</code></td><td>MODIFICADO</td><td>Ya no borra días sin fichajes</td></tr><tr><td><code>pDateEmployee_Validate_Period.sql</code></td><td>SIN CAMBIOS</td><td>Sigue validando solo lo existente</td></tr></tbody></table>