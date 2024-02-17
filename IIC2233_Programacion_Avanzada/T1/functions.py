from os.path import exists
from os import path, system, name, mkdir
from sys import exit
from random import randint, choice, random
import parametros as pr



# Manejo de archivos
def lectura_archivos(nombre_archivo: str) -> list:
    if exists(path.join(nombre_archivo)): # Verifica, si existe los archivos del juego
        with open(path.join(nombre_archivo), "rt", encoding="utf-8") as file:
            file.readline()
            return [i.strip().split(",") for i in file]
    else:
        exit("No existe el archivo...") # Si no existe, se cierra el programa


def verificar_carpeta() -> bool: # Verifica si existe la carpeta donde se guardan las partidas
    if not exists(pr.strings["path"]):
        mkdir(path.join("Partida"))
        exit("Se ha creado la carpeta 'Partidas'..")
    
    return True 


def guardar_partida(Torneo: object, nombre_partida) -> None:
    if verificar_carpeta():
        with open(path.join("Partidas", nombre_partida + ".txt"), "wt", encoding="utf-8") as file:
            torneo = str(Torneo.__str__())
            file.write(torneo) # Se encarga de guardar la partida
            

def leer_partida(nombre_partida, arenas, excavadores, items): # Se encarga de leer la partida
    if verificar_carpeta():
        with open(path.join("Partidas", nombre_partida), "rt", encoding="utf-8") as file:
            archivo = [i.split("$23*") for i in file] # Se encarga de procesar el archivo
            descomprimir_arenas = [archivo[0][0].split(",")[1], archivo[0][0].split(",")]
            descomprimir_excavadores = [i.split(",") for i in archivo[0][1].split("%3#@")]
            descomprimir_items = [i.split(",") for i in archivo[0][2].split("%3#@")]
            arena_obj = cargar_arena(*arenas, *descomprimir_arenas)
            arena_obj.items(items_iniciales(*items)) # Se cargan los items iniciales
            excavadores_obj = cargar_excavadores(*excavadores, descomprimir_excavadores)
            item_obj = cargar_items(*items, descomprimir_items)
            dias_torneo = (archivo[0][4].split(",")[0], archivo[0][4].split(",")[1])
            metros_torneo = (archivo[0][3].split(",")[0], archivo[0][3].split(",")[1])
            tipo_arena = archivo[0][5]
            torneo_1 = [arena_obj, pr.eventos, excavadores_obj, item_obj]
            torneo_2 = [metros_torneo, dias_torneo, tipo_arena]
            return torneo_1 + torneo_2
    else:
        exit("No existe la partida...")


def carga_archivos(archivos: dict) -> dict: # Carga los archivos para una nueva partida
    n_equipo = pr.CANTIDAD_EXCAVADORES_INICIALES # Se repesenta el numero inicial de excavadores
    archivos["arena"] = buscar_elemento(lectura_archivos("arenas.csv"), pr.ARENA_INICIAL)
    archivos["excavadores"] = excavadores_iniciales(lectura_archivos("excavadores.csv"), n_equipo)
    archivos["tesoros"] = lectura_archivos("tesoros.csv")
    archivos["consumibles"] = lectura_archivos("consumibles.csv")
    
    return archivos


# Manejo de funciones para la partida
def buscar_elemento(archivo: list, tipo: str)-> list: # Arena inicial
    lista_seleccionados = []
    for i in archivo:
        if i[1] == tipo:
            lista_seleccionados.append(i)

    if lista_seleccionados != []: 
        return choice(lista_seleccionados)
    
    else:
        exit("No hay elementos en la lista...") # Si no hay elementos, se cierra el programa
    

def excavadores_iniciales(archivo: list, variable: int) -> list: # Excavadores iniciales
    seleccion_excavadores = []
    for i in range(variable):
        seleccion_excavadores.append(archivo[randint(0, len(archivo) - 1)])
   
    return seleccion_excavadores


def items_iniciales(Tesoros: object, Consumibles: object) -> list: # Instancia los items
    cargar_archivos = carga_archivos({}) # Carga los archivos
    items_iniciales = []
    tesoros_iniciales = []
    consumibles_iniciales = []
    for i in (cargar_archivos["tesoros"]):
        i.insert(1, "tesoro")   
        tesoros_iniciales.append(Tesoros(*i))

    for i in (cargar_archivos["consumibles"]):
        i.insert(1, "consumible")
        consumibles_iniciales.append(Consumibles(*i))

    items_iniciales.append(tesoros_iniciales)
    items_iniciales.append(consumibles_iniciales)

    return items_iniciales # Se retornan los tesoros


def instanciar_excavadores(Docencio: object, Tareo: object, Hibrido: object) -> list:
    cargar_archivos = carga_archivos({})
    equipo_excavadores = []
    for i in (cargar_archivos["excavadores"]): # Instancia los excavadores iniciales
        if i[1] == "docencio":
            equipo_excavadores.append(Docencio(*i))

        elif i[1] == "tareo":
            equipo_excavadores.append(Tareo(*i))

        elif i[1] == "hibrido":
            equipo_excavadores.append(Hibrido(*i))

    return equipo_excavadores


def instanciar_arenas(Normal, Mojada, Rocosa, Magnetica, Tesoros, Consumibles) -> object:
    cargar_archivos = carga_archivos({}) 
    if pr.ARENA_INICIAL == "normal": # Instancia la arena inicial
        arena = Normal(*cargar_archivos["arena"])

    elif pr.ARENA_INICIAL == "mojada":
        arena = Mojada(*cargar_archivos["arena"])
    
    elif pr.ARENA_INICIAL == "rocosa":
        arena = Rocosa(*cargar_archivos["arena"])

    elif pr.ARENA_INICIAL == "magnetica":
        arena = Magnetica(*cargar_archivos["arena"])
    arena.items(items_iniciales(Tesoros, Consumibles))

    return arena


def instanciar_excavador(Docencio: object, Tareo: object, Hibrido: object, tipo: str) -> object:
    cargar_archivos = lectura_archivos("excavadores.csv") 
    excavadores_iniciales = [i for i in cargar_archivos if i[1] == tipo]
    if tipo == "docencio": # Instancia un excavador aleatorio cada vez que se utiliza un tesoro(c1)
        return Docencio(*choice(excavadores_iniciales))
    
    elif tipo == "tareo":
        return Tareo(*choice(excavadores_iniciales))
    
    elif tipo == "hibrido":
        return Hibrido(*choice(excavadores_iniciales))


def instanciar_arena(Normal, Mojada, Rocosa, Magnetica, tipo) -> object:
    cargar_archivos = lectura_archivos("arenas.csv") # Instancia arena aleatoria por tesoro(c2)
    arenas_iniciales = [i for i in cargar_archivos if i[1] == tipo]
    if tipo == "normal":
        return Normal(*choice(arenas_iniciales))
    
    elif tipo == "mojada":
        return Mojada(*choice(arenas_iniciales))
    
    elif tipo == "rocosa":
        return Rocosa(*choice(arenas_iniciales))
    
    elif tipo == "magnetica":
        return Magnetica(*choice(arenas_iniciales))
    

def cargar_arena(Normal, Mojada, Rocosa, Magnetica, tipo, str) -> object:
    if tipo == "normal":
        return Normal(*str)
    
    elif tipo == "mojada":
        return Mojada(*str)
    
    elif tipo == "rocosa":
        return Rocosa(*str)
    
    elif tipo == "magnetica":
        return Magnetica(*str)
    

def cargar_excavadores(Docencio: object, Tareo: object, Hibrido: object, string) -> object:
    lista_excavadores = []
    if [""] not in string:
        for i in string:
            if i[1] == "docencio":
                lista_excavadores.append(Docencio(*i))
            
            elif i[1] == "tareo":
                lista_excavadores.append(Tareo(*i))
            
            elif i[1] == "hibrido":
                lista_excavadores.append(Hibrido(*i))

    return lista_excavadores


def cargar_items(Tesoros: object, Consumibles: object, string) -> list:
    lista_items = []
    if [""] not in string:
        for i in string:
            if i[1] == "tesoro":
                lista_items.append(Tesoros(*i))
            elif i[1] == "consumible":
                lista_items.append(Consumibles(*i))

    return lista_items


def ocurrencia_evento(probabilidad: float) -> str:
    return random() <= probabilidad   
    

def probabilidad_evento() -> str:    
    if ocurrencia_evento(pr.PROB_INICIAR_EVENTO):
        if random() <= pr.PROB_LLUVIA:
            return "lluvia"
        
        elif random() <= pr.PROB_TERREMOTO:
            return "terremoto"
        
        elif random() <= pr.PROB_DERRUMBE:
            return "derrumbe"
    else:
        return "ninguno"


def probabilidad_item(probabilidad) -> str:    
    if ocurrencia_evento(pr.PROB_ENCONTRAR_ITEM):
        if probabilidad <= pr.PROB_ENCONTRAR_TESORO:
            return "tesoro"
        
        elif probabilidad <= pr.PROB_ENCONTRAR_CONSUMIBLE:
            return "consumible"
    else:
        return "ninguno"
    

# Funciones esteticas para el programa
def clear() -> None: # Citado en el readme
    if name == "nt":
        system("cls")
    else:
        system("clear")


def estado_torneo(archivo: list, strings: dict, dias: tuple, arena: str, excavado: tuple) -> None:
    print(strings["estado_torneo"])
    print(f"Dia torneo DCCavaCava: {dias[0]} / {dias[1]}")
    print(f"Tipo de arena: {arena}") 
    print(f"Metros excavados: {round(excavado[0], 2)} / {round(excavado[1], 2)}")
    print("-" * 75 + "\n" + strings["excavadores"] + "\n" + "-" * 75)
    n_excavador = 0

    for i in archivo:
        n_excavador += 1
        nombre = i.nombre
        tipo = i.tipo
        energia = i.energia
        fuerza = i.fuerza
        suerte = i.suerte
        felicidad = i.felicidad
        expacios = "|{:<6}|{:<20}|{:<10}|{:<8}|{:<7}|{:<7}|{:<10}|"
        print(expacios.format(n_excavador, nombre, tipo, energia, fuerza, suerte, felicidad))
    print("-" * 75)


def mostrar_items(archivo: list, strings: dict) -> str|int: # Muestra los items
    print(*strings["estado_items"], sep="\n")
    n_item = 0
    for i in archivo:
        n_item += 1
        nombre = i.nombre
        tipo = i.tipo
        descripcion = i.descripcion
        expacios = "|{:<4}|{:<40}|{:<11}|{:<70}|"
        print(expacios.format(n_item, nombre, tipo, descripcion))
    print(pr.strings["opcion_salida"][0])
    print("-" * 129)
    opcion_jugador = (input("Ingrese el numero del item que desea usar: "))

    if opcion_jugador.isdigit() and  0 < int(opcion_jugador) < (len(archivo)) + 1:
        return int(opcion_jugador) - 1
    
    elif opcion_jugador == "x":
        return "x"
    
    else:
        clear()
        return mostrar_items(archivo, strings) # Recursividad
    

def mostrar_archivos(archivo: list) -> str:
    print(*pr.strings["mostrar_archivos"], sep="\n")
    n_archivo = 0
    for i in archivo:
        n_archivo += 1
        nombre = i[:(len(i) - 4)]
        extencion = i[(len(i) - 4):]
        expacios = "|{:<4}|{:<35}|{:<9}|"
        print(expacios.format(n_archivo, nombre, extencion))
    print(pr.strings["opcion_salida"][1])
    opcion_jugador = (input("Ingrese el numero del archivo que desea cargar: "))

    if opcion_jugador.isdigit() and  0 < int(opcion_jugador) < (len(archivo)) + 1:
        return archivo[int(opcion_jugador) - 1]
    
    elif opcion_jugador == "x":
        return "x"
    else:
        clear()
        return mostrar_archivos(archivo)

