# Fichaje con Zonas Horarias

## Objetivo de la funcionalidad

El nuevo sistema de fichajes garantiza que las horas registradas en SebastianHR sean coherentes, auditables y legales, independientemente de:

  - La ubicación física del empleado

  - La configuración horaria del dispositivo

  - La oficina asignada

  - La localización desde donde ficha

  - El modo horario configurado para el empleado

  - La posible manipulación manual del reloj del móvil

El sistema separa hora laboral (CheckTime) de hora real (CheckTimeUtc) para obtener precisión absoluta sin romper los procesos actuales de turnos, jornadas y pareja de fichajes.

## Conceptos clave

### CheckTime (hora laboral oficial)

Es la hora que determina:

  - Turnos

  - Jornadas

  - DateJourney

  - Cálculos de horas

  - Matching E/S

  - Informes oficiales

  - Pantallas de usuario

Siempre debe mostrarse al usuario.

### CheckTimeUtc (instante real del fichaje)

  - Nunca se muestra al usuario

  - Se usa para:

    - Auditoría

    - Antifraude

    - Integraciones externas

    - Trazabilidad

    - Reconstrucción de horarios si cambian políticas

## Jerarquía de zonas horarias aplicadas

El sistema evalúa tres fuentes de tiempo antes de generar CheckTime.

### Zona horaria de oficina

Definida en Offices.TimeZoneId.  
Válida para empleados fijos.

### Zona horaria de localización (LocId)

Útil cuando el fichaje se realiza desde:

  - Sedes de clientes

  - Centros externos

  - Zonas geolocalizadas

  - Localizaciones de tipo remoto con TZ definida

### Zona horaria del dispositivo

Viene desde:

  - App móvil (DeviceLocalTime + DeviceTimeZoneId)

  - Navegador (cuando se permite el acceso)

Aporta hora real, incluso para viajeros internacionales.

## TimeZoneMode (modo horario del empleado)

SebastianHR opera según el modo configurado en Employees.TimeZoneMode:

| Modo | Nombre | Descripción |
| --- | --- | --- |
| 0 | OfficeTimeZone | Se aplica siempre la TZ de oficina |
| 1 | LocationTimeZone | Se aplica TZ de localización > dispositivo > oficina |
| 2 | DeviceTimeZone | Se aplica siempre la TZ del dispositivo |

  - Modo 0 para empleados administrativos, puestos estables, operarios de planta.

  - Modo 1 para técnicos que fichan en múltiples sedes o centros.

  - Modo 2 para viajeros internacionales, consultores globales, personal del área comercial que cambia de país.

## Flujo técnico completo del cálculo de horas

  1. El dispositivo envía:

    - DeviceLocalTime

    - DeviceTimeZoneId

  2. El servidor calcula:

    - `CheckTimeUtc = DeviceLocalTime - DeviceOffsetMin`

  3. El sistema determina la TZ de destino según TimeZoneMode

  4. El servidor calcula CheckTime:

CheckTime = CheckTimeUtc + Offset(TargetTimeZone)

  5. Se evalúa antifraude comparando:

diferencia = |CheckTimeUtc - NowUTC|

  6. Si la diferencia > X minutos (configurable, por defecto 8)  
→ Incidencia 19: fraude horario posible.

  7. El resto del sistema (turnos, pairs, planning) funciona igual, porque solo usa CheckTime.

## Escenarios comunes y recomendaciones de consultor

### Escenario A — Oficina Madrid, empleado viajando a México

Necesita TimeZoneMode = 2 (device)  
Para que 08:00 México no se conviertan en 15:00 Madrid.

### Escenario B — Empleado de oficina que ficha desde Canarias ocasionalmente

TimeZoneMode = 0 (office)

Para mantener sus horarios laborales oficiales.

### Escenario C — Técnico que trabaja mitad en Madrid y mitad en cliente Portugal

TimeZoneMode = 1 (location)

La localización del cliente determina la hora, no la oficina.

### Escenario D — Empleado remoto con localización "Teletrabajo Madrid"

Configurar Localización con TimeZoneId = "Romance Standard Time"  

TimeZoneMode = 1 para que el fichaje respete esa "sede virtual".

### Escenario E — Empresas multinacionales con múltiples sedes

Pueden definir localizaciones con TZ específicas por país.  
Los empleados en modo 1 o 2 funcionarán automáticamente.

## Diagnóstico de problemas frecuentes

### “El empleado ficha a una hora distinta a la que ve en su móvil”

Explicación típica:

  - Está en modo 0 (oficina)

  - Está en un país diferente

  - La hora se adapta a la oficina, no al dispositivo

 Solución: ¿Debe ser viajero? Cambiar TimeZoneMode a 2.

### “Un empleado de oficina ve horas incoherentes al fichar desde cliente”

Causa habitual:

  - Localización sin TimeZoneId definido

  - Para modo 1, esto hace fallback al dispositivo

 Solución:  
Definir TimeZoneId en Locations.

### “Nos aparece incidencia 19 (fraude) sin motivo aparente”

Razones comunes:

  - Móvil con hora manual

  - Móvil sin sincronización automática

  - VPN que cambia de zona horaria

  - Hora del servidor del móvil atrasada

 Solución:  
Revisar configuración horaria del dispositivo.

### “La hora que aparece en informes no coincide con la hora real del país del empleado”

Recordar:  
Los informes SIEMPRE usan la hora laboral (CheckTime)  
La hora real (CheckTimeUtc) NO es la que rige la jornada.

## Buenas prácticas para consultores

✔ Establecer por defecto:

  - Administrativos → Mode 0

  - Técnicos de campo → Mode 1

  - Empleados globales → Mode 2

✔ Definir siempre TimeZoneId en:

  - Oficinas

  - Localizaciones críticas

  - Sedes internacionales

✔ Revisar Settings antes de activar fichaje por móvil

✔ Revisar la hora del servidor y del móvil cuando haya incidencias de fraude

✔ Comunicar al cliente que los fichajes no cambian el comportamiento de turnos, siempre siguen funcionando con CheckTime.

## FAQ para consultores

### ¿Hay que modificar triggers, turnos o cálculos de jornada?

No. Nada.

Todo sigue usando CheckTime, por lo que el comportamiento es exactamente igual que antes.

### ¿Se puede reconstruir horas si cambia la política horaria?

Sí, porque CheckTimeUtc queda guardado.  
Consultoría avanzada: Reproceso masivo basado en UTC.

### ¿Los empleados ven CheckTimeUtc?

No.

Solo CheckTime.

### ¿Influye la hora del servidor?

Solo como fallback temporal.  
Toda la lógica depende de TZ + offset.

## Resumen final para consultores

  - La separación CheckTime / CheckTimeUtc es esencial para cumplir normativa y soportar movilidad.

  - El modo horario determina cuál es la zona horaria laboral aplicable.

  - Todo el cálculo interno del sistema sigue funcionando igual que antes.

  - La determinación de la TZ objetivo es completamente automática.

  - El antifraude garantiza que un fichaje no pueda alterarse manipulando la hora del móvil.

Con esto, puedes:

  - Diagnosticar cualquier caso de fichado “raro”.

  - Configurar correctamente a los empleados según su perfil.

  - Explicar al cliente cualquier situación aparente contradictoria.

  - Ofrecer un servicio avanzado de consultoría sin necesidad de tocar código.
