# Revertir la integración con AHORA ERP

### Introducción

La integración entre Sebastian HR y AHORA ERP es un proceso irreversible que no podrá deshacerse desde la propia aplicación una vez activado. 

Esta documentación detalla los cambios que se aplican durante el proceso de activación y proporciona los pasos necesarios para revertir manualmente al estado original.

### Requisitos Previos

  * Conocimientos de SQL: Es necesario tener conocimientos sólidos del lenguaje SQL y de la estructura de tablas de Flexygo.
  * Acceso directo a base de datos: Los cambios deberán ejecutarse directamente en el servidor SQL.
  * Comprensión del proceso: Es fundamental leer y comprender completamente este documento antes de proceder.

### Advertencias

  * BACKUP OBLIGATORIO: Realice copias de seguridad completas de las bases de datos antes de iniciar cualquier proceso.
  * ENTORNOS DE PRODUCCIÓN: Extreme las precauciones al ejecutar estos scripts en entornos de producción. Se recomienda probar primero en desarrollo/pruebas.
  * OJO: Lee cada script antes de ejecutarlo. Si no entiendes lo que hace, no lo ejecutes. Un error puede tener consecuencias graves en tu sistema.

Esta guía está diseñada para ayudarle a realizar el proceso de reversión de manera controlada y segura. Tómese el tiempo necesario para comprender cada paso y no dude en consultar con el equipo técnico si tiene alguna duda.

  

### RESUMEN DE CAMBIOS

### 1\. Configuración Genérica del ERP (Siempre se ejecuta)

#### Base de Datos: ConfTabla: Objects

  * Activa 8 objetos relacionados con documentos e imágenes del ERP
  * Configura conexión y tipos de operación para estos objetos

Objetos activados:

  * `AHORA_Documento`, `AHORA_Documentos`, `AHORA_Imagen`, `AHORA_Imagenes`
  * `AHORA_Documento_Documento`, `AHORA_Documentos_Documento`
  * `AHORA_Documento_Tabla`, `AHORA_Documentos_Tablas`

Cambios por objeto:

  * `Active` = 1 (activado)
  * `ConnStringID` = 'ERPConnectionString'
  * `InsertType`, `UpdateType`, `DeleteType` = 'erpstored'

#### Base de Datos: DataTabla: Settings

  * `AhoraERP`: Content = 1

### 2\. Integración de Empleados

#### Base de Datos: Conf

Tabla: Objects

<table style="width: 100%; border-collapse: collapse; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><thead><tr style="background-color: #3498db; color: white;"><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Objeto</th><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Campo</th><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Valor Nuevo</th></tr></thead><tbody><tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_EmpleadoERP</code></td><td style="padding: 10px; border: 1px solid #ddd;">Active</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">1</strong></td></tr><tr><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_EmpleadosERP</code></td><td style="padding: 10px; border: 1px solid #ddd;">Active</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">1</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_Employee</code></td><td style="padding: 10px; border: 1px solid #ddd;">InsertType</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">'dll'</strong></td></tr><tr><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_Employee</code></td><td style="padding: 10px; border: 1px solid #ddd;">InsertProcessName</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">'HR_ERP_InsertEmployeeOnSebastianAndOnERP'</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_Employee</code></td><td style="padding: 10px; border: 1px solid #ddd;">UpdateType</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">'dll'</strong></td></tr><tr><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_Employee</code></td><td style="padding: 10px; border: 1px solid #ddd;">UpdateProcessName</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">'HR_ERP_UpdateEmployeeOnSebastianAndOnERP'</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_EmployeePersonalData</code></td><td style="padding: 10px; border: 1px solid #ddd;">InsertType</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">'dll'</strong></td></tr><tr><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_EmployeePersonalData</code></td><td style="padding: 10px; border: 1px solid #ddd;">InsertProcessName</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">'HR_ERP_InsertEmployeeOnSebastianAndOnERP'</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_EmployeePersonalData</code></td><td style="padding: 10px; border: 1px solid #ddd;">UpdateType</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">'dll'</strong></td></tr><tr><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_EmployeePersonalData</code></td><td style="padding: 10px; border: 1px solid #ddd;">UpdateProcessName</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">'HR_ERP_UpdateEmployeeOnSebastianAndOnERP'</strong></td></tr></tbody></table>

 

Tabla: Jobs

  * `hr_AhoraERP_Employees`: Enabled = 1Tabla: Navigation_Nodes

  * NodeId `497A5C4E-4C47-4200-85EA-21FB3E3A0F65`: Enabled = 1

#### Base de Datos: DataTabla: Settings

  * `AhoraEmployees`: Content = 1

### 3\. Integración de Gastos/Partes

#### Base de Datos: Conf

Tabla: Objects

