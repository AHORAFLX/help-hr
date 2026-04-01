# Métricas de la jornada del empleado

### 1\. Conceptos básicos de la jornada

Para entender qué pasa con cada caso (vacaciones, baja, festivo, etc.), primero hay que tener claras las métricas de la jornada que maneja el sistema:

  1. Horas planificadas

     * Lo que dice el calendario / planning que toca trabajar ese día.

     * Vienen del turno del día (hora de entrada, salida, pausas…).

     * Se ven afectadas por Festivos y Vacaciones (tiempo de descanso del trabajador). También afectan las horas de vacaciones,

     * En tu función se calcula a partir de `Effective` del turno.

  2. Horas teóricas

     * Lo que “se espera” que compute a efectos de jornada y saldo.

     * Es el punto de comparación para saber si falta tiempo, sobra, etc.

     * Se ven afectadas por las ausencias computables y parten de las horas planificadas.

     * Es como decir: _“Hoy, para estar al día, este empleado debería computar X horas (trabajadas o justificadas)”_.

  3. Horas trabajadas / fichadas

     * Lo que el empleado realmente ha fichado (entradas / salidas) ese día.

     * Se calculan a partir de los fichajes (Markings / MarkingsPair), descontando descansos.

  4. Horas de ausencia computables

     * Horas que no se trabajan pero sí cuentan como tiempo a favor del empleado (por ejemplo: baja médica, permiso retribuido, ciertas ausencias productivas…).

     * En tu código están en `ComputableAbsenceHours`.

  5. Horas computadas (Computed)

     * Es la suma de :

> Horas trabajadas + horas de ausencia computable

     * Es el tiempo que el sistema reconoce como “computado” para saldos, bancos de horas, etc.

  6. Balance / saldo del día

     * Diferencia entre horas computadas y horas teóricas:

> `Balance = Horas computadas – Horas teóricas`

     * Si es positivo, el empleado “gana” tiempo; si es negativo, “debe” tiempo.



### 2\. ¿Qué hace el sistema en un día normal (sin nada raro)?

### Día laborable normal, sin ausencias, sin festivo, sin baja

  * Horas planificadas  
= todas las horas del turno (`Effective`).

  * Horas teóricas  
= esas mismas horas del turno.

> Teoría = horario completo, porque se espera que trabaje todo.

  * Horas trabajadas

    * Si el empleado ficha todas las horas → igual que las planificadas.

    * Si ficha menos → menor que lo planificado (por ejemplo, se va antes).

  * Horas de ausencia computables  
= 0 (no hay ausencia).

  * Horas computadas  
= horas trabajadas.

  * Balance

    * Si trabaja todo lo planificado → balance ≈ 0.

    * Si trabaja menos → balance negativo.

    * Si trabaja más (horas extra) → balance positivo.

Este es el caso base sobre el que se construye todo lo demás.



### 3\. Festivos de calendario

### 3.1 Festivo no trabajado

Día marcado como festivo en el calendario del empleado , y el empleado no trabaja ese día.

En tu lógica:

  * Horas planificadas  
= 0 (el festivo “apaga” la planificación del turno).

  * Horas teóricas  
= 0

> El sistema entiende que no se esperaba trabajo ese día.

  * Horas trabajadas

    * Normalmente 0 (no ficha).

    * Si ficha por error, habría horas trabajadas, pero conceptualmente no debería.

  * Horas de ausencia computables  
= 0 (no hay ausencia, es un festivo).

  * Horas computadas  
= 0.

  * Balance  
= 0 (no se genera ni deuda ni exceso por ser festivo).

 A efectos de saldo diario, un festivo no trabajado es neutro.



### 3.2 Festivo trabajado (Work on Festive)

En tu lógica aparece el indicador de si el festivo se trabaja o no (`WorkOnFestive` / `FestiveWorked`).

Cuando es festivo pero se configura como trabajado (por ejemplo, campaña, tienda abierta, etc.):

  * Horas planificadas  
= horas de turno (como un día normal).

  * Horas teóricas  
= mismas horas del turno (se espera que trabaje).

  * Horas trabajadas

    * Según fichajes: si cumple todo, igual que teóricas.

  * Horas de ausencia computables  
= 0, salvo que además haya ausencias.

  * Horas computadas  
= trabajadas.

  * Balance

    * Igual que un día normal: se mira lo que hace respecto a las horas teóricas.

Festivo trabajado se comporta (en métricas) como un día normal , aunque luego puede tener tratamiento especial para nómina/plus festivo.

 

### 4\. Vacaciones (grupo 1)

Las vacaciones son un tipo especial de ausencia:

  * No se trabaja ,

  * pero sí cuentan como tiempo “debido” cumplido.

Tus reglas hacen esto:

### 4.1 Vacaciones de día completo

  * Horas planificadas  
= 0 (el día deja de considerarse día laborable planificado).

  * Horas teóricas  
= 0 (no se espera que el trabajador compute horas ese día).

  * Horas trabajadas  
= 0 (no hay fichajes).

  * Horas de ausencia computables  
= todas las horas del turno.

> Si el turno era de 8 h, computable = 8 h.

  * Horas computadas  
= 8 h (vacaciones).

  * Balance  
= 0 (el empleado ni gana ni pierde saldo, la vacación le cubre completamente el día).

Las vacaciones sostienen el saldo: no “debe” horas por estar de vacaciones.



### 5\. Bajas laborales (Employees_Leaves)

Las bajas (IT, enfermedad, accidente…) también se tratan como un caso en el que el empleado no trabaja pero tampoco se le penaliza.

En tu función, cuando hay baja:

  * Se marca el día como FullLeaveDay.

  * Ese día se trata de forma parecida a vacaciones/permiso retribuido a efectos de horas teóricas.

Efectos típicos:

  * Horas planificadas  
→ 0 en muchos casos (depende de la combinación, pero conceptualmente se “apaga” la planificación como día de baja).

  * Horas teóricas  
→ 0 (no se espera que trabaje mientras está de baja).

  * Horas trabajadas  
→ normalmente 0.

  * Horas de ausencia computables  
→ el sistema puede computar esas horas como ausencias justificadas a favor (según parametrización).

  * Horas computadas  
→ la baja puede contar como horas computadas (para saldo), aunque no haya fichajes.

La idea funcional es:  
“Mientras está de baja, el empleado no se come el saldo, no acumula deuda de horas.”


### 6\. Ausencias productivas retribuidas (GroupId 3,4,7 + UnPaid = 0)

> El Grupo 7 se refiere a "Vacaciones por horas", pero este grupo es tratado como una ausencia parcial a efectos de cómputo y no haremos más distinción en el resto del documento.

Ejemplos típicos:

  * Cita médica retribuida

  * Visitas oficiales justificadas

  * Formación considerada trabajo

  * Otros permisos configurados como “productivos”

### 6.1 Día completo (sin horas parciales)

En tu código:

  * Si es ausencia productiva y no se ha informado un rango de horas concreto (`HoursAbsentProductive = 0` pero es día completo):

    * Horas planificadas → se mantienen (sigue siendo día laborable).

    * Horas teóricas → pasan a 0 (se cubre todo el día con ausencia productiva).

    * Horas de ausencia computables → todas las horas del turno (como si hubiera trabajado).

    * Horas trabajadas → 0 (no ficha).

    * Horas computadas → igual a las del turno.

Es como decir:  
“No ha venido, pero es como si hubiera trabajado a efectos de saldo.”

### 6.2 Ausencia productiva parcial

Ejemplo: turno de 8 h y ausencia productiva de 2 horas por médico.

  * Horas planificadas  
= 8 (no cambia el turno).

  * Horas teóricas  
= 8 – horas de ausencia computable → 6 horas.

> El sistema espera que trabaje 6 h y las otras 2 cuentan como justificadas.

  * Horas de ausencia computables  
= 2 h (lo que dura la ausencia).

  * Horas trabajadas

    * Si ficha 6 h → perfecto.

  * Horas computadas  
= 6 h trabajadas + 2 h computables = 8 h.

  * Balance  
= 0 (ha cumplido el día aunque sólo haya trabajado 6 h).

Resultado funcional:  
La ausencia productiva parcial “rellena” el día para no penalizar al empleado.

 

### 7\. Permisos retribuidos (GroupId 6 + UnPaid = 0)

Funcionan prácticamente igual que las ausencias productivas retribuidas:

  * Pueden ser de día completo o parciales.

  * Forman parte de las condiciones:

    * Día completo → Horas teóricas = 0, computables = jornada completa.

    * Parcial → bajan las horas teóricas y suman computables por la parte del permiso.

Permiso retribuido = no trabajas, pero cuenta como tiempo a favor.

 

### 8\. Ausencias no productivas / no retribuidas (GroupId 3,4,7 + UnPaid = 1)

Ejemplos:

  * Ausencia personal no retribuida

  * Ausencia por motivos propios que no cotizan ni computan

  * O configuraciones de causas no productivas

En tu vista, estas se marcan como NoProductiveAbsence.

Efectos:

  * Horas planificadas  
= las del turno (no se apaga el día).

  * Horas teóricas  
= se mantienen como si tuviera que trabajar toda la jornada (no se bajan por esta ausencia).

  * Horas de ausencia computables  
= 0 (esas horas NO cuentan como trabajadas ni justificadas a favor).

  * Horas trabajadas

    * Lo que realmente fiche (posiblemente menos que teórica).

  * Horas computadas  
= sólo las trabajadas.

  * Balance  
= negativo por las horas de ausencia no productiva.

Interpretación clara para el usuario:

> Estas ausencias cuentan como “tiempo que debería haber trabajado pero no ha trabajado y no se le cubre” → generan deuda.

 

### 9\. Permisos NO retribuidos (GroupId 6 + UnPaid = 1)

Igual filosofía que las ausencias no productivas:

  * No bajan horas teóricas.

  * No suman horas computables.

  * El hueco queda como deuda frente a la jornada teórica.

“Te hemos concedido el permiso, pero a efectos de horas, no se consideran trabajadas ni justificadas.”

 

### 10\. Ausencias pendientes y no justificadas (GroupId 2 y 5)

  * Pendiente (GroupId 2): algo que aún no se ha justificado o validado.

  * No justificada (GroupId 5): ausencia sin motivo aceptado.

Funcionalmente:

  * Horas teóricas  
= se mantienen (se esperaba que trabajara).

  * Horas computables de ausencia  
= 0.

  * Horas trabajadas

    * Probablemente 0 o menos de la teórica.

  * Horas computadas  
= sólo las trabajadas.

  * Balance  
= negativo, reflejando ausencia injustificada o no resuelta.

Esto resalta visualmente los días donde falta tiempo sin justificar.

 

### 11\. Resumen mental rápido para usuarios

Te dejo un resumen “de andar por casa” que puedes trasladar a manual:

  * Festivo NO trabajado  
→ No se esperan horas, no suma ni resta.

  * Festivo trabajado  
→ Es como un día normal (aunque luego se le pueda pagar distinto).

  * Vacaciones / Bajas / Permisos retribuidos / Ausencias productivas retribuidas  
→ Cubren la jornada:

> “Aunque no venga, a efectos de horas está al día.”

  * Ausencias NO retribuidas, permisos no retribuidos, no justificadas, pendientes  
→ No cubren nada:

> “Ese tiempo cuenta como que debía venir y no vino → genera saldo negativo.”

  * Ausencias parciales retribuidas  
→ El trozo ausente cuenta como trabajado, el resto se compara con fichajes.

  

  

<table><thead><tr><th>Tipo de ausencia / día</th><th>¿Computa como trabajado?</th><th>¿Genera deuda?</th><th>¿Cubre el turno?</th><th>Comentario</th></tr></thead><tbody><tr><td><strong>Vacaciones día completo</strong></td><td>✔ Sí</td><td>✖ No</td><td>✔ Completo</td><td>Día cubierto</td></tr><tr><td><strong>Vacaciones por horas (retrib.)</strong></td><td>✔ Sí (parcial)</td><td>✖ No</td><td>✔ Parcial</td><td>Cubre tramo solicitado</td></tr><tr><td><strong>Vacaciones por horas (no retr.)</strong></td><td>✖ No</td><td>✔ Sí</td><td>✖ No</td><td>Funciona como ausencia no productiva</td></tr><tr><td><strong>Ausencia productiva retribuida</strong></td><td>✔ Sí</td><td>✖ No</td><td>✔ Completo/parcial</td><td>Justificada y computable</td></tr><tr><td><strong>Permiso retribuido</strong></td><td>✔ Sí</td><td>✖ No</td><td>✔</td><td>Igual que ausencia productiva</td></tr><tr><td><strong>Ausencia no productiva</strong></td><td>✖ No</td><td>✔ Sí</td><td>✖ No</td><td>Justificada pero no computa</td></tr><tr><td><strong>Permiso NO retribuido</strong></td><td>✖ No</td><td>✔ Sí</td><td>✖ No</td><td>No cubre horas</td></tr><tr><td><strong>Ausencia pendiente</strong></td><td>✖ No</td><td>✔ Sí</td><td>✖ No</td><td>Aún sin validar</td></tr><tr><td><strong>Ausencia no justificada</strong></td><td>✖ No</td><td>✔ Sí</td><td>✖ No</td><td>Penaliza como ausencia</td></tr><tr><td><strong>Baja laboral</strong></td><td>✔ Sí (según config.)</td><td>✖ No</td><td>✔</td><td>Protege al empleado</td></tr><tr><td><strong>Festivo</strong></td><td>N/A</td><td>N/A</td><td>N/A</td><td>Día neutro (si no se trabaja)</td></tr><tr><td><strong>Festivo trabajado</strong></td><td>✔ Sí</td><td>Según horas</td><td>✔</td><td>Día laboral normal</td></tr></tbody></table>