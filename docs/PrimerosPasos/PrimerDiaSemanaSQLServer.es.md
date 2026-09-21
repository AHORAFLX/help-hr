# Configurar primer día de la semana

En SQL Server, el primer día de la semana se determina mediante la configuración del idioma del servidor o la sesión. La configuración regional afecta cómo se interpretan y muestran las fechas, incluido el primer día de la semana. Por defecto, muchas configuraciones regionales en SQL Server tienen el domingo como primer día de la semana. 

Esta configuración puede afectar a como Sebastian HR aplica las fechas, asi que es necesario disponer de una configuración adecuada para su correcto funcionamiento.

Puedes cambiar la configuración del primer día de la semana de la siguiente forma:

## Cambiar la configuración del idioma del servidor

```sql
EXEC sp_configure 'default language', 5; -- 0 representa el idioma Español
    GO
    RECONFIGURE WITH OVERRIDE;
```

Con esta configuración el primer día de la semana pasará a ser el lunes.

Al cambiar la configuración del idioma del servidor en SQL Server, a menudo es necesario reiniciar el servicio de SQL Server para que los cambios surtan efecto. Este reinicio garantiza que las nuevas configuraciones se apliquen adecuadamente y afecten a todas las sesiones y operaciones en el servidor. 

Para obtener el valor actual de la configuración del idioma del servidor antes de cambiarlo, puedes realizar una consulta a la vista del sistema _sys.configurations_. Aquí tienes un ejemplo:

## Obtener el valor actual de la configuración del idioma del servidor

```sql
    SELECT 
        name AS 'Configuración',
        value_in_use AS 'ValorActual'
    FROM sys.configurations
    WHERE name = 'default language';
```

Puedes obtener la lista de lenguajes con la siguiente consulta:

## Obtener la lista de lenguajes disponibles

```sql
SELECT * from sys.syslanguages
```

Es recomendable instalar la instancia en la _Collation Modern_Spanish_CI_AS._

Para obtener los datos de la collation de la instancia actual:

## Obtener datos de configuración de la instancia

```sql
    SELECT serverproperty('Collation') AS 'Collation';
```