# Gestión de creación y bloqueo de usuarios y empleados

Este artículo describe las acciones disponibles para la creación automática de usuarios y el bloqueo de usuarios y empleados según su estado. Las funcionalidades varían ligeramente entre los modos PRO y LITE , destacando algunas opciones exclusivas del modo PRO.

 

### 1\. Creación de usuarios

###  ¿Desde dónde se puede hacer?

  * Desde la lista de empleados (Solo modo PRO)  
Menú: `Acciones > Crear usuarios`  
Se crean usuarios únicamente para los empleados filtrados en la lista que no tengan ya un usuario asignado.

  * Desde la lista de usuarios  
Menú: `Acciones > Crear usuarios`

    * En modo PRO : Se crean usuarios para todos los empleados activos que aún no tengan usuario.

    * En modo LITE : Se crean usuarios para todos los empleados sin usuario , sin importar su estado.

### Valores por defecto

Los usuarios generados heredan los siguientes valores por defecto:

  * Rol : `Users`

  * Idioma : El idioma del usuario que ejecuta la acción

  * Área : Sin definir

  * Perfil : `default`

### Parámetros configurables

Antes de ejecutar el proceso, se debe seleccionar la lógica de generación del nombre de usuario (username) :

  * Correo electrónico

  * DNI

  * Patrón compuesto (basado en nombre y apellidos) :+  
Se prueba secuencialmente hasta encontrar un username libre. Los patrones son:

  * napellido1  
noapellido1 
  * napellido1apellido2 
  * noapellido1apellido2 
  * nomapellido1apellido2

>  _Ejemplo:_ Para Noelia Álvarez Gómez , los intentos serían: `nalvarez`, `noalvarez`, `nalvarezgomez`, etc.



### 2\. Bloqueo de usuarios de empleados bloqueados

  * Desde la lista de empleados (Solo modo PRO)  
Menú: `Acciones > Bloquear usuarios de empleados bloqueados`

  * Desde la lista de usuarios  
Menú: `Acciones > Bloquear usuarios de empleados bloqueados`

Esta acción bloquea los usuarios vinculados a empleados que tengan activado el check de bloqueo en su ficha.


### 3\. Bloqueo de usuarios de empleados inactivos (Solo modo PRO)

  * Desde la lista de empleados  
Menú: `Acciones > Bloquear usuarios de empleados inactivos`

  * Desde la lista de usuarios  
Menú: `Acciones > Bloquear usuarios de empleados inactivos`

Se bloquean los usuarios de empleados que no tengan ningún contrato activo en la actualidad.



### 4\. Bloqueo de empleados inactivos (Solo modo PRO)

Menú: `Acciones > Bloquear empleados inactivos`

  

Esta acción bloquea directamente a los empleados que no tienen contrato activo , independientemente de su estado anterior.