<table style="width: 100%; border-collapse: collapse; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><thead><tr style="background-color: #3498db; color: white;"><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Objeto</th><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Campo</th><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Valor Nuevo</th></tr></thead><tbody><tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_TiposGastos_Linea</code></td><td style="padding: 10px; border: 1px solid #ddd;">Active</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">1</strong></td></tr><tr><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_TiposGastos_Lineas</code></td><td style="padding: 10px; border: 1px solid #ddd;">Active</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">1</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_TiposGastos_Linea</code></td><td style="padding: 10px; border: 1px solid #ddd;">InsertType, UpdateType, DeleteType</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">'erpstored'</strong></td></tr><tr><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">emp_TiposGastos_Lineas</code></td><td style="padding: 10px; border: 1px solid #ddd;">InsertType, UpdateType, DeleteType</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">'erpstored'</strong></td></tr></tbody></table>

 

Tabla: Objects_Properties

<table style="width: 100%; border-collapse: collapse; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-size: 0.9em;"><thead><tr style="background-color: #3498db; color: white;"><th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Objeto</th><th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Propiedad</th><th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Campo</th><th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Valor Nuevo</th></tr></thead><tbody><tr style="background-color: #f9f9f9;"><td style="padding: 8px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px;">emp_Expenses_Type</code></td><td style="padding: 8px; border: 1px solid #ddd;">CodExpenses</td><td style="padding: 8px; border: 1px solid #ddd;">IsRequired</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #3498db;">0</strong></td></tr><tr><td style="padding: 8px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px;">emp_Expenses_Types</code></td><td style="padding: 8px; border: 1px solid #ddd;">CodExpenses</td><td style="padding: 8px; border: 1px solid #ddd;">IsRequired</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #3498db;">0</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 8px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px;">emp_Part_Expenses</code></td><td style="padding: 8px; border: 1px solid #ddd;">IdClient</td><td style="padding: 8px; border: 1px solid #ddd;">Hide, TypeId, CustomPropName, ConnStringId</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #3498db;">0, 'custom', 'pEmp_ERP_Clients_CustomControl', 'ERPConnectionString'</strong></td></tr><tr><td style="padding: 8px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px;">emp_Part_Expenses</code></td><td style="padding: 8px; border: 1px solid #ddd;">Client</td><td style="padding: 8px; border: 1px solid #ddd;">Hide</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #3498db;">1</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 8px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px;">emp_Travel</code></td><td style="padding: 8px; border: 1px solid #ddd;">IdClient</td><td style="padding: 8px; border: 1px solid #ddd;">Hide, TypeId, CustomPropName, ConnStringId</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #3498db;">0, 'custom', 'pEmp_ERP_Clients_CustomControl', 'ERPConnectionString'</strong></td></tr><tr><td style="padding: 8px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px;">emp_Travel</code></td><td style="padding: 8px; border: 1px solid #ddd;">Client</td><td style="padding: 8px; border: 1px solid #ddd;">Hide</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #3498db;">1</strong></td></tr></tbody></table>

 

Otras Tablas Modificadas:

  * Objects_Properties_Dependencies: Active = 1 para emp_Part_Expenses.IdClient y emp_Travel.IdClient
  * Jobs: hr_AhoraERP_SendExpensesToERP Enabled = 1
  * Navigation_Nodes: NodeId 0F1F1B5C-6117-42CA-A7F1-C7B4CA3AE804 Enabled = 1
  * ChatGPT_Settings: Actualiza SystemPrompt para 'Asistente-Gastos'
  * ChatGPT_Settings_DataModel: Inserta 2 registros para vClientesERP
  * Processes_Params: Configura IdClient y Client en Emp_RequestTravel
  * Processes_Params_Dependencies: Inserta dependencia para Emp_RequestTravel.IdClient

#### Base de Datos: DataTabla: Settings

  * `AhoraExpenses`: Content = 1
  * `AhoraSendExpensesDocuments`: Content = [valor del parámetro]Vistas

  * Crea vista `vClientesERP` apuntando a ERPConnectionString.dbo.Clientes_Datos

### 4️. INTEGRACIÓN DE PROYECTOS

#### Base de Datos: Conf

Tabla: Objects

<table style="width: 100%; border-collapse: collapse; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><thead><tr style="background-color: #3498db; color: white;"><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Objeto</th><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Campo</th><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Valor Nuevo</th></tr></thead><tbody><tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">Project</code></td><td style="padding: 10px; border: 1px solid #ddd;">CanInsert, CanDelete</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">0</strong></td></tr><tr><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">Projects</code></td><td style="padding: 10px; border: 1px solid #ddd;">CanInsert, CanDelete</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">0</strong></td></tr></tbody></table>

 

Tabla: Objects_Properties

