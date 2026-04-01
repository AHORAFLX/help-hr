# Proyectos

### 1️⃣ `ProjectMode` (tipo de proyecto)

  * Define cómo se gestiona el proyecto en términos de registro y seguimiento.

  * Es más operativo y determina qué se permite imputar o calcular.

  * Valores típicos:

<table class="w-fit min-w-(--thread-content-width)" data-end="801" data-start="397"><thead data-end="436" data-start="397"><tr data-end="436" data-start="397"><th data-col-size="sm" data-end="421" data-start="397">Valor</th><th data-col-size="md" data-end="436" data-start="421">Significado</th></tr></thead><tbody data-end="801" data-start="476"><tr data-end="579" data-start="476"><td data-col-size="sm" data-end="501" data-start="476"><code data-end="494" data-start="478">Sin planificar</code></td><td data-col-size="md" data-end="579" data-start="501">Proyecto de solo registro, no se calculan horas ni costes automáticamente.</td></tr><tr data-end="689" data-start="580"><td data-col-size="sm" data-end="605" data-start="580"><code data-end="601" data-start="582">Horas de proyecto</code></td><td data-col-size="md" data-end="689" data-start="605">Se registran horas trabajadas; el coste económico no se calcula automáticamente.</td></tr><tr data-end="801" data-start="690"><td data-col-size="sm" data-end="715" data-start="690"><code data-end="711" data-start="692">Coste de proyecto</code></td><td data-col-size="md" data-end="801" data-start="715">Se registran horas, gastos y costes fijos; se calcula el coste total del proyecto.</td></tr></tbody></table>

 

  * Impacto en la lógica de negocio:

    * Controla qué tablas se usan: `Projects_EmployeeHours`, `Projects_Expenses`, `Projects_FixedCosts`.

    * Controla si la vista de coste (`vProject_TotalCost`) devuelve un valor o cero.

 

### ? Significado de los tipos de presupuesto

Te propongo la siguiente codificación estándar — pensada para que encaje con los modos de proyecto (`ProjectModeId`) y con tu futura gestión de horas, costes e imputaciones:

<table class="w-fit min-w-(--thread-content-width)" data-end="1846" data-start="888"><thead data-end="960" data-start="888"><tr data-end="960" data-start="888"><th data-col-size="sm" data-end="903" data-start="888">BudgetTypeId</th><th data-col-size="sm" data-end="917" data-start="903">Descripción</th><th data-col-size="lg" data-end="939" data-start="917">Aplicación práctica</th><th data-col-size="md" data-end="960" data-start="939">Campos relevantes</th></tr></thead><tbody data-end="1846" data-start="1036"><tr data-end="1244" data-start="1036"><td data-col-size="sm" data-end="1044" data-start="1036"><strong data-end="1043" data-start="1038">1</strong></td><td data-col-size="sm" data-end="1059" data-start="1044"><strong data-end="1058" data-start="1046">Fijo (€)</strong></td><td data-col-size="lg" data-end="1210" data-start="1059">El cliente o dirección aprueba un presupuesto cerrado en dinero. No importa cuántas horas se imputen; lo importante es no sobrepasar el coste total.</td><td data-col-size="md" data-end="1244" data-start="1210"><code data-end="1225" data-start="1212">BudgetTotal</code> (€, obligatorio)</td></tr><tr data-end="1454" data-start="1245"><td data-col-size="sm" data-end="1253" data-start="1245"><strong data-end="1252" data-start="1247">2</strong></td><td data-col-size="sm" data-end="1275" data-start="1253"><strong data-end="1274" data-start="1255">Por Horas (€/h)</strong></td><td data-col-size="lg" data-end="1404" data-start="1275">El presupuesto depende de las horas trabajadas <em data-end="1339" data-start="1324">multiplicadas</em> por una tarifa. No hay límite prefijado de horas ni de importe.</td><td data-col-size="md" data-end="1454" data-start="1404"><code data-end="1419" data-start="1406">BudgetTotal</code> opcional, <code data-end="1443" data-start="1430">BudgetHours</code> opcional</td></tr><tr data-end="1647" data-start="1455"><td data-col-size="sm" data-end="1463" data-start="1455"><strong data-end="1462" data-start="1457">3</strong></td><td data-col-size="sm" data-end="1489" data-start="1463"><strong data-end="1488" data-start="1465">Horas estimadas (h)</strong></td><td data-col-size="lg" data-end="1592" data-start="1489">El presupuesto se define por un número de horas previstas. Se mide desviación en horas, no en euros.</td><td data-col-size="md" data-end="1647" data-start="1592"><code data-end="1607" data-start="1594">BudgetHours</code> (obligatorio), <code data-end="1636" data-start="1623">BudgetTotal</code> opcional</td></tr><tr data-end="1846" data-start="1648"><td data-col-size="sm" data-end="1656" data-start="1648"><strong data-end="1655" data-start="1650">4</strong></td><td data-col-size="sm" data-end="1684" data-start="1656"><strong data-end="1683" data-start="1658">Mixto (Horas + Coste)</strong></td><td data-col-size="lg" data-end="1788" data-start="1684">Se establece tanto un límite de horas como de dinero. Útil para proyectos internos o de control dual.</td><td data-col-size="md" data-end="1846" data-start="1788" dir="ltr"><code data-end="1803" data-start="1790">BudgetTotal</code> (€) y <code data-end="1823" data-start="1810">BudgetHours</code> (h) ambos relevantes</td></tr></tbody></table>

 

 

### 3️⃣ Diferencia clave

<table class="w-fit min-w-(--thread-content-width)" data-end="2264" data-start="1871"><thead data-end="1956" data-start="1871"><tr data-end="1956" data-start="1871"><th data-col-size="sm" data-end="1887" data-start="1871">Campo</th><th data-col-size="sm" data-end="1925" data-start="1887">Función principal</th><th data-col-size="md" data-end="1956" data-start="1925">Afecta qué</th></tr></thead><tbody data-end="2264" data-start="2041"><tr data-end="2147" data-start="2041"><td data-col-size="sm" data-end="2057" data-start="2041"><code data-end="2056" data-start="2043">ProjectMode</code></td><td data-col-size="sm" data-end="2094" data-start="2057">Operativo / tipo de seguimiento</td><td data-col-size="md" data-end="2147" data-start="2094">Qué se registra y calcula (horas, gastos, costes)</td></tr><tr data-end="2264" data-start="2148"><td data-col-size="sm" data-end="2164" data-start="2148"><code data-end="2162" data-start="2150">BudgetType</code></td><td data-col-size="sm" data-end="2201" data-start="2164">Financiero / tipo de presupuesto</td><td data-col-size="md" data-end="2264" data-start="2201">Cómo se interpreta y compara el coste frente al presupuesto</td></tr></tbody></table>

 

  

### ? Relación conceptual entre `Projects_Modes` y `Projects_BudgetTypes`

Aunque `Projects_Modes` y `Projects_BudgetTypes` son tablas independientes , en la práctica están relacionadas lógicamente :  
cada modo de proyecto admite ciertos tipos de presupuesto.

 

### ? 1️⃣ Lógica de relación

<table class="w-fit min-w-(--thread-content-width)" data-end="1183" data-start="551"><thead data-end="642" data-start="551"><tr data-end="642" data-start="551"><th data-col-size="sm" data-end="569" data-start="551"><code data-end="568" data-start="553">ProjectModeId</code></th><th data-col-size="sm" data-end="596" data-start="569"><code data-end="595" data-start="571">Projects_Modes.Descrip</code></th><th data-col-size="md" data-end="622" data-start="596">Posibles <code data-end="621" data-start="607">BudgetTypeId</code></th><th data-col-size="md" data-end="642" data-start="622">Ejemplo práctico</th></tr></thead><tbody data-end="1183" data-start="738"><tr data-end="852" data-start="738"><td data-col-size="sm" data-end="758" data-start="738"><strong data-end="757" data-start="740">1 - UNMANAGED</strong></td><td data-col-size="sm" data-end="791" data-start="758">Sin planificar / No gestionado</td><td data-col-size="md" data-end="812" data-start="791"><em data-end="804" data-start="793">(ninguno)</em> o NULL</td><td data-col-size="md" data-end="852" data-start="812">Proyectos sin control presupuestario</td></tr><tr data-end="1031" data-start="853"><td data-col-size="sm" data-end="869" data-start="853"><strong data-end="868" data-start="855">2 - HOURS</strong></td><td data-col-size="sm" data-end="901" data-start="869">Control por horas de proyecto</td><td data-col-size="md" data-end="985" data-start="901">2 = “Por horas facturables”<br/>3 = “Por horas estimadas”<br/>4 = “Mixto (€/h + h)”</td><td data-col-size="md" data-end="1031" data-start="985">Proyecto interno con seguimiento de tiempo</td></tr><tr data-end="1183" data-start="1032"><td data-col-size="sm" data-end="1048" data-start="1032"><strong data-end="1047" data-start="1034">3 - COSTS</strong></td><td data-col-size="sm" data-end="1080" data-start="1048">Control de coste por proyecto</td><td data-col-size="md" data-end="1134" data-start="1080">1 = “Presupuesto fijo (€)”<br/>4 = “Mixto (€/h + h)”</td><td data-col-size="md" data-end="1183" data-start="1134">Proyecto de cliente con presupuesto económico</td></tr></tbody></table>

 

 

✅ Regla práctica:

  * Usa `ProjectMode` para decidir qué datos puede imputar el usuario y qué cálculos se realizan.

  * Usa `BudgetType` para decidir cómo se mide la rentabilidad o se compara con presupuesto , sin afectar la imputación de datos.