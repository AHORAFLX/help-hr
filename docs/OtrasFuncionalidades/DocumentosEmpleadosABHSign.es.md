# Documentos de empleados y ABH Sign

En Sebastian HR, el equipo de recursos humanos tiene la capacidad de gestionar documentos de manera eficiente, permitiendo subir archivos de forma masiva y enlazarlos con los/las empleados/as correspondientes.

## Cómo Vincular Documentos a Empleados/as

Para empezar, dirígete a la lista de empleados/as. Desde allí, selecciona "Acciones" y luego "Documentos de empleados/as". Esto te llevará a la página de gestión de documentos, donde podrás subir y vincular archivos.

![](../docs_assets/images/95MoH7CwdnCfAX5cozXCpByNlRqLEb4MeA.png)

## Subida y Vinculación de Documentos

Para subir documentos, haz clic en "Acciones" y elige "Agregar documentos". Esto abrirá el gestor de documentos, donde podrás arrastrar y soltar los archivos que necesites.

![](../docs_assets/images/HhFbtF13kgAWmEytuj99S_qkIEAvXxAm2A.png)

Asegúrate de que los nombres de los documentos cumplan con los parámetros necesarios para que el sistema pueda identificar correctamente a los/las empleados/as.

![](../docs_assets/images/VjjyI4k8p3bqha8ohebUv0OcNKPVYv0-RA.png)

Una vez que los documentos se hayan subido, se habilitarán varias opciones en el menú "Acciones". Selecciona los documentos que deseas vincular y haz clic en "Enlazar seleccionados".

![](../docs_assets/images/4TAyfLl-VFTkseC29ydxUQ4uUZGh6NF3ng.png)

Durante este proceso, deberás asignar un nombre y una fecha que se aplicarán a todos los documentos enlazados, seleccionar la categoría de la gestión documental y elegir uno de los modos de vinculación (Id, nombre o DNI).

![](../docs_assets/images/NRs6FdedOzqMR0Xgi34L0JCXZ6kvOAv_dw.png)  

Los documentos que se enlacen correctamente desaparecerán de la lista y estarán disponibles en la página del/de la empleado/a para su descarga.

Si algún documento no se puede vincular, el sistema mostrará un mensaje indicando el motivo del error.

![](../docs_assets/images/1ITNwleTdGEgJG_9nC6O2AxWwVC6osi0IQ.png)

## Firma con ABH Sign

Además de vincular documentos, existe la posibilidad de enviarlos para su firma a través de ABH Sign. Para ello, en el proceso para vincular los documentos, marcaremos la opción "Enviar para firmar".

![](../docs_assets/images/qfVHkcc5UYNaGbMYfXbIWt8_8-xSUnYB4g.png)  

Para utilizar este servicio, es necesario cumplir con los siguientes requisitos:

  * Tener contratado el servicio ABH Sign.
  * Configurar ABH Sign para el objeto empleados/as y las categorías correspondientes.
    * Al configurar los reports/categorías, el proceso del campo AfterProcess debe ser `HR_AfterSignEmployeesDocuments`![](../docs_assets/images/_1KPF165eQLTf-MWQ6c18PtcVLQs-4Papw.png)
  * Disponer de suficientes créditos para enviar los documentos a firmar.
  * Asegurarte de que los/las empleados/as tengan registrado un correo electrónico y un número de teléfono válidos.
  * Los documentos deben estar en formato PDF.
  * Para que el check "Enviar para firmar" esté activo, se tiene que tener configurada la categoría seleccionada en el proceso.![](../docs_assets/images/f5juhlhrYHp4yTqKdNJHAiz-44ML7Jnu9g.png)

Al enviar documentos para firmar, el documento original se vincula a la gestión documental del/de la empleado/a y, simultáneamente, se envía un correo electrónico al/a la empleado/a con acceso al documento en la plataforma de firma.

Una vez que el/la empleado/a firma el documento, el original se elimina de la gestión documental y se reemplaza por el documento firmado.

!!! warning "Importante"
    Asegúrate de que los Cron Job `GetPendingAbhSigns` y `ClearAbhSign` están activos, ya que se encargan de recorrer los documentos pendientes y comprobar si se han firmado, y de actualizar los documentos caducados.

## Múltiples firmas en un documento

Un documento puede llevar asociadas varias firmas. Para ello, necesitaremos hacer las siguientes configuraciones:

![](../docs_assets/images/rZrA4FKqs7TE_YSk-v4fJL7me-zTpXdV2A.png)

## Espacios de firma

![](../docs_assets/images/acj2OlYXOvJFAncDpBi9oql2aO24d7PfJg.png)

Cada firma debe tener un espacio asignado en el documento. Desde el botón se abre un asistente en el que se puede subir un documento de ejemplo y seleccionar el espacio para la firma.

![](../docs_assets/images/E0uUBm_kiTMCJNM3pM-e6V1l1E5ExEuEKA.png)  

## Configuración de los firmantes![](../docs_assets/images/Epy89oXvWx0LZh38Wd0-G7FB8SJkM31GrA.png)

Para cada espacio de firma, debe indicarse quién será el firmante. Las opciones disponibles son:

  * Jefe del departamento del empleado
  * Un empleado concreto
  * Responsable del empleado
  * Líder del grupo del empleado (solo disponible en HR PRO)
  * Supervisor del grupo del empleado (solo disponible en HR PRO)
  * Otro: Se puede especificar un correo electrónico y un teléfono, aunque no estén asociados a un empleado.

Además, se debe indicar el comportamiento del proceso en caso de que no se encuentre alguno de los firmantes o que no tenga email o teléfono:

  * Enviar de todas formas, omitiendo al firmante que falta.
  * No enviar el documento si no se puede completar la lista de firmantes.
   ![](../docs_assets/images/qIaPpKwf7KDb5dqvs_51ekTGzcxjt3WYTQ.png)

## Firmante principal

El Firmante n.º 1 es siempre el propietario del documento. Para este firmante no es necesario realizar ninguna configuración adicional.

## Finalización del proceso

El documento se considera firmado cuando todos los firmantes han completado su firma. En ese momento:

  * Se ejecuta una sola vez el proceso definido en el campo AfterSign.
  * Se guarda un único documento firmado y un único documento de evidencias con todas las firmas registradas.

## Evidencias de la Firma

Junto con el documento firmado, se genera un documento de evidencias que cumple con los requisitos necesarios para garantizar la validez de la firma. Este documento de evidencias también se añade a la gestión documental del/de la empleado/a.

![](../docs_assets/images/KjVPtgcmDYsahefxWsGd3weSQgxzb6G-KA.png)

## Ver el Estado de la Firma

Puedes verificar el estado de la firma en el sistema, asegurándote de que todos los documentos hayan sido firmados correctamente en el menú de mantenimiento / Documentos de empleados / Documentos enviados para firmar.

![](../docs_assets/images/kF-qezNB7m30neRVel7JLXnnms8Vk5MJSw.png)

## Seguridad aplicada a los documentos

  * Los roles de RRHH pueden ver los documentos de todos los empleados.
  * El resto de roles (users y admin) únicamente pueden ver sus propios documentos.
