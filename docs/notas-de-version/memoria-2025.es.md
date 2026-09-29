# Memoria Sebastian HR 2025

## Introducción

Este documento recoge las principales funcionalidades y mejoras implementadas en Sebastian HR durante el año 2025.

## Relación de funcionalidades

### Gestión de personal

- [Aplicación masiva de periodos vacacionales](../ausencias-y-vacaciones/periodos-vacacionales.es.md): Permite aplicar periodos vacacionales de forma masiva a múltiples empleados, optimizando la gestión de recursos humanos.
- [Gestión de Ámbitos de visibilidad de empleado](../empleados-y-organizacion/ambitos-de-visibilidad.es.md): Control granular sobre qué información pueden visualizar diferentes perfiles de usuarios. Nuevo rol "Manager"
- Equipos "Privados": Funcionalidad para crear y gestionar equipos con acceso restringido.
- [Contadores de horas de empleados](../horas/contadores-de-horas.es.md): Sistema de seguimiento y contabilización de horas trabajadas por empleado en distintos tipos de contadores.
- [Cuadrantes de Empleados](../turnos-y-planificacion/cuadrantes.es.md): Herramienta visual para el cálculo y control del tiempo de empleados.
- [Gestión de Usuarios y procesos masivos](../empleados-y-organizacion/usuarios-de-empleados.es.md): Capacidad para realizar operaciones masivas sobre múltiples usuarios simultáneamente.
- Periodo de prueba en contratos: Gestión específica para el seguimiento de periodos de prueba contractuales.
- [Control de incidencias del empleado en su dashboard](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/incidencias-en-el-dashboard.es.md): Panel personalizado donde cada empleado puede visualizar sus propias incidencias de fichajes.
- [Modificación Masiva de Datos de Empleados](../empleados-y-organizacion/modificacion-masiva-de-empleados.es.md): Permite actualizar información de múltiples empleados simultáneamente
- Bloqueo de periodos por tipo de ausencia/vacaciones: Permite definir periodos por tipo de ausencia en los que no se pueden solicitar y/o insertar ausencias o vacaciones. Ver [Bloqueo de periodos por tipo de Ausencia](../ausencias-y-vacaciones/bloqueo-de-periodos.es.md)

### Control de fichajes y jornadas

- [Restricciones de fichaje](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/restricciones-de-fichaje.es.md): Sistema de reglas para limitar y controlar los fichajes según criterios establecidos.
- [Nuevo cálculo de asignación de fichaje a jornada (doble parámetro)](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/asignacion-de-turno-y-fecha-de-jornada.es.md): Algoritmo mejorado que utiliza dos parámetros para una asignación más precisa.
- [Reglas de Control de Localizaciones (teletrabajo)](../fichajes-y-jornadas/gestion-de-fichajes-y-jornadas/reglas-de-control-de-localizaciones.es.md): Gestión y validación de fichajes remotos y control de trabajo a distancia.
- Mejoras en la gestión de jornadas para realizar acciones masivas (ausencias no planificadas): Herramientas optimizadas para gestionar múltiples ausencias de forma eficiente.

### Vacaciones y descansos

- [Vacaciones por Horas](../horas/horas-de-vacaciones.es.md): Sistema flexible que permite gestionar las vacaciones en unidades horarias en lugar de días completos.
- Paradas incluidas/no incluidas en jornada: Configuración para determinar qué paradas computan como tiempo de trabajo efectivo. (Ver [Descansos remunerados](../turnos-y-planificacion/descansos-remunerados.es.md))
- [Descansos remunerados](../turnos-y-planificacion/descansos-remunerados.es.md): Gestión específica de descansos que forman parte del tiempo retribuido.

### Turnos y horarios

- [Procesos de Reasignación automática de turnos](../turnos-y-planificacion/reasignacion-automatica-de-turnos.es.md): Sistema inteligente que redistribuye automáticamente los turnos según la jornada realizada.
- Poder establecer varios precios de hora extras, según las reglas establecidas: Configuración flexible de tarifas diferenciadas para horas extraordinarias. (ver [Tipo Salarios y cálculos de precios por tipo horas.](../nominas/salarios-y-precios-de-hora.es.md) y [Gestión de tiempo extra](../horas/gestion-de-tiempo-extra.es.md))

### Documentación y notificaciones

- [Documentación: confirmación de entrega y visibilidad](../documentos-y-comunicacion/confirmacion-de-entrega.es.md): Sistema de trazabilidad para documentos corporativos con confirmación de recepción.
- [Configurar visibilidad de documentos por categoría de documento.](../documentos-y-comunicacion/visibilidad-de-documentos-por-categoria.es.md): Permite configurar qué empleados, oficinas, empresas, áreas o equipos pueden visualizar los documentos almacenados en una categoría o carpeta específica
- [Documentos de empleados/as y ABH Sign](../documentos-y-comunicacion/documentos-y-abh-sign.es.md): Integración con sistema de firma electrónica para documentación laboral.
- [Gestión de avisos y notificaciones](../documentos-y-comunicacion/configuracion-de-notificaciones.es.md): Herramienta completa para la comunicación interna mediante avisos personalizables.
- [Separación inteligente de PDFs](../documentos-y-comunicacion/separacion-inteligente-de-pdfs.es.md): permite procesar de forma automatizada un único documento PDF que contenga múltiples nóminas, o cualquier otro tipo de documento que incluya el DNI del empleado.
- [Asistente IA Tally para Introducción de Gastos](https://ayuda.ahora.es/sebastian-hr-empleados/reservas-viajes-y-gastos/asistente-ia-tally-gastos/): Agente IA que facilita la introducción de partes de gastos en el sistema.

### Contratos y suplementos

- [Suplementos condicionales de contrato](../contratos-y-convenios/suplementos-de-contrato.es.md): Gestión de complementos salariales variables según condiciones específicas.

### Integraciones y herramientas

- Mejoras en la integración con ERP AHORA: Optimización de la sincronización y transferencia de datos con el sistema ERP.
- Importar documentos en formato A3NOM: Capacidad de importación de archivos en formato estándar de nóminas A3.
- Paquete Listados Excel para colección empleados: Conjunto de plantillas Excel predefinidas para exportación de datos.
- Sebastian PRO vs LITE: Diferenciación de funcionalidades entre las versiones profesional y básica del producto.

### Gestión de instancias

- [Solicitudes con flujos de aprobación](../solicitudes-e-instancias/solicitudes-con-flujos-de-aprobacion.es.md): Permite establecer flujos de aprobación sobre los tipos de solicitud que se establezcan en la aplicación.
- [Mejoras en la gestión de instancias incluyendo nuevos casos de uso](../solicitudes-e-instancias/flujos-de-aprobacion.es.md): Ampliación del sistema de workflows para contemplar escenarios adicionales, como la gestión cuando no existen validadores asignados.
