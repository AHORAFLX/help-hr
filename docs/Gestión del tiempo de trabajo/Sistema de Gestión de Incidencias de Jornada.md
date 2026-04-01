# Sistema de Gestión de Incidencias de Jornada

Flexygo HR Docs

```
v3.5 | 2026-01-08
```
#### Contenido

  * Resumen Ejecutivo
  * 1\. Arquitectura de Datos
  * 2\. Catálogo de Categorías
  * 3\. Tipos de Incidencia (38)
  * 4\. Estados de Incidencias
  * 5\. Momentos de Detección
  * 6\. Procedimientos Detección
  * 7\. Procedimientos Resolución
  * 8\. Mecanismo DirtyFlag
  * 9\. Bloqueo de Validación
  * 10\. Vistas Dashboard
  * 11\. Auto-Resolución
  * 12\. Flujo Completo
  * 13\. Archivos Clave
  * 14\. Configuración Cron

## Documentación: Sistema de Gestión de Incidencias de Jornada

### Resumen Ejecutivo

El sistema de gestión de incidencias de Flexygo HR proporciona un mecanismo unificado para detectar, registrar, gestionar y resolver anomalías en las jornadas laborales de los empleados. Esta funcionalidad está diseñada para cumplir con el Real Decreto 8/2019 sobre registro de jornada y garantizar la integridad de los datos de asistencia.

### 1\. Arquitectura de Datos

### 1.1 Diagrama Entidad-Relación

erDiagram WorkdayIncidenceCategory ||--o{ WorkdayIncidenceType : "categoriza" WorkdayIncidenceType ||--o{ Employees_Assistence_Incidences : "tipifica" WorkdayIncidenceStatus ||--o{ Employees_Assistence_Incidences : "estado" Employees_Assistence ||--o{ Employees_Assistence_Incidences : "jornada" WorkdayIncidenceCategory { varchar CategoryCode PK nvarchar CategoryName nvarchar Description varchar Icon varchar Colour int SortOrder } WorkdayIncidenceType { smallint IncidenceTypeId PK varchar Code UK nvarchar Description varchar Category FK tinyint Severity nvarchar IconClass bit Active varchar DetectionMoment bit AutoResolvable bit BlocksValidation } WorkdayIncidenceStatus { varchar StatusCode PK nvarchar StatusName nvarchar Description bit IsFinal int SortOrder } Employees_Assistence_Incidences { int EmployeeId PK_FK date Date PK_FK smallint IncidenceTypeId PK_FK datetime DetectedAt varchar Source varchar StatusCode FK datetime ResolvedAt int ResolvedBy varchar ResolutionType }

### 1.2 Descripción de Tablas

<table><thead><tr><th>Tabla</th><th>Propósito</th><th>Archivo</th></tr></thead><tbody><tr><td><a class="file-link" href="#">WorkdayIncidenceCategory</a></td><td>Catálogo de categorías de incidencias</td><td>Tabla maestra</td></tr><tr><td><a class="file-link" href="#">WorkdayIncidenceType</a></td><td>Catálogo de 38 tipos de incidencias</td><td>Tabla maestra</td></tr><tr><td><a class="file-link" href="#">WorkdayIncidenceStatus</a></td><td>Estados posibles de incidencias</td><td>Tabla maestra</td></tr><tr><td><a class="file-link" href="#">Employees_Assistence_Incidences</a></td><td>Incidencias activas por jornada</td><td>Tabla transaccional</td></tr></tbody></table>

 

### 2\. Catálogo de Categorías

<table><thead><tr><th>Código</th><th>Nombre</th><th>Descripción</th><th>Color</th></tr></thead><tbody><tr><td><strong>MARKING</strong></td><td>Fichaje</td><td>Incidencias relacionadas con fichajes individuales</td><td><span class="badge badge-warning">warning</span></td></tr><tr><td><strong>WORKDAY</strong></td><td>Jornada</td><td>Incidencias a nivel de día completo de trabajo</td><td><span class="badge badge-info">info</span></td></tr><tr><td><strong>PLANNING</strong></td><td>Planificación</td><td>Problemas con turnos, calendarios y asignaciones</td><td><span class="badge badge-neutral">primary</span></td></tr><tr><td><strong>INTEGRITY</strong></td><td>Integridad</td><td>Violaciones de datos cerrados o validados</td><td><span class="badge badge-danger">danger</span></td></tr><tr><td><strong>COMPLIANCE</strong></td><td>Cumplimiento</td><td>Incumplimiento de normativa laboral (RD 8/2019)</td><td><span class="badge badge-danger">danger</span></td></tr><tr><td><strong>ABSENCE</strong></td><td>Ausencias</td><td>Problemas con vacaciones, permisos y bajas</td><td><span class="badge badge-info">info</span></td></tr></tbody></table>

 

### 3\. Catálogo Completo de Tipos de Incidencia

#### 3.1 MARKING (IDs 1-16) - Incidencias de Fichajes

<table><thead><tr><th>ID</th><th>Código</th><th>Descripción</th><th>Severidad</th><th>Detección</th><th>Auto-Resoluble</th><th>Bloquea</th></tr></thead><tbody><tr><td>1</td><td><code>UNIDENTIFIED</code></td><td>Sin identificar</td><td><span class="badge badge-info">Info</span></td><td>RECALC</td><td>✅</td><td>❌</td></tr><tr><td>2</td><td><code>UNIDENTIFIED_EMPLOYEE</code></td><td>Empleado no identificado</td><td><span class="badge badge-danger">Critical</span></td><td>TRIGGER</td><td>❌</td><td>✅</td></tr><tr><td>3</td><td><code>UNASSIGNED_SHIFT</code></td><td>Turno sin asignar</td><td><span class="badge badge-warning">Warning</span></td><td>RECALC</td><td>✅</td><td>❌</td></tr><tr><td>4</td><td><code>ILLOGICAL_SEQUENCE</code></td><td>Secuencia E/S incorrecta</td><td><span class="badge badge-danger">Critical</span></td><td>CRON_FAST</td><td>✅</td><td>✅</td></tr><tr><td>5</td><td><code>INCORRECT_MARKING_TYPE</code></td><td>Tipo de fichaje incorrecto</td><td><span class="badge badge-warning">Warning</span></td><td>RECALC</td><td>✅</td><td>❌</td></tr><tr><td>7</td><td><code>DESTINATION_CLOSED</code></td><td>Jornada destino cerrada</td><td><span class="badge badge-warning">Warning</span></td><td>TRIGGER</td><td>❌</td><td>❌</td></tr><tr><td>8</td><td><code>ALL_MARKINGS_IGNORED</code></td><td>Todos fichajes ignorados</td><td><span class="badge badge-warning">Warning</span></td><td>CRON_FAST</td><td>✅</td><td>❌</td></tr><tr><td>9</td><td><code>NO_CONTRACT</code></td><td>Empleado sin contrato</td><td><span class="badge badge-danger">Critical</span></td><td>RECALC</td><td>❌</td><td>✅</td></tr><tr><td>10</td><td><code>DELAYED_ENTRY</code></td><td>Entrada retrasada</td><td><span class="badge badge-info">Info</span></td><td>CRON_FAST</td><td>✅</td><td>❌</td></tr><tr><td>11</td><td><code>EARLY_DEPARTURE</code></td><td>Salida anticipada</td><td><span class="badge badge-info">Info</span></td><td>CRON_FAST</td><td>✅</td><td>❌</td></tr><tr><td>12</td><td><code>IP_NOT_ALLOWED</code></td><td>IP no permitida</td><td><span class="badge badge-warning">Warning</span></td><td>TRIGGER</td><td>❌</td><td>❌</td></tr><tr><td>13</td><td><code>PLANNING_IMPACT</code></td><td>Afecta planificación</td><td><span class="badge badge-warning">Warning</span></td><td>CRON_FAST</td><td>✅</td><td>❌</td></tr><tr><td>14</td><td><code>UNASSIGNED_MARKING</code></td><td>Fichaje sin asignar</td><td><span class="badge badge-warning">Warning</span></td><td>CRON_FAST</td><td>✅</td><td>❌</td></tr><tr><td>15</td><td><code>OUT_OF_SHIFT_RANGE</code></td><td>Fuera de límite de turno</td><td><span class="badge badge-warning">Warning</span></td><td>CRON_FAST</td><td>✅</td><td>❌</td></tr><tr><td>16</td><td><code>TIME_FRAUD</code></td><td>Desfase horario dispositivo</td><td><span class="badge badge-danger">Critical</span></td><td>CRON_FAST</td><td>✅</td><td>❌</td></tr></tbody></table>

 

NOTE El ID 6 (`UNPLANNED_PRESENCE`) fue eliminado y el hueco está reservado.

#### 3.2 WORKDAY (IDs 17-23) - Incidencias de Jornada

<table><thead><tr><th>ID</th><th>Código</th><th>Descripción</th><th>Severidad</th><th>Detección</th><th>Auto-Resoluble</th><th>Bloquea</th></tr></thead><tbody><tr><td>17</td><td><code>WORKED_ON_NON_WORKDAY</code></td><td>Fichaje registrado en día no laboral</td><td><span class="badge badge-warning">Warning</span></td><td>RECALC</td><td>✅</td><td>❌</td></tr><tr><td>18</td><td><code>MISSING_MARKINGS</code></td><td>Día laboral sin fichajes registrados</td><td><span class="badge badge-warning">Warning</span></td><td>RECALC</td><td>✅</td><td>❌</td></tr><tr><td>19</td><td><code>WORKED_ON_LEAVE</code></td><td>Fichaje registrado durante baja médica</td><td><span class="badge badge-danger">Critical</span></td><td>RECALC</td><td>❌</td><td>✅</td></tr><tr><td>20</td><td><code>WORKED_ON_HOLIDAY</code></td><td>Fichaje registrado en día de vacaciones</td><td><span class="badge badge-warning">Warning</span></td><td>RECALC</td><td>✅</td><td>❌</td></tr><tr><td>21</td><td><code>WORKED_ON_BANK_HOLIDAY</code></td><td>Fichaje en festivo sin turno de festivos</td><td><span class="badge badge-info">Info</span></td><td>RECALC</td><td>✅</td><td>❌</td></tr><tr><td>22</td><td><code>PARTIAL_DAY_CONFLICT</code></td><td>Ausencia parcial con tiempo trabajado excedido</td><td><span class="badge badge-warning">Warning</span></td><td>RECALC</td><td>✅</td><td>❌</td></tr><tr><td>23</td><td><code>OVERTIME_ON_FREE_DAY</code></td><td>Trabajo registrado en día libre según turno</td><td><span class="badge badge-info">Info</span></td><td>RECALC</td><td>✅</td><td>❌</td></tr></tbody></table>

 

#### 3.3 INTEGRITY (IDs 24-29) - Operaciones en Períodos Cerrados

<table><thead><tr><th>ID</th><th>Código</th><th>Descripción</th><th>Severidad</th><th>Detección</th><th>Auto-Resoluble</th><th>Bloquea</th></tr></thead><tbody><tr><td>24</td><td><code>MARKING_ON_CLOSED</code></td><td>Fichaje añadido a día cerrado</td><td><span class="badge badge-warning">Warning</span></td><td>CRON_FAST</td><td>❌</td><td>❌</td></tr><tr><td>25</td><td><code>MODIFY_CLOSED_MARKING</code></td><td>Modificación de fichaje cerrado</td><td><span class="badge badge-warning">Warning</span></td><td>TRIGGER</td><td>❌</td><td>❌</td></tr><tr><td>26</td><td><code>DELETE_CLOSED_MARKING</code></td><td>Eliminación de fichaje cerrado</td><td><span class="badge badge-danger">Critical</span></td><td>TRIGGER</td><td>❌</td><td>❌</td></tr><tr><td>27</td><td><code>DATEJOURNEY_CHANGE_CLOSED</code></td><td>Cambio de DateJourney en día cerrado</td><td><span class="badge badge-warning">Warning</span></td><td>TRIGGER</td><td>❌</td><td>❌</td></tr><tr><td>28</td><td><code>ABSENCE_ON_CLOSED</code></td><td>Ausencia/vacaciones añadida a día cerrado</td><td><span class="badge badge-warning">Warning</span></td><td>CRON_FAST</td><td>❌</td><td>❌</td></tr><tr><td>29</td><td><code>LEAVE_ON_CLOSED</code></td><td>Baja médica añadida a día cerrado</td><td><span class="badge badge-danger">Critical</span></td><td>CRON_FAST</td><td>❌</td><td>❌</td></tr></tbody></table>

 

#### 3.4 COMPLIANCE (IDs 30-38) - Cumplimiento Normativo Laboral

<table><thead><tr><th>ID</th><th>Código</th><th>Descripción</th><th>Severidad</th><th>Detección</th><th>Auto-Resoluble</th><th>Bloquea</th></tr></thead><tbody><tr><td>30</td><td><code>EXCEEDED_DAILY_HOURS</code></td><td>Superado límite horas diarias (según convenio)</td><td><span class="badge badge-warning">Warning</span></td><td>CRON_GLOBAL</td><td>✅</td><td>❌</td></tr><tr><td>31</td><td><code>EXCEEDED_WEEKLY_HOURS</code></td><td>Superado límite horas semanales (según convenio)</td><td><span class="badge badge-warning">Warning</span></td><td>CRON_GLOBAL</td><td>✅</td><td>❌</td></tr><tr><td>32</td><td><code>INSUFFICIENT_REST</code></td><td>Descanso entre jornadas &lt;12h</td><td><span class="badge badge-danger">Critical</span></td><td>CRON_GLOBAL</td><td>✅</td><td>✅</td></tr><tr><td>33</td><td><code>EXCEEDED_OVERTIME_LIMIT</code></td><td>Exceso horas extra anuales (&gt;80h)</td><td><span class="badge badge-danger">Critical</span></td><td>CRON_GLOBAL</td><td>❌</td><td>❌</td></tr><tr><td>34</td><td><code>MISSING_MANDATORY_BREAK</code></td><td>Trabajo &gt;6h sin pausa registrada</td><td><span class="badge badge-warning">Warning</span></td><td>CRON_GLOBAL</td><td>✅</td><td>❌</td></tr><tr><td>35</td><td><code>WEEKLY_REST_VIOLATION</code></td><td>Descanso semanal no respetado</td><td><span class="badge badge-danger">Critical</span></td><td>CRON_GLOBAL</td><td>✅</td><td>✅</td></tr><tr><td>36</td><td><code>EXCEEDED_MONTHLY_OVERTIME</code></td><td>Exceso horas extra mensuales</td><td><span class="badge badge-warning">Warning</span></td><td>CRON_GLOBAL</td><td>✅</td><td>❌</td></tr><tr><td>37</td><td><code>EXCEEDED_MONTHLY_HOURS</code></td><td>Superado límite horas mensuales</td><td><span class="badge badge-warning">Warning</span></td><td>CRON_GLOBAL</td><td>✅</td><td>❌</td></tr><tr><td>38</td><td><code>EXCEEDED_ANNUAL_HOURS</code></td><td>Superado límite horas anuales</td><td><span class="badge badge-danger">Critical</span></td><td>CRON_GLOBAL</td><td>❌</td><td>❌</td></tr></tbody></table>

 

### 4\. Estados de Incidencias

<table><thead><tr><th>Código</th><th>Nombre</th><th>Descripción</th><th>Es Final</th></tr></thead><tbody><tr><td><code>PENDING</code></td><td>Pendiente</td><td>Incidencia detectada, pendiente de gestión</td><td>❌</td></tr><tr><td><code>RESOLVED</code></td><td>Resuelta</td><td>Incidencia resuelta (manual, justificada o automática)</td><td>✅</td></tr><tr><td><code>IGNORED</code></td><td>Ignorada</td><td>Incidencia descartada intencionalmente</td><td>✅</td></tr></tbody></table>

 

### 5\. Momentos de Detección

flowchart LR subgraph Tiempo_Real["⚡ Tiempo Real"] TRIGGER["TRIGGER  
En triggers SQL"] end subgraph Cron_Frecuente["? Cada 5-10 min"] RECALC["RECALC  
pCron_Incidences_Recalc"] CRON_FAST["CRON_FAST  
pCron_Incidences_Fast"] end subgraph Cron_Diario["? 1-2x/día"] CRON_GLOBAL["CRON_GLOBAL  
pCron_Incidences_Global"] end TRIGGER --> Insert_EAI[(Employees_Assistence_Incidences)] RECALC --> Insert_EAI CRON_FAST --> Insert_EAI CRON_GLOBAL --> Insert_EAI

<table><thead><tr><th>Momento</th><th>Frecuencia</th><th>Procedimiento</th><th>Incidencias Detectadas</th></tr></thead><tbody><tr><td><strong>TRIGGER</strong></td><td>Tiempo real</td><td>Triggers en tablas</td><td>IDs 2, 7, 12, 25, 26, 27</td></tr><tr><td><strong>RECALC</strong></td><td>Cada 5 min</td><td><a class="file-link" href="#">pCron_Incidences_Recalc</a></td><td>IDs 1, 3, 5, 9, 17-23</td></tr><tr><td><strong>CRON_FAST</strong></td><td>Cada 5-10 min</td><td><a class="file-link" href="#">pCron_Incidences_Fast</a></td><td>IDs 4, 8, 10-16, 24, 28, 29</td></tr><tr><td><strong>CRON_GLOBAL</strong></td><td>1-2x/día</td><td><a class="file-link" href="#">pCron_Incidences_Global</a></td><td>IDs 30-38</td></tr></tbody></table>

 

### 6\. Procedimientos de Detección

### 6.1 pCron_Incidences_Fast

Propósito: Detecta incidencias de MARKING e INTEGRITY que requieren cálculo moderado.

#### Parámetros:

  * `@DaysBack INT = 3` \- Días hacia atrás a procesar
  * `@MaxRecords INT = 500` \- Máximo de jornadas por ejecución
  * `@BaseDate DATE = NULL` \- Fecha base para el cálculo
  * `@EmployeeId INT = NULL` \- Filtrar por empleado
  * `@TargetDates T_EmployeeDateTable` \- Tabla TVP para procesamiento BATCH

#### Casos de Uso:
    
    
1. Ejecución estándar (Cron)

```sql
EXEC dbo.pCron_Incidences_Fast @DaysBack = 3
    
    -- 2. Recálculo BATCH
    EXEC dbo.pCron_Incidences_Fast @TargetDates = @MiTabla
    
    -- 3. Recálculo histórico un empleado
    EXEC dbo.pCron_Incidences_Fast @BaseDate = '2025-11-30', @DaysBack = 7, @EmployeeId = 123
```

### 6.2 pCron_Incidences_Global

Propósito: Detecta incidencias de COMPLIANCE (cumplimiento normativo).

Características especiales:

  * Obtiene límites de horas desde el convenio colectivo (`Collective_Agreement`)
  * Campos utilizados: `MaxDailyHours`, `MaxWeeklylHours`, `MaxMonthylHours`, `MaxAnnualHours`
  * Valores por defecto: 10h diarias, 40h semanales

### 6.3 pCron_Incidences_Recalc

Propósito: Orquestador que prioriza jornadas sucias (`DirtyFlag = 1`) y llama a `pEmployees_Assistence_RecalcMetrics`.

### 7\. Procedimientos de Resolución

### 7.1 pIncidence_Resolve - Resolución Individual
    
    
    EXEC dbo.pIncidence_Resolve 
        @EmployeeId = 123,
        @Date = '2025-12-20',
        @IncidenceTypeId = 10,
        @ResolutionType = 'JUSTIFIED',  -- 'MANUAL', 'JUSTIFIED', 'IGNORED'
        @ResolvedBy = 1

### 7.2 pIncidence_Resolve_Batch - Resolución Masiva
    
    
    DECLARE @Incidencias AS T_EmployeeDateTable;
    INSERT INTO @Incidencias VALUES (123, '2025-12-20'), (124, '2025-12-20');
    
    EXEC dbo.pIncidence_Resolve_Batch 
        @IncidenceTable = @Incidencias,
        @IncidenceTypeId = 10,
        @ResolutionType = 'MANUAL',
        @ResolvedBy = 1

### 7.3 pIncidence_InsertFromMarking - Inserción desde Aplicación
    
    
    -- Usado desde VB.NET/API cuando se detecta incidencia en tiempo real
    EXEC dbo.pIncidence_InsertFromMarking 
        @EmployeeId = 123,
        @Date = '2025-12-20',
        @IncidenceTypeId = 12,  -- IP_NOT_ALLOWED
        @Source = 'APP'

### 8\. Mecanismo DirtyFlag


El `DirtyFlag` en `Employees_Assistence` se utiliza para detectar cambios en jornadas ya validadas/consolidadas.

flowchart TD subgraph Cambio["Cambio en Jornada Cerrada"] A[Nuevo Fichaje] --> B{StatusId > 0?} C[Nueva Ausencia] --> B D[Nueva Baja] --> B end B -->|Sí| E[pEmployeeAssistence_MarkDirty] E --> F[DirtyFlag = 1] E --> G[DirtyReason = tipo de cambio] E --> H[Registro en DirtyLog] F --> I[pCron_Incidences_Fast] G --> I I --> J{DirtyReason contiene...} J -->|Marking/fichaje| K[ID 24: MARKING_ON_CLOSED] J -->|Vacación/Ausencia| L[ID 28: ABSENCE_ON_CLOSED] J -->|Baja| M[ID 29: LEAVE_ON_CLOSED]

Procedimiento: pEmployeeAssistence_MarkDirty

### 9\. BlocksValidation - Bloqueo de Validación

Incidencias con `BlocksValidation = 1` impiden la validación de jornadas mientras estén pendientes.

### Incidencias Bloqueantes (5 tipos)

<table><thead><tr><th>ID</th><th>Código</th><th>Descripción</th></tr></thead><tbody><tr><td>2</td><td><code>UNIDENTIFIED_EMPLOYEE</code></td><td>Empleado no identificado</td></tr><tr><td>4</td><td><code>ILLOGICAL_SEQUENCE</code></td><td>Secuencia E/S incorrecta</td></tr><tr><td>9</td><td><code>NO_CONTRACT</code></td><td>Empleado sin contrato</td></tr><tr><td>19</td><td><code>WORKED_ON_LEAVE</code></td><td>Fichaje durante baja médica</td></tr><tr><td>32</td><td><code>INSUFFICIENT_REST</code></td><td>Descanso entre jornadas &lt;12h</td></tr><tr><td>35</td><td><code>WEEKLY_REST_VIOLATION</code></td><td>Descanso semanal no respetado</td></tr></tbody></table>

 

Implementación en pDateEmployee_Validate_Period:
    
    
```sql
IF EXISTS (
SELECT 1 
        FROM dbo.vIncidences_Active I
        INNER JOIN #ToValidate T ON I.EmployeeId = T.EmployeeId AND I.[Date] = T.[Date]
        WHERE I.BlocksValidation = 1
    )
    BEGIN
        RAISERROR(...);  -- Bloquea la validación
        RETURN 0;
    END
```
### 10\. Vistas para Dashboard

  * vIncidences_Unified: Vista base con todas las incidencias y sus tipos.
  * vIncidences_Active: Solo incidencias con `StatusCode = 'PENDING'`.
  * vDashboard_Compliance_Alerts: Incidencias de categoría COMPLIANCE e INTEGRITY pendientes.
  * vDashboard_Validation_Funnel: Métricas agregadas por empresa/oficina/mes:
    * Total jornadas
    * Pendientes / Validadas / Consolidadas
    * Jornadas "sucias" (`DirtyFlag = 1`)
    * Bloqueadas (con incidencias BlocksValidation = 1)

### 11\. Auto-Resolución

Las incidencias con `AutoResolvable = 1` se resuelven automáticamente cuando:

  1. La condición que las causó ya no existe
  2. Se ejecuta el procedimiento de detección correspondiente


Ejemplo Si un empleado tenía `DELAYED_ENTRY` y se añade una ausencia parcial que justifica la entrada tardía, al recalcular se marca como `RESOLVED` con `ResolutionType = 'AUTO_RESOLVED'`.

### 12\. Flujo Completo de Incidencias

sequenceDiagram participant App as Aplicación participant Trigger as Triggers SQL participant Cron as Flexygo Cron participant EAI as Employees_Assistence_Incidences participant UI as Dashboard UI participant User as Usuario RRHH Note over App,User: DETECCIÓN App->>Trigger: Nuevo fichaje/ausencia Trigger->>EAI: INSERT incidencia (TRIGGER) Cron->>EAI: EXEC pCron_Incidences_Fast (cada 5-10 min) Cron->>EAI: EXEC pCron_Incidences_Global (1-2x/día) Note over App,User: VISUALIZACIÓN EAI->>UI: vIncidences_Active UI->>User: Dashboard con incidencias pendientes Note over App,User: RESOLUCIÓN alt Automática Cron->>EAI: UPDATE StatusCode='RESOLVED', ResolutionType='AUTO_RESOLVED' else Manual User->>EAI: EXEC pIncidence_Resolve (MANUAL/JUSTIFIED/IGNORED) end Note over App,User: VALIDACIÓN User->>App: Validar período App->>EAI: ¿Existe BlocksValidation=1? alt Sí App-->>User: ERROR: Bloqueo de validación else No App->>App: Proceder con validación end

### 13\. Archivos Clave del Sistema

### Tablas

```
WorkdayIncidenceCategory.sql
WorkdayIncidenceType.sql
WorkdayIncidenceStatus.sql
Employees_Assistence_Incidences.sql
```
### Datos de Catálogo

```
WorkdayIncidenceCategory.sql (data)
WorkdayIncidenceType.sql (data)
WorkdayIncidenceStatus.sql (data)
```
### Procedimientos de Detección

```
pCron_Incidences_Fast.sql
pCron_Incidences_Global.sql
pCron_Incidences_Recalc.sql
```
### Procedimientos de Gestión

```
pIncidence_Resolve.sql
pIncidence_Resolve_Batch.sql
pIncidence_InsertFromMarking.sql
pEmployeeAssistence_MarkDirty.sql
```
### Vistas

```
vIncidences_Unified.sql
vIncidences_Active.sql
vDashboard_Compliance_Alerts.sql
vDashboard_Validation_Funnel.sql
```
### 14\. Configuración Cron Recomendada

<table><thead><tr><th>Procedimiento</th><th>Frecuencia</th><th>Comando</th></tr></thead><tbody><tr><td>pCron_Incidences_Recalc</td><td>Cada 5 min</td><td><code>EXEC dbo.pCron_Incidences_Recalc</code></td></tr><tr><td>pCron_Incidences_Fast</td><td>Cada 5-10 min</td><td><code>EXEC dbo.pCron_Incidences_Fast @DaysBack = 3</code></td></tr><tr><td>pCron_Incidences_Global</td><td>1-2x/día</td><td><code>EXEC dbo.pCron_Incidences_Global @DaysBack = 7</code></td></tr></tbody></table>

 

Documentación generada: 2026-01-08 | Versión del sistema: v3.5