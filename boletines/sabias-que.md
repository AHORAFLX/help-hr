# ¿Sabías que...? Boletín informativo de Sebastian HR

Píldoras breves para los boletines, organizadas por lotes. Cada lote lleva su fecha de creación y la numeración de las píldoras continúa de un lote al siguiente. Cada píldora se apoya en un artículo de la ayuda de Sebastian HR, enlazado al final, y puede usarse suelta. Las marcadas con **[PRO]** solo están disponibles en el modo PRO.

---

## Lote 1 · 29/09/2026

### 1. ¿Sabías que Sebastian HR puede repartir tus nóminas por ti? **[PRO]**

Cada mes llega el mismo trabajo: un PDF enorme con las nóminas de toda la plantilla que hay que partir a mano y subir, una por una, a la ficha de cada empleado. Con el Separador Inteligente de PDFs basta con subir ese único documento.

El sistema lee el PDF con inteligencia artificial, identifica a cada empleado por su DNI, separa sus páginas y las vincula con su ficha. Si una nómina ocupa varias páginas seguidas, la reconoce como un solo documento. Sirve también para cualquier otro documento que incluya el DNI del empleado.

Antes de archivar nada puedes revisar el resultado: qué documentos se han vinculado, cuáles no, y asignar a mano los que falten. Al validar, cada documento se guarda en la gestión documental del empleado, dentro de la categoría Nóminas. Solo necesitas una API Key de OpenAI para empezar.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/OtrasFuncionalidades/SeparacionInteligentePDFs/)

### 2. ¿Sabías que puedes olvidarte de los fichajes de salida que faltan?

Un empleado que se va a casa sin fichar la salida deja una jornada incompleta que alguien tiene que corregir después. Si activas **Fin de turno automático** en el turno, Sebastian HR se encarga: cuando falta la salida, la registra a la hora de fin planificada.

Tú decides cuántos minutos de margen esperar antes de cerrar. Por ejemplo, si el turno termina a las 18:00 y configuras 10 minutos, a partir de las 18:10 el sistema registra una salida a las 18:00. La salida queda marcada como fichaje del sistema, así que siempre sabrás cuáles se han generado solos.

Ten en cuenta que está pensado para turnos que empiezan y terminan el mismo día: en los turnos nocturnos que acaban en otra fecha conviene seguir revisando la salida a mano.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/GestionTiempoTrabajo/AutomatizarFichajesPendientes/)

### 3. ¿Sabías que el turno de un empleado puede corregirse solo? **[PRO]**

Es habitual que un empleado acabe trabajando un turno distinto del planificado: entra de tarde en vez de mañana, cubre a un compañero... Con la reasignación automática de turnos no hace falta corregir la planificación a mano.

Sebastian HR revisa los fichajes reales de la jornada y busca, entre los turnos candidatos, el que mejor encaja con las horas de entrada y salida. Si no coincide con el planificado, cambia el turno y deja constancia del cambio para que siempre puedas consultarlo.

Tú decides a qué empleados se aplica (desde su ficha) y qué turnos pueden intercambiarse. También puedes limitar la búsqueda a los turnos de la oficina, de la unidad organizativa o del ámbito del empleado.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/GestionTiempoTrabajo/ReasignacionAutomaticaTurnos/)

### 4. ¿Sabías que los descansos pueden descontarse sin que nadie fiche?

Hay empresas en las que los empleados no fichan la pausa del almuerzo o del café, pero esas pausas no deben contar como tiempo trabajado. En Sebastian HR puedes configurar, descanso a descanso, si el empleado debe ficharlo o si el sistema lo descuenta automáticamente.

El descuento se aplica al calcular las horas de la jornada: el sistema no crea fichajes nuevos, sino que resta el descanso del tiempo fichado. Para que se descuente, el empleado debe tener un fichaje que englobe el horario del descanso.

Puedes combinar ambos modos en un mismo turno: por ejemplo, un descanso corto que se descuenta solo y una pausa de comida que el empleado sí ficha.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/GestionTiempoTrabajo/DescuentoAutomaticoDescansos/)

### 5. ¿Sabías que puedes garantizar un descanso mínimo en cada turno?

Si el turno establece una pausa de 20 minutos, pero el empleado solo ficha 10, ¿cuánto descanso debe contar? Con la opción **Establecer parada mínima**, Sebastian HR ajusta el descanso fichado al mínimo que marca el turno.

Como al fichar no se indica si se sale a descansar o por otro motivo, defines una franja alrededor de la hora del descanso. Por ejemplo, si el descanso es a las 10:00 con un margen de 30 minutos, las salidas entre las 9:30 y las 10:30 se tratan como posibles descansos. Si el empleado descansa más de lo previsto, sus fichajes no se tocan.

Y si el empleado no ha fichado ninguna pausa, puedes hacer que el sistema la introduzca automáticamente con el horario del turno, activando la opción **Fichaje automático si no existe parada**.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/GestionTiempoTrabajo/DescansoMinimoTurno/)

### 6. ¿Sabías que puedes cerrar el calendario en temporada alta?

Campaña de Navidad, inventario, cierre fiscal, una auditoría... Hay fechas en las que necesitas a todo el equipo. Con los periodos bloqueados puedes impedir que se soliciten vacaciones o ausencias en esas fechas, y configurar un bloqueo distinto para cada tipo de ausencia.

Cuando un empleado intenta pedir días en un periodo bloqueado, ve un mensaje con el nombre del periodo, sus fechas y el motivo que hayas indicado. Las vacaciones que ya estaban aprobadas se respetan: el bloqueo solo afecta a las solicitudes nuevas.

Tú decides si el bloqueo también impide a los gestores asignar ausencias. Déjalo desmarcado para poder hacer excepciones en temporada alta, o márcalo para cierres en los que no haya excepciones posibles.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/AusenciasVacaciones/BloqueoPeriodosPorAusencia/)

### 7. ¿Sabías que puedes modificar a decenas de empleados de una sola vez?

Una reorganización, un traslado de oficina o un nuevo responsable para todo un equipo no tienen por qué suponer abrir ficha por ficha. Marca los empleados en la lista, abre **Acciones > Modificar datos de empleados** y cambia los datos de todos a la vez.

Puedes actualizar la organización (área, departamento, responsable) y la configuración de fichajes (tipo de gestión de fichajes, si requieren planificación para fichar, ubicación de la oficina, ubicación remota...). Solo se modifican los campos que rellenes; los que dejes vacíos mantienen su valor en cada ficha.

Los cambios se aplican en el momento a todos los empleados seleccionados, así que revisa bien la selección antes de pulsar **Ejecutar proceso**.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/GestionEmpleados/ModificacionMasivaEmpleados/)

### 8. ¿Sabías que puedes saber quién ha leído un comunicado importante?

Un nuevo protocolo, una política interna o un plan de prevención: hay documentos que no basta con publicar, tienes que poder demostrar que cada empleado los ha recibido. Al crear una publicación en Sebastian HR puedes activar la **confirmación de entrega**.

Eliges quién la ve (empleados concretos, áreas, equipos, oficinas o compañías) y cada uno encuentra en su página de inicio un apartado **Para confirmar**. Al pulsar **Confirmar entrega**, queda registrada la fecha de confirmación.

Desde el panel de control ves qué publicaciones tienen confirmaciones pendientes y quién falta por confirmar. Incluso puedes enviar un aviso a un empleado concreto para que lo revise.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/OtrasFuncionalidades/ConfirmacionEntregaYVisibilidad/)

### 9. ¿Sabías que Sebastian HR te avisa antes de que caduque un contrato temporal? **[PRO]**

Un contrato que vence sin que nadie se dé cuenta o un periodo de prueba que termina sin evaluar son sustos que se pueden evitar. Sebastian HR incluye ocho notificaciones configurables para las fechas clave de tu plantilla.

Te avisa de la caducidad de certificados, el fin de contratos temporales, el fin del periodo de prueba, el fin de bajas y excedencias, la caducidad del documento de identidad, los cumpleaños, las incidencias de fichaje y los documentos pendientes de confirmar.

En cada notificación decides con cuántos días de antelación avisar, si se envía por correo, como aviso en la aplicación o de ambas formas, y quién la recibe: gestores del empleado, roles, empleados concretos o cualquier dirección de correo. En algunas notificaciones también puedes avisar al propio empleado.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/OtrasFuncionalidades/ConfiguracionNotificaciones/)

### 10. ¿Sabías que un fichaje guarda dos horas distintas?

Si un empleado de una oficina de Madrid ficha a las 8:00 desde México, ¿qué hora debe constar? Para que la respuesta sea siempre coherente, Sebastian HR guarda dos horas en cada fichaje: la **hora oficial**, en la zona horaria que corresponde al empleado, que usan turnos, cálculos e informes; y la **hora UTC**, el instante real del fichaje, que sirve para auditarlo.

Qué zona horaria se aplica depende del modo que tenga el empleado en su ficha: la de su oficina, la del lugar donde ficha o la de su dispositivo. Así, el personal administrativo mantiene sus horarios oficiales y quien viaja o trabaja en la sede de un cliente ficha con la hora local.

Además, si el reloj del dispositivo difiere en más de 8 minutos del del servidor, el fichaje se marca con la incidencia **Desfase horario dispositivo** para que RRHH lo revise.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/GestionTiempoTrabajo/FichajeConZonasHorarias/)

### 11. ¿Sabías que Sebastian HR no deja fichar a quien no tiene contrato en vigor? **[PRO]**

En modo PRO, cada vez que un empleado ficha, el sistema comprueba que tenga un contrato en vigor ese día. Si no lo tiene, si su contrato discontinuo está interrumpido o si tiene una baja laboral activa, el fichaje se deniega y el empleado ve un mensaje que le remite a su administrador.

Además, desde la ficha de cada empleado puedes activar dos restricciones más: que solo pueda fichar si tiene un turno planificado ese día, y que solo pueda hacerlo dentro de los límites horarios de su turno.

Estas comprobaciones se aplican cuando el propio empleado ficha, desde un ordenador, un móvil o un punto de acceso. No afectan a los fichajes que introduce RRHH a mano ni a los que llegan por integraciones.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/GestionTiempoTrabajo/RestriccionesFichaje/)

### 12. ¿Sabías que las horas extra se liquidan mediante bolsas? **[PRO]**

Desde el registro de tiempo extra puedes agrupar las horas pendientes de cada empleado en una bolsa de horas con un solo clic. La bolsa no está pensada para ir acumulando horas, sino para liquidarlas de una vez.

La gestión se hace en dos pasos. Primero **compensas**: decides cómo se saldan las horas, ya sea con dinero, con tiempo de descanso (en horas o en días) o con un ajuste sin contraprestación. Después **liquidas**: el sistema genera automáticamente los abonos de nómina y suma los días u horas de descanso a los acumulados del empleado.

Si te equivocas, puedes deshacer la liquidación siempre que los abonos no se hayan incluido todavía en una liquidación de nómina.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/GestionTiempoTrabajo/BolsaHoras/)

### 13. ¿Sabías que puedes limitar qué fichas de empleado ve cada usuario? **[PRO]**

En una empresa con varias sedes o departamentos, no todos los responsables necesitan ver a toda la plantilla. Con los ámbitos de visibilidad, cada usuario accede solo a los empleados con los que tiene relación: los de su compañía, los de sus equipos, los de los departamentos que supervisa...

La configuración se basa en la estructura de tu organización: compañía, oficina, departamento, equipo, unidad organizativa o responsable. En el caso del responsable, puedes limitar el acceso a los empleados que dependen directamente de él o extenderlo a toda su jerarquía.

Resulta especialmente útil con el rol **Manager**, pensado para mandos intermedios: les da acceso a los fichajes de su equipo sin abrirles toda la información de RRHH.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/OtrasFuncionalidades/AmbitosVisibilidadEmpleado/)

### 14. ¿Sabías que Sebastian HR se puede conectar con tus otros sistemas?

Tu ERP, una aplicación de fichaje propia, una herramienta de BI o el portal de tu empresa pueden trabajar directamente con los datos de Sebastian HR gracias a su Web API.

La API permite tanto leer como modificar datos: crear empleados, insertar fichajes, aceptar instancias o consultar jornadas y contratos, entre otras operaciones. Las llamadas se hacen mediante peticiones HTTP en JSON, un estándar que cualquier equipo técnico conoce.

Cada integración se identifica con un usuario de Sebastian HR y actúa con sus permisos, así que tú decides a qué datos puede acceder cada conexión.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/Integraciones/WebAPI/)

### 15. ¿Sabías que los informes respetan los filtros de tu lista de empleados?

¿Necesitas un informe solo de una oficina o de un departamento? No hace falta buscar el filtro dentro del informe: filtra primero la lista de empleados, pulsa **Informes** y el Excel o el PDF saldrá solo con esos empleados.

El catálogo cubre la plantilla, el control horario, la planificación, las ausencias y vacaciones, los contratos, las horas extra, la formación y la salud laboral. También incluye los informes de auditoría y cumplimiento para cuando llega una inspección de trabajo, como el libro de registro de horas o el paquete de inspección integral.

Algunos informes solo están disponibles en modo PRO. Los informes de un día o de un periodo concreto se lanzan desde la gestión mensual.

<!-- TODO:enlace: el artículo "Catálogo de informes" todavía no está publicado en ayuda.ahora.es/sebastian-hr/1.0/. Añadir el enlace cuando se publique. -->

### 16. ¿Sabías que una solicitud puede aprobarla cualquiera de sus validadores?

Cuando unas vacaciones o un permiso necesitan la aprobación de varias personas, tú decides cómo avanza la solicitud. Con la opción **Todos los pasos**, la solicitud llega a todos los validadores a la vez y basta con que uno la gestione para aprobarla o denegarla.

Sin esa opción, los pasos se generan en orden: el segundo validador no la recibe hasta que el primero la aprueba y, si alguno la deniega, la solicitud se deniega sin pasar al siguiente.

También puedes decidir qué pasa cuando falta un validador, por ejemplo si el empleado no tiene responsable en su ficha: omitir ese paso o cancelar la solicitud. En la lista de instancias, la etiqueta **AUTO** indica cuáles se han aprobado automáticamente.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/GestionInstancias/FlujosInstancias/)

### 17. ¿Sabías que el empleado ve sus incidencias de fichaje nada más entrar?

Cuanto antes se detecta un fichaje olvidado o mal hecho, más fácil es corregirlo. Por eso, en su página de inicio, el empleado ve en la tarjeta **Mis instancias** un círculo amarillo con el número de incidencias de fichaje que tiene pendientes.

Al pulsarlo se abre la lista de jornadas afectadas, con sus fichajes, las horas trabajadas y la diferencia respecto a lo previsto, para que pueda pedir la corrección a tiempo. Cuenta incidencias como una secuencia de entrada y salida incorrecta o un desfase horario del dispositivo.

Tú decides cuántos días hacia atrás se revisan desde la configuración de la aplicación. Por defecto son los últimos 30 días.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/GestionTiempoTrabajo/IncidenciasDashboard/)

### 18. ¿Sabías que los pluses del contrato llegan solos a la prenómina?

Los suplementos de contrato te permiten registrar los pluses de cada empleado directamente en su contrato. Pueden ser **fijos**, que se pagan siempre, o **condicionales**, que se pagan solo cuando se cumple una condición: trabajar de noche, hacer horas extra validadas o trabajar en festivo.

Al calcular la prenómina, Sebastian HR comprueba las condiciones día a día y convierte cada suplemento en su ajuste de nómina correspondiente. Nadie tiene que contar a mano cuántas noches o festivos ha trabajado cada empleado.

Para que el cálculo sea correcto, las jornadas del periodo deben estar cerradas (en estado BALANCE) antes de generar la prenómina.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/NominasSalarios/SuplementosContrato/)

### 19. ¿Sabías que Sebastian HR tiene dos ediciones, LITE y PRO?

Desde la versión 8.0, Sebastian HR se ofrece en dos ediciones con distinto alcance y licencia, para que cada empresa elija la que se ajusta a lo que necesita.

**LITE** cubre lo esencial: gestión de empleados y fichajes, control de horarios, vacaciones y ausencias, comunicación interna, documentación y firma de documentos. **PRO** incluye todo lo anterior y añade la gestión de horas extra, los contratos, las prenóminas, los contadores y la bolsa de horas, y la planificación avanzada de turnos.

Si tu empresa usa el antiguo Portal Sebastian, LITE es su evolución natural: mantiene sus funcionalidades, las mejora y lo sustituirá progresivamente.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/Versiones/VersionesSebastianHRProLite/)

### 20. ¿Sabías que puedes dar acceso a los documentos por carpetas?

No todos los documentos de la empresa son para todo el mundo: la documentación financiera, los protocolos de un departamento o la información de una sede concreta. Con la visibilidad por categoría defines quién puede ver los documentos de cada carpeta.

Puedes dar acceso por áreas, compañías, oficinas, equipos o a empleados concretos, y combinar varios criterios: basta con cumplir uno de ellos para ver la carpeta. Si no configuras ninguna restricción, la carpeta es visible para todos.

La configuración se aplica en el momento y afecta a todos los documentos de la carpeta, tanto a los que ya contiene como a los que se añadan después. Así no tienes que asignar permisos documento a documento.

[Lee el artículo completo](https://ayuda.ahora.es/sebastian-hr/1.0/OtrasFuncionalidades/VisibilidadDocumentosPorCategoria/)
