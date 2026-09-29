# Fichaje con Zonas Horarias

## Objetivo de la funcionalidad

Sebastian HR registra los fichajes de forma coherente aunque el empleado fiche desde otro país, desde la sede de un cliente o con un dispositivo en otra zona horaria. Para ello guarda dos horas por cada fichaje:

- **Hora oficial**: la hora laboral del fichaje en la zona horaria que le corresponde al empleado. Es la que usan los turnos, las jornadas, los cálculos de horas, los informes y las pantallas.
- **Hora UTC**: el instante real en que se hizo el fichaje. Sirve para auditar el fichaje y para detectar desfases entre el reloj del dispositivo y el del servidor.

El empleado solo ve la hora oficial. RRHH puede consultar también la hora UTC y el detalle del cálculo (ver [Consultar y corregir la zona horaria de un fichaje](#consultar-y-corregir-la-zona-horaria-de-un-fichaje)).

## De dónde sale la zona horaria

Hay tres fuentes posibles:

| Fuente | Dónde se configura |
| --- | --- |
| Oficina | Campo **Huso horario** del centro de trabajo (`Mantenimiento > Organización > Centros de trabajo`). Si no tiene ninguno, se usa la hora de Madrid. |
| Localización | Campo de huso horario de la localización (`Mantenimiento > Registros de tiempo > Localizaciones`). Solo cuenta si el fichaje se hace en esa localización. |
| Dispositivo | La envía el móvil o el navegador desde el que ficha el empleado (la zona horaria configurada en el equipo). |

## Modo de zona horaria del empleado

En la ficha del empleado, el campo **Modo de zona horaria** decide qué fuente se usa:

| Modo | Qué zona se aplica | Para quién |
| --- | --- | --- |
| Usar la zona horaria de la oficina (modo estándar) | Siempre la de la oficina. | Administrativos, puestos estables, operarios de planta. |
| Usar la zona horaria de la localización si la hay (modo ubicación) | La de la localización; si no tiene, la del dispositivo; si tampoco, la de la oficina. | Técnicos que fichan en varias sedes o centros. |
| Usar la zona horaria real del dispositivo (modo móvil real) | La del dispositivo; si no llega, la de la oficina. Ignora la de la localización. | Personal que viaja a otros países. |

!!! note "Cambiar el modo no recalcula fichajes antiguos"
    Cada fichaje guarda el modo con el que se registró. Si cambias el modo de un empleado, solo afecta a sus fichajes nuevos.

Los fichajes que introduce RRHH manualmente se interpretan siempre en la hora de la oficina.

## Control de desfase horario

Al registrar un fichaje del empleado, el sistema compara la hora del dispositivo con el reloj del servidor. Si la diferencia supera 8 minutos, marca el fichaje y se genera en la jornada la incidencia **Desfase horario dispositivo**, que RRHH debe revisar y resolver manualmente.

Este control:

- no bloquea ni corrige el fichaje: solo lo señala para revisión;
- no se aplica a los fichajes introducidos manualmente ni a los generados por el sistema;
- toma como referencia el reloj del servidor, por lo que este debe estar bien sincronizado.

## Consultar y corregir la zona horaria de un fichaje

En la gestión diaria de fichajes, la opción **Ver trazabilidad del tiempo** muestra, para cada fichaje, la hora del dispositivo y su zona, la hora UTC, el resultado del control de desfase y la zona que se aplicó finalmente. La ven los usuarios con rol de administración o de Recursos Humanos.

Desde ese mismo panel se puede cambiar el modo de zona horaria de un fichaje o de un día completo, siempre que la jornada no esté cerrada. Al guardar, se recalcula la hora oficial a partir de la hora UTC.

## Escenarios comunes

### Oficina en Madrid, empleado de viaje en México

Modo **móvil real**, para que las 08:00 de México no se registren como las 15:00 de Madrid.

### Empleado de oficina que ficha desde Canarias ocasionalmente

Modo **estándar**, para mantener sus horarios oficiales.

### Técnico que trabaja entre Madrid y un cliente en Portugal

Modo **ubicación**, con una localización para el cliente que tenga su huso horario. La localización del cliente determina la hora, no la oficina.

### Empleado en teletrabajo

Crea una localización (por ejemplo, "Teletrabajo Madrid") con el huso horario de Madrid y asigna al empleado el modo **ubicación**.

### Empresas con sedes en varios países

Define localizaciones con el huso horario de cada país. Solo se aplican a los empleados en modo **ubicación**.

## Diagnóstico de problemas frecuentes

### "El empleado ficha a una hora distinta a la que ve en su móvil"

Lo habitual es que esté en modo estándar y fiche desde otro país: la hora se adapta a la oficina, no al dispositivo. Si el empleado viaja con frecuencia, cámbialo a modo móvil real.

### "Un empleado ve horas incoherentes al fichar desde un cliente"

Suele ser una localización sin huso horario: en modo ubicación, el sistema pasa entonces a usar la zona del dispositivo. Define el huso horario en la localización.

### "Aparece la incidencia Desfase horario dispositivo sin motivo aparente"

Causas habituales:

- el reloj del móvil está puesto a mano o no se sincroniza automáticamente;
- la zona horaria del dispositivo no corresponde a la hora que muestra;
- el reloj del servidor no está sincronizado.

### "La hora de los informes no coincide con la hora real del país del empleado"

Los informes usan siempre la hora oficial, que depende del modo de zona horaria del empleado. Revisa el modo y el huso horario de su oficina o localización.

!!! warning "Restricciones de fichaje y zonas horarias"
    Las [restricciones de fichaje](restricciones-de-fichaje.es.md) comparan con la hora del servidor, no con la zona horaria del empleado. Un empleado en otro país con **Requiere fichar en los límites del turno** activado puede quedar bloqueado aunque esté dentro de su horario.

## Buenas prácticas

- Asigna el modo según el perfil: administrativos en modo estándar, técnicos de campo en modo ubicación y personal que viaja en modo móvil real.
- Define siempre el huso horario en las oficinas, en las localizaciones importantes y en las sedes internacionales.
- Cuando aparezcan incidencias de desfase horario, revisa la hora del servidor y la del móvil.
