# Agregar los imports que estimen necesarios
from os.path import exists
from os import path, system, listdir
import tablero


# Funciones que se encargan de imprimir el menu de inicio y de obtener el nombre del archivo
def prints_menu() -> None: # Se encarga de imprimir el menu de inicio
    print("*** Menu de Inicio ***\nIndique el nombre del archivo que desea abrir:")
    numero_archivo = 1
    if not exists("Archivos"): # Si no existe la carpeta Archivos
        system("mkdir Archivos") # Se crea la carpeta Archivos
    if listdir(path.join("Archivos")) != []: # Si la carpeta Archivos no esta vacia
        for elemento in listdir(path.join("Archivos")):
            print(f"{str(numero_archivo)}: {elemento}")
            numero_archivo += 1
    else:
        print("No hay archivos disponibles...")
        quit()
        
        
def menu_inicio() -> str: # Se encarga que obtener el nombre del archivo y verificar que exista
    prints_menu()
    nombre_archivo = input("Nombre del archivo: ")
    if nombre_archivo != '':
        system("cls") # Limpia la consola
        if exists(path.join("Archivos",nombre_archivo)):
            return nombre_archivo # Se retorna el nombre del archivo
        else:
            return "no_archivo" # No existe el archivo
    else:
        system("cls")
        return menu_inicio()


def menu_seleccion() -> str: # Se encarga de verificar que la entrada sea valida
    system("cls")
    print("** Menu de Acciones **\n")
    print("[1] Mostrar tablero\n[2] Validar bombas y tortugas\n[3] Validar solucion")
    print("[4] Solucionar tablero\n[5] Salir programa\n")
    opcion_seleccionada = input("Seleccione una opcion: ")
    if opcion_seleccionada in ["1", "2", "3", "4", "5"]: # Evita caidas del programa
        return opcion_seleccionada
    else:
        return menu_seleccion() # Llama a la funcion para que el usuario ingrese una opcion valida
    

# Funciones que se encargan de cargar y guardar el tablero
def cargar_tablero(nombre_archivo: str) -> list:
    with open(nombre_archivo, "rt", encoding="utf-8") as archivo:
        lectura_archivo = archivo.read().split(",")
        n_dim = int(lectura_archivo.pop(0)) # Numero de dimenciones
        tablero_juego = [lectura_archivo[(i * n_dim):n_dim + n_dim * (i)] for i in range(n_dim)] 
    return tablero_juego # Se retorna el tablero de juego como una lista de listas


def guardar_tablero(nombre_archivo: str, tablero: list) -> None:
    with open(path.join("Archivos", nombre_archivo), "wt", encoding="utf-8") as archivo:
        linea_archivo = '' + str(len(tablero)) + ',' 
        for fila in tablero:
            linea_archivo += ",".join(fila) + ","
        archivo.write(linea_archivo[0:len(linea_archivo) - 1]) # Escribe el tablero en el archivo


# Funcion que verifica, si hay bombas invalidas
def verificar_valor_bombas(tablero: list) -> int:
    bombas_invalidas = 0 # Contador de bombas invalidas
    valores_bomba = [str(numero) for numero in range(2, 2 * len(tablero))] + ["T", "-"]
    for fila in tablero: # Iteramos sobre el tablero
        for valor in fila:
            if valor not in valores_bomba: # Si el valor no es valido
                bombas_invalidas += 1
    return bombas_invalidas # Se retorna el numero de bombas invalidas


# Funciones que verifica el alcance de las bombas
def movimiento_valido(coordenada: tuple, tablero: list, coordenadas_origen: tuple) -> bool:
    if coordenada[0] < 0 or coordenada[0] >= len(tablero): #citado_sala de ayuda
        return False
    if coordenada[1] < 0 or coordenada[1] >= len(tablero[0]):
        return False
    coordenada_numerica = tablero[coordenada[0]][coordenada[1]].isnumeric()
    coor_origen = coordenada != coordenadas_origen
    if tablero[coordenada[0]][coordenada[1]] == 'T' or coordenada_numerica and coor_origen:
        return False
    return True


def explosion_izquierda(coordenada: tuple, tablero: list, coordenadas_origen: tuple):
    if movimiento_valido((coordenada[0], coordenada[1]), tablero, coordenadas_origen):
        return explosion_izquierda((coordenada[0], coordenada[1] - 1), tablero, coordenadas_origen)
    else:
        return coordenada[1]


def explosion_derecha(coordenada: tuple, tablero: list, coordenadas_origen):
    if movimiento_valido((coordenada[0], coordenada[1]), tablero, coordenadas_origen):
        return explosion_derecha((coordenada[0], coordenada[1] + 1), tablero, coordenadas_origen)
    else:
        return coordenada[1]


def explosion_arriba(coordenada: tuple, tablero: list, coordenadas_origen):
    if movimiento_valido((coordenada[0], coordenada[1]), tablero, coordenadas_origen):
        return explosion_arriba((coordenada[0] + 1, coordenada[1]), tablero, coordenadas_origen)
    else:
        return coordenada[0]
    

