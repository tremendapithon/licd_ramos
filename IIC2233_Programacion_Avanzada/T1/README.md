# Tarea 1: DCCavaCava 🏖⛏

## Consideraciones generales :octocat:

<Consideraciones> En mi tarea se implemento todo lo solicitado en el enunciado de la tarea, ademas del bonus de "guardar partida".

<Consideraciones> En mi tarea se utiliza la funcion de limpiar consola y se pasa de un menu a otro a traves de un "input()" que espera el ingreso de un enter para continuar.

### Cosas implementadas y no implementadas :white_check_mark: :x:


#### Programación Orientada a Objetos: 42 pts (35%)
##### ✅  Diagrama:
Diagrama hecho y con una breve explicacion de este.
##### ✅ Definición de clases, atributos, métodos y properties: 
Se lleva acabo en los archivos objects.py y objects_1.py
##### ✅ Relaciones entre clases:
Todas las clases interactuan en la clase MenuJuego() del archivo objects_1.py

#### Preparación programa: 11 pts (9%)
##### ✅ Creación de partidas:
Se pueden crear y cargar partidas sin problemas (lo he probodo con un archivo de 700 lineas)


#### Entidades: 22 pts (18%)
##### ✅ Excavador:
Con todos sus metodos y artibutos
##### ✅ Arena:
Con todos sus metodos y artibutos
##### ✅ Torneo:
Con todos sus metodos y artibutos. Quiero mencionar que el atributo de "eventos" no lo encontre que fuera util utilizarlo, ya que lo hice de otra forma.


#### Flujo del programa: 31 pts (26%)
##### ✅ Menú de Inicio:
Menu de inicio recursivo y aprueba de inputs incorrectos
##### ✅ Menú Principal:
Menu principipal recursivo y aprueba de inputs incorrectos
##### ✅ Simulación día Torneo:
La clase MenuJuego llama al metodo self.Torneo.simular_dia()
##### ✅ Mostrar estado torneo:
La clase MenuJuego llama al metodo self.Torneo.estado_torneo()
##### ✅ Menú Ítems:
La clase MenuJuego llama al metodo self.Torneo.menu_items(), cabe considerar que la tabla del torneo es creada atraves de un .format(), por lo que podria tener problemas en las ventanas mas chicas.
##### ✅ Guardar partida:
Guarda la partida con un nombre personalizado y esta se puede ver en tiempo real, si se vuelve al menu de inicio.
##### ✅ Robustez:
Programa testeado con archivos gigantes, y siempre funcionara mientras se respete el formato del archivo. Ademas en caso de no existir algun archivo o elemento, el programa se va cerrar automaticamente.


#### Manejo de archivos: 14 pts (12%)
##### ✅ Archivos CSV:
Lectura correcta de los archivos .csv, los va a leer siempre y cuando estos existan en la carpeta en donde este el main.py junto a los otros archivos. 
##### ✅ Archivos TXT:
Las partidas se guardan unicamente en una sola linea, cosa que despues se trabaje y recupere esa informacion.

##### ✅ parametros.py:
Todos los parametros arbitarios estan en el archivo. Ademas existe un diccionario llamado "strings" que lo hice para imprimir mejor los textos o tablas que hayan en el programa, ya que se puede manejar de forma mas ordena y limpia.


#### Bonus: 3 décimas máximo
##### ✅ Guardar Partida:
Bonus implementado en su totalidad, ya que el programa puede cargar y guardar todas las partidas en la carpera "Partidas", en el mismo directorio del archivo.

## Ejecución :computer:

El módulo principal de la tarea a ejecutar es  ```main.py``` y este tiene que tener en su directorio los archivos ```objects.py```, ```objects_1.py```, ```functions.py``` y ```parametros.py```. Ademas, es recomendable que se cree en el mismo directorio del ```main.py``` la carpeta ```Partidas```; en el caso de que esta carpeta no exista el mismo programa va crear una y se va cerrar.

Cabe mencionar que los archivos .csv de los excavadores, arenas, tesoros y consumibles deben estar en el mismo direcctorio que el archivo ```main.py``` junto a los archivos anteriormente mencionados. Sin embargo, en el caso de que no existan el programa se va cerrar y no se podra ejecutar.


1. ```Partidas``` en ```T1```, la carpeta Partidas


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: choice, random, randint
2. ```sys```: exit
3. ```os``` : listdir, path
4. ``` os.path ``` : exists
5. ``` abc ```: ABC, abstracmethod

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```objects_1.py```: Contiene las clases ```MenuJuego```, ```Torneo```, (las cuales van a correr en main.py)...
2. ```functions.py```: Esta hecha para <manejar los archivos .csv y .txt,  crear todas las instancias de los objetos, realizar funciones de estatetica en el programa (imprimir tablas y limpiar la consola) y para realizar la logica en general>
3. ```parametros.py```: se encarga de manejar todos los parametros que durante todo el programa no van a variar, debido que en algunas funciones del modulo <functions.py> tengo listas vacias que necesito que sean vacias para que el programa funcione
4. ```objects.py```: Contiene las clases de ```Excavador```, ```Arena```, ```Items``` y sus respectivas subclases.

Todo lo anterior terminan corriendo en el archivo ```main.py```


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <Supuestos>: En arenas: Debido a que no esta especificado en el enunciado, yo para efectos practicos deje que todas las arenas tengan siempre los mismos tesoros y consumibles de los archivos "tesoros.csv" y "consumibles.csv", es decir, que cuando un excavador vaya a encontrar un item este no se va eliminar de la arena (siempre va existir)

2. <Supuestos>: En excavadores, como no se ha especificado en el enunciado de la tarea, al momento de cargar una nueva partida, los excavadores se pueden repetir multiples veces, es decir, que a pesar de que en el archivo de los excavadores exista un unico "MatiasMasJuan", al momento de que inicie la partida pueden existir "n" "MatiasMasJuan"

3. <Considerar> La clase que ejecuta todo es la clase MenuJuego, esta recive a la clase torneo y se encarga de instanciar todos los objetos que esten en "objects.py" e introducirlos en la clase Torneo para que puedan interacturar entre si.

4. <Considerar> Por temas esteticos utilizo dos elementos, la funcion functions.clear() para limpiar la consola y el comando input() para darle un toque de menu. Si le dificulta la revision, los puede quitar sin problemas.
 
-------

## Referencias de código externo :book:


1. https://micro.recursospython.com/recursos/como-limpiar-la-consola.html limpieza de la consola en la libreria functions, esta funcion sirve para linux, mac y windows. Sin embargo, en caso de tener problemas la funcion esta en la linea numero < 239 hasta la 243 del ```functions.py``` >.

2. Sala de ayuda T1, de la linea 209 hasta la 235 del archivo ```functions.py``` utilice gran parte de la idea de lo expuesto en clases. A la final con estas funciones hice que funcionaran las probabilidades de los items y los eventos.