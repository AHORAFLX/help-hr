# Revertir la integración de Ahora ERP
La integración entre Sebastian HR y AHORA ERP es un proceso irreversible que no podrá deshacerse desde la propia aplicación una vez activado. 

Esta documentación detalla los cambios que se aplican durante el proceso de activación y proporciona los pasos necesarios para revertir manualmente al estado original.

## Requisitos previos

  - **Conocimientos de SQL**: Es necesario tener conocimientos sólidos del lenguaje SQL y de la estructura de tablas de Flexygo.
  - **Acceso directo a base de datos**: Los cambios deberán ejecutarse directamente en el servidor SQL.
  - **Comprensión del proceso**: Es fundamental leer y comprender completamente este documento antes de proceder.

## Advertencias

  - **Backup obligatorio**: Realice copias de seguridad completas de las bases de datos antes de iniciar cualquier proceso.
  - **Entornos de producción**: Extreme las precauciones al ejecutar estos scripts en entornos de producción. Se recomienda probar primero en desarrollo/pruebas.
  - **Ojo**: Lee cada script antes de ejecutarlo. Si no entiendes lo que hace, no lo ejecutes. Un error puede tener consecuencias graves en tu sistema.

!!! info "Tómate tu tiempo"
    Esta guía está diseñada para ayudarle a realizar el proceso de reversión de manera controlada y segura. Tómese el tiempo necesario para comprender cada paso y no dude en consultar con el equipo técnico si tiene alguna duda.


## Configuración genérica del ERP

Esta configuración **siempre se ejecuta**.

### Base de datos: Conf — Tabla: Objects

  - Activa 8 objetos relacionados con documentos e imágenes del ERP
  - Configura conexión y tipos de operación para estos objetos

**Objetos activados:**

  - `AHORA_Documento`, `AHORA_Documentos`, `AHORA_Imagen`, `AHORA_Imagenes`
  - `AHORA_Documento_Documento`, `AHORA_Documentos_Documento`
  - `AHORA_Documento_Tabla`, `AHORA_Documentos_Tablas`

**Cambios por objeto:**

  - `Active` = 1 (activado)
  - `ConnStringID` = 'ERPConnectionString'
  - `InsertType`, `UpdateType`, `DeleteType` = 'erpstored'

### Base de datos: Data — Tabla: Settings

  - `AhoraERP`: Content = 1

## Integración de empleados

### Base de datos: Conf

**Objects**

| Objeto | Campo | Valor Nuevo |
| --- | --- | --- |
| `emp_EmpleadoERP` | Active | **1** |
| `emp_EmpleadosERP` | Active | **1** |
| `emp_Employee` | InsertType | **'dll'** |
| `emp_Employee` | InsertProcessName | **'HR_ERP_InsertEmployeeOnSebastianAndOnERP'** |
| `emp_Employee` | UpdateType | **'dll'** |
| `emp_Employee` | UpdateProcessName | **'HR_ERP_UpdateEmployeeOnSebastianAndOnERP'** |
| `emp_EmployeePersonalData` | InsertType | **'dll'** |
| `emp_EmployeePersonalData` | InsertProcessName | **'HR_ERP_InsertEmployeeOnSebastianAndOnERP'** |
| `emp_EmployeePersonalData` | UpdateType | **'dll'** |
| `emp_EmployeePersonalData` | UpdateProcessName | **'HR_ERP_UpdateEmployeeOnSebastianAndOnERP'** |

**Jobs**

| Objeto | Campo | Valor Nuevo |
| --- | --- | --- |
| `hr_AhoraERP_Employees` | Enabled | 1 |

**Navigation_Nodes**

| Objeto | Campo | Valor Nuevo |
| --- | --- | --- |
| NodeId `497A5C4E-4C47-4200-85EA-21FB3E3A0F65` | Enabled | 1 |

### Base de datos: Data

**Settings**

| Objeto | Campo | Valor Nuevo |
| --- | --- | --- |
| `AhoraEmployees` | Content | 1 |

## Integración de gastos y partes

### Base de datos: Conf

**Objects**

| Objeto | Campo | Valor Nuevo |
| --- | --- | --- |
| `emp_TiposGastos_Linea` | Active | **1** |
| `emp_TiposGastos_Lineas` | Active | **1** |
| `emp_TiposGastos_Linea` | InsertType, UpdateType, DeleteType | **'erpstored'** |
| `emp_TiposGastos_Lineas` | InsertType, UpdateType, DeleteType | **'erpstored'** |

**Objects_Properties**

| Objeto | Propiedad | Campo | Valor Nuevo |
| --- | --- | --- | --- |
| `emp_Expenses_Type` | CodExpenses | IsRequired | **0** |
| `emp_Expenses_Types` | CodExpenses | IsRequired | **0** |
| `emp_Part_Expenses` | IdClient | Hide, TypeId, CustomPropName, ConnStringId | **0, 'custom', 'pEmp_ERP_Clients_CustomControl', 'ERPConnectionString'** |
| `emp_Part_Expenses` | Client | Hide | **1** |
| `emp_Travel` | IdClient | Hide, TypeId, CustomPropName, ConnStringId | **0, 'custom', 'pEmp_ERP_Clients_CustomControl', 'ERPConnectionString'** |
| `emp_Travel` | Client | Hide | **1** |

### Otras tablas modificadas:

| Tabla | Cambio |
| --- | --- |
| Objects_Properties_Dependencies | Active = 1 para emp_Part_Expenses.IdClient y emp_Travel.IdClient |
| Jobs | hr_AhoraERP_SendExpensesToERP Enabled = 1 |
| Navigation_Nodes | NodeId 0F1F1B5C-6117-42CA-A7F1-C7B4CA3AE804 Enabled = 1 |
| ChatGPT_Settings | Actualiza SystemPrompt para 'Asistente-Gastos' |
| ChatGPT_Settings_DataModel | Inserta 2 registros para vClientesERP |
| Processes_Params | Configura IdClient y Client en Emp_RequestTravel |
| Processes_Params_Dependencies | Inserta dependencia para Emp_RequestTravel.IdClient |

### Base de datos: Data

**Settings**

| Objeto | Campo | Valor Nuevo |
| --- | --- | --- |
| `AhoraExpenses` | Content | 1 |
| `AhoraSendExpensesDocuments` | Content | [valor del parámetro] |

**Vistas**

Crear la vista `vClientesERP` apuntando a `ERPConnectionString.dbo.Clientes_Datos`.

## Integración de proyectos

### Base de datos: Conf

**Objects**

| Objeto | Campo | Valor Nuevo |
| --- | --- | --- |
| `Project` | CanInsert, CanDelete | **0** |
| `Projects` | CanInsert, CanDelete | **0** |

**Objects_Properties**

| Objeto | Propiedad | Campo | Valor Nuevo |
| --- | --- | --- | --- |
| `Project, Projects` | Descrip, ExternalCodeId, ProjectId | Locked | **1** |

**Jobs**

| Objeto | Campo | Valor Nuevo |
| --- | --- | --- |
| `hr_AhoraERP_Projects` | Enabled | **1** |

### Base de datos: Data

**Settings**

| Objeto | Campo | Valor Nuevo |
| --- | --- | --- |
| `AhoraProjects` | Content | **1** |

## Valores originales

Estos son los valores antes de la integración.

### Configuración genérica del ERP

| Tabla | Campo | Valor Original |
| --- | --- | --- |
| Objects (AHORA_*) | Active | **false** |
| Settings | AhoraERP Content | **'0'** |

### Integración de empleados

| Objeto | Campo | Valor Original |
| --- | --- | --- |
| `emp_EmpleadoERP` | Active | **false** |
| `emp_Employee` | InsertType | **'standard'** |
| `emp_Employee` | UpdateType | **'stored'** |
| `emp_Employee` | UpdateProcessName | **'pEmp_Update_Employee'** |
| `emp_EmployeePersonalData` | InsertType, UpdateType | **'standard'** |
| Jobs | hr_AhoraERP_Employees Enabled | **false** |
| Settings | AhoraEmployees Content | **'0'** |

### Integración de gastos

| Objeto/Tabla | Propiedad/Campo | Campo | Valor Original |
| --- | --- | --- | --- |
| emp_TiposGastos_Linea | - | Active | **false** |
| emp_Part_Expenses | IdClient | Hide | **true** |
| emp_Part_Expenses | IdClient | TypeId | **'text'** |
| emp_Part_Expenses | Client | Hide | **false** |
| emp_Travel | IdClient | Hide, TypeId | **true, 'number'** |
| Emp_RequestTravel | IdClient | Hide | **true** |
| Settings | AhoraExpenses | Content | **'0'** |
| Vista | vClientesERP | - | **No existe** |

### Integración de proyectos

| Objeto | Campo/Propiedad | Valor Original |
| --- | --- | --- |
| Project, Projects | CanInsert, CanDelete | **true** |
| Project, Projects | Descrip, ExternalCodeId Locked | **false** |
| Jobs | hr_AhoraERP_Projects Enabled | **false** |
| Settings | AhoraProjects Content | **'0'** |

## Scripts de reversión

!!! warning "Importante"
    - Hacer backup completo antes de ejecutar
    - Ejecutar en transacciones para poder hacer rollback si hay errores
    - Reiniciar la aplicación después de revertir

### Integración de proyectos

**Base de datos: Conf**

Revertir Jobs

```sql
UPDATE Jobs 
    SET Enabled = 0 
    WHERE JobName = 'hr_AhoraERP_Projects';
    
    -- Revertir Objects
    UPDATE Objects 
    SET CanInsert = 1, CanDelete = 1 
    WHERE ObjectName IN ('Project', 'Projects');
    
    -- Revertir Objects_Properties
    UPDATE Objects_Properties 
    SET Locked = 0 
    WHERE ObjectName IN ('Project', 'Projects') 
      AND PropertyName IN ('Descrip', 'ExternalCodeId');
```
**Base de datos: Data**

```sql    
    -- Revertir Settings
    UPDATE Settings 
    SET Content = '0' 
    WHERE IdSettings = 'AhoraProjects';
```

### Revertir integración de gastos/partes

**Base de datos: Conf**

```sql    
    -- Revertir Jobs
    UPDATE Jobs SET Enabled = 0 WHERE JobName = 'hr_AhoraERP_SendExpensesToERP';
    
    -- Revertir Navigation_Nodes
    UPDATE Navigation_Nodes SET Enabled = 0 
    WHERE NodeId = '0F1F1B5C-6117-42CA-A7F1-C7B4CA3AE804';
    
    -- Revertir Objects
    UPDATE Objects SET Active = 0 
    WHERE ObjectName IN ('emp_TiposGastos_Linea', 'emp_TiposGastos_Lineas');
    
    UPDATE Objects SET InsertType = 'standard', UpdateType = 'standard', 
    DeleteType = 'standard' WHERE ObjectName IN ('emp_TiposGastos_Linea', 'emp_TiposGastos_Lineas');
    
    -- Revertir Objects_Properties
    UPDATE Objects_Properties SET IsRequired = 0 
    WHERE ObjectName IN ('emp_Expenses_Type', 'emp_Expenses_Types') 
      AND PropertyName = 'CodExpenses';
    
    UPDATE Objects_Properties 
    SET Hide = 1, TypeId = 'text', CustomPropName = NULL, ConnStringId = NULL 
    WHERE ObjectName = 'emp_Part_Expenses' AND PropertyName = 'IdClient';
    
    UPDATE Objects_Properties SET Hide = 0 
    WHERE ObjectName = 'emp_Part_Expenses' AND PropertyName = 'Client';
    
    UPDATE Objects_Properties 
    SET Hide = 1, TypeId = 'number', CustomPropName = NULL, ConnStringId = NULL 
    WHERE ObjectName = 'emp_Travel' AND PropertyName = 'IdClient';
    
    UPDATE Objects_Properties SET Hide = 0 
    WHERE ObjectName = 'emp_Travel' AND PropertyName = 'Client';
    
    -- Revertir Dependencies
    UPDATE Objects_Properties_Dependencies SET Active = 0 
    WHERE ObjectName IN ('emp_Part_Expenses', 'emp_Travel') AND PropertyName = 'IdClient';
    
    -- Revertir Processes_Params
    UPDATE Processes_Params 
    SET Hide = 1, TypeId = 'text', CustomPropName = NULL, 
        DetachedFromProcess = 0, ConnStringId = 'DataConnectionString' 
    WHERE ProcessName = 'Emp_RequestTravel' AND ParamName = 'IdClient';
    
    UPDATE Processes_Params SET Hide = 0 
    WHERE ProcessName = 'Emp_RequestTravel' AND ParamName = 'Client';
    
    -- Revertir Processes_Params_Dependencies
    DELETE FROM Processes_Params_Dependencies 
    WHERE ProcessName = 'Emp_RequestTravel' AND ParamName = 'IdClient';
    
    -- Revertir ChatGPT
    DELETE FROM ChatGPT_Settings_DataModel 
    WHERE SettingId = 'Asistente-Gastos' AND TableName = 'vClientesERP';
```
**Base de datos: Data**

```sql    
    -- Revertir Settings
    UPDATE Settings SET Content = '0' 
    WHERE IdSettings IN ('AhoraExpenses', 'AhoraSendExpensesDocuments');
    
    -- Eliminar vista
    DROP VIEW IF EXISTS vClientesERP;
```

### Revertir integración de empleados

**Base de datos: Conf**

```sql    
    -- Revertir Jobs
    UPDATE Jobs SET Enabled = 0 WHERE JobName = 'hr_AhoraERP_Employees';
    
    -- Revertir Navigation_Nodes
    UPDATE Navigation_Nodes SET Enabled = 0 
    WHERE NodeId = '497A5C4E-4C47-4200-85EA-21FB3E3A0F65';
    
    -- Revertir Objects
    UPDATE Objects SET Active = 0 
    WHERE ObjectName IN ('emp_EmpleadoERP', 'emp_EmpleadosERP');
    
    UPDATE Objects SET InsertType = 'standard', InsertProcessName = NULL 
    WHERE ObjectName = 'emp_Employee';
    
    UPDATE Objects SET UpdateType = 'stored', 
    UpdateProcessName = 'pEmp_Update_Employee' 
    WHERE ObjectName = 'emp_Employee';
    
    UPDATE Objects 
    SET InsertType = 'standard', InsertProcessName = NULL, 
        UpdateType = 'standard', UpdateProcessName = NULL 
    WHERE ObjectName = 'emp_EmployeePersonalData';
```
**Base de datos: Data**

```sql    
    -- Revertir Settings
    UPDATE Settings SET Content = '0' WHERE IdSettings = 'AhoraEmployees';
```

### Revertir configuración genérica del ERP

**Base de datos: Conf**

```sql    
    -- Desactivar objetos AHORA
    UPDATE Objects SET Active = 0 
    WHERE ObjectName IN (
'AHORA_Documento', 'AHORA_Documento_Documento', 'AHORA_Documento_Tabla', 'AHORA_Imagen',
'AHORA_Documentos', 'AHORA_Documentos_Documento', 'AHORA_Documentos_Tablas', 'AHORA_Imagenes'
    );
    
    -- Revertir configuración de conexión

UPDATE Objects 
    SET ConnStringID = 'DataConnectionString', InsertType = 'standard', 
        UpdateType = 'standard', DeleteType = 'standard' 
    WHERE ObjectName IN (
        'AHORA_Documento', 'AHORA_Documentos', 'AHORA_Documento_Documento',
'AHORA_Documentos_Documento', 'AHORA_Documento_Tabla', 'AHORA_Documentos_Tablas',
'AHORA_Imagenes', 'AHORA_Imagen'
    );
```

**Base de datos: Data**

```sql
    -- Revertir Settings
UPDATE Settings SET Content = '0' WHERE IdSettings = 'AhoraERP';
```

### Script completo: base de datos Conf

Script completo para revertir la integración en la base de datos de configuración. Incluye manejo de transacciones y errores.

```sql   
    -- ============================================================================
    -- SCRIPT DE REVERSIÓN - BASE DE DATOS CONF (Flexygo_HRBD)
    -- ============================================================================
    -- IMPORTANTE: Ejecutar PRIMERO este script en la base de datos Conf
    -- Hacer BACKUP antes de ejecutar
    -- ============================================================================

BEGIN TRY
        BEGIN TRANSACTION;
        PRINT '=== INICIANDO REVERSIÓN DE INTEGRACIÓN AHORA ERP (BASE CONF) ===';
    
        -- 1. REVERTIR PROYECTOS
        PRINT '1. Revirtiendo integración de Proyectos...';
        UPDATE Jobs SET Enabled = 0 WHERE JobName = 'hr_AhoraERP_Projects';
        UPDATE Objects SET CanInsert = 1, CanDelete = 1 
        WHERE ObjectName IN ('Project', 'Projects');
        UPDATE Objects_Properties SET Locked = 0 
        WHERE ObjectName IN ('Project', 'Projects') 
          AND PropertyName IN ('Descrip', 'ExternalCodeId');
    
        -- 2. REVERTIR GASTOS/PARTES
        PRINT '2. Revirtiendo integración de Gastos/Partes...';
        UPDATE Jobs SET Enabled = 0 WHERE JobName = 'hr_AhoraERP_SendExpensesToERP';
        UPDATE Navigation_Nodes SET Enabled = 0 
        WHERE NodeId = '0F1F1B5C-6117-42CA-A7F1-C7B4CA3AE804';
        UPDATE Objects SET Active = 0 
        WHERE ObjectName IN ('emp_TiposGastos_Linea', 'emp_TiposGastos_Lineas');
        UPDATE Objects SET InsertType = 'standard', UpdateType = 'standard', 
               DeleteType = 'standard' 
        WHERE ObjectName IN ('emp_TiposGastos_Linea', 'emp_TiposGastos_Lineas');
        UPDATE Objects_Properties SET IsRequired = 0 
        WHERE ObjectName IN ('emp_Expenses_Type', 'emp_Expenses_Types') 
          AND PropertyName = 'CodExpenses';
        UPDATE Objects_Properties 
        SET Hide = 1, TypeId = 'text', CustomPropName = NULL, ConnStringId = NULL 
        WHERE ObjectName = 'emp_Part_Expenses' AND PropertyName = 'IdClient';
        UPDATE Objects_Properties SET Hide = 0 
        WHERE ObjectName = 'emp_Part_Expenses' AND PropertyName = 'Client';
        UPDATE Objects_Properties 
        SET Hide = 1, TypeId = 'number', CustomPropName = NULL, ConnStringId = NULL 
        WHERE ObjectName = 'emp_Travel' AND PropertyName = 'IdClient';
        UPDATE Objects_Properties SET Hide = 0 
        WHERE ObjectName = 'emp_Travel' AND PropertyName = 'Client';
        UPDATE Objects_Properties_Dependencies SET Active = 0 
        WHERE ObjectName IN ('emp_Part_Expenses', 'emp_Travel') 
          AND PropertyName = 'IdClient';
        UPDATE Processes_Params 
        SET Hide = 1, TypeId = 'text', CustomPropName = NULL, 
            DetachedFromProcess = 0, ConnStringId = 'DataConnectionString' 
        WHERE ProcessName = 'Emp_RequestTravel' AND ParamName = 'IdClient';
        UPDATE Processes_Params SET Hide = 0 
        WHERE ProcessName = 'Emp_RequestTravel' AND ParamName = 'Client';
        DELETE FROM Processes_Params_Dependencies 
        WHERE ProcessName = 'Emp_RequestTravel' AND ParamName = 'IdClient';
        DELETE FROM ChatGPT_Settings_DataModel 
        WHERE SettingId = 'Asistente-Gastos' AND TableName = 'vClientesERP';
    
        -- 3. REVERTIR EMPLEADOS
        PRINT '3. Revirtiendo integración de Empleados...';
        UPDATE Jobs SET Enabled = 0 WHERE JobName = 'hr_AhoraERP_Employees';
        UPDATE Navigation_Nodes SET Enabled = 0 
        WHERE NodeId = '497A5C4E-4C47-4200-85EA-21FB3E3A0F65';
        UPDATE Objects SET Active = 0 
        WHERE ObjectName IN ('emp_EmpleadoERP', 'emp_EmpleadosERP');
        UPDATE Objects SET InsertType = 'standard', InsertProcessName = NULL 
        WHERE ObjectName = 'emp_Employee';
        UPDATE Objects SET UpdateType = 'stored', 
               UpdateProcessName = 'pEmp_Update_Employee' 
        WHERE ObjectName = 'emp_Employee';
        UPDATE Objects 
        SET InsertType = 'standard', InsertProcessName = NULL, 
            UpdateType = 'standard', UpdateProcessName = NULL 
        WHERE ObjectName = 'emp_EmployeePersonalData';
    
        -- 4. REVERTIR CONFIGURACIÓN GENÉRICA
        PRINT '4. Revirtiendo configuración genérica del ERP...';
        UPDATE Objects SET Active = 0 
        WHERE ObjectName IN (
            'AHORA_Documento', 'AHORA_Documentos', 'AHORA_Imagen', 'AHORA_Imagenes',
            'AHORA_Documento_Documento', 'AHORA_Documentos_Documento',
            'AHORA_Documento_Tabla', 'AHORA_Documentos_Tablas'
        );
        UPDATE Objects 
        SET ConnStringID = 'DataConnectionString', InsertType = 'standard', 
            UpdateType = 'standard', DeleteType = 'standard' 
        WHERE ObjectName IN (
            'AHORA_Documento', 'AHORA_Documentos', 'AHORA_Documento_Documento', 
            'AHORA_Documentos_Documento', 'AHORA_Documento_Tabla', 
            'AHORA_Documentos_Tablas', 'AHORA_Imagenes', 'AHORA_Imagen'
        );
    
        COMMIT TRANSACTION;
        PRINT '=== REVERSIÓN BASE CONF COMPLETADA EXITOSAMENTE ===';
        PRINT 'SIGUIENTE PASO: Ejecutar el script para la BASE DE DATOS DATA';
    
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
        BEGIN
            ROLLBACK TRANSACTION;
            PRINT '=== TRANSACCIÓN REVERTIDA ===';
        END
        
        PRINT '=== ERROR EN LA REVERSIÓN (BASE CONF) ===';
        PRINT 'Error: ' + ERROR_MESSAGE();
        PRINT 'Línea: ' + CAST(ERROR_LINE() AS NVARCHAR(10));
        PRINT 'Procedimiento: ' + ISNULL(ERROR_PROCEDURE(), 'Script principal');
        PRINT 'Severidad: ' + CAST(ERROR_SEVERITY() AS NVARCHAR(10));
        PRINT 'Estado: ' + CAST(ERROR_STATE() AS NVARCHAR(10));
        
        -- Re-lanzar el error para detener la ejecución
        THROW;
    END CATCH;
```  

### Script completo: base de datos Data

Script completo para revertir la integración en la base de datos de datos. Ejecutar DESPUÉS del script de Conf.

```sql    
    -- ============================================================================
    -- SCRIPT DE REVERSIÓN - BASE DE DATOS DATA (Flexygo_HR_DataBD)
    -- ============================================================================
    -- IMPORTANTE: Ejecutar DESPUÉS del script de la base de datos Conf
    -- Hacer BACKUP antes de ejecutar
    -- ============================================================================

BEGIN TRY
        BEGIN TRANSACTION;
        PRINT '=== INICIANDO REVERSIÓN DE INTEGRACIÓN AHORA ERP (BASE DATA) ===';
    
        -- 1. REVERTIR PROYECTOS
        PRINT '1. Revirtiendo Settings de Proyectos...';
        UPDATE Settings SET Content = '0' WHERE IdSettings = 'AhoraProjects';
    
        -- 2. REVERTIR GASTOS/PARTES
        PRINT '2. Revirtiendo Settings y Vista de Gastos/Partes...';
        UPDATE Settings SET Content = '0' 
        WHERE IdSettings IN ('AhoraExpenses', 'AhoraSendExpensesDocuments');
        DROP VIEW IF EXISTS vClientesERP;
    
        -- 3. REVERTIR EMPLEADOS
        PRINT '3. Revirtiendo Settings de Empleados...';
        UPDATE Settings SET Content = '0' WHERE IdSettings = 'AhoraEmployees';
    
        -- 4. REVERTIR CONFIGURACIÓN GENÉRICA
        PRINT '4. Revirtiendo Settings de configuración genérica...';
        UPDATE Settings SET Content = '0' WHERE IdSettings = 'AhoraERP';
    
        COMMIT TRANSACTION;
        PRINT '=== REVERSIÓN BASE DATA COMPLETADA EXITOSAMENTE ===';
        PRINT 'IMPORTANTE: Reiniciar la aplicación para aplicar los cambios.';
        PRINT 'RECORDATORIO: Puede eliminar la cadena de conexión ERPConnectionString.';
    
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
        BEGIN
            ROLLBACK TRANSACTION;
            PRINT '=== TRANSACCIÓN REVERTIDA ===';
        END
        
        PRINT '=== ERROR EN LA REVERSIÓN (BASE CONF) ===';
        PRINT 'Error: ' + ERROR_MESSAGE();
        PRINT 'Línea: ' + CAST(ERROR_LINE() AS NVARCHAR(10));
        PRINT 'Procedimiento: ' + ISNULL(ERROR_PROCEDURE(), 'Script principal');
        PRINT 'Severidad: ' + CAST(ERROR_SEVERITY() AS NVARCHAR(10));
        PRINT 'Estado: ' + CAST(ERROR_STATE() AS NVARCHAR(10));
        
        -- Re-lanzar el error para detener la ejecución
        THROW;
    END CATCH;
```   

## Notas adicionales

!!! warning "Consideraciones importantes"
    1. Backup obligatorio: siempre hacer backup completo antes de ejecutar los scripts de reversión.
    2. Reload cache: después de cualquier cambio, reiniciar la aplicación.
    3. Testing: probar en entorno de desarrollo/pruebas antes de producción.
    4. Cadena de conexión: una vez revertida la integración, puede quitarse la cadena de conexión ERPConfConnectionString.