def explosion_abajo(coordenada: tuple, tablero: list, coordenadas_origen):
    if movimiento_valido((coordenada[0], coordenada[1]), tablero, coordenadas_origen):
        return explosion_abajo((coordenada[0] - 1, coordenada[1]), tablero, coordenadas_origen)
    else:
        return coordenada[0]


def mov_horizontal(coordenadas: tuple, tablero: list) -> int:
    movimiento_izquierdo = coordenadas[1] - explosion_izquierda(coordenadas, tablero, coordenadas)
    movimiento_derecho = explosion_derecha(coordenadas, tablero, coordenadas) - coordenadas[1]
    return movimiento_derecho + movimiento_izquierdo - 1


def mov_vertical(coordenadas: tuple, tablero: list) -> int:
    movimiento_arriba = explosion_arriba(coordenadas, tablero, coordenadas) - coordenadas[0]
    movimiento_abajo = coordenadas[0] -explosion_abajo(coordenadas, tablero, coordenadas) 
    return movimiento_arriba + movimiento_abajo - 1


def verificar_alcance_bomba(tablero: list, coordenada: tuple) -> int:
    if tablero[coordenada[0]][coordenada[1]] in ["-", "T"]:
        return 0
    else:
        return mov_horizontal(coordenada, tablero) + mov_vertical(coordenada, tablero) - 1
    

# Funcion que se encarga de hacer cumplir la regla numero 3
def verificar_bombas_tablero(tablero: list) -> int:
    bombas_invalidas = 0
    for i1 in range(len(tablero)):
        for i2 in range(len(tablero[i1])):
            if tablero[i1][i2].isnumeric():
                if int(tablero[i1][i2]) != verificar_alcance_bomba(tablero, (i1, i2)):
                    bombas_invalidas += 1
    return bombas_invalidas


# Funciones que verifican, si hay totugas invalidas
def verificar_similitud(punto_1: tuple, punto_2: tuple, tablero: list) -> bool:
    if tablero[punto_1[0]][punto_1[1]] == tablero[punto_2[0]][punto_2[1]] == 'T':
        return True
    else:
        return False


def verificar_horizontalmente(tablero: list) -> list:
    tortugas_invalidas = []
    for i1 in range(len(tablero)):
        for i2 in range(len(tablero[i1])):
            if 0 < i2 < len(tablero[i1]) - 1: # Se ve al medio
                verificacion_izquierda = tablero[i1][i2] == tablero[i1][i2 - 1] == "T"
                verificacion_derecha = tablero[i1][i2] == tablero[i1][i2 + 1] == "T"
                if verificacion_izquierda or verificacion_derecha:
                    tortugas_invalidas.append((i1, i2))
            elif i2 == 0: # Exteremo izquierdo
                if tablero[i1][0] == tablero[i1][1]  == "T":
                    tortugas_invalidas.append((i1, i2))
            elif i2 == len(tablero[i1]) - 1: # Extremo derecho
                if tablero[i1][-1] == tablero[i1][-2] == "T":
                    tortugas_invalidas.append((i1, i2))
    return tortugas_invalidas


def verificar_verticalmente(tablero: list, tortugas_invalidas: list) -> list:
    for i1 in range(len(tablero)):
        for i2 in range(len(tablero[i1])):
            if 0 < i1 < len(tablero) - 1 and (i1, i2) not in tortugas_invalidas:
                verificacion_arriba = tablero[i1][i2] == tablero[i1 - 1][i2] == "T"
                verificacion_abajo = tablero[i1][i2] == tablero[i1 + 1][i2] == "T"
                if verificacion_arriba or verificacion_abajo:
                    tortugas_invalidas.append((i1, i2))
            elif i1 == 0 and (i1,i2) not in tortugas_invalidas: # Extremo superior
                if tablero[0][i2] == tablero[1][i2] == "T":
                    tortugas_invalidas.append((i1, i2))
            elif i1 == len(tablero) - 1 and (i1,i2) not in tortugas_invalidas: # Extremo inferior
                if tablero[-1][i2] == tablero[-2][i2] == "T":
                    tortugas_invalidas.append((i1, i2))
    return tortugas_invalidas


def verificar_tortugas(tablero: list) -> int:
    tortugas_invalidas = verificar_horizontalmente(tablero)
    tortugas_invalidas = verificar_verticalmente(tablero, tortugas_invalidas)
    return len(tortugas_invalidas)


# Funcion que resuelve el tablero
def solucionar_tablero(tablero: list) -> list:
    pass

"""
if __name__ == "__main__":
    tablero_2x2 = [
        ['-', 2],
        ['-', '-']
    ]
    resultado = verificar_valor_bombas(tablero_2x2)
    print(resultado)  # Debería ser 0

    resultado = verificar_alcance_bomba(tablero_2x2, (0, 1))
    print(resultado)  # Debería ser 3

    #tablero_resuelto = solucionar_tablero(tablero_2x2)
    #print(tablero_resuelto)

    tablero_2x2_sol = [
        ['T', 2],
        ['-', '-']
    ]

    resultado = verificar_alcance_bomba(tablero_2x2, (0, 1))
    print(resultado)  # Debería ser 2

    resultado = verificar_tortugas(tablero_2x2_sol)
    print(resultado)  # Debería ser 0
"""


