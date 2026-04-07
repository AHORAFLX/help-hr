# Requisitos recomendados para la Instalación de Sebastian HR

Para asegurar un rendimiento óptimo y una experiencia fluida en el uso de Sebastian HR , es esencial contar con una infraestructura adecuada. A continuación, se describen las configuraciones recomendadas según el volumen de usuarios: 

###   

### Menos de 100 Usuarios

Para instalaciones con menos de 100 usuarios, se deben seguir [los mínimos necesarios para una instalación de flexy go](Requisitos recomendados para la Instalación de Sebastian HR.md)/Requisitos%20mínimos.md).

 

### Entre 100 y 300 Usuarios

Para instalaciones de mayor alcance, se recomienda una configuración que soporte el incremento de carga de trabajo y volumen de datos. En este caso, se deben considerar las siguientes especificaciones:

### Servidor SQL

  

El servidor de base de datos SQL debe estar preparado para manejar una carga significativa de operaciones y almacenar un volumen considerable de información. Por ello, se recomienda:

  * Windows Sever 2016 Standard o superior.
  * Versión de SQL: Estándar o Enterprise, 2016 o superior.
  * Memoria RAM: 24 GB.
  * Procesador: 6 u 8 núcleos (cores) para garantizar la capacidad de respuesta.
  * Espacio de disco: 500 GB iniciales, dependiendo del tamaño de la base de datos. Este espacio puede ampliarse en función del crecimiento del sistema.

  

### Servidor IIS

  

El servidor encargado de gestionar las solicitudes de los usuarios y alojar el sistema requiere características similares para mantener un buen rendimiento:

  * Windows Sever 2016 Standard o superior.
  * Memoria RAM: 20 GB.
  * Procesador: 6 núcleos (cores).
  * Espacio de disco: 500 GB. Si se manejan numerosos documentos, imágenes u otros archivos, será necesario planificar ampliaciones en el almacenamiento.

  

Nota: Los valores indicados son una estimación a la alza para garantizar que los recursos sean suficientes en el tiempo y no se queden cortos ante incrementos de carga o crecimiento del sistema. 

Sin embargo, se sugiere monitorizar el uso de recursos una vez implementado el sistema y ajustar según las necesidades reales.

  

 

### Más de 300 Usuarios

Para instalaciones con más de 300 usuarios, se sugiere:

  * Empezar con las configuraciones recomendadas para el rango de 100 a 300 usuarios.
  * Monitorizar continuamente el uso de recursos, como memoria, procesador y almacenamiento.
  * Escalar la infraestructura conforme aumente la carga de trabajo, añadiendo más recursos si es necesario.

  

 

### Distribución en Dos Servidores

En escenarios con un volumen elevado de usuarios simultáneos, es recomendable separar las cargas en dos servidores distintos:

  

  1. Servidor SQL para la gestión de datos.
  2. Servidor IIS para las operaciones y la interfaz del usuario.

  

Esta configuración mejora el rendimiento, reduce los tiempos de respuesta y evita cuellos de botella en la comunicación entre componentes.

  

 

### Documentación adicional

[FLEXYGO SQL Install Server](https://www.youtube.com/watch?v=ttcadOncjAM)

[FLEXYGO IIS Install server](https://www.youtube.com/watch?v=fFKLuk1N4e4)

[Sugerencias para optimización del IIS](https://help.flexygo.com/support/solutions/articles/154000157271-sugerencias-para-optimizaci%C3%B3n-del-iis)