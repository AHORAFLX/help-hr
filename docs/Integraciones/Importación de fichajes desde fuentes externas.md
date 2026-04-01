# Importación de fichajes desde fuentes externas



  

### Objetivo

Permitir la importación masiva y optimizada de fichajes desde sistemas externos (control horario, fichadores biométricos, ERPs, apps móviles, etc.) hacia Sebastian HR , utilizando el procedimiento almacenado:

  

    
    
    pMarkings_BulkInsert_API
    

  

Este procedimiento:

  * Inserta los fichajes en la tabla `dbo.Markings`.

  * Calcula automáticamente fechas de jornada y pares de entrada/salida.

  * Registra errores en `dbo.APIErrorLog`.

  * Garantiza atomicidad transaccional , con _rollback automático_ ante cualquier fallo.

 

### Requisitos previos

### Base de datos Sebastian HR

  * Acceso al esquema `dbo`.

  * Procedimiento `pMarkings_BulkInsert_API` instalado y actualizado.

### Tipos de tabla requeridos

Los siguientes tipos deben existir antes de ejecutar el procedimiento:

  * `dbo.T_MarkingsTable_All`

  * `dbo.T_BigIntTable`

  * `dbo.T_EmployeeDateTable`

### Procedimientos auxiliares requeridos

El procedimiento principal los invoca internamente:

  * `dbo.pMarkings_Internal_CalculateDateJourneyBatch`

  * `dbo.pMarkings_Internal_RecalculatePairsBatch`

 

### Estructura del procedimiento
    
    

```sql
EXEC dbo.pMarkings_BulkInsert_API      @MarkingsData = <tabla de datos>,     @SourceAPI = N'<nombre del sistema origen>',     @APIUserId = <id usuario que ejecuta>,     @APIIP = N'<ip de origen opcional>';
```    

### Parámetros

<table><thead><tr><th>Parámetro</th><th>Tipo</th><th>Descripción</th></tr></thead><tbody><tr><td><code>@MarkingsData</code></td><td><code>dbo.T_MarkingsTable_All READONLY</code></td><td>Tabla con los fichajes a insertar</td></tr><tr><td><code>@SourceAPI</code></td><td><code>NVARCHAR(100)</code></td><td>Identificador del sistema origen (ej. “ControlBiosoft”, “Workday”)</td></tr><tr><td><code>@APIUserId</code></td><td><code>INT</code></td><td>ID del usuario del sistema que realiza la operación</td></tr><tr><td><code>@APIIP</code></td><td><code>NVARCHAR(25)</code></td><td>Dirección IP del sistema cliente (opcional)</td></tr></tbody></table>

 

 

### Estructura esperada del tipo `dbo.T_MarkingsTable_All`

<table><thead><tr><th>Columna</th><th>Tipo</th><th>Descripción</th></tr></thead><tbody><tr><td><code>CheckTime</code></td><td><code>DATETIME</code></td><td>Fecha y hora del fichaje</td></tr><tr><td><code>MarkingTypeId</code></td><td><code>CHAR(1)</code></td><td>Tipo de marcaje (<code>E</code> entrada, <code>S</code> salida)</td></tr><tr><td><code>EmployeeId</code></td><td><code>INT</code></td><td>ID interno del empleado en Sebastian HR</td></tr><tr><td><code>EmployeeExternalCode</code></td><td><code>NVARCHAR(50)</code></td><td>Código del empleado en el sistema externo (opcional)</td></tr><tr><td><code>ExternalId</code></td><td><code>NVARCHAR(50)</code></td><td>Identificador único externo del fichaje (evita duplicados)</td></tr><tr><td><code>TerminalCode</code></td><td><code>NVARCHAR(50)</code></td><td>Código o nombre del dispositivo origen</td></tr><tr><td><code>LocId</code></td><td><code>INT</code></td><td><strong>Obligatorio.</strong> Identificador de la localización física donde se realiza el fichaje (por ejemplo: Oficina Central, Almacén, Remoto, Cliente A, etc.)</td></tr><tr><td><code>Location</code></td><td><code>NVARCHAR(100)</code></td><td><strong>Obligatorio si aplica fichaje móvil.</strong> Coordenadas GPS en formato <code>longitud,latitud</code> (por ejemplo: <code>-3.70379,40.41678</code>)</td></tr><tr><td><code>ProjectId</code>, <code>JobId</code></td><td><code>INT</code></td><td>Campos opcionales de contexto laboral (proyecto, tarea, etc.)</td></tr></tbody></table>

 

> ⚠️ Si `LocId` no se proporciona, el procedimiento puede rechazar el registro o derivar a una ubicación por defecto según configuración interna.

### Flujo interno del procedimiento

  1. Validación inicial

     * Comprueba que `@MarkingsData` contiene registros.

     * Calcula el siguiente `RegId` disponible y los asigna secuencialmente.

  2. Inserción masiva (bypass triggers)

     * Inserta en `dbo.Markings` con `NoAutoCalculatePairs = 1` para evitar disparadores automáticos.

     * Registra temporalmente los `RegId` insertados.

  3. Cálculo de fecha de jornada

     * Llama a `pMarkings_Internal_CalculateDateJourneyBatch` para determinar la fecha de jornada según la planificación del empleado.

  4. Cálculo de pares de entrada/salida

     * Actualiza `NoAutoCalculatePairs = 0`.

     * Ejecuta `pMarkings_Internal_RecalculatePairsBatch` para recalcular fichajes emparejados por empleado y fecha.

  5. Commit o rollback

     * Si no hay errores, hace `COMMIT`.

     * Si falla, hace `ROLLBACK` y registra el error en `dbo.APIErrorLog`.

 

### Ejemplo de uso
    
```sql 
    DECLARE @Data dbo.T_MarkingsTable_All; 
    INSERT INTO @Data (CheckTime, MarkingTypeId, EmployeeId, ExternalId, TerminalCode, LocId, Location) VALUES     ('2025-11-05T08:00:00', 'E', 101, 'BIO-001', 'TER-01', 1, '-3.70379,40.41678'),    ('2025-11-05T17:00:00', 'S', 101, 'BIO-002', 'TER-01', 1, '-3.70379,40.41678'); 
    EXEC dbo.pMarkings_BulkInsert_API     @MarkingsData = @Data,    @SourceAPI = N'BioControlSystem',    @APIUserId = 1,    @APIIP = N'192.168.1.10';
    
```

### Rendimiento y configuración

<table><thead><tr><th>Volumen de registros</th><th>Timeout recomendado</th></tr></thead><tbody><tr><td>100–200</td><td>30–60 segundos</td></tr><tr><td>500–1000</td><td>120–180 segundos</td></tr><tr><td>1000+ o empleados sin planificación</td><td>180–300 segundos</td></tr></tbody></table>

 

> Consejo: Configura el `CommandTimeout` de la aplicación cliente (ej. C# o API) en función del tamaño del lote.

 

### Buenas prácticas

  * Validar empleados y LocId antes de enviar datos.

  * Evitar duplicados en `ExternalId` para mantener integridad.

  * Asegurar precisión GPS en `Location` cuando provenga de apps móviles.

  * Registrar errores en APIErrorLog para diagnóstico rápido.

  * Ejecuciones por lotes o nocturnas para grandes volúmenes.

