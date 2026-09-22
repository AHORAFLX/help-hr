# Creación y bloqueo de usuarios y empleados

Este artículo describe las acciones disponibles para la creación automática de usuarios y el bloqueo de usuarios y empleados según su estado. Las funcionalidades varían ligeramente entre los modos PRO y LITE, destacando algunas opciones exclusivas del modo PRO.

## Creación de usuarios

### ¿Desde dónde se puede hacer?

- Desde la lista de usuarios:  
`Acciones > Crear usuarios`

    - En modo **PRO**: Se crean usuarios para todos los empleados activos que aún no tengan usuario.

    - En modo **LITE**: Se crean usuarios para todos los empleados sin usuario, sin importar su estado.

- <span class="fh-version-tag hr-pro-mode no-margin margin-right-s" title="Disponible en modo pro">Pro</span>Desde la lista de empleados  
`Acciones > Crear usuarios`  
Se crean usuarios únicamente para los empleados filtrados en la lista que no tengan ya un usuario asignado.

### Valores por defecto

Los usuarios generados heredan los siguientes valores por defecto:

| Campo | Valor por defecto |
| --- | --- |
| Rol | `Users` |
| Idioma | El idioma del usuario que ejecuta la acción |
| Área | Sin definir |
| Perfil | `default` |

### Elección de nombres

Antes de ejecutar el proceso, se debe seleccionar la lógica de generación del nombre de usuario (username).

En esta se puede elegir entre tres opciones que serán las encargadas de asignarles este:

  - Correo electrónico
  - DNI
  - Un patrón compuesto (basado en nombre y apellidos):+  
Se prueba secuencialmente hasta encontrar un username libre. Los patrones son:

      - napellido1  
    noapellido1 
      - napellido1apellido2 
      - noapellido1apellido2 
      - nomapellido1apellido2

!!! example "Ejemplo"
    Para Noelia Álvarez Gómez, los intentos serían: `nalvarez`, `noalvarez`, `nalvarezgomez`, etc.

## Bloqueo de usuarios de empleados bloqueados

  - Desde la lista de usuarios  
 `Acciones > Bloquear usuarios de empleados bloqueados`
 
  - <span class="fh-version-tag hr-pro-mode no-margin margin-right-s" title="Disponible en modo pro">Pro</span>Desde la lista de empleados  
 `Acciones > Bloquear usuarios de empleados bloqueados`


Esta acción bloquea los usuarios vinculados a empleados que tengan activado el check de bloqueo en su ficha.

## Bloqueo de usuarios de empleados inactivos <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span>

  - Desde la lista de empleados  
`Acciones > Bloquear usuarios de empleados inactivos`

  - Desde la lista de usuarios   
`Acciones > Bloquear usuarios de empleados inactivos`

Se bloquean los usuarios de empleados que no tengan ningún contrato activo en la actualidad.

## Bloqueo de empleados inactivos <span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span>

Navega a:  
`Acciones > Bloquear empleados inactivos`

Esta acción bloquea directamente a los empleados que no tienen contrato activo, independientemente de su estado anterior.