<table style="width: 100%; border-collapse: collapse; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><thead><tr style="background-color: #3498db; color: white;"><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Objeto</th><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Propiedad</th><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Campo</th><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Valor Nuevo</th></tr></thead><tbody><tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px;">Project, Projects</code></td><td style="padding: 10px; border: 1px solid #ddd;">Descrip, ExternalCodeId, ProjectId</td><td style="padding: 10px; border: 1px solid #ddd;">Locked</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">1</strong></td></tr></tbody></table>

 

Tabla: Jobs

  * `hr_AhoraERP_Projects`: Enabled = 1

#### Base de Datos: DataTabla: Settings

  * `AhoraProjects`: Content = 1

### VALORES ORIGINALES

Estos son los valores antes de la integración. 

### 1️. CONFIGURACIÓN GENÉRICA DEL ERP

<table style="width: 100%; border-collapse: collapse; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><thead><tr style="background-color: #3498db; color: white;"><th style="padding: 12px; text-align: left; border: 1px solid rgb(221, 221, 221); width: 35.4232%;">Tabla</th><th style="padding: 12px; text-align: left; border: 1px solid rgb(221, 221, 221); width: 34.6395%;">Campo</th><th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Valor Original</th></tr></thead><tbody><tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid rgb(221, 221, 221); width: 35.4232%;">Objects (AHORA_*)</td><td style="padding: 10px; border: 1px solid rgb(221, 221, 221); width: 34.6395%;">Active</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">false</strong></td></tr><tr><td style="padding: 10px; border: 1px solid rgb(221, 221, 221); width: 35.4232%;">Settings</td><td style="padding: 10px; border: 1px solid rgb(221, 221, 221); width: 34.6395%;">AhoraERP Content</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">'0'</strong></td></tr></tbody></table>

 

### 2️. INTEGRACIÓN DE EMPLEADOS

<table style="width: 100%; border-collapse: collapse; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-size: 0.9em;"><thead><tr style="background-color: #3498db; color: white;"><th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Objeto</th><th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Campo</th><th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Valor Original</th></tr></thead><tbody><tr style="background-color: #f9f9f9;"><td style="padding: 8px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px;">emp_EmpleadoERP</code></td><td style="padding: 8px; border: 1px solid #ddd;">Active</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">false</strong></td></tr><tr><td style="padding: 8px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px;">emp_Employee</code></td><td style="padding: 8px; border: 1px solid #ddd;">InsertType</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">'standard'</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 8px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px;">emp_Employee</code></td><td style="padding: 8px; border: 1px solid #ddd;">UpdateType</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">'stored'</strong></td></tr><tr><td style="padding: 8px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px;">emp_Employee</code></td><td style="padding: 8px; border: 1px solid #ddd;">UpdateProcessName</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">'pEmp_Update_Employee'</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 8px; border: 1px solid #ddd;"><code style="background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px;">emp_EmployeePersonalData</code></td><td style="padding: 8px; border: 1px solid #ddd;">InsertType, UpdateType</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">'standard'</strong></td></tr><tr><td style="padding: 8px; border: 1px solid #ddd;">Jobs</td><td style="padding: 8px; border: 1px solid #ddd;">hr_AhoraERP_Employees Enabled</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">false</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 8px; border: 1px solid #ddd;">Settings</td><td style="padding: 8px; border: 1px solid #ddd;">AhoraEmployees Content</td><td style="padding: 8px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">'0'</strong></td></tr></tbody></table>

 

### 3️. INTEGRACIÓN DE GASTOS 

<table style="width: 100%; border-collapse: collapse; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-size: 0.85em;"><thead><tr style="background-color: #3498db; color: white;"><th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Objeto/Tabla</th><th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Propiedad/Campo</th><th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Campo</th><th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Valor Original</th></tr></thead><tbody><tr style="background-color: #f9f9f9;"><td style="padding: 6px; border: 1px solid #ddd;">emp_TiposGastos_Linea</td><td style="padding: 6px; border: 1px solid #ddd;">-</td><td style="padding: 6px; border: 1px solid #ddd;">Active</td><td style="padding: 6px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">false</strong></td></tr><tr><td style="padding: 6px; border: 1px solid #ddd;">emp_Part_Expenses</td><td style="padding: 6px; border: 1px solid #ddd;">IdClient</td><td style="padding: 6px; border: 1px solid #ddd;">Hide</td><td style="padding: 6px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">true</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 6px; border: 1px solid #ddd;">emp_Part_Expenses</td><td style="padding: 6px; border: 1px solid #ddd;">IdClient</td><td style="padding: 6px; border: 1px solid #ddd;">TypeId</td><td style="padding: 6px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">'text'</strong></td></tr><tr><td style="padding: 6px; border: 1px solid #ddd;">emp_Part_Expenses</td><td style="padding: 6px; border: 1px solid #ddd;">Client</td><td style="padding: 6px; border: 1px solid #ddd;">Hide</td><td style="padding: 6px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">false</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 6px; border: 1px solid #ddd;">emp_Travel</td><td style="padding: 6px; border: 1px solid #ddd;">IdClient</td><td style="padding: 6px; border: 1px solid #ddd;">Hide, TypeId</td><td style="padding: 6px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">true, 'number'</strong></td></tr><tr><td style="padding: 6px; border: 1px solid #ddd;">Emp_RequestTravel</td><td style="padding: 6px; border: 1px solid #ddd;">IdClient</td><td style="padding: 6px; border: 1px solid #ddd;">Hide</td><td style="padding: 6px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">true</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 6px; border: 1px solid #ddd;">Settings</td><td style="padding: 6px; border: 1px solid #ddd;">AhoraExpenses</td><td style="padding: 6px; border: 1px solid #ddd;">Content</td><td style="padding: 6px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">'0'</strong></td></tr><tr><td style="padding: 6px; border: 1px solid #ddd;">Vista</td><td style="padding: 6px; border: 1px solid #ddd;">vClientesERP</td><td style="padding: 6px; border: 1px solid #ddd;">-</td><td style="padding: 6px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">No existe</strong></td></tr></tbody></table>

 

### 4️. INTEGRACIÓN DE PROYECTOS

<table style="width: 100%; border-collapse: collapse; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"><thead><tr style="background-color: #3498db; color: white;"><th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Objeto</th><th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Campo/Propiedad</th><th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Valor Original</th></tr></thead><tbody><tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;">Project, Projects</td><td style="padding: 10px; border: 1px solid #ddd;">CanInsert, CanDelete</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #3498db;">true</strong></td></tr><tr><td style="padding: 10px; border: 1px solid #ddd;">Project, Projects</td><td style="padding: 10px; border: 1px solid #ddd;">Descrip, ExternalCodeId Locked</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">false</strong></td></tr><tr style="background-color: #f9f9f9;"><td style="padding: 10px; border: 1px solid #ddd;">Jobs</td><td style="padding: 10px; border: 1px solid #ddd;">hr_AhoraERP_Projects Enabled</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">false</strong></td></tr><tr><td style="padding: 10px; border: 1px solid #ddd;">Settings</td><td style="padding: 10px; border: 1px solid #ddd;">AhoraProjects Content</td><td style="padding: 10px; border: 1px solid #ddd;"><strong style="color: #2c3e50;">'0'</strong></td></tr></tbody></table>

 

### SCRIPTS DE REVERSIÓN

### IMPORTANTE

  * Hacer backup completo antes de ejecutar
  * Ejecutar en transacciones para poder hacer rollback si hay errores
  * Reiniciar la aplicación después de revertir

### 4️. INTEGRACIÓN DE PROYECTOS

####   

#### Base de Datos: Conf
    
    
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
#### Base de Datos: Data
    
```sql    
    -- Revertir Settings
    UPDATE Settings 
    SET Content = '0' 
    WHERE IdSettings = 'AhoraProjects';
```
### 2️. REVERTIR INTEGRACIÓN DE GASTOS/PARTES

#### Base de Datos: Conf
    
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
#### Base de Datos: Data
    
```sql    
    -- Revertir Settings
    UPDATE Settings SET Content = '0' 
    WHERE IdSettings IN ('AhoraExpenses', 'AhoraSendExpensesDocuments');
    
    -- Eliminar vista
    DROP VIEW IF EXISTS vClientesERP;
```
### 3️. REVERTIR INTEGRACIÓN DE EMPLEADOS

#### Base de Datos: Conf
    
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
#### Base de Datos: Data
    
```sql    
    -- Revertir Settings
    UPDATE Settings SET Content = '0' WHERE IdSettings = 'AhoraEmployees';
```
### 4️. REVERTIR CONFIGURACIÓN GENÉRICA DEL ERP

#### Base de Datos: Conf
    
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

#### Base de Datos: Data
    
    

```sql
    -- Revertir Settings
UPDATE Settings SET Content = '0' WHERE IdSettings = 'AhoraERP';
```
### SCRIPT COMPLETO - Base de Datos CONF 

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

### SCRIPT COMPLETO - Base de Datos DATA


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

### NOTAS ADICIONALES

Consideraciones Importantes:

  1. Backup Obligatorio: Siempre hacer backup completo antes de ejecutar los scripts de reversión.
  2. Reload Cache: Después de cualquier cambio, reiniciar la aplicación.
  3. Testing: Probar en entorno de desarrollo/pruebas antes de producción.
  4. Cadena de conexión: una vez revertida la integración, puede quitarse la cadena de conexión ERPConfConnectionString