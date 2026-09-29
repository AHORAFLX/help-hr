# Restricciones de Ausencias

## Introducción

El sistema de gestión de ausencias permite configurar dos tipos de restricciones para controlar cómo y cuánto pueden solicitar los empleados:

1. Restricciones por Solicitud: Límites por petición individual

2. Restricciones por Periodo: Límites acumulados en un periodo concreto (anual o mensual)

## Tipos de restricciones

### Restricciones por solicitud (individual)

Controlan una única petición. Útil para evitar solicitudes muy cortas o muy largas.

### Campos de configuración de la restricción por solicitud

- Mínimo de horas por solicitud

- Máximo de horas por solicitud

### Ejemplo 1: Permiso por cita médica

**Configuración:**

- Mínimo: 1 hora
- Máximo: 4 horas

Solicitud de 30 minutos → DENEGADA  
Solicitud de 2 horas → ACEPTADA  
Solicitud de 6 horas → DENEGADA

### Ejemplo 2: Permiso por mudanza

**Configuración:**

- Mínimo: 4 horas
- Máximo: 8 horas

Solicitud de 2 horas → DENEGADA  
Solicitud de 6 horas → ACEPTADA  
Solicitud de 1 día completo (8h) → ACEPTADA

### Restricciones por periodo (acumulado)

Controlan el total acumulado de solicitudes aprobadas durante un periodo (mes o año).

### Campos de configuración de la restricción por periodo

- Periodo (Anual o Mensual)

- Máximo de días

- Máximo de horas

## Cómo se calculan las restricciones por periodo

El sistema convierte automáticamente días y horas según la jornada del empleado (normalmente 8 h/día), pero esto viene especificado en el convenio colectivo vinculado al contrato del empleado. En caso de no tener contrato contará 8 horas.

### Reglas de conversión

| Configuración | Validación |
| --- | --- |
| Solo días | Convierte horas a días (horas ÷ 8) |
| Solo horas | Convierte días a horas (días × 8) |
| Días + horas | Convierte días a horas y suma ambos |

## Ejemplos prácticos

### Ejemplo 1: solo límite de días (asuntos propios)

**Configuración:**

- Periodo: Anual
- Máximo días: 4
- Máximo horas: (vacío)

**Situación del empleado:**

| Fecha | Tipo | Equivalente | Acumulado |
| --- | --- | --- | --- |
| 15/03/2024 | 1 día | 1 día | 1 día |
| 10/05/2024 | 7 horas | 0.875 días | 1.875 días |
| 20/07/2024 | 1 día | 1 día | 2.875 días |
| 05/09/2024 | 6 horas | 0.75 días | 3.625 días |

**Nueva solicitud: 5 horas.** Conversión: 5 ÷ 8 = 0.625 días. Total: 4.25 → DENEGADA.

**Nueva solicitud: 3 horas.** Conversión: 3 ÷ 8 = 0.375 días. Total: 4.0 → ACEPTADA.

### Ejemplo 2: solo límite de horas (lactancia acumulada)

**Configuración:**

- Periodo: Mensual
- Máximo horas: 20 h

**Situación:**

| Fecha | Tipo | Equivalente | Acumulado |
| --- | --- | --- | --- |
| 04/11/2024 | 2 horas | 2 h | 2 h |
| 07/11/2024 | 3 horas | 3 h | 5 h |
| 12/11/2024 | 1 día | 8 h | 13 h |
| 18/11/2024 | 4 horas | 4 h | 17 h |

**Nueva solicitud: 5 horas → DENEGADA.**

**Nueva solicitud: 3 horas → ACEPTADA.**

### Ejemplo 3: límite días + horas (formación)

**Configuración:**

- Periodo: Anual
- Máximo días: 3 (24 h)
- Máximo horas: 8 h
- Límite total: 32 horas

**Situación:**

| Fecha | Tipo | Equivalente | Acumulado |
| --- | --- | --- | --- |
| 15/02/2024 | 1 día | 8 h | 8 h |
| 20/04/2024 | 5 horas | 5 h | 13 h |
| 10/06/2024 | 1 día | 8 h | 21 h |
| 15/09/2024 | 4 horas | 4 h | 25 h |

**Nueva solicitud:**

- 10 horas → Total 35 → DENEGADA

- 1 día (8 h) → Total 33 → DENEGADA

- 6 horas → Total 31 → ACEPTADA

### Ejemplo 4: límite mensual (reducción de jornada)

**Configuración:**

- Periodo: Mensual
- Máximo días: 2 (16 h)
- Máximo horas: 4 h adicionales
- Límite total: 20 h/mes

**Situación octubre 2024:**

| Fecha | Tipo | Equivalente | Acumulado |
| --- | --- | --- | --- |
| 07/10/2024 | 3 horas | 3 h | 3 h |
| 14/10/2024 | 1 día | 8 h | 11 h |
| 21/10/2024 | 4 horas | 4 h | 15 h |

**Nueva solicitud:**

- 1 día (8h) → Total 23 → DENEGADA

En noviembre, el contador vuelve a 0.

## Combinación de ambas restricciones

!!! example "Ejemplo: permiso retribuido"

    Restricción por solicitud:

    - Mínimo: 2 horas
    - Máximo: 8 horas

    Restricción por periodo:

    - Periodo anual
    - Máximo días: 5 (40 horas)

### Validaciones

- 6 horas → válida

- 1 hora → inválida (mínimo 2h)

- 10 horas → inválida (máximo 8h)

- 5 horas con 36 acumuladas → inválida (41 > 40)

## Advertencias importantes

### Las restricciones solo se validan al crear solicitudes

No se revisan cuando se edita una existente.

Con un acumulado de 38/40 horas:

- Editar una solicitud de 6 h → permitido
- Crear una nueva solicitud de 3 h → denegado  

### Solo cuentan solicitudes aprobadas o pendientes

- Aprobadas (StatusId = 1)

- Pendientes (StatusId = 2)

No cuentan:

- Denegadas (3)

- Canceladas (4)

## Tabla resumen de configuraciones

| Restricción | Días Config | Horas Config | Validación | Ejemplo |
| --- | --- | --- | --- | --- |
| Por solicitud | - | Min/Max | Por petición individual | 1-4h |
| Periodo: Solo días | 4 días | - | Todo en días (horas ÷ 8) | 4 días |
| Periodo: Solo horas | - | 24 h | Todo en horas (días × 8) | 24 h |
| Periodo: Días + horas | 3 días | 8 h | Todo en horas sumadas | 32 h totales |
