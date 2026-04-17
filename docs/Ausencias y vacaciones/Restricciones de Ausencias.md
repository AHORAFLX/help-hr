# Restricciones de Ausencias

### Introducción

El sistema de gestión de ausencias permite configurar dos tipos de restricciones para controlar cómo y cuánto pueden solicitar los empleados:

  1. Restricciones por Solicitud : Límites por petición individual

  2. Restricciones por Periodo : Límites acumulados en un periodo concreto (anual o mensual)



## Tipos de Restricciones

### 1\. Restricciones por Solicitud (Individual)

Controlan una única petición. Útil para evitar solicitudes muy cortas o muy largas.

### Campos de configuración

  * Mínimo de horas por solicitud

  * Máximo de horas por solicitud

### Ejemplo 1: Permiso por cita médica
    

Configuración: - Mínimo: 1 hora - Máximo: 4 horas 
Solicitud de 30 minutos → DENEGADA  
Solicitud de 2 horas → ACEPTADA  
Solicitud de 6 horas → DENEGADA
    

### Ejemplo 2: Permiso por mudanza
    
    
Configuración: - Mínimo: 4 horas - Máximo: 8 horas 
Solicitud de 2 horas → DENEGADA  
Solicitud de 6 horas → ACEPTADA  
Solicitud de 1 día completo (8h) → ACEPTADA
    

 

### 2\. Restricciones por Periodo (Acumulado)

Controlan el total acumulado de solicitudes aprobadas durante un periodo (mes o año).

### Campos de configuración

  * Periodo (Anual o Mensual)

  * Máximo de días

  * Máximo de horas


## Cómo se Calculan las Restricciones por Periodo

El sistema convierte automáticamente días y horas según la jornada del empleado (normalmente 8 h/día), pero esto viene especificado en el convenio colectivo vinculado al contrato del empleado. En caso de no tener contrato contará 8 horas.

### Reglas de conversión

<table><thead><tr><th>Configuración</th><th>Validación</th></tr></thead><tbody><tr><td>Solo días</td><td>Convierte horas a días (horas ÷ 8)</td></tr><tr><td>Solo horas</td><td>Convierte días a horas (días × 8)</td></tr><tr><td>Días + horas</td><td>Convierte días a horas y suma ambos</td></tr></tbody></table>

 



## Ejemplos Prácticos

### Ejemplo 1: Solo límite de DÍAS (Asuntos propios)

### Configuración
    
    
Periodo: Anual Máximo días: 4 Máximo horas: (vacío)
    

### Situación del empleado

<table><thead><tr><th>Fecha</th><th>Tipo</th><th>Equivalente</th><th>Acumulado</th></tr></thead><tbody><tr><td>15/03/2024</td><td>1 día</td><td>1 día</td><td>1 día</td></tr><tr><td>10/05/2024</td><td>7 horas</td><td>0.875 días</td><td>1.875 días</td></tr><tr><td>20/07/2024</td><td>1 día</td><td>1 día</td><td>2.875 días</td></tr><tr><td>05/09/2024</td><td>6 horas</td><td>0.75 días</td><td>3.625 días</td></tr></tbody></table>

 

### Nueva solicitud: 5 horas

  * Conversión: 5 ÷ 8 = 0.625 días

  * Total: 4.25 → DENEGADA

### Nueva solicitud: 3 horas

  * Conversión: 3 ÷ 8 = 0.375 días

  * Total: 4.0 → ACEPTADA

### Ejemplo 2: Solo límite de HORAS (Lactancia acumulada)

### Configuración
    
    
Periodo: Mensual Máximo horas: 20 h
    

### Situación

<table><thead><tr><th>Fecha</th><th>Tipo</th><th>Equivalente</th><th>Acumulado</th></tr></thead><tbody><tr><td>04/11/2024</td><td>2 horas</td><td>2 h</td><td>2 h</td></tr><tr><td>07/11/2024</td><td>3 horas</td><td>3 h</td><td>5 h</td></tr><tr><td>12/11/2024</td><td>1 día</td><td>8 h</td><td>13 h</td></tr><tr><td>18/11/2024</td><td>4 horas</td><td>4 h</td><td>17 h</td></tr></tbody></table>

 

### Nueva solicitud: 5 horas → DENEGADA

### Nueva solicitud: 3 horas → ACEPTADA

### Ejemplo 3: Límite DÍAS + HORAS (Formación)

### Configuración
    

Periodo: Anual Máximo días: 3 (24 h) Máximo horas: 8 h Límite total: 32 horas
    

### Situación

<table><thead><tr><th>Fecha</th><th>Tipo</th><th>Equivalente</th><th>Acumulado</th></tr></thead><tbody><tr><td>15/02/2024</td><td>1 día</td><td>8 h</td><td>8 h</td></tr><tr><td>20/04/2024</td><td>5 horas</td><td>5 h</td><td>13 h</td></tr><tr><td>10/06/2024</td><td>1 día</td><td>8 h</td><td>21 h</td></tr><tr><td>15/09/2024</td><td>4 horas</td><td>4 h</td><td>25 h</td></tr></tbody></table>

 

### Nueva solicitud

  * 10 horas → Total 35 → DENEGADA

  * 1 día (8 h) → Total 33 → DENEGADA

  * 6 horas → Total 31 → ACEPTADA


### Ejemplo 4: Límite MENSUAL (Reducción de jornada)

### Configuración
    
    
Periodo: Mensual Máximo días: 2 (16 h) Máximo horas: 4 h adicionales Límite total: 20 h/mes
    

### Situación octubre 2024

<table><thead><tr><th>Fecha</th><th>Tipo</th><th>Equivalente</th><th>Acumulado</th></tr></thead><tbody><tr><td>07/10/2024</td><td>3 horas</td><td>3 h</td><td>3 h</td></tr><tr><td>14/10/2024</td><td>1 día</td><td>8 h</td><td>11 h</td></tr><tr><td>21/10/2024</td><td>4 horas</td><td>4 h</td><td>15 h</td></tr></tbody></table>

 

### Nueva solicitud

  * 1 día (8h) → Total 23 → DENEGADA

En noviembre, el contador vuelve a 0.

 

## Combinación de Ambas Restricciones

Ejemplo: Permiso retribuido
    
    
Restricción por solicitud: - Mínimo: 2 horas - Máximo: 8 horas 
Restricción por periodo: - Periodo anual - Máximo días: 5 (40 horas)


### Validaciones

  * 6 horas → válida

  * 1 hora → inválida (mínimo 2h)

  * 10 horas → inválida (máximo 8h)

  * 5 horas con 36 acumuladas → inválida (41 > 40)

 

## Advertencias Importantes

### 1\. Las restricciones solo se validan al CREAR solicitudes

No se revisan cuando se edita una existente.
    
    
Acumulado: 38/40 horas Editar una solicitud de 6h → permitido  Crear nueva solicitud de 3h → denegado  

### 2\. Solo cuentan solicitudes APROBADAS o PENDIENTES

  * Aprobadas (StatusId = 1)

  * Pendientes (StatusId = 2)

No cuentan:

  * Denegadas (3)

  * Canceladas (4)

 

## Tabla Resumen de Configuraciones

<table><thead><tr><th>Restricción</th><th>Días Config</th><th>Horas Config</th><th>Validación</th><th>Ejemplo</th></tr></thead><tbody><tr><td>Por solicitud</td><td>-</td><td>Min/Max</td><td>Por petición individual</td><td>1-4h</td></tr><tr><td>Periodo: Solo días</td><td>4 días</td><td>-</td><td>Todo en días (horas ÷ 8)</td><td>4 días</td></tr><tr><td>Periodo: Solo horas</td><td>-</td><td>24 h</td><td>Todo en horas (días × 8)</td><td>24 h</td></tr><tr><td>Periodo: Días + horas</td><td>3 días</td><td>8 h</td><td>Todo en horas sumadas</td><td>32 h totales</td></tr></tbody></table>

 
