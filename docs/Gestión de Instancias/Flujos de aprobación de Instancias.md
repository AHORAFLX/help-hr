# Flujos de aprobación de Instancias

Para conocer la funcionalidad general de la gestión de instancias visita los siguientes enlaces:

  

[Sebastian HR - Instancias I - Conceptos y flujo de aprobación](https://www.youtube.com/watch?v=JA8NGSR0bpY&list=PL9w4-AXXOetUYg92G8-dCIZ1MZ8IR_7Fp&index=13)

  

[Sebastian HR - Instancias II - Casos de uso](https://www.youtube.com/watch?v=YwhqGFkPVhI&list=PL9w4-AXXOetUYg92G8-dCIZ1MZ8IR_7Fp&index=14)

  

  

En el presente documento nos centraremos en cual es comportamiento de los flujos de aprobación en base a la parametrización existente y la ausencia o no de validador para un o varios de los pasos de la instancia.

  

Como se muestran en los videos anteriores en cada flujo de instancia podemos indicar la opción de "Todos los pasos" :

  

  * Si activamos esta opción estaremos indicando que se generen todos los pasos de la instancia en el momento de añadir la instancia, esto hará que le aparezca a todos los validadores y la instancia podrá ser gestionada por cualquiera de ellos, aprobándose o denegándose en el momento que la gestione uno de los validadores. 
  * Si no activamos esta opción, los pasos se irán generando de forma secuencial en el orden que se indica en el flujo, hasta que el primer validador no apruebe su paso, no se generará el siguiente paso de validación. Cuando un validador de la secuencia deniega el paso, se deniega la instancia y no se generan los siguientes pasos.

  

Además podemos configurar como queremos que se comporte el flujo de validación en el caso de que para alguno/s de los pasos no exista el validador. (Por ejemplo si el paso tiene como validador el responsable del empleado y el empleado no tiene informado su responsable en la ficha del empleado). Para esto tenemos un parámetro en la configuración dentro del apartado aplicación: 

  

![](../../docs_assets/images/VRW_VGhungLKmg788OZqNi3R-2RScjoMzA.png)

  

### Escenarios y Comportamientos según parametrización

### A. Flujo de Un Solo Paso

<table><thead><tr><th>Omitir si no hay validador</th><th>Todos los Pasos</th><th>Validador</th><th>Resultado</th></tr></thead><tbody><tr><td>OFF</td><td>OFF</td><td>Sin validador</td><td dir="ltr">La instancia se cancela.</td></tr><tr><td>OFF</td><td>OFF</td><td>Con validador</td><td dir="ltr">La instancia se aprueba o deniega según la acción del validador.</td></tr><tr><td>ON</td><td>OFF</td><td>Sin validador</td><td dir="ltr">La instancia se aprueba automáticamente.</td></tr><tr><td>ON</td><td>OFF</td><td>Con validador</td><td dir="ltr">La instancia se aprueba o deniega según la acción del validador.</td></tr><tr><td>OFF</td><td>ON</td><td>Sin validador</td><td dir="ltr">La instancia se cancela.</td></tr><tr><td>OFF</td><td>ON</td><td>Con validador</td><td dir="ltr">La instancia se aprueba o deniega según la acción del validador.</td></tr><tr><td>ON</td><td>ON</td><td>Sin validador</td><td>La instancia y la solicitud se aprueban automáticamente.</td></tr><tr><td>ON</td><td>ON</td><td>Con validador</td><td dir="ltr">La instancia  se aprueba o deniega según la acción del validador.</td></tr></tbody></table>

 

 *

### B. Flujo de Dos Pasos (extrapolable a mas pasos)

### Tabla 1: Flujo de Dos Pasos con Todos los Pasos = OFF

<table><thead><tr><th>Omitir si no hay validador</th><th>Todos los Pasos</th><th>Validador</th><th>Resultado</th></tr></thead><tbody><tr><td><strong>OFF</strong></td><td><strong>OFF</strong></td><td>Sin validadores</td><td>La instancia y la solicitud se cancelan.</td></tr><tr><td><strong>OFF</strong></td><td><strong>OFF</strong></td><td>Paso 1 sin validador, Paso 2 con validador</td><td>La instancia se cancela al solicitarse (por ausencia de validador en el Paso 1).</td></tr><tr><td><strong>OFF</strong></td><td><strong>OFF</strong></td><td>Paso 1 con validador, Paso 2 sin validador</td><td>La instancia se cancela al validar el Paso 1 (por ausencia de validador en el Paso 2).</td></tr><tr><td><strong>OFF</strong></td><td><strong>OFF</strong></td><td>Ambos pasos con validadores</td><td>Flujo normal: cada paso se valida de forma secuencial.</td></tr><tr><td><strong>ON</strong></td><td><strong>OFF</strong></td><td>Sin validadores</td><td>La instancia y la solicitud se aprueban automáticamente (autoaccepted=true).</td></tr><tr><td><strong>ON</strong></td><td><strong>OFF</strong></td><td>Paso 1 sin validador, Paso 2 con validador</td><td>Se omite el Paso 1 y la gestión se delega al validador del Paso 2.</td></tr><tr><td><strong>ON</strong></td><td><strong>OFF</strong></td><td>Paso 1 con validador, Paso 2 sin validador</td><td>Al aprobar el Paso 1, se aprueba la instancia, omitiendo el Paso 2.</td></tr><tr><td><strong>ON</strong></td><td><strong>OFF</strong></td><td>Ambos pasos con validadores</td><td>Flujo normal: cada paso se valida de forma secuencial.</td></tr></tbody></table>

 

 

### Tabla 2: Flujo de Dos Pasos con Todos los Pasos = ON

<table><thead><tr><th>Omitir si no hay validador</th><th>Todos los Pasos</th><th>Validador</th><th>Resultado</th></tr></thead><tbody><tr><td><strong>OFF</strong></td><td><strong>ON</strong></td><td>Sin validadores</td><td>La instancia se cancela al solicitarse.</td></tr><tr><td><strong>OFF</strong></td><td><strong>ON</strong></td><td>Paso 1 sin validador, Paso 2 con validador</td><td>La instancia se cancela al solicitarse.</td></tr><tr><td><strong>OFF</strong></td><td><strong>ON</strong></td><td>Paso 1 con validador, Paso 2 sin validador</td><td>La instancia se cancela al solicitarse (por ausencia de un validador en alguno de los pasos).</td></tr><tr><td><strong>OFF</strong></td><td><strong>ON</strong></td><td>Ambos pasos con validadores</td><td>Cualquier acción de un validador decide el estado final de la instancia.</td></tr><tr><td><strong>ON</strong></td><td><strong>ON</strong></td><td>Sin validadores</td><td>La instancia se aprueba automáticamente.</td></tr><tr><td><strong>ON</strong></td><td><strong>ON</strong></td><td>Paso 1 sin validador, Paso 2 con validador</td><td>La gestión se delega al validador del Paso 2.</td></tr><tr><td><strong>ON</strong></td><td><strong>ON</strong></td><td>Paso 1 con validador, Paso 2 sin validador</td><td>La gestión se delega al validador del Paso 1.</td></tr><tr><td><strong>ON</strong></td><td><strong>ON</strong></td><td>Ambos pasos con validadores</td><td dir="ltr">Cualquier acción de un validador decide el estado final de la instancia.</td></tr></tbody></table>

 

  

  

Tipo de validación: No requiere validación.

  

En el caso que definamos en algún paso del flujo que el tipo de validación: No requiere validación la instancia se validará automáticamente en el momento en el que el usuario introduzca la instancia, esto será así aunque existan otros pasos en el flujo que tenga el validador definido.

  

Coincidencia de validadores.

  

En el caso que tengamos definido el flujo con el parámetro Todos los Pasos = ON , si en el momento de calcular los validadores de los pasos del flujo se obtiene el mismo validador en diferentes pasos del flujo solo tendrá en cuenta uno de los pasos asignados al validador, esto es no generará varias validaciones de la misma instancia a un mismo validador.

  

Por ejemplo, para validar unas vacaciones tenemos un flujo de dos pasos, el primer paso el tipo de validación es el responsable del empleado y el segundo paso es el responsable del departamento asignado al empleado. Si cuando calculamos el flujo ambos validadores son el mismo empleado, únicamente se le enviará una solicitud de gestión de instancia y no dos (una por cada paso)

  

Auto validaciones.

  

Podemos visualizar desde la lista de instancias mediante la etiqueta AUTO, si la instancia ha sido validad por parte de algún validador o si por el contrario ha sido validada automáticamente por la configuración de nuestro flujo y/o por la ausencia de validadores:

  

![](../../docs_assets/images/xqcVR6OmcJ_ZCyFYhbfTSWanAHaumR6eAQ.png)