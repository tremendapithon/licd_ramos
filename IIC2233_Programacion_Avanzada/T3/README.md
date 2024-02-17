# Tarea 3: DDCachos :school_satchel:


### Cosas implementadas y no implementadas :white_check_mark: :x:


#### Networking: 18 pts (16%)


##### ✅ Protocolo:
Protocolo empleado: TCP y con puerto por default 8080

##### ✅ Correcto uso de sockets:

##### ✅ Conexión
La conexion fue planificada para enviar y recibir mensajes, captando las excepciones necesarias.

##### ✅ Manejo de Clientes:
Se pueden conectar N clientes, cuando se alcanza el maximo de capacidad, se les notifica que estan en la sala de espera o que existe una partida en curso, en caso de que se inicie una.

##### ✅ Desconexión Repentina:
El servidor vota y elimina el cliente que se desconecta repentinamente, tanto para la sala de espera como para la partida.

---

#### Arquitectura Cliente - Servidor: 18 pts (16%)


##### ✅ Roles:
El servidor es el encargado de manejar la partida (aunque se instancia una clase en el server que se encarga de majenar la partida), mientras que el cliente solo envia y recibe mensajes, despues se los comunica al frontend.

##### ✅ Consistencia:
No fue necesario el uso de lock debido que generaba problemas en la comunicacion del cliente - server y se terminaba bloqueando el programa, y la informacion de los clientes se mantiene actualiza en las pestanas de los clientes.

##### ✅ Logs:
Se crea un metodo en el server que se encarga de imprimir en consola cada estado que ocurre en el servidor, como por ejemplo cuando se conecta un cliente, cuando se desconecta, cuando se inicia una partida, etc.

---

#### Manejo de Bytes: 26 pts (22%)


Se implementa todo lo solicitado en la encriptacion e incluso he incluido un test para probrar la codificacion y decodificacion de los bytes, en el archivo ```test_de/codificacion.py``` en la carpeta ```server```, en esta prueba no presento el problema de ```unpickling stack underflow```.

##### ✅ Codificación
##### ✅ Decodificación
##### ✅ Encriptación
##### ✅ Desencriptación

##### ✅ Integración:
Durante la implementacion tenia un error de ```unpickling stack underflow```, pero lo pude manejar con una exepcion y volviendo ejecutar la funcion de recibir_bytes(), evitando que se pierda informacion y que el cliente pueda recibir su informacion. Este problema se ve manifestado cuando el ponderador de N es un multiplo de 10, y hace que no se pueda conectar un 5to cliente, pero lo demas si funciona.

---

#### Interfaz Gráfica: 22 pts (19%)


##### ✅ Ventana de Inicio:
Se visualiza toda la informacion solicitada en el enunciado, y cuando un cliente quiere acceder al server cuando la sala esta llena o existe un partida en curso, este es notificado que espere la siguiente partida. Ademas, cuando se le notifica de que puede entrar, se le manda un pop-up con la opcion de ```volver a intentar```

##### 🟠 Ventana de juego
Se puede visualizar los nombres de los jugadores y estos se van actualizando a medida que se van desconectando.
Tambien se puede visualizar los dados entregados de forma aleatoria, incluso se ha implementado los botones de ```cambiar dados``` y de ```anunciar valor```.
Ademas se puede pasar turno, dudar, y estos cambios se ven reflejados en todos los clientes. Incluso, si un cliente se desconecta y es su turno, el turno del jugador pasara al siguiente jugador.

---

#### Reglas de DCCachos: 22 pts (19%)

##### 🟠 Inicio del juego:
Se le pasa a los usuarios sus dados y se establece quien parte la partida.

##### ❌ Bots:
No implementado.

##### 🟠 Ronda:
SOlo se puede anunciar el valor, con la condicion que este sea estrictamente mayor al valor anterior, y se puede cambiar los dados, pero solo una vez por ronda.

##### ❌ Termino del juego:
No implementado.

---

#### Archivos: 10 pts (9%)

Implementados como lo solicitado en el enunciado.

##### ✅ Parámetros (JSON)
##### ✅ main.py
##### ✅ Cripto.py

---

#### Bonus: 4 décimas máximo
##### ❌ Cheatcodes
##### ❌ Turno con tiempo

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```, el cual se encuentra en las carpetas ```server``` y ```cliente```.
Primero se debe ejecutar el ```main.py``` en la carpeta server para inicializar el servidor y despues se debe ejecutar el ```main.py``` de la carpeta cliente para concectarse e inicar el juego.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```math``` con la funcion ceil
2. ```sys```
3. ```socket```
4. ```threading```
5. ```pickle``` con dumps, loads
6. ```PyQt5```
7. ```os``` con la funcion system, path
8. ```json``` con la funcion load
9. ```time``` con la funcion sleep


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```cripo.py```: Contiene las funciones para encripar y desencriptar.
2. ```funtions.py```: Contiene funciones para la comunicacion y funciones menores
3. ```funtion_json.py```: Contiene la funcion para leer parametros.json

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Como no se especifica como debe ser la sala de espera; la hice de tal forma que cuando un cliente se desconecta, se le va a notificar a todos los clientes que estan en espera la disponibilidad de la sala y de esa manera podran acceder a la sala. Por debajo lo que hago es cerrar el programa, desconectar al cliente en espera y volver a cargar el programa, pero desde el mismo programa que fue cerrado, gracias al modulo ```os.system```.
(Pregunte si podia hacerlo de esa forma en una issue, y me dijieron que si la issue en cuestion es la: <https://github.com/IIC2233/Syllabus/issues/423>)

2. En una parte de la encriptacion y desencriptacion utilizo lo mencionado en la issue #466, en especifico el intercambio de los bytes usando: N % len(msg), por lo que sigo al pie de la letra la encriptacion y desencriptacion del mensaje. Ademas fue algo mencionado en la instancia de una issue.

3. Considerar el error ```unpickling stack underflow``` cuando N es un multiplo de 10 o valores terminados con 8 (algunos casos), en los otros casos no ocurre ningun problema. Ademas he preguntado por el error y aun no lo entiendo e incluso no me han respondido, para que lo pueda tener en cuenta al momento de corregir. Incluso trate de correrlo y ver donde esta el problema, pero se que me esta llegando bien el largo del mensaje y los bytes del mensaje.

-------

## Referencias de código externo :book:

Para realizar mi tarea utilize la base o el esqueleto del servidor del siguiente link:
1. <https://github.com/IIC2233/Syllabus/tree/main/Experiencias/E6>, lo use en la estructura basica del cliente y del server. 



