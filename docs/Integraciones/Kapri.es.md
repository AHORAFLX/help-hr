# Integración con terminales Kapri (Kimaldi)

Configuración del fichaje mediante terminales **Kapri** de Kimaldi: activación de la integración, alta de terminales y puesta en marcha de los dos modos de identificación disponibles — **QR** y **NFC**.

---

## Conceptos

Un **terminal Kapri** es un dispositivo físico de Kimaldi que identifica al
empleado (leyendo un código QR o una tarjeta NFC) y avisa a Sebastian HR para
que registre el fichaje.

La comunicación es **bidireccional**:

- El terminal avisa a Sebastian HR cada vez que alguien ficha.
- Sebastian HR se conecta al terminal para comprobar que está accesible y para
  mostrar mensajes en su pantalla (por ejemplo, el aviso de bienvenida al
  fichar).

Hay tres interruptores que conviene tener claros porque son **independientes**
entre sí:

| Interruptor | Dónde se ve | Qué controla |
|---|---|---|
| **Activate integration / Disable integration** | Cabecera de la página Kapri | Enciende o apaga toda la integración |
| **QR Clock in** | Cabecera de la página Kapri | Permite fichar mostrando un código QR |
| **NFC Clock in** | Cabecera de la página Kapri | Permite fichar acercando una tarjeta NFC |

!!! warning "Importante"
    Tener la integración activada pero los interruptores QR y NFC apagados significa que el terminal lee la tarjeta o el QR, pero **el fichaje se rechaza** y el empleado ve un mensaje de error en la pantalla del dispositivo.

---

## Cómo llegar a la página de configuración

**Ruta en el menú:** `Integraciones > Kapri` (icono de antena).

![Menú Integraciones > Kapri](images/01-menu-kapri.png)

La página se divide en tres paneles:

| Zona | Contenido |
|---|---|
| Superior | Estado de la integración, interruptores QR y NFC, botón de activar/desactivar |
| Izquierda | Listado de terminales Kapri |
| Derecha | Empleados con tarjeta NFC asignada |

![Vista completa de la página de configuración de Kapri](images/02-pagina-completa.png)

### Si solo ves la cabecera

Es el comportamiento esperado. **Mientras la integración esté desactivada, los
paneles de terminales y de tarjetas NFC no se muestran.** Aparecen en cuanto la
actives (paso siguiente).

![Cabecera con la integración desactivada](images/03-cabecera-desactivada.png)

---

## Activar la integración

En la cabecera de la página, pulsa **«Activate integration»**.

Al activarla:

- El indicador de la cabecera pasa a mostrar **«Integration enabled»**.
- El botón cambia a **«Disable integration»**.
- Aparecen los paneles de terminales y de tarjetas NFC.
- La página se refresca automáticamente.

![Cabecera con la integración activada](images/04-cabecera-activada.png)

> **El botón es un conmutador, no dos botones distintos.** Vuelve a pulsarlo y
> hace exactamente lo contrario: desactiva toda la integración de golpe (los
> terminales dejan de aceptar fichajes). No pide confirmación adicional, así
> que ten cuidado en producción.

Solo un usuario con permisos de administrador puede activar o desactivar la
integración.

---

## Dar de alta un terminal y hacer que funcione

### Crear el terminal en Sebastian HR

En el panel **«Kapri terminals»** pulsa **«New Kapri Terminal»** (o, si la lista
está vacía, **«Add a Kapri terminal»**).

![Formulario de alta de un terminal Kapri](images/05-nuevo-terminal.png)

Rellena los campos del bloque **«Kapri Settings»**:

| Campo | Obligatorio | Qué es |
|---|---|---|
| **Terminal Code** | Sí | Código con el que identificas el terminal en Sebastian HR. Es el que queda grabado en cada fichaje |
| **Description** | No | Texto descriptivo (ubicación, planta…) |
| **Enabled** | Sí | Si lo apagas, el terminal queda dado de alta pero **sus lecturas se rechazan** |
| **IP** | Sí en la práctica | Dirección IP del terminal en la red. Sin ella no se puede probar la conexión ni mostrar mensajes en su pantalla |
| **EUI64** | Sí en la práctica | Identificador único del dispositivo, indicado en la etiqueta o el menú del propio terminal. **Es el dato con el que Sebastian HR reconoce qué terminal le está avisando** |
| **Cloud Token** | Sí en la práctica | Clave compartida con el terminal. Debe escribirse **exactamente igual** que la configurada en el dispositivo |

