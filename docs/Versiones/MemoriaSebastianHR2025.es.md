# Memoria Sebastian HR 2025

## Introducción

Este documento recoge las principales funcionalidades y mejoras implementadas en Sebastian HR durante el año 2025.

## Relación de funcionalidades

### Gestión de personal

  - [Aplicación masiva de periodos vacacionales](../AusenciasVacaciones/PeriodosVacacionales.es.md) \- Permite aplicar periodos vacacionales de forma masiva a múltiples empleados, optimizando la gestión de recursos humanos.
  - [Gestión de Ámbitos de visibilidad de empleado](../OtrasFuncionalidades/AmbitosVisibilidadEmpleado.es.md) \- Control granular sobre qué información pueden visualizar diferentes perfiles de usuarios. Nuevo rol “Manager”
  - Equipos "Privados" \- Funcionalidad para crear y gestionar equipos con acceso restringido.
  - [Contadores de horas de empleados](../GestionTiempoTrabajo/ContadoresHoras.es.md) \- Sistema de seguimiento y contabilización de horas trabajadas por empleado en distintos tipos de contadores.
  - [Cuadrantes de Empleados](../GestionTiempoTrabajo/Cuadrantes.es.md) \- Herramienta visual para el cálculo y control del tiempo de empleados.
  - [Gestión de Usuarios y procesos masivos](../OtrasFuncionalidades/GestionUsuariosYEmpleados.es.md) \- Capacidad para realizar operaciones masivas sobre múltiples usuarios simultáneamente.
  - Periodo de prueba en contratos \- Gestión específica para el seguimiento de periodos de prueba contractuales.
  - [Control de incidencias del empleado en su dashboard](../GestionTiempoTrabajo/IncidenciasDashboard.es.md) \- Panel personalizado donde cada empleado puede visualizar sus propias incidencias de fichajes.
  - [Modificación Masiva de Datos de Empleados](../GestionEmpleados/ModificacionMasivaEmpleados.es.md) \- Permite actualizar información de múltiples empleados simultáneamente
  - Bloqueo de periodos por tipo de ausencia/vacaciones: Permite definir periodos por tipo de ausencia en los que no se pueden solicitar y/o insertar ausencias o vacaciones. Ver [Bloqueo de periodos por tipo de Ausencia](../AusenciasVacaciones/BloqueoPeriodosPorAusencia.es.md)

### Control de fichajes y jornadas

  - [Restricciones de fichaje](../GestionTiempoTrabajo/RestriccionesFichaje.es.md) \- Sistema de reglas para limitar y controlar los fichajes según criterios establecidos.
  - [Nuevo cálculo de asignación de fichaje a jornada (doble parámetro)](../GestionTiempoTrabajo/GuiaDateJourneyAsignacionTurno.es.md)
  \- Algoritmo mejorado que utiliza dos parámetros para una asignación más precisa.
  - [Reglas de Control de Localizaciones (teletrabajo)](../GestionTiempoTrabajo/ReglasControlLocalizaciones.es.md) \- Gestión y validación de fichajes remotos y control de trabajo a distancia.
  - Mejoras en la gestión de jornadas para realizar acciones masivas (ausencias no planificadas) \- Herramientas optimizadas para gestionar múltiples ausencias de forma eficiente.

### Vacaciones y descansos

  - [Vacaciones por Horas](../GestionTiempoTrabajo/HorasVacaciones.es.md) \- Sistema flexible que permite gestionar las vacaciones en unidades horarias en lugar de días completos.
  - Paradas incluidas/no incluidas en jornada \- Configuración para determinar qué paradas computan como tiempo de trabajo efectivo. (Ver [Descansos remunerados](../GestionTiempoTrabajo/DescansosRemunerados.es.md))
  - [Descansos remunerados](../GestionTiempoTrabajo/DescansosRemunerados.es.md) \- Gestión específica de descansos que forman parte del tiempo retribuido.

### Turnos y horarios

  - [Procesos de Reasignación automática de turnos](../GestionTiempoTrabajo/ReasignacionAutomaticaTurnos.es.md) \- Sistema inteligente que redistribuye automáticamente los turnos según la jornada realizada.
  - Poder establecer varios precios de hora extras, según las reglas establecidas \- Configuración flexible de tarifas diferenciadas para horas extraordinarias. (ver [Tipo Salarios y cálculos de precios por tipo horas.](../NominasSalarios/TipoSalarioCalculoPrecioHoras.es.md) y [Gestión de tiempo extra](../GestionTiempoTrabajo/GestionTiempoExtra.es.md))

### Documentación y notificaciones

  - [Documentación: confirmación de entrega y visibilidad](../OtrasFuncionalidades/ConfirmacionEntregaYVisibilidad.es.md) \- Sistema de trazabilidad para documentos corporativos con confirmación de recepción.
  - [Configurar visibilidad de documentos por categoría de documento.](../OtrasFuncionalidades/VisibilidadDocumentosPorCategoria.es.md) Permite configurar qué empleados, oficinas, empresas, áreas o equipos pueden visualizar los documentos almacenados en una categoría o carpeta específica
  - [Documentos de empleados/as y ABH Sign](../OtrasFuncionalidades/DocumentosEmpleadosABHSign.es.md) \- Integración con sistema de firma electrónica para documentación laboral.
  - [Gestión de avisos y notificaciones](../OtrasFuncionalidades/ConfiguracionNotificaciones.es.md) \- Herramienta completa para la comunicación interna mediante avisos personalizables.
  - [Separación inteligente de PDFs](../OtrasFuncionalidades/SeparacionInteligentePDFs.es.md) \- permite procesar de forma automatizada un único documento PDF que contenga múltiples nóminas, o cualquier otro tipo de documento que incluya el DNI del empleado.
  - [Asistente IA Tally para Introducción de Gastos](../NominasSalarios/AsistenteIATallyGastos.es.md) \- Agente IA que facilita la introducción de partes de gastos en el sistema.

### Contratos y suplementos

  - [Suplementos condicionales de contrato](../NominasSalarios/SuplementosContrato.es.md) \- Gestión de complementos salariales variables según condiciones específicas.

### Integraciones y herramientas

  - Mejoras en la integración con ERP AHORA \- Optimización de la sincronización y transferencia de datos con el sistema ERP.
  - Importar documentos en formato A3NOM \- Capacidad de importación de archivos en formato estándar de nóminas A3.
  - Paquete Listados Excel para colección empleados \- Conjunto de plantillas Excel predefinidas para exportación de datos.
  - Sebastian PRO vs LITE \- Diferenciación de funcionalidades entre las versiones profesional y básica del producto.

### Gestión de instancias

  - [Solicitudes con flujos de aprobación](../GestionInstancias/SolicitudesFlujosAprobacion.es.md) \- Permite establecer flujos de aprobación sobre los tipos de solicitud que se establezcan en la aplicación.
  - [Mejoras en la gestión de instancias incluyendo nuevos casos de uso](../GestionInstancias/FlujosInstancias.es.md) \- Ampliación del sistema de workflows para contemplar escenarios adicionales, como la gestión cuando no existen validadores asignados.
