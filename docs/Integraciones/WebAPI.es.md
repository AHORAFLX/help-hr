# Web API

La Web API de Sebastian HR permite que otros sistemas (un ERP, una aplicación de fichaje, una herramienta de BI, un portal propio...) lean y modifiquen datos de Sebastian HR mediante peticiones HTTP con cuerpo y respuesta en JSON.

Este artículo explica cómo autenticarse, cómo se construyen las llamadas y qué operaciones ofrece la API, agrupadas por área funcional.

## Conceptos

La API expone dos tipos de operaciones:

| Tipo | Para qué sirve | Método y URL |
| --- | --- | --- |
| Proceso | Acciones que crean o modifican datos: crear un empleado, insertar un fichaje, aceptar una instancia... | `POST {url}/webapi/exec/{Proceso}` |
| Consulta | Lecturas de datos: listar empleados, consultar jornadas, ver contratos... | `GET {url}/webapi/list/{Objeto}/{Vista}` |

- `{url}` es la dirección base de tu instalación de Sebastian HR (por ejemplo, `https://rrhh.miempresa.com`).
- Todos los procesos y consultas públicos empiezan por `API_` (por ejemplo, `API_EmployeeCreate` o `API_EmployeeList`).
- Las consultas cuyo nombre empieza por `API_Aux_` son **catálogos auxiliares**: devuelven los valores válidos de un campo (países, categorías, tipos de ausencia...) para que puedas rellenar o validar los parámetros de los procesos.

## Autenticación

Todas las llamadas requieren un token de acceso de tipo *Bearer*. Para obtenerlo, envía el usuario y la contraseña de Sebastian HR al endpoint `/token` como formulario (`application/x-www-form-urlencoded`):

```http
POST {url}/token
Content-Type: application/x-www-form-urlencoded

grant_type=password&username=usuario&password=contraseña
```

La respuesta incluye el token en el campo `access_token`. Añádelo en la cabecera `Authorization` de todas las peticiones siguientes:

```http
Authorization: Bearer {access_token}
```

!!! warning "Permisos del usuario"
    La API actúa con la identidad del usuario del token. Algunas operaciones dependen directamente de él (por ejemplo, `API_InstanceList` devuelve solo las instancias de ese usuario y `API_InstanceManage` gestiona el paso de aprobación que tiene asignado). Usa un usuario con los roles adecuados para la integración.

## Ejecutar un proceso

Los procesos se invocan con `POST` y reciben sus parámetros como un objeto JSON en el cuerpo de la petición:

```http
POST {url}/webapi/exec/API_MarkingInsert
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "employeeId": 1,
  "markingTypeId": "E",
  "deviceLocalTime": "2026-08-26T12:30:00",
  "deviceTimeZoneId": "Romance Standard Time",
  "terminalCode": "APP-MOBILE"
}
```

- Los parámetros opcionales se pueden omitir o enviar como `null`.
- Las fechas se envían en formato ISO (`yyyy-MM-dd` o `yyyy-MM-ddTHH:mm:ss`) y las horas como `HH:mm`.
- Cuando un proceso genera un identificador (por ejemplo, `PartId` al crear un gasto o `NewsId` al crear una noticia), lo devuelve en los datos de la respuesta.

## Ejecutar una consulta

Las consultas se invocan con `GET`. El objeto y la vista forman parte de la URL, y el resto de opciones se pasan como parámetros de la *query string*:

```http
GET {url}/webapi/list/emp_Employee/API_EmployeeList?filter=Blocked=0&page=0&pageSize=100
Authorization: Bearer {access_token}
```

### Parámetros de la URL

| Parámetro | Descripción |
| --- | --- |
| `filter` | Condición adicional para acotar los resultados, con sintaxis SQL (por ejemplo, `Employees_Holidays.EmployeeId=1 AND StatusId=1`). Opcional. |
| `page` | Número de página, empezando en `0`. |
| `pageSize` | Número de registros por página. |
| `orderBy` | Ordenación de los resultados (por ejemplo, `Date DESC`). Si no se indica, se usa el orden por defecto de la vista. |
| `defaults` | Objeto JSON con los parámetros obligatorios de la vista. Solo lo usan algunas consultas (ver apartado siguiente). |

!!! tip "Recomendación"
    Codifica los valores de `filter` y `defaults` en la URL (espacios, comillas, llaves...) antes de enviar la petición. La mayoría de clientes HTTP lo hacen automáticamente.

### Parámetros de vista obligatorios

Algunas consultas trabajan sobre un rango de fechas y un empleado que se envían en el parámetro `defaults`. En ellas, todos los parámetros de `defaults` son obligatorios y ninguno se puede omitir:

```http
GET {url}/webapi/list/emp_Marking/API_MarkingList?defaults={"EmployeeId":7,"StartDate":"20260901","EndDate":"20260930"}&page=0&pageSize=100
```

- Las fechas de `defaults` van en formato `yyyyMMdd` (o `yyyyMM` en las consultas mensuales).
- `defaults` y `filter` se pueden combinar: `defaults` fija el empleado y el periodo, y `filter` acota los resultados dentro de ese periodo.

Las consultas que usan `defaults` son `API_MarkingList`, `API_WorkdayList`, `API_WorkdayTotals`, `API_WorkdayMonthlyTotals` y `API_PlanningList`.

### Uso del filtro

El valor de `filter` se añade a la condición `WHERE` de la consulta. Por eso:

- Solo admite **columnas reales** de las tablas de la consulta, no los alias de las columnas devueltas. Por ejemplo, en `API_WorkdayList` se puede filtrar por `EDD.BalanceMinutes`, pero no por `BalanceHoursText`; un alias produce el error `El nombre de columna '...' no es válido`.
- Cuando una columna existe en varias tablas, hay que cualificarla con el nombre de la tabla (`Markings.EmployeeId`, `Employees.Department`...). Los ejemplos de cada consulta indican la forma correcta.
- En las consultas que devuelven totales, el filtro se aplica **antes de agrupar**, así que no se puede filtrar por las columnas calculadas.
- Para condiciones sobre tablas relacionadas se puede usar una subconsulta `EXISTS` (ver los ejemplos de [Listar cursos](#listar-cursos) o [Listar equipos](#listar-equipos)).

!!! warning "Acota las consultas grandes"
    Las consultas de fichajes y jornadas trabajan sobre las tablas más grandes del sistema. Acota siempre el rango de fechas y usa la paginación.

### Catálogos auxiliares

Cada área incluye, cuando aplica, un apartado de catálogos con las vistas `API_Aux_` que devuelven los valores válidos de los parámetros de sus procesos. Se consultan igual que cualquier otra vista:

```http
GET {url}/webapi/list/emp_Employee/API_Aux_Countries?filter=IsoCode='ES'&page=0&pageSize=100
```

Muchos catálogos devuelven solo los valores activos, por lo que es posible que un registro histórico contenga un valor que ya no aparece en el catálogo.

## Empleados

### Crear empleado

```text
POST {url}/webapi/exec/API_EmployeeCreate
```

Crea un empleado. En modo PRO puede crear también su contrato en la misma llamada.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `Name`, `Surname`, `Gender`, `BirthDate`, `CountryOfBirth` | Sí | Datos básicos del empleado. |
| `IDNumber`, `IdentificationDocTypeId`, `NSS` | Sí | Documento de identidad, tipo de documento y número de la Seguridad Social. |
| `CurrentReference`, `InsertDate` | Sí | Usuario que da de alta el empleado y fecha de alta. |
| `WithoutContract` | Sí | `true` crea solo el empleado; `false` crea también el contrato. |
| `CompanyId`, `ContractType`, `StartDate`, `Office`, `PositionId`, `CategoryId`, `CollectiveAgreementId`, `QuoteTypeId`, `RegimeId`, `AnualSalary` | Si `WithoutContract = false` <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span> | Datos del contrato. |
| `Address`, `Address_Google`, `City`, `Country`, `PostalCode`, `ProvinceState` | No | Dirección. |
| `EmployeeMail`, `EmployeePhone`, `PersonalEmail`, `PersonalPhone`, `PersonalObservations`, `EmergContactName`, `EmergContactPhone`, `IdentificationDocRenovationDate` | No | Contacto y otros datos personales. |
| `EndDate`, `EndTrialPeriod`, `Justification`, `HourPrice`, `MonthPrice`, `Payments`, `WorkDayPercentage`, `Tea`, `TeaId`, `TerminationReasonId`, `FillTotalHolidays`, `RoundHolidaysValue` | No | Datos adicionales del contrato. |
| `Alias`, `IBAN`, `CountryControl`, `BankNumberEntity`, `BankNumberOffice`, `CD`, `AccountNumber` | No | Cuenta bancaria. |

Si la [integración con Ahora ERP](IntegracionAhoraERP.es.md) de empleados está activa, el empleado se sincroniza con el ERP tras crearlo.

!!! example "Ejemplo"
    Alta de un empleado sin contrato (modo LITE):

    ```json
    {
      "Name": "Juan",
      "Surname": "Pérez Fernández",
      "Gender": "M",
      "BirthDate": "1985-07-22",
      "CountryOfBirth": "ES",
      "NSS": "281111111111",
      "IDNumber": "87654321X",
      "IdentificationDocTypeId": "DNI",
      "CurrentReference": 1,
      "InsertDate": "2026-08-11T10:00:00",
      "WithoutContract": true,
      "PersonalPhone": "655443322",
      "PersonalEmail": "juan.perez@gmail.com"
    }
    ```

### Modificar empleado

```text
POST {url}/webapi/exec/API_EmployeeUpdate
```

Modifica un empleado existente. Solo se actualizan los campos informados; el resto se deja como está.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `employeeId` | Sí | Empleado que se modifica. |
| `name`, `surname`, `gender`, `mail`, `phone`, `office`, `department`, `positionId`, `blocked`, `hideSalary`... | No | Datos generales del empleado. |
| `nss`, `birthDate`, `countryOfBirth`, `address`, `city`, `postalCode`, `country`, `idNumber`, `identificationDocTypeId`, `personalEmail`, `personalPhone`, `familySituationId`, `children`... | No | Datos personales del empleado. |

Si la integración con Ahora ERP está activa, los cambios se replican en el ERP.

!!! example "Ejemplo"
    ```json
    {
      "employeeId": 12,
      "surname": "HR Actualizado",
      "mail": "sistema@flexygo.com",
      "address": "Calle Sistema, 1",
      "city": "Valencia",
      "postalCode": "46002"
    }
    ```

### Listar empleados

```text
GET {url}/webapi/list/emp_Employee/API_EmployeeList
```

Lista los empleados con sus datos básicos, organizativos, personales y del contrato actual.

**Devuelve**: `EmployeeId`, `Name`, `Surname`, `FullName`, `Gender`, `Mail`, `Phone`, `Blocked`, `Discharge`, `Office`/`OfficeDescrip`, `Department`/`DepartmentDescrip`, `Category`/`CategoryDescrip`, `PositionId`/`PositionDescrip`, `Group`/`GroupDescrip`, `UnitId`/`OrgUnitName`, `ScopeId`/`ScopeDescrip`, `NSS`, `IDNumber`, `IdentificationDocTypeId`, `BirthDate`, `Country`, `CountryOfBirth`, `Address`, `City`, `PostalCode`, `ProvinceState`, `PersonalEmail`, `PersonalPhone`, `ContractId`, `ContractStartDate`, `ContractEndDate`, `ContractualStatus`, `CurrentMode`, `Locked`, `ContractType`/`ContractTypeDescrip`, `CompanyId`/`CompanyDescrip`, `RegimeId`/`RegimeDescrip`, `CollectiveAgreementId`/`CollectiveAgreementDescrip`, `TeaId`/`TeaDescrip`, `Inserted`, `LastUpdate`.

Filtro de ejemplo, solo empleados no bloqueados: `filter=Blocked=0`.

### Catálogos de empleados

Valores válidos para los parámetros de [Crear empleado](#crear-empleado):

| Vista | Valores para | Devuelve |
| --- | --- | --- |
| `emp_Employee/API_Aux_Countries` | `Country`, `CountryOfBirth`, `CountryControl` (solo países activos) | `IsoCode`, `Iso3`, `Name`, `IsoName`, `Active` |
| `emp_Employee/API_Aux_IdentificationDocTypes` | `IdentificationDocTypeId` (solo tipos activos) | `TypeId`, `Descrip`, `Active` |
| `emp_Category/API_Aux_Categories` | `CategoryId` | `Category`, `Descrip` |
| `emp_Collective_Agreement/API_Aux_CollectiveAgreements` | `CollectiveAgreementId` | `CollectiveAgreementId`, `CollectiveAgreementCode`, `Descrip` |
| `emp_Company/API_Aux_Companies` | `CompanyId` | `CompanyId`, `Company`, `CIF` |
| `emp_Contract_Type/API_Aux_ContractTypes` | `ContractType` | `ContractType`, `Descrip` |
| `emp_Contract_TerminationReason/API_Aux_TerminationReasons` | `TerminationReasonId` (solo activos) | `TerminationReasonId`, `Descrip`, `Active` |
| `emp_Office/API_Aux_Offices` | `Office` | `Office`, `Descrip`, `CompanyId`, `City`, `Province`, `Country` |
| `emp_Position/API_Aux_Positions` | `PositionId` | `PositionId`, `Position` |
| `emp_Quote_Type/API_Aux_QuoteTypes` | `QuoteTypeId` | `QuoteTypeId`, `Descrip` |
| `emp_Regime/API_Aux_Regimes` | `RegimeId` | `RegimeId`, `Code`, `Descrip` |
| `emp_TemporaryEmploymentAgency/API_Aux_TemporaryEmploymentAgencies` | `TeaId` (solo agencias activas) | `TeaId`, `Name`, `Email`, `Phone`, `Disabled` |

## Fichajes

### Insertar un fichaje

```text
POST {url}/webapi/exec/API_MarkingInsert
```

Inserta un fichaje individual. Calcula la zona horaria a partir de la oficina, la ubicación o el dispositivo, y aplica la detección de fraude.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `employeeId` | Sí | Empleado que ficha. |
| `markingTypeId` | Sí | `E` = entrada, `S` = salida. |
| `deviceLocalTime` | Sí | Fecha y hora local del dispositivo. |
| `deviceTimeZoneId` | No | Zona horaria del dispositivo, en formato Windows (`Romance Standard Time`) o IANA (`Europe/Madrid`). |
| `locId` | No | Ubicación del fichaje. |
| `terminalCode` | No | Código del terminal o aplicación que registra el fichaje. |
| `location` | No | Coordenadas `latitud,longitud`. |
| `ip` | No | IP de origen. |
| `comments` | No | Comentarios. |
| `markClassId` | No | Clase de fichaje. |
| `isManualEntry` | No | Indica si es un fichaje introducido manualmente. Por defecto `false`. |

**Devuelve**: `RegId`, `CheckTime`, `CheckTimeUtc`, `IncidentTypeId`.

!!! warning "Detección de fraude"
    Si la hora del fichaje difiere más de 8 minutos de la hora actual del servidor y no es un fichaje manual (`isManualEntry = false`), se marca con la incidencia de posible fraude. Para registrar fichajes de otro momento (correcciones, cargas de datos pasados o pruebas con fechas fijas), envía `"isManualEntry": true`.

!!! example "Ejemplo"
    ```json
    {
      "employeeId": 7,
      "markingTypeId": "S",
      "deviceLocalTime": "2026-08-10T17:00:00",
      "deviceTimeZoneId": "Romance Standard Time",
      "locId": 2,
      "terminalCode": "TERM-001",
      "location": "39.4699,-0.3763",
      "comments": "Salida tras reunión con cliente",
      "isManualEntry": true
    }
    ```

### Insertar fichajes en bloque

```text
POST {url}/webapi/exec/API_MarkingInsertBulk
```

Inserta muchos fichajes en una sola llamada. Como referencia, unos 500 registros tardan entre 15 y 30 segundos, y 5.000 o más, entre 1 y 4 minutos.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `markingsJson` | Sí | Array JSON serializado como texto. Cada elemento admite los mismos campos que [Insertar un fichaje](#insertar-un-fichaje) y requiere al menos `deviceLocalTime` y `employeeId`. |
| `sourceApi` | Sí | Nombre del sistema de origen (por ejemplo, `ScheduledSync`). |
| `apiUserId` | No | Usuario de la API. |
| `apiIp` | No | IP de origen. |

El `employeeId` de cada fichaje debe corresponder a un empleado existente; si no, la carga falla. La advertencia sobre detección de fraude de [Insertar un fichaje](#insertar-un-fichaje) también se aplica a cada elemento del lote.

!!! example "Ejemplo"
    ```json
    {
      "markingsJson": "[{\"deviceLocalTime\":\"2026-08-10T08:00:00\",\"markingTypeId\":\"E\",\"employeeId\":7,\"isManualEntry\":true},{\"deviceLocalTime\":\"2026-08-10T17:00:00\",\"markingTypeId\":\"S\",\"employeeId\":7,\"isManualEntry\":true}]",
      "sourceApi": "ExternalSystem"
    }
    ```

### Listar fichajes

```text
GET {url}/webapi/list/emp_Marking/API_MarkingList?defaults={defaults}
```

Devuelve los fichajes individuales (sin emparejar entradas y salidas) de un empleado en un rango de fechas de jornada.

| Parámetro de `defaults` | Descripción |
| --- | --- |
| `EmployeeId` | Empleado. |
| `StartDate`, `EndDate` | Rango de fechas de jornada (`yyyyMMdd`, ambos inclusive). |

- Un empleado en un mes: `defaults={"EmployeeId":7,"StartDate":"20260901","EndDate":"20260930"}`
- Solo entradas no ignoradas: `filter=Markings.MarkingTypeId='E' AND Markings.Ignore=0`

**Devuelve**, ordenado por hora de fichaje: `RegId`, `EmployeeId`/`EmployeeFullName`, `CheckTime`, `CheckTimeUtc`, `DateJourney`, `MarkingTypeId`/`MarkingTypeDescrip`, `TerminalCode`, `LocId`/`LocationDescrip`, `Ignore`, `Comments`, `MarkClassId`, `IsManualEntry`, `Inserted`, `LastUpdate`.

### Jornadas día a día

```text
GET {url}/webapi/list/emp_vHR_Employee_Daydate/API_WorkdayList?defaults={defaults}
```

Devuelve las horas trabajadas y el estado de la jornada con una fila por empleado y día. Es el equivalente en la API de la pantalla de jornadas, con el empleado y el rango de fechas como parámetros.

Los parámetros de `defaults` son los mismos que en [Listar fichajes](#listar-fichajes).

- Un empleado, una semana: `defaults={"EmployeeId":7,"StartDate":"20260831","EndDate":"20260906"}`

| Filtro de ejemplo | Resultado |
| --- | --- |
| `Employees.Department=6` | Solo empleados de un departamento. |
| `vHR_Employee_Daydate.StatusId=1` | Solo jornadas validadas. |
| `EDD.BalanceMinutes<0` | Días por debajo de la jornada teórica. |
| `EDD.FullLeaveDay=1` | Solo días de baja. |

**Devuelve**:

- **Empleado y contexto**: `EmployeeId`/`EmployeeFullName`, `DateJourney`, `DayOfWeekName`, `Department`/`DepartmentName`, `CompanyId`, `Office`, `ContractId`, `CategoryId`, `PositionId`, `CalendarId`, `GroupMarkingsModeId`.
- **Turno**: `ShiftId`, `ShiftDescrip`, `ShiftAlias`, `ShiftColour`, `ShiftTextColour`, `ShiftTypeId`, `ShiftTypeDescrip`, `ShiftStart`, `ShiftEnd`, `RawShiftStart`, `RawShiftEnd`, `RawShiftChanged`.
- **Fichajes**: `FirstInput`, `LastOutput`.
- **Horas decimales**: `WorkHours`, `TheoryHours`, `PlannedHours`, `ComputedHours`, `AbsenceHours`.
- **Minutos**: `WorkedMinutes`, `TheoryMinutes`, `PlannedMinutes`, `ComputableMinutes`, `AbsenceMinutes`, `AvailabilityMinutes`, `StopWorkedMinutes`, `BalanceMinutes`, `ScheduleMinutes`, y su versión en `HH:mm` (`WorkedHoursText`, `TheoryHoursText`, `PlannedHoursText`, `ComputedHoursText`, `AbsenceHoursText`, `AvailabilityHoursText`, `StopWorkedHoursText`, `BalanceHoursText`). También `RatioWork`.
- **Estado**: `StatusId`/`StatusDescrip` (0 = Generado, 1 = Validado, 2 = Balance), `StatusDay`, `DayTypeId`, `CalculatedDayTypeId`/`CalculatedDayTypeDescrip`.
- **Tipo de día**: `FreeDay`, `FullAbsenceDay`, `FullHolidayDay`, `FullLeaveDay`, `WorkFestiveDay`, `FestiveCalendar`, `WorkOnFestive`, `ShowFestive`, `HasComputedPartialAbsence`.
- **Ubicación**: `LastLocation`/`LocationDescrip`, `LocTypeId`/`LocationTypeDescrip`, `LastLatitude`, `LastLongitude`.
- **Origen**: `Origin`, `TimePlanned`, `HasOnlineModification`, `DirtyFlag`, `DirtyReason`, `IdDoc`.
- **Horas extra e incidencias**: `ExtraComputeMinutes`, `ExtraComputeHoursText`, `Incidences`, `IncidencesBlocked`.

`BalanceMinutes` es el saldo del día (tiempo trabajado + paradas computadas − horas teóricas). Un valor negativo indica que el empleado no ha llegado a su jornada.

### Totales de jornada por empleado

```text
GET {url}/webapi/list/emp_vHR_Employee_Daydate/API_WorkdayTotals?defaults={defaults}
```

Devuelve los mismos datos que [Jornadas día a día](#jornadas-dia-a-dia), pero agregados para todo el rango: una fila por empleado, ordenada por nombre. Los parámetros de `defaults` son los mismos.

- Un empleado en un mes: `defaults={"EmployeeId":7,"StartDate":"20260801","EndDate":"20260831"}`

**Devuelve**:

- **Empleado**: `EmployeeId`/`EmployeeFullName`, `Department`/`DepartmentName`, `TotalDays`.
- **Minutos sumados**: `WorkedMinutes`, `TheoryMinutes`, `PlannedMinutes`, `ComputableMinutes`, `AbsenceMinutes`, `AvailabilityMinutes`, `StopWorkedMinutes`, `BalanceMinutes`, `ScheduleMinutes`.
- **Horas**: en decimal (`WorkedHours`, `TheoryHours`, `PlannedHours`, `ComputedHours`, `AbsenceHours`, `BalanceHours`) y en `HH:mm` (`WorkedHoursText`, `TheoryHoursText`, `PlannedHoursText`, `ComputedHoursText`, `AbsenceHoursText`, `AvailabilityHoursText`, `StopWorkedHoursText`, `BalanceHoursText`). `RatioWork` es el porcentaje de horas computadas sobre las teóricas del periodo.
- **Días por estado**: `DaysStatusGenerated`, `DaysStatusValidated`, `DaysStatusBalance`.
- **Días por tipo**: `TotalAbsences`, `TotalHolidays`, `TotalLeaves`, `TotalFreeDays`, `TotalFestiveDays`, `DaysWithPartialAbsence`.
- **Horas extra e incidencias**: `ExtraComputeMinutes`, `ExtraComputeHoursText`, `TotalIncidences`, `TotalIncidencesBlocked`.

### Totales de jornada por mes

```text
GET {url}/webapi/list/emp_vHR_Employee_Daydate/API_WorkdayMonthlyTotals?defaults={defaults}
```

Devuelve los mismos totales que [Totales de jornada por empleado](#totales-de-jornada-por-empleado), agrupados por empleado y mes natural.

| Parámetro de `defaults` | Descripción |
| --- | --- |
| `EmployeeId` | Empleado. |
| `StartMonth`, `EndMonth` | Rango de meses en formato `yyyyMM`. Se consulta desde el día 1 de `StartMonth` hasta el último día de `EndMonth`. |

- Un empleado, de junio a septiembre: `defaults={"EmployeeId":7,"StartMonth":"202606","EndMonth":"202609"}`

**Devuelve** las mismas columnas que [Totales de jornada por empleado](#totales-de-jornada-por-empleado) más `Year`, `Month`, `MonthKey` (`yyyyMM`) y `MonthName`, ordenadas por empleado y mes.

## Instancias

Cada tipo de instancia (cambio de información personal, añadir o modificar fichaje, vacaciones y ausencias, cancelación y solicitudes genéricas) tiene su propio proceso de creación. La gestión (aceptar o denegar) es común a todos los tipos. Consulta [Flujos de aprobación de instancias](../GestionInstancias/FlujosInstancias.es.md) para conocer el funcionamiento de los flujos de aprobación.

### Solicitar cambio de información personal

```text
POST {url}/webapi/exec/API_InstancePersonalDataChange
```

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `employeeId` | Sí | Empleado que solicita el cambio. |
| `comments`, `status` | No | Comentario y estado inicial de la instancia. |
| `nss`, `birthDate`, `country`, `address`, `provinceState`, `city`, `postalCode`, `idNumber`, `identificationDocTypeId`, `identificationDocRenovationDate`, `countryOfBirth`, `personalEmail`, `personalPhone`, `familySituationId`, `children`, `drivingLicense`, `emergContactName`, `emergContactPhone`, `studiesLevel` | No | Datos personales que se quieren cambiar. |

!!! example "Ejemplo"
    ```json
    {
      "employeeId": 7,
      "comments": "Me he mudado de domicilio",
      "address": "Avenida del Puerto, 45, 2º B",
      "city": "Valencia",
      "postalCode": "46023",
      "personalPhone": "699112233"
    }
    ```

### Solicitar añadir un fichaje

```text
POST {url}/webapi/exec/API_InstanceAddMarking
```

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `employeeId` | Sí | Empleado. |
| `checktime` | Sí | Fecha y hora del fichaje. |
| `markingTypeId` | Sí | `E` = entrada, `S` = salida. |
| `comments`, `terminalCode`, `locId` | No | Comentario, terminal y ubicación. |

### Solicitar modificar un fichaje

```text
POST {url}/webapi/exec/API_InstanceModifyMarking
```

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `employeeId` | Sí | Empleado. |
| `regId` | Sí | Identificador del fichaje que se quiere modificar. Debe ser un fichaje del propio empleado; se puede obtener con el catálogo `API_Aux_Markings`. |
| `ignore` | Sí | `true` para solicitar que el fichaje se ignore. |
| `checktime`, `markingTypeId`, `terminalCode`, `locId`, `comments` | No | Nuevos valores del fichaje y comentario. |

### Solicitar vacaciones o ausencias

```text
POST {url}/webapi/exec/API_InstanceHolidaysRequest
```

Solicita vacaciones, una ausencia o una baja. El tipo de instancia resultante depende del grupo al que pertenece el tipo indicado en `holidayType`.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `employeeId` | Sí | Empleado. |
| `date1`, `date2` | Sí | Fecha de inicio y de fin. |
| `holidayType` | Sí | Tipo de vacaciones o ausencia (catálogo `API_Aux_HolidaysTypes`). |
| `reason` | Sí | Motivo. |
| `notContribution` | Sí | Indica si el periodo no cotiza. |
| `time1`, `time2` | No | Hora de inicio y de fin, para solicitudes parciales de un solo día. |

!!! warning "Requisito previo"
    El tipo de vacaciones o ausencia debe pertenecer a un grupo con tipo de instancia asignado y con un flujo de aprobación configurado. Si no, la instancia no se puede crear.

!!! example "Ejemplo"
    Ausencia parcial de un día:

    ```json
    {
      "employeeId": 7,
      "date1": "2026-09-10",
      "date2": "2026-09-10",
      "time1": "09:00",
      "time2": "13:00",
      "reason": "Cita médica",
      "holidayType": 4,
      "notContribution": false
    }
    ```

### Cancelar vacaciones o ausencias

```text
POST {url}/webapi/exec/API_InstanceCancelHolidays
```

Solicita cancelar vacaciones o ausencias ya aprobadas.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `employeeId` | Sí | Empleado. |
| `date1`, `date2` | Sí | Rango de fechas. |
| `allIds` | Sí | `true` cancela todos los días del rango; `false` cancela solo los indicados en `holidaysIds`. |
| `holidaysIds` | No | Identificadores (`RegId`) de los días que se cancelan, separados por comas. Solo se usa si `allIds = false`. |
| `comments` | No | Comentario. |

### Crear una solicitud genérica

```text
POST {url}/webapi/exec/API_InstanceRequest
```

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `employeeId` | Sí | Empleado. |
| `requestTypeId` | Sí | Tipo de solicitud (catálogo `API_Aux_RequestTypes`). |
| `deadline` | No | Fecha límite. |
| `comments` | No | Comentario. |

### Aceptar o denegar una instancia

```text
POST {url}/webapi/exec/API_InstanceManage
```

Acepta o deniega una instancia en el paso de aprobación que tiene pendiente el usuario del token.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `insId` | Sí | Identificador de la instancia. |
| `action` | Sí | `1` = Aceptar, `2` = Denegar. |
| `comments` | No | Comentario o motivo. |

### Aceptar o denegar instancias por tipo

```text
POST {url}/webapi/exec/API_InstanceManageByType
```

Acepta o deniega en bloque todas las instancias pendientes de un tipo asignadas a un validador. Si una instancia falla, el resto del lote se sigue procesando.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `typeId` | Sí | Tipo de instancia (catálogo `API_Aux_InstanceTypes`). |
| `validatorEmployeeId` | Sí | Empleado validador. |
| `action` | Sí | `1` = Aceptar, `2` = Denegar. |
| `comments` | No | Comentario. |

**Devuelve** el número de instancias procesadas (`Processed`) y con error (`Errors`).

### Listar mis instancias

```text
GET {url}/webapi/list/Instance/API_InstanceList
```

Lista las instancias creadas por el usuario del token. Para ver solo las pendientes: `filter=StatusId=0`.

**Devuelve**: `InsId`, `TypeId`/`TypeDescrip`, `Date`, `EmployeeId`, `Description`, `StatusId`/`StatusDescrip`, `Comments`, `AutoAccepted`, `Inserted`, `LastUpdate`.

### Listar instancias como validador

```text
GET {url}/webapi/list/Instance/API_InstanceValidatorList
```

Lista las instancias en las que el usuario del token es validador de algún paso, pendientes o ya gestionadas. Para ver solo las que quedan por validar: `filter=StatusId=0`.

**Devuelve**: `InsId`, `TypeId`/`TypeDescrip`, `Date`, `EmployeeId`, `EmployeeFullName`, `Description`, `StatusId`/`StatusDescrip`, `Comments`, `Step`, `Inserted`, `LastUpdate`.

### Catálogos de instancias

| Vista | Valores para | Devuelve |
| --- | --- | --- |
| `emp_Employee/API_Aux_FamilySituations` | `familySituationId` | `FamilySituationId`, `Descrip` |
| `StudiesLevel/API_Aux_StudiesLevels` | `studiesLevel` (solo activos) | `StudiesLevel`, `Descrip` |
| `emp_Markings_Type/API_Aux_MarkingTypes` | `markingTypeId` | `MarkingTypeId`, `Descrip` |
| `Location/API_Aux_Locations` | `locId` (solo ubicaciones activas) | `LocId`, `Descrip`, `TypeId`, `Disabled` |
| `emp_Holidays_Type/API_Aux_HolidaysTypes` | `holidayType` (solo tipos activos y solicitables) | `Type`, `Descrip`, `Code`, `GroupId`, `Requestable`, `Disabled` |
| `emp_Request_Type/API_Aux_RequestTypes` | `requestTypeId` | `TypeId`, `Descrip`, `InstanceTypeId` |
| `Instance_Type/API_Aux_InstanceTypes` | `typeId` (solo tipos activos) | `TypeId`, `Descrip`, `Disabled`, `Active` |
| `emp_Marking/API_Aux_Markings` | `regId` en [Solicitar modificar un fichaje](#solicitar-modificar-un-fichaje) | `RegId`, `EmployeeId`, `EmployeeFullName`, `CheckTime`, `CheckTimeUtc`, `DateJourney`, `MarkingTypeId`/`MarkingTypeDescrip`, `TerminalCode`, `LocId`/`LocationDescrip`, `Ignore`, `Comments`, `MarkClassId`, `IsManualEntry`, `Inserted`, `LastUpdate` |

`API_Aux_Markings` se filtra siempre por empleado y fecha mediante `filter`, por ejemplo: `filter=Markings.EmployeeId=1 AND CheckTime>='20260810' AND CheckTime<'20260811'`.

## Turnos

### Crear un turno

```text
POST {url}/webapi/exec/API_ShiftInsert
```

Crea un turno completo con sus líneas diarias y sus paradas. Si falla alguna línea o parada, se deshace todo el turno.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `Name` | Sí | Nombre del turno. |
| `Days` | Sí | Array JSON serializado como texto, con un elemento por día: `DayId` (1 = lunes ... 7 = domingo), `StartTime` y `EndTime` (`HH:mm`) y, opcionalmente, `Stops` (paradas con `StartTime` y `EndTime`). |
| `Alias` | No | Alias del turno. |

!!! example "Ejemplo"
    Turno de noche los fines de semana (cruza la medianoche):

    ```json
    {
      "Name": "Turno de noche fin de semana",
      "Alias": "TN-FDS",
      "Days": "[{\"DayId\":6,\"StartTime\":\"22:00\",\"EndTime\":\"06:00\"},{\"DayId\":7,\"StartTime\":\"22:00\",\"EndTime\":\"06:00\"}]"
    }
    ```

### Listar turnos

```text
GET {url}/webapi/list/emp_Shift/API_ShiftList
```

Lista los turnos completos: la cabecera y, en la columna `DaysJson`, sus líneas diarias y paradas en un único JSON por turno, con una estructura similar a la de [Crear un turno](#crear-un-turno).

**Devuelve**: `ShiftId`, `Descrip`, `Alias`, `Colour`, `TextColour`, `TypeId`/`TypeDescrip`, `UnitId`/`OrgUnitName`, `Office`/`OfficeDescrip`, `ScopeId`/`ScopeDescrip`, `EmployeeId`/`EmployeeFullName`, `Order`, `Flextime`, `BreakSigned`, `Disabled`, `Inserted`, `LastUpdate` y `DaysJson` (array con `Line`, `StartDay`, `EndDay`, `StartTime`, `Duration`, `BreakMinutes` y `Stops`, que contiene `Stop`, `StopTypeId`, `StartTime`, `DurationMinutes` y `Signing`).

## Planificación

### Consultar la planificación

```text
GET {url}/webapi/list/Emp_Month_PlannerNoFilter/API_PlanningList?defaults={defaults}
```

Devuelve la planificación diaria de un empleado en un rango de fechas: turno, horas teóricas, planificadas y trabajadas, y todo lo que altera el día (festivo, día libre, vacaciones, baja, ausencia o permiso). Es el mismo cálculo que el calendario semanal del empleado, con el empleado y el rango como parámetros.

| Parámetro de `defaults` | Descripción |
| --- | --- |
| `EmployeeId` | Empleado. |
| `StartDate`, `EndDate` | Rango de fechas (`yyyyMMdd`). |

- Hoy: `defaults={"EmployeeId":7,"StartDate":"20260904","EndDate":"20260904"}`
- Esta semana: `defaults={"EmployeeId":7,"StartDate":"20260831","EndDate":"20260906"}`
- Este mes: `defaults={"EmployeeId":7,"StartDate":"20260901","EndDate":"20260930"}` (con `pageSize=31`)

| Filtro de ejemplo | Resultado |
| --- | --- |
| `vEmployeeMonthPlannerNoFilter.NoShift=0` | Solo días con turno planificado. |
| `vEmployeeMonthPlannerNoFilter.FullLeaveDay=1` | Solo días de baja. |
| `vEmployeeMonthPlannerNoFilter.FullHoliday=1` | Solo días de vacaciones. |
| `vEmployeeMonthPlannerNoFilter.Permit=1` | Solo días de permiso. |

**Devuelve** una fila por día:

- **Día**: `EmployeeId`/`EmployeeFullName`, `DateValue`, `Today`, `DayOfWeekName`, `DayNumber`, `MonthName`.
- **Turno**: `ShiftId`, `ShiftDescrip`, `ShiftAlias`, `ShiftColour`, `ShiftTextColour`, `ShiftStart`, `ShiftEnd`, `StartPlanHour`, `EndPlanHour`, `ShiftDurationHours`, `ShiftBreakHours`, `ShiftEffectiveHours`, `WorkOnFestive`, `PlanningOrigin`, `ScheduleId`, `PlanningGroupId`, `UnitId`, `NoShift`.
- **Horas**: en decimal (`TheoreticalHours`, `PlannedHours`, `WorkedHours`, `AbsenceHours`, `HolidayHours`, `DiffHours`) y en `HH:mm` (`TheoreticalHoursText`, `PlannedHoursText`, `WorkedHoursText`, `AbsenceHoursText`, `HolidayHoursText`, `DiffHoursText`). `DiffStatus` indica si el empleado está por debajo (0), exacto (1) o en exceso (2).
- **Tipo de día**: `Festive`, `FreeDay`, `FullAbsenceDay`, `FullHolidayDay`, `FullLeaveDay`, `FullPendingExcusedAbsenceDay`, `PermitDay`, `HasHolidaysHours`.
- **Ausencias y bajas**: `HasAbsences`, `AbsenceCount`, `AbsenceHoursTotal`, `PermitCount`, `HasPendingAbsence`, `AbsencesJson`, `HasLeave`, `LeaveCount`, `LeavesJson`.
- **Contexto**: `Office`, `CalendarId`, `ContractId`, `GroupMarkingsModeId`.

`AbsencesJson` contiene las ausencias, vacaciones y permisos aceptados del día (`RegId`, `Type`/`TypeDescrip`, `GroupId`/`GroupDescrip`, `StartTime`, `EndTime`, `PartialDay`, `HoursAbsent`, `HoursAbsentProductive`, `Holidays`, `HolidaysHours`, `PendingAbsence`, `ProductiveAbsence`, `NoProductiveAbsence`, `NoExcusedAbsence`, `Permit`, `Unpaid`, `Reason`). `LeavesJson` contiene las bajas vigentes ese día (`RegId`, `StartDate`, `EndDate`, `LeaveId`/`LeaveCauseDescrip`, `LeaveTypeId`/`LeaveTypeDescrip`, `LeaveGroupId`/`LeaveGroupDescrip`, `StatusId`/`StatusDescrip`, `LeaveDeclared`, `LeaveLiquidated`, `Reason`). Ambos valen `null` si no hay registros.

!!! note "Horas teóricas y planificadas"
    `TheoreticalHours` ya descuenta las ausencias parciales y las vacaciones por horas, y vale 0 en los días completos de vacaciones, baja, ausencia, ausencia pendiente de justificar, permiso o festivo. `PlannedHours` mantiene siempre las horas planificadas por el turno.

## Vacaciones y ausencias

Las acciones de solicitar y cancelar vacaciones o ausencias se hacen mediante instancias: consulta [Solicitar vacaciones o ausencias](#solicitar-vacaciones-o-ausencias) y [Cancelar vacaciones o ausencias](#cancelar-vacaciones-o-ausencias).

### Listar vacaciones y ausencias

```text
GET {url}/webapi/list/emp_Employee_Holiday/API_HolidaysList
```

Lista las vacaciones y ausencias de los empleados, con una fila por día. Los días de una misma solicitud comparten `GroupingCode` e `InsId`, por lo que se pueden reagrupar.

Filtro de ejemplo por empleado y estado aprobado: `filter=Employees_Holidays.EmployeeId=1 AND StatusId=1`.

**Devuelve**: `RegId`, `EmployeeId`, `StartDate`, `EndDate`, `PartialDay`, `StartTime`, `EndTime`, `Type`/`TypeDescrip`, `GroupId`/`GroupDescrip`, `StatusId`/`StatusDescrip`, `Reason`, `DenyReason`, `ApprovedBy`, `ApprovedDate`, `NotContribution`, `HHRRValidated`, `HHRRApprovedBy`, `HHRRApprovedDate`, `HHRRDenyReason`, `InsId`, `GroupingCode`, `HolidayPeriodId`, `Inserted`, `LastUpdate`.

### Totales de vacaciones

```text
GET {url}/webapi/list/emp_Employee_Holiday_Total/API_HolidaysTotals
```

Devuelve las vacaciones totales, utilizadas y disponibles por empleado y año.

Filtro de ejemplo por empleado y año: `filter=Employees_Holidays_Totals.EmployeeId=1 AND Year=2026`.

**Devuelve**:

- **Vacaciones del año anterior**: `LastYearLimitDate` (fecha límite para disfrutarlas, o `NULL` si no hay límite) e `IsLastYearLimitExpired` (si esa fecha ya ha pasado).
- **Vacaciones por estado**: `Acepted`, `Pending`, `Denied`.
- **Ausencias y permisos**: `JustifAbsences`, `NoJustifAbsences`, `OtherAbsences`, `TotalAbsences`, `Permissions`.
- **Días asignados**: `HolidaysLastYears`, `Holidays`, `DayTypeId`, `BagCompensationDays`, `BagCompensationHours`, `Adjust`, `BankHolidaysRecognition`, `Other`.
- **Cálculos**: `Remaining`, `TotalCount`, `TotalNoHolidayCount`, `RemainingNoLastYear`, `LastYearUsedOnPeriod`, `LastYearRemainingOrExpired`.

### Catálogos de vacaciones

| Vista | Valores para | Devuelve |
| --- | --- | --- |
| `emp_Employee_Holiday/API_Aux_HolidaysStatuses` | `StatusId` en `API_HolidaysList` (1 = Aceptada, 2 = Pendiente, 3 = Denegada, 4 = Cancelada) | `StatusId`, `Descrip` |
| `emp_Holidays_Type/API_Aux_HolidaysTypes` | `Type` en `API_HolidaysList` | `Type`, `Descrip`, `Code`, `GroupId`, `Requestable`, `Disabled` |

`API_Aux_HolidaysTypes` solo devuelve los tipos activos y solicitables, así que no incluye tipos inactivos que puedan aparecer en el histórico.

## Contratos

### Contrato actual

```text
GET {url}/webapi/list/emp_Employee_ContractData/API_ContractCurrent
```

Devuelve el contrato activo del usuario del token.

**Devuelve**: `ContractId`, `EmployeeId`, `CompanyId`/`CompanyDescrip`, `Office`/`OfficeDescrip`, `ContractType`/`ContractTypeDescrip`, `StartDate`, `EndDate`, `InitialEndDate`, `EndTrialPeriod`, `WorkdayPercentage`, `AnualSalary`, `Incentive`, `Plus`, `Paymentes`, `HolidaysNumber`, `CollectiveAgreementId`/`CollectiveAgreementDescrip`, `QuoteTypeId`/`QuoteTypeDescrip`, `HourPrice`, `MonthPrice`, `MonthlyPayment`, `RegimeId`/`RegimeDescrip`, `Tea`, `TeaId`/`TeaDescrip`, `Justification`, `TerminationReasonId`/`TerminationReasonDescrip`, `Iban`, `BankNumberEntity`, `BankNumberOffice`, `BankNumberCD`, `BankNumber`, `Inserted`, `LastUpdate`.

### Listar contratos

```text
GET {url}/webapi/list/emp_Employee_ContractData/API_ContractList
```

Lista todos los contratos de todos los empleados. Devuelve las mismas columnas que [Contrato actual](#contrato-actual) más `IsCurrent` (`1` si es el contrato activo del empleado).

Filtro de ejemplo por empleado: `filter=Employees_ContractData.EmployeeId=1`.

### Histórico de contratos

```text
GET {url}/webapi/list/emp_Employee_ContractData_ModHistory/API_ContractHistory
```

Devuelve el histórico de cambios de los contratos (condiciones iniciales, cambio de lugar de trabajo, de salario o de categoría, cierre, reapertura y ampliación), con el valor anterior y el nuevo de cada modificación.

Filtro de ejemplo por contrato: `filter=ContractId=1`.

**Devuelve**: `ModId`, `ContractId`, `EmployeeId`, `TypeModId`/`TypeModDescrip`, `DateFrom`, `CategoryId`/`CategoryDescrip`, `OldCategoryId`/`OldCategoryDescrip`, `PositionId`/`PositionDescrip`, `OldPositionId`/`OldPositionDescrip`, `QuoteTypeId`, `OldQuoteTypeId`, `HourPrice`, `OldHourPrice`, `MonthPrice`, `OldMonthPrice`, `MonthlyPayment`, `AnualSalary`, `Paymentes`, `RegimeId`, `OldRegime`, `EndDate`, `OldEndDate`, `TerminationReasonId`/`TerminationReasonDescrip`, `OldTerminationReasonId`/`OldTerminationReasonDescrip`, `ExtendContractReason`, `Inserted`, `LastUpdate`.

## Gastos

Un gasto se compone de una cabecera y de una o varias líneas. Primero se crea la cabecera, que devuelve su `PartId`, y después se añaden las líneas indicando ese `PartId`.

### Crear la cabecera de un gasto

```text
POST {url}/webapi/exec/API_ExpenseHeaderInsert
```

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `EmployeeId` | Sí | Empleado. |
| `Date` | Sí | Fecha del gasto. |
| `Client` | Sí | Cliente. |
| `IdClient` | No | Código del cliente en el ERP. |
| `StartTime`, `EndTime` | No | Horario. |
| `Billable` | No | Indica si el gasto es facturable. |
| `Comment` | No | Comentario. |

**Devuelve** el `PartId` de la cabecera creada.

### Añadir una línea de gasto

```text
POST {url}/webapi/exec/API_ExpenseLineInsert
```

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `PartId` | Sí | Cabecera a la que pertenece la línea. |
| `Descrip` | Sí | Descripción. |
| `ExpensesTypeId` | Sí | Tipo de gasto (catálogo `API_Aux_ExpensesTypes`). |
| `PaymentType` | Sí | Forma de pago (catálogo `API_Aux_PaymentTypes`). |
| `NumPeople` | Sí | Número de personas. |
| `TotalAmount` | Sí | Importe total. |
| `Units`, `UnitAmount` | No | Unidades e importe unitario (por ejemplo, kilómetros y precio por kilómetro). |
| `Factura`, `DocumentNumber` | No | Si tiene factura y su número. |
| `ExternalId` | No | Identificador externo. |

!!! example "Ejemplo"
    ```json
    {
      "PartId": 1,
      "Descrip": "Desplazamiento coche propio",
      "ExpensesTypeId": 2,
      "NumPeople": 1,
      "Units": 80,
      "UnitAmount": 0.23,
      "TotalAmount": 18.40,
      "PaymentType": 0,
      "Factura": false
    }
    ```

### Listar gastos

```text
GET {url}/webapi/list/emp_Part_Expenses/API_ExpenseList
```

Lista los gastos con el nombre del empleado, el estado y el importe total de sus líneas. Por defecto se ordenan del más reciente al más antiguo (`Date DESC`).

Filtro de ejemplo por empleado: `filter=Part_Expenses.EmployeeId=2`.

### Catálogos de gastos

| Vista | Valores para | Devuelve |
| --- | --- | --- |
| `emp_Expenses_Type/API_Aux_ExpensesTypes` | `ExpensesTypeId` | `ExpensesTypeId`, `Descrip`, `UnitAmount`, `CodExpenses`, `DefaultPaymentTypeId` |
| `emp_Payment_Type/API_Aux_PaymentTypes` | `PaymentType` | `PaymentTypeId`, `Descrip`, `Payroll`, `Payroll_Advance` |

## Reservas

### Crear una reserva

```text
POST {url}/webapi/exec/API_ReserveInsert
```

Reserva un recurso para un empleado. La reserva se rechaza si se solapa con otra reserva activa del mismo recurso ese día.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `EmployeeId` | Sí | Empleado. |
| `ResourceId` | Sí | Recurso (catálogo `API_Aux_Resources`). |
| `ReserveDate` | Sí | Fecha de la reserva. |
| `AllDay` | Sí | `true` reserva el día completo. |
| `InitDate`, `EndDate` | Si `AllDay = false` | Hora de inicio y de fin (`HH:mm`). |
| `Type` | No | Tipo de reserva (catálogo `API_Aux_ReserveTypes`). El valor `-1` está reservado a los bloqueos. |

!!! example "Ejemplo"
    ```json
    {
      "EmployeeId": 2,
      "ResourceId": 1,
      "ReserveDate": "2026-09-10",
      "AllDay": false,
      "InitDate": "10:00",
      "EndDate": "11:00",
      "Type": 1
    }
    ```

### Cancelar una reserva

```text
POST {url}/webapi/exec/API_ReserveCancel
```

Cancela una reserva, siempre que no haya empezado.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `ReserveId` | Sí | Reserva que se cancela. |

### Bloquear un recurso

```text
POST {url}/webapi/exec/API_ResourceBlock
```

Bloquea un recurso durante un día o una franja horaria, sin necesidad de asociarlo a un empleado.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `ResourceId` | Sí | Recurso. |
| `ReserveDate` | Sí | Fecha del bloqueo. |
| `AllDay` | Sí | `true` bloquea el día completo. |
| `InitDate`, `EndDate` | Si `AllDay = false` | Hora de inicio y de fin (`HH:mm`). |
| `BlockReasonId` | No | Motivo del bloqueo (catálogo `API_Aux_BlockReasons`). |
| `EmployeeId` | No | Empleado asociado. |

### Listar reservas y bloqueos

```text
GET {url}/webapi/list/emp_Reserve/API_ReserveList
```

Lista las reservas y los bloqueos de recursos con el empleado, el recurso, el tipo y el estado.

| Caso | Filtro |
| --- | --- |
| Todas las reservas | Sin filtro. |
| Reservas entre dos fechas | `Reserves.ReserveDate>='20260901' AND Reserves.ReserveDate<='20260930'` |
| Recursos bloqueados entre dos fechas | `Reserves.Type=-1 AND Reserves.ReserveDate>='20260901' AND Reserves.ReserveDate<='20260930'` |
| Mis reservas de esta semana | `Reserves.EmployeeId=7 AND Reserves.ReserveDate>='20260831' AND Reserves.ReserveDate<='20260906'` |

**Devuelve**: `ReserveId`, `EmployeeId`/`EmployeeFullName` (vacío en bloqueos sin empleado), `ResourceId`/`ResourceDescrip`, `ReserveDate`, `EndReserveDate`, `InitDate`, `EndDate`, `AllDay`, `IgnoreSaturdays`, `IgnoreSundays`, `Type`/`TypeDescrip` (`-1` en los bloqueos), `StatusId`/`StatusDescrip` (0 = Activa, 1 = Cancelada), `BlockReasonId`/`BlockReasonDescrip` (solo en bloqueos), `Inserted`, `LastUpdate`.

### Catálogos de reservas

| Vista | Valores para | Devuelve |
| --- | --- | --- |
| `emp_Resource/API_Aux_Resources` | `ResourceId` (solo recursos activos) | `ResourceId`, `Descrip`, `ClassificationResourceId`/`ClassificationResourceDescrip`, `Disabled` |
| `emp_Classification_Resource_Type/API_Aux_ReserveTypes` | `Type` en `API_ReserveInsert` (excluye el tipo de bloqueo) | `TypeId`, `Type`, `Duration`, `ClassificationResourceId`/`ClassificationResourceDescrip` |
| `Reserves_Block_Reason/API_Aux_BlockReasons` | `BlockReasonId` | `BlockReasonId`, `Descrip` |

## Noticias

### Crear una noticia

```text
POST {url}/webapi/exec/API_NewsInsert
```

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `Title` | Sí | Título. |
| `CategoryId` | Sí | Categoría (catálogo `API_Aux_NewsCategories`). |
| `PubDate`, `EndDate` | Sí | Fecha de publicación y de fin. |
| `Descrip` | No | Contenido. |
| `Image` | No | Imagen. |
| `OnTop` | No | Fija la noticia en la parte superior. |
| `StatusId` | No | Estado. Por defecto, Borrador. |
| `TypeId` | No | Tipo. Por defecto, Normal. El tipo `1` (Lectura obligatoria) crea un aviso para todos los usuarios. |

**Devuelve** el `NewsId` de la noticia creada.

### Modificar una noticia

```text
POST {url}/webapi/exec/API_NewsUpdate
```

Modifica una noticia existente. Solo se actualizan los campos informados.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `NewsId` | Sí | Noticia que se modifica. |
| `CategoryId`, `Descrip`, `EndDate`, `Image`, `OnTop`, `PubDate`, `StatusId`, `Title`, `TypeId` | No | Los mismos campos que en [Crear una noticia](#crear-una-noticia). |

### Crear una categoría de noticias

```text
POST {url}/webapi/exec/API_NewsCategoryInsert
```

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `Descrip` | Sí | Nombre de la categoría. |

**Devuelve** el `CategoryId` de la categoría creada.

### Reaccionar a una noticia

```text
POST {url}/webapi/exec/API_NewsReact
```

Registra o quita el "me gusta" o "no me gusta" de un empleado sobre una noticia.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `EmployeeId` | Sí | Empleado. |
| `NewsId` | Sí | Noticia. |
| `Reaction` | Sí | `1` = Me gusta, `2` = No me gusta, `3` = Quitar la reacción. |

### Listar noticias

```text
GET {url}/webapi/list/emp_News_Article/API_NewsList
```

Lista las noticias con su categoría, estado, tipo y el resumen de reacciones y lecturas. Para ver el detalle de una noticia concreta: `filter=News_Articles.NewsId=5`.

**Devuelve**: `NewsId`, `Title`, `Descrip`, `PubDate`, `EndDate`, `Image`, `OnTop`, `CategoryId`/`CategoryDescrip`, `StatusId`/`StatusDescrip` (0 = Borrador, 1 = Definitiva), `TypeId`/`TypeDescrip` (0 = Normal, 1 = Lectura obligatoria), `LikesCount`, `NoLikesCount`, `ReadersCount` (empleados que han abierto la noticia, hayan reaccionado o no), `Inserted`, `LastUpdate`.

### Reacciones a una noticia

```text
GET {url}/webapi/list/emp_News_Read/API_NewsReactionList
```

Lista las reacciones de los empleados a una noticia. Filtra siempre por noticia: `filter=News_Reads.NewsId=5`. Los empleados que han leído la noticia sin reaccionar no aparecen.

**Devuelve**: `NewsId`, `EmployeeId`/`EmployeeFullName`, `ReactionId` (1 = Me gusta, 2 = No me gusta), `ReactionDescrip`, `Likes`, `NoLikes`, `ReadTimes`, `FirstReadDate`, `LastReadDate`.

### Catálogos de noticias

| Vista | Valores para | Devuelve |
| --- | --- | --- |
| `emp_News_Category/API_Aux_NewsCategories` | `CategoryId` | `CategoryId`, `Descrip` |
| `emp_News_State/API_Aux_NewsStatuses` | `StatusId` (0 = Borrador, 1 = Definitiva) | `StatusId`, `Descrip`, `CssClass` |
| `emp_News_Type/API_Aux_NewsTypes` | `TypeId` (0 = Normal, 1 = Lectura obligatoria) | `Type`, `Descrip`, `CssClass` |

## Cursos

### Apuntar a un empleado a un curso

```text
POST {url}/webapi/exec/API_CourseSubscribe
```

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `CourseId` | Sí | Curso. |
| `EmployeeId` | Sí | Empleado. |
| `Confirmed` | No | Indica si la inscripción queda confirmada. |

Si el curso ya ha alcanzado su número máximo de asistentes, el proceso devuelve un error.

### Desapuntar a un empleado de un curso

```text
POST {url}/webapi/exec/API_CourseUnsubscribe
```

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `CourseId` | Sí | Curso. |
| `EmployeeId` | Sí | Empleado. |

### Listar cursos

```text
GET {url}/webapi/list/emp_Course/API_CourseList
```

Lista los cursos con su categoría, carpeta, estado, tipo y profesor principal, junto con el resumen de inscritos y valoraciones.

| Caso | Filtro |
| --- | --- |
| Todos los cursos | Sin filtro. |
| Cursos futuros | `Courses.StartDate>='20260925'` |
| Cursos en los que está inscrito un empleado | `EXISTS (SELECT 1 FROM Courses_Assistants WHERE Courses_Assistants.CourseId = Courses.CourseId AND Courses_Assistants.EmployeeId = 7)` |
| Cursos que imparte un empleado | `Courses.MainTeacher=7` |

**Devuelve**: `CourseId`, `Title`, `Descrip`, `StartDate`, `EndDateDate`, `EndInscripcionDate`, `MaxAtendants`, `AssistantsCount`, `ConfirmedCount`, `CategoryId`/`CategoryDescrip`, `FolderId`/`FolderDescrip`, `Status`/`StatusDescrip`, `Type`/`TypeDescrip`, `MainTeacher`/`MainTeacherFullName`, `Address`, `Link`, `CostType`, `Price`, `Image`, `AvgSatisfaction`, `EvaluationsCount`, `Inserted`, `LastUpdate`.

### Detalle de un curso

```text
GET {url}/webapi/list/emp_Course/API_CourseDetail
```

Devuelve en una sola llamada los datos del curso, su programa, su calendario de sesiones y sus inscritos. Filtra siempre por curso: `filter=Courses.CourseId=3`.

**Devuelve** las mismas columnas que [Listar cursos](#listar-cursos), más `CourseContent`, `CertificateId` y tres columnas con JSON anidado:

- **ProgramJson**: programa del curso (`RegId`, `Title`, `Descrip`, `Date`, `Teacher`/`TeacherFullName`).
- **TimeTableJson**: calendario de sesiones (`RegId`, `Start`, `End`, `Descrip`).
- **AssistantsJson**: inscritos (`RegId`, `EmployeeId`/`EmployeeFullName`, `Confirmed`, `Approved`, `Evaluated`, `ConfirmedDate`, `Calification`, `Comments`).

### Valoraciones de un curso

```text
GET {url}/webapi/list/emp_Courses_Evaluation/API_CourseReactionList
```

Lista las valoraciones de satisfacción de los asistentes a un curso. Filtra siempre por curso: `filter=Courses_Evaluations.CourseId=3`.

**Devuelve**: `EvaluationId`, `CourseId`, `EmployeeId`/`EmployeeFullName`, `Satisfaction`, `Comment`, `Inserted`.

### Catálogos de cursos

| Vista | Valores para | Devuelve |
| --- | --- | --- |
| `emp_Courses_Category/API_Aux_CourseCategories` | `CategoryId` | `CategoryId`, `Descrip` |
| `emp_Courses_State/API_Aux_CourseStatuses` | `Status` (-1 = Cancelado, 0 = Activo, 1 = Cerrado) | `StatusId`, `Descrip`, `CssClass` |
| `emp_Courses_Type/API_Aux_CourseTypes` | `Type` (0 = Sin definir, 1 = Evento, 2 = Curso) | `TypeId`, `Descrip` |
| `emp_Courses_Folder/API_Aux_CourseFolders` | `FolderId` | `FolderId`, `Descrip`, `CategoryId`/`CategoryDescrip` |

## Documentación

### Listar categorías de documentación

```text
GET {url}/webapi/list/emp_Documents_Category/API_DocumentCategoryList
```

Lista las categorías de documentación con el número de documentos de cada una.

**Devuelve**: `CategoryId`, `Descrip`, `ArticlesCount`, `Inserted`, `LastUpdate`.

### Listar carpetas de documentación

```text
GET {url}/webapi/list/emp_Document_Folder/API_DocumentFolderList
```

Lista las carpetas de documentación con su categoría y el número de documentos de cada una. Filtro de ejemplo por categoría: `filter=Documents_Folders.CategoryId=1`.

**Devuelve**: `FolderId`, `Descrip`, `CategoryId`/`CategoryDescrip`, `ArticlesCount`, `Inserted`, `LastUpdate`.

### Listar documentos

```text
GET {url}/webapi/list/emp_Documents_Article/API_DocumentList
```

Lista los documentos con su categoría, carpeta y resumen de reacciones y lecturas. Filtros de ejemplo: `filter=Documents_Articles.CategoryId=1`, `filter=Documents_Articles.FolderId=1`. Para ver el detalle de un documento concreto: `filter=Documents_Articles.ArticleId=4`.

**Devuelve**: `ArticleId`, `Descrip`, `FullText`, `LanguageId`, `ConfirmDelivery` (documento de entrega obligatoria que requiere confirmación), `CategoryId`/`CategoryDescrip`, `FolderId`/`FolderDescrip`, `LikesCount`, `NoLikesCount`, `ReadersCount`, `Inserted`, `LastUpdate`.

### Reacciones a un documento

```text
GET {url}/webapi/list/emp_Documents_Read/API_DocumentReactionList
```

Lista las reacciones de los empleados a un documento. Filtra siempre por documento: `filter=Documents_Reads.ArticleId=4`. Los empleados que han leído el documento sin reaccionar no aparecen.

**Devuelve**: `ArticleId`, `EmployeeId`/`EmployeeFullName`, `ReactionId` (1 = Me gusta, 2 = No me gusta), `ReactionDescrip`, `Likes`, `NoLikes`, `ReadTimes`, `FirstReadDate`, `LastReadDate`, `DeliveryConfirmationDate` (solo en documentos de entrega obligatoria ya confirmados).

## Sugerencias

### Crear una sugerencia

```text
POST {url}/webapi/exec/API_SuggestionInsert
```

Crea una sugerencia en el buzón, en estado pendiente, y la notifica a los usuarios de RRHH.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `Title` | Sí | Título. |
| `Descrip` | Sí | Descripción. |
| `TypeId` | Sí | `complain`, `equipment`, `improvement` u `other`. |
| `ComplaintTypeId` | No | Tipo de denuncia, cuando `TypeId = complain`. |
| `EmployeeId` | No | Autor. Si no se informa, la sugerencia es anónima. |
| `Public` | No | Indica si la sugerencia es pública. |
| `Comments`, `Image` | No | Comentarios e imagen. |

### Gestionar una sugerencia

```text
POST {url}/webapi/exec/API_SuggestionManage
```

Acepta, deniega o cambia el estado de una sugerencia, y lo notifica al autor si no es anónima.

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `SuggestionId` | Sí | Sugerencia. |
| `NewStatus` | Sí | `accepted`, `denied` o `pending`. |
| `Comments` | No | Comentario. |

### Reaccionar a una sugerencia

```text
POST {url}/webapi/exec/API_SuggestionReact
```

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `EmployeeId` | Sí | Empleado. |
| `SuggestionId` | Sí | Sugerencia. |
| `Reaction` | Sí | `1` = Me gusta, `2` = No me gusta, `3` = Quitar la reacción. |

### Listar sugerencias

```text
GET {url}/webapi/list/emp_Suggestion_Mailbox/API_SuggestionList
```

Lista las sugerencias con su autor, tipo, estado, tipo de denuncia y resumen de reacciones.

| Caso | Filtro |
| --- | --- |
| Todas las sugerencias, públicas y privadas (pensado para RRHH) | Sin filtro. |
| Sugerencias públicas (la vista adecuada para un empleado) | `Suggestions_Mailbox.Public=1` |
| Sugerencias de un empleado (no incluye las enviadas como anónimas) | `Suggestions_Mailbox.EmployeeId=7` |

**Devuelve**: `SuggestionId`, `EmployeeId`/`EmployeeFullName` (vacío si es anónima), `Title`, `Descrip`, `TypeId`/`TypeDescrip`, `StatusId`/`StatusDescrip`, `Public`, `Comments`, `ComplaintTypeId`/`ComplaintTypeDescrip`, `Image`, `LikesCount`, `NoLikesCount`, `CreatedDate`.

### Reacciones a una sugerencia

```text
GET {url}/webapi/list/emp_Suggestion_Mailbox_Like/API_SuggestionReactionList
```

Lista las reacciones de los empleados a una sugerencia. Filtra siempre por sugerencia: `filter=Suggestions_Mailbox_Likes.SuggestionId=2`.

**Devuelve**: `SuggestionId`, `EmployeeId`/`EmployeeFullName`, `Like` (1 = Me gusta, 0 = No me gusta), `ReactionDescrip`, `CreatedDate`.

### Catálogos de sugerencias

| Vista | Valores para | Devuelve |
| --- | --- | --- |
| `emp_Suggestion_Mailbox_Type/API_Aux_SuggestionTypes` | `TypeId` | `TypeId`, `Descrip` |
| `emp_Suggestion_Mailbox_Status/API_Aux_SuggestionStatuses` | `NewStatus` | `StatusId`, `Descrip` |
| `emp_Suggestions_Mailbox_Complaint_Type/API_Aux_SuggestionComplaintTypes` | `ComplaintTypeId` | `ComplaintTypeId`, `Descrip` |

## Equipos

### Listar equipos

```text
GET {url}/webapi/list/emp_Team/API_TeamList
```

Lista los equipos con su responsable y su número de miembros.

| Caso | Filtro |
| --- | --- |
| Todos los equipos | Sin filtro. |
| Equipos de un empleado | `EXISTS (SELECT 1 FROM Employees_Teams WHERE Employees_Teams.TeamId = Teams.TeamId AND Employees_Teams.EmployeeId = 7)` |

**Devuelve**: `TeamId`, `Descrip`, `Photo`, `IconClass`, `ExternalId`, `ResponsableId`/`ResponsableFullName`, `Private`, `Disabled`, `MembersCount`, `Inserted`, `LastUpdate`.

### Miembros de un equipo

```text
GET {url}/webapi/list/emp_Employee_Team/API_TeamMemberList
```

Lista los empleados de un equipo. Filtra siempre por equipo: `filter=Employees_Teams.TeamId=3`.

**Devuelve**: `TeamId`, `EmployeeId`, `EmployeeFullName`, `EmployeeMail`, `EmployeeOffice`, `Inserted`.

### Catálogo de equipos

| Vista | Valores para | Devuelve |
| --- | --- | --- |
| `emp_Team/API_Aux_Teams` | `TeamId` (solo equipos activos) | `TeamId`, `Descrip`, `ResponsableId`, `Private` |

## Bajas

Las solicitudes de baja de los empleados se gestionan como instancias: consulta [Solicitar vacaciones o ausencias](#solicitar-vacaciones-o-ausencias).

### Listar bajas

```text
GET {url}/webapi/list/emp_Employee_Leave/API_LeaveList
```

Lista las bajas con el empleado, la causa, el tipo, el grupo y el estado.

| Caso | Filtro |
| --- | --- |
| Todas las bajas | Sin filtro. |
| Bajas de un empleado | `Employees_Leaves.EmployeeId=7` |
| Empleados de baja hoy | `Employees_Leaves.StatusId=1 AND Employees_Leaves.date<='20260925' AND (Employees_Leaves.dateEnd IS NULL OR Employees_Leaves.dateEnd>='20260925')` |

**Devuelve**: `RegId`, `EmployeeId`/`EmployeeFullName`, `StartDate`, `EndDate`, `Reason`, `LeaveId`/`LeaveCauseDescrip`, `LeaveTypeId`/`LeaveTypeDescrip`, `LeaveGroupId`/`LeaveGroupDescrip`, `LeaveDeclared`, `LeaveLiquidated`, `StatusId`/`StatusDescrip` (1 = Aceptada, 2 = Pendiente, 3 = Denegada), `Inserted`, `LastUpdate`.

### Catálogos de bajas

| Vista | Valores para | Devuelve |
| --- | --- | --- |
| `emp_Employee_Leave/API_Aux_LeaveStatuses` | `StatusId` | `StatusId`, `Descrip` |
| `emp_Leave_Types_Group/API_Aux_LeaveGroups` | `LeaveGroupId` (solo grupos activos) | `LeaveGroupId`, `Descrip` |
| `emp_Leave_Type/API_Aux_LeaveTypes` | `LeaveTypeId` (solo tipos activos) | `LeaveTypeId`, `Descrip`, `LeaveGroupId`/`LeaveGroupDescrip`, `ProofRequired`, `Requestable`, `EmployeeEnabled` |
| `emp_LeaveCause/API_Aux_LeaveCauses` | `LeaveId` (solo causas activas) | `LeaveId`, `Descrip`, `LeaveTypeId`/`LeaveTypeDescrip` |