Aunque el formulario solo exige *Terminal Code* y *Enabled*, sin **IP**,
**EUI64** y **Cloud Token** el terminal no llega a fichar:

- Sin **EUI64**, el aviso que manda el terminal no se puede asociar a ningún
  terminal dado de alta y se descarta.
- Sin **Cloud Token** coincidente, el aviso se rechaza por credenciales.
- Sin **IP**, no hay prueba de conexión ni mensajes en la pantalla del
  terminal.

### Configurar el dispositivo Kapri

En la propia pantalla/menú de administración del terminal:

1. Ponlo en modo **CLOUD**.
2. Configura el **cloud token** con el mismo valor que has escrito en *Cloud
   Token*.
3. Asegúrate de que el terminal es accesible desde el servidor de Sebastian HR
   por red (puerto **9445**).

### Probar la conexión

En la fila del terminal, pulsa el icono de **enchufe** («Test connection»).
Solo aparece si el terminal está *Enabled*; si no lo está, verás en su lugar la
etiqueta gris **«Disabled»**.

![Listado de terminales con el botón de probar conexión](images/06-lista-terminales.png)

La prueba comprueba, en este orden, que: el terminal existe, tiene IP y token
configurados, responde correctamente cuando se le pregunta, su identificador
coincide con el que tienes guardado, y su clave coincide con la tuya.

Si todo va bien recibes el mensaje **«Connection with the Kapri terminal was
successful»** seguido de la descripción del dispositivo.

![Mensaje de conexión correcta](images/07-conexion-correcta.png)

| Mensaje que puedes ver | Causa habitual |
|---|---|
| *This terminal is not configured on Sebastian HR* | El código de terminal no existe |
| *The terminal does not have an IP address configured* | Falta la IP |
| *The terminal does not have a cloud token configured* | Falta el Cloud Token |
| *Could not connect to the Kapri terminal* | Red, firewall o puerto 9445 cerrado |
| *The terminal responded with an error* | El dispositivo contesta pero rechaza la petición |
| *…does not match the configured EUI64* | En esa IP hay otro terminal distinto al que esperabas |
| *The cloud token configured in Sebastian HR does not match the one stored in the terminal* | La clave no coincide entre la aplicación y el dispositivo |

La comparación de la clave **distingue mayúsculas de minúsculas**; la del
identificador del dispositivo no.

---

## Configurar el modo QR

### Activarlo (modo QR)

En la cabecera de la página, activa el interruptor **«QR Clock in»**.

Al activarlo, Sebastian HR genera automáticamente un código QR para cada
empleado, listo para usarse.

Al desactivarlo, esos códigos dejan de estar disponibles.

### Rotación de códigos

Los códigos QR se **renuevan automáticamente cada 30 minutos**. Es una medida
de seguridad: un QR capturado en una foto deja de servir en menos de media
hora.

### Cómo lo usa el empleado

En la pantalla de inicio de la app del empleado, junto al saludo, aparece un
**icono de QR**.

![Icono de QR en la pantalla de inicio del empleado](images/10-icono-qr-empleado.png)

Al pulsarlo se abre el código a pantalla completa, listo para acercarlo al
lector del terminal.

![Código QR del empleado a pantalla completa](images/11-pantalla-qr.png)

El icono **solo se muestra si el empleado tiene un código QR asignado**; si el
modo QR está desactivado, no aparece.

### Limitación conocida: empleados nuevos

La generación de códigos para todos los empleados ocurre **una sola vez**, en
el momento de activar el interruptor. Pasado ese momento, la renovación
automática solo actualiza los códigos de quienes ya lo tenían.

Consecuencia: **un empleado dado de alta después de activar el modo QR no
tendrá código** y no verá el icono. La solución actual es apagar y volver a
encender el interruptor «QR Clock in», lo que regenera los códigos de todos los
empleados (el cambio no tiene impacto práctico, ya que de todas formas rotan
cada 30 minutos).

---

## Configurar el modo NFC

### Activarlo (modo NFC)

En la cabecera, activa el interruptor **«NFC Clock in»**.

A diferencia del QR, **activar NFC no asigna nada automáticamente**: las
tarjetas hay que asignarlas una a una a cada empleado.

### Asignar una tarjeta a un empleado

En el panel derecho **«NFC Employees»**, pulsa **«Configure NFC Card»**.

![Formulario para configurar una tarjeta NFC](images/08-configurar-nfc.png)

El formulario tiene dos campos:

- **Employee** — el empleado al que asignas la tarjeta (obligatorio).
- **NFC UID** — el identificador de la tarjeta.

Para rellenar el identificador tienes dos vías:

**a) Lectura directa (solo en un móvil Android con navegador compatible).** Se
muestra un panel con el texto **«READ NFC — Hold any NFC card or tag near the
reader»**. Acerca la tarjeta al teléfono y el campo se rellena solo.

> Si acercas la tarjeta antes de elegir el empleado, verás el aviso *«You need
> to set the employee first»*. **Selecciona siempre primero el empleado.**

**b) Introducción manual.** En cualquier otro dispositivo verás el aviso **«READ
NFC NOT AVAILABLE»** y tendrás que escribir el identificador a mano (viene
impreso o se puede leer con cualquier lector NFC genérico).

Al guardar, el listado de empleados con NFC se actualiza automáticamente.

### Gestionar tarjetas ya asignadas

El listado de la derecha muestra foto, nombre, área y centro de trabajo de cada
empleado con tarjeta, junto con su identificador.

![Listado de empleados con tarjeta NFC asignada](images/09-lista-nfc.png)

Cada fila ofrece:

- **Clic en la fila** — reabre el formulario para cambiar el identificador.
- **Icono de flechas cruzadas** — traspasa la tarjeta a otro empleado en un
  único paso. Es la forma correcta de reasignar una tarjeta física cuando
  alguien cambia de puesto o causa baja.
- **Icono de papelera** — desvincula la tarjeta de ese empleado.

---

## Qué ve el empleado al fichar

Cuando un empleado se identifica en el terminal (con QR o con tarjeta), el
sistema comprueba, por este orden, que:

1. El terminal que avisa está dado de alta en Sebastian HR.
2. Ese terminal tiene el interruptor **Enabled** activado.
3. La clave que envía el terminal coincide con su **Cloud Token**.
4. El modo usado (QR o NFC) está activado en la cabecera de la página.
5. Existe un empleado con ese código QR o esa tarjeta.

Si alguna comprobación falla, la pantalla del propio terminal muestra un
mensaje de error correspondiente (por ejemplo *«Terminal disabled»*, *«QRs
disabled»*, *«NFCs disabled»* o *«No employee found»*) y el fichaje no se
registra.

Si todo es correcto, la pantalla del terminal muestra **«Welcome»** o **«Bye»**
según corresponda, junto con el nombre del empleado y la hora, y el fichaje
queda registrado.

---

## Lista de verificación

Para dejar un terminal Kapri operativo de principio a fin:

- [ ] Menú `Integraciones > Kapri`
- [ ] Pulsar **«Activate integration»** (aparecen los paneles de terminales y NFC)
- [ ] Crear el terminal con **Terminal Code**, **IP**, **EUI64** y **Cloud Token**
- [ ] Dejar el terminal con **Enabled** activado
- [ ] Configurar el dispositivo en modo **CLOUD**, con el mismo token
- [ ] Verificar el acceso del servidor al terminal por el **puerto 9445**
- [ ] Pulsar el icono de **enchufe** y confirmar *«Connection successful»*
- [ ] Activar **«QR Clock in»** y/o **«NFC Clock in»** según el modo que quieras usar
- [ ] Si usas NFC: asignar tarjetas desde **«Configure NFC Card»**
- [ ] Si usas QR: comprobar que el empleado ve el icono de QR en su pantalla de inicio
- [ ] Fichar una vez de prueba y comprobar que el terminal muestra *«Welcome»*
