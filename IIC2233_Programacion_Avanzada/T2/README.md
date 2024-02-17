# Tarea 2: DCCazafantasmas 👻🧱🔥


## Consideraciones generales :octocat:

<Mi programa hace gran parte de lo solicitado en el enunciado de la tarea, incluso lo he testeado multiples veces viendo si tiene algun error en su ejecucion, sin embargo no me ha dado ningun error grave. Ademas como consideracion al momento de probar la ventana de juego, se debe considerar que los estados o acciones no validas por parte del usuario seran mostradas en el recuadro de la parte superior de la ventana de juego (el recuadro esta acompanado con la leyenda de "Estado").>


-------


## Ventanas: 27 pts (27%)


#### ✅ Ventana de Inicio:

La ventana de inicio cumple con todo lo solicitado en el enunciado de tarea, ya que verifica las condiciones para que el nombre de usuario sea valido, ademas se encarga de determinar si el usuario va ejecutar un mapa o va crear uno propio. Si el usuario selecciona una opcion distinta a "crear mapa", se va desplejar el modo de juego, pero en cambio si el usuario selecciona la opcion de "crear mapa", el usuario podra crear su propio mapa y ser capaz de jugarlo presionando el boton "JUGAR". (Por debajo las ventanas del modo constructor y la del modo de jego son distintas, pero se conectan a traves del ```main.py```)


#### ✅ Ventana de Juego:

La ventana de juego cumple con todo lo solicitado en el enunciado, aunque quiero mencionar que la ventana de juego se separo en dos ventanas aparte, la ventana del modo constructor y la de juego (ambas en la carpeta ```frontend```). Cada una de las ventanas se ejecutan de forma independiente, pero son conectadas a traves del ```main.py```. 
Ademas se agregaron los botones de pausa (pausa la partida cortando las senales entre el ```frontend_juego.py``` y el ```backend_juego.py```) y el boton de salir (cierra el juego). 


-------


## Mecánicas de juego: 47 pts (47%)


#### ✅ Luigi:

Las mecanicas de luigi han sido implementadas con todo lo solicitado en el enunciado, aunque es importante aclarar que el movimiento de luigi es ```continuo, si se deja presionada una tecla, luigi se movera en esa direccion hasta que se presione otra tecla o en su defecto dejar de pulsarla```, lo anterior es un punto importante al momento de recorregir, ademas su velocidad puede ser ajustada con un parametro en el archivo ```parametros.py```, llamado ```AJUSTAR_VELOCIDAD```, el cual es un ```float``` que idealmente debe ser menor a 0.5.
Ademas cuando luigi toca un emigo, este sera devuelto al punto en el que partio (punto de inicio) y se le restara una vida (por detras una property se encarga de verificar que la vida de luigi sea menor a 0, todo este calculo lo hago en el backend, aunque hay una property de la vida en el frontend que solamente se encarga de mostrar el pop-up de que se perdio la partida).
Sin embargo no unico no implementado es cuando el luigi pierde todas las vidas se transforma en un fantasma.


#### ❌ Fantasmas:
No se ha implementado nada de los fantasmas, sin embargo cuando luigi choca con uno de ellos, luigi pierde una vida.

#### ✅ Modo Constructor:

El modo constructor cumple con todo lo solicitado en el enunciado, ya que se actualiza en tiempo real cuando se establecen las entidades en el mapa de juego. Ademas cuando se presiona el boton iniciar juego en el modo constructor, la ventana del modo constructor se cierra (.hide()) y se muestra la ventana de juego con el mapa creado en la ventana anterior.

Otro apartado ha recalcar es que cuando el usuario selecciona una entidad o un bloque, este aparece como seleccionado en la parte de arriba de la ventana (en una casilla), ademas se muestra el estado si este se puede agregar o no.

-> Si no se puede agregar es porque la casilla que se intento seleccionar estaba ocupada o era un bordermap. En este caso, se debe volver a intentar agregar el elemento en una casilla distinta.

#### ✅ Fin de ronda:

Cuando se finaliza la ronda, se muestra la razon por que se perdio y se despliega las opciones de volver a jugar (bonus) que te manda a la ventana de inicio para que puedas iniciar otra vez un juego nuevo o la opcion de salir, que simplemente cierra el programa. Por debajo existe un metodo en el frontend que resetea todo el mapa y le avisa al backend que se debe resetear el mapa, ademas de que se debe resetear la vida de luigi y la cantidad de enemigos que se han eliminado.
Sin embargo, cuando luigi pierde todas las vidas no se transforma en un fantasma.

-------


## Interacción con el usuario: 14 pts (14%)


#### ✅ Clicks:

Todos los del usuario son procesados en la ventana juego en el modo constructor.

#### 🟠 Animaciones:

No se cumple con todas las animaciones como lo solicitan, sin embargo cuando el luigi se mueve a traves del mapa su animacion va cambiando. Por lo que este punto lo he dejado a medio completar, pero a pesar de ello la animacion del personaje se actualiza cada vez que luigi se mueve.


-------


## Funcionalidades con el teclado: 8 pts (8%)


#### ✅ Pausa:

El boton de pausa funciona correctamente, sin embargo solo funciona cuando se pulsa solo una vez, es decir, se puso como condicion el metodo ```isAutoRepeat().```

#### ✅ K + I + L:

El cheatcode funciona como se solicita, y este debe ser precionado en orden, es decir, tecla por tecla para que sea efectivo el cheatcode, ademas por debajo el programa elimina todos los enemigos del mapa (de una lista de listas). Y se notifica al usuario en la ventana de juego que se uso el cheatcode en la parte superior de la ventana.

#### ✅ I + N + F:

El cheatcode funciona como se solicita y este tambien debe ser precionado en orden, es decir, que sea tecla por tecla. Ademas por debajo el programa le agrega 9999 vidas a luigi (sin embargo no puede perder vida), pone en pausa el Qtimer (el que se encarga de mostrar el tiempo de la partida) y se notifica al usuario en la ventana de juego que se uso el cheatcode en la parte superior de la ventana.


-------


## Archivos: 4 pts (4%)


#### 🟠 Sprites:

Se maneja los sprites de forma parcial, ya que si bien los ulizo para crear la ventana de juego, no los utilizo correctamente para la animacion de las entidades.

#### ✅ Parametros.py:

Se cumple con la totalidad de lo solicitado, ya que todos los PATH, VARIABLES CONSTANTES, etc. Estan en ese archivo y es importado correctamente.


## Bonus: 8 décimas máximo


#### ✅ Volver a Jugar:

Bonus implementado en su totalidad y este se muestra al momento de finalizar una partida, ya que en el pop up del resultado de la partida te da la opcion de volver a jugar, mandandote a la ventana de inicio para que puedas seleccionar un mapa o crear uno desde 0.

#### ❌ Follower Villain:

No implementado.

#### ❌ Drag and Drop:

No implementado.

-------

## Ejecución :computer:

El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:

Se tienen que crear las siguientes carpetas y archivos en el mismo directorio que el ```main.py```:
1. ```mapas``` en la misma carpeta del ```main.py```
2. ```sprites``` en la misma carpeta del ```main.py```
3. ```sonidos``` en la misma carpeta del ```main.py```

Tienen que estar las carpetas en la misma carpeta que el ```main.py```, es decir, en la carpeta ```T02```.
1. ```frontend``` con sus respectivos archivos
2. ```backend``` con sus respectivos archivos

-------

## Librerías :books:

#### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. use PyQt5.Qtcore en los archivos ```frontend_juego.py```, ```frontend_inicio.py```, ```frontend_constructor.py```, ```elementos_graficos.py``` y  ```backend_juego.py```.
2. use PyQt5.QtWidgets en los archivos ```frontend_juego.py```, ```frontend_inicio.py```, ```frontend_constructor.py```, ```elementos_graficos.py``` y en el ```main.py```.
3. use PyQt5.Gui en los archivos ```frontend_juego.py```, ```frontend_inicio.py```, ```frontend_constructor.py``` y ```elementos_graficos.py```.
4. use PyQt5.QtMultimedia en el archivo ```frontend_juego.py```. (debe instalarse en caso de que no este instalado, sin embargo en las issues me dijieron que si se podia usar)
5. use os en los archivos ```frontend_juego.py```, ```frontend_inicio.py```, ```frontend_constructor.py```, ```elementos_graficos.py``` y ```backend_juego.py```.
6. use random en el archivo ```backend_juego.py```.
7. use sys en los archivos ```frontend_juego.py``` y ```frontend_inicio.py```.
8. use time en el archivo ```frontend_juego.py```.
9. use PyQt5 en el archivo ```frontend_inicio.py```.


### Librerías propias


Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```backend_juego.py``` en la carpeta ```backend```
2. ```funciones.py``` en la carpeta ```backend```
3. ```frontend_constructor.py``` en la carpeta ```frontend```
4. ```frontend_inicio.py``` en la carpeta ```frontend```
5. ```frontend_juego.py``` en la carpeta ```frontend```
6. ```elementos_graficos.py``` en la carpeta ```frontend```
7. ```parametros.py``` en la carpeta del ```main.py```


-------


## Referencias de código externo :book:

Para realizar mi tarea use como referencia de código (extraje la idea): 

1. Linea 165 hasta la 183 en el archivo ```frontend_constructor.py``` fue sacado de: 
https://stackoverflow.com/questions/44707794pyqt-combo-box-change-value-of-a-label

2. Desde la linea 8 hasta la 39 en el archivo ```elementos_graficos.py``` fue sacado de:
https://stackoverflow.com/questions/45575626/make-qlabel-clickable