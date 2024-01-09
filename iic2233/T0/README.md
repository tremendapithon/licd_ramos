### Tarea 0: DCCeldas 💣🐢🏰 ###


## Consideraciones generales :octocat:

La tarea entregada de DCCELDAS es capaz de cargar un archivo que este en el directorio de "Archivos", en el caso de que este no exista, el mismo programa lo crea y se cierra; a su vez, si no existen archivos en la carpetas "Archivos", el programa se cierra automaticamente.

Al momento de que se tenga que seleccionar un archivo, el usuario debera escribir el nombre del archivo con su extension correspondiente para que se pueda ejecutar, en el caso contrario, el programa no podra mostrar el menu de acciones.

Una vez cargado el archivo se le da elegir al usuario una opcion, y el usuario debera escoger una opcion hasta que desee cerrar el programa.

Todas las opciones funcionan, menos la opcion numero 4, que solo verifica que se pueda resolver y guarda el tablero como se pide en la pauta.


### Cosas implementadas y no implementadas :white_check_mark: :x:

- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

#### Menú de Inicio (5 pts) (7%)
##### ✅ Seleccionar Archivo
##### ✅ Validar Archivos

#### Menú de Acciones (11 pts) (15%) 
##### ✅ Opciones
##### ✅ Mostrar tablero 
##### ✅ Validar bombas y tortugas
##### ✅ Revisar solución 
##### ❌ Solucionar tablero -> Solo valida que el tablero se pueda resolver, y guarda en la solucion en el archivo indicado
##### ✅ Salir

#### Funciones (34 pts) (45%)
##### ✅ Cargar tablero
##### ✅ Guardar tablero
##### ✅ Valor bombas
##### ✅ Alcance bomba
##### ✅ Verificar tortugas
##### 🟠 Solucionar tablero

#### General: (19 pts) (25%)
##### ✅ Manejo de Archivos
##### 🟠 Menús -> Solo falta las opcion 4 -> Ve si es tablero es solucionable, si lo es, lo guarda como solucion.
##### ✅ tablero.py
##### ✅ Módulos
##### ✅ PEP-8

#### Bonus: 6 décimas
##### ✅ Funciones atómicas
##### ❌ Regla 5


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:

1. Los archivos main.py, functions.py y tablero.py deben estar en la misma carpeta y directorio junto a la carpeta de "Archivos", y estos a su vez en alguna carpeta llamada "T0".
2. Debe crear o importar los tableros en formato .txt, y dejarlos en una carpeta bajo el nombre de "Archivos" en la misma ruta que el archivo del main.py. Aunque esta carpeta no exista, el programa va crear una por defecto carpeta llamada Archivos.
3. Considerando lo anterior, si la carpeta no tiene archivos, el programa se va cerrar automaticamente hasta que exista al menos 1 archivo.
4. Todos los archivos tienen que estar en formato string, eso considera a los simbolos, letras y numeros. Ademas, el archivo debe estar en una sola linea.


## Librerías :books:

### Librerías externas utilizadas
La lista de librerías externas utilizadas en la tarea son:

libreria "os" con las funciones path, system, listdir
libreria "os.path" con la funcion exists
libreria "msvcrt" con la funcion getch

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

libreria "tablero" las cuales tienen su ubicacion junto al archivo main.py
libreria "functions" las cuales tienen su ubicacion junto al archivo main.py

-------

## Consideraciones

En el apartado del if __init__ == "__main__", hay un error en este lugar:
    tablero_2x2_sol = [
        ['T', 2],
        ['-', '-']
    ]

    resultado = verificar_alcance_bomba(tablero_2x2, (0, 1))
    print(resultado)  # Debería ser 2 -> este valor debe ser 3, debido que se refieren al tablero antes de la solucion

    resultado = verificar_tortugas(tablero_2x2_sol)
    print(resultado)  # Debería ser 0
# Otra consideracion es que para mis funciones, los numeros son strings y no enteros. Ademas, lo deje comentado, ya que si no, mi programa no funciona.


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:

1. https://github.com/IIC2233/Syllabus/blob/main/Tareas/T0/Sala%20Ayuda/laberinto.py lo que hace es verificar que las direcciones en donde me puedo mover sean valida y esta implementada en el archivo functions.py en la funcion movimiento_valido de las lineas 77 hasta la 86, esta funcion despues se ultiliza para la funcion verificar_alcanze_bombas.
