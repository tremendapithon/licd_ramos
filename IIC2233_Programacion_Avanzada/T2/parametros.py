from os import path, listdir
import random


ANCHO_GRILLA = 11 # NO EDITAR
LARGO_GRILLA = 16 # NO EDITAR

# Complete con los demás parámetros
MIN_CARACTERES = 3
MAX_CARACTERES = 9
MAXIMO_FANTASMAS_VERTICAL = 50
MAXIMO_FANTASMAS_HORIZONTAL = 50
MAXIMO_PARED = 100
MAXIMO_ROCA = 90
MAXIMO_FUEGO = 50
TIEMPO_CUENTA_REGRESIVA = 15

MIN_VELOCIDAD = 0
MAX_VELOCIDAD = 1
PONDERADOR_VELOCIDAD_FANTASMAS = random.random() * (MAX_VELOCIDAD - MIN_VELOCIDAD) + MIN_VELOCIDAD

CANTIDAD_VIDAS = 3
CONDICION_CARACTERES = (MIN_CARACTERES, MAX_CARACTERES)
MULTIPLICADOR_PUNTAJE = 10

AJUSTAR_VELOCIDAD = 0.09 # EDITAR para cambiar velocidad de Luigi
LISTA_PERSONAJES = ["luigi", "ghost_v", "ghost_h", "rock", "wall", "osstar", "fire"]

# Cantidad de elementos
CANTIDAD_ELEMENTOS = [
    1,
    MAXIMO_FANTASMAS_VERTICAL,
    MAXIMO_FANTASMAS_HORIZONTAL,
    MAXIMO_ROCA,
    MAXIMO_PARED,
    1,
    MAXIMO_FUEGO
]

# Path de los archivos 
PATH_SPRITES = [
    path.join("sprites", "Personajes", "luigi_rigth_1.png"),
    path.join("sprites", "Personajes", "red_ghost_vertical_1.png"),
    path.join("sprites", "Personajes", "white_ghost_rigth_1.png"),
    path.join("sprites", "Elementos", "rock.png"),
    path.join("sprites", "Elementos", "wall.png"),
    path.join("sprites", "Elementos", "osstar.png"),
    path.join("sprites", "Elementos", "fire.png")
    ]

# Animaciones de Luigi
ANIMACIONES_LUIGI = { 
    "LUIGI_ARRIBA" : [
        path.join("sprites", "Personajes", "luigi_up_1.png"),
        path.join("sprites", "Personajes", "luigi_up_2.png"),
        path.join("sprites", "Personajes", "luigi_up_3.png")
    ],
    "LUIGI_ABAJO": [
        path.join("sprites", "Personajes", "luigi_down_1.png"),
        path.join("sprites", "Personajes", "luigi_down_2.png"),
        path.join("sprites", "Personajes", "luigi_down_3.png")
    ],
    "LUIGI_DERECHA": [
        path.join("sprites", "Personajes", "luigi_rigth_1.png"),
        path.join("sprites", "Personajes", "luigi_rigth_2.png"),
        path.join("sprites", "Personajes", "luigi_rigth_3.png")
    ],
    "LUIGI_IZQUIERDA": [
        path.join("sprites", "Personajes", "luigi_left_1.png"),
        path.join("sprites", "Personajes", "luigi_left_2.png"),
        path.join("sprites", "Personajes", "luigi_left_3.png")
    ]
}

PATH_QTDESIGNER = path.join("frontend", "qt_designer", "ventana_qt.ui")
PATH_BACKGROUND = path.join("sprites", "Fondos", "fondo_inicio.png")
PATH_LOGO = path.join("sprites", "Elementos", "logo.png")
PATH_BORDERMAP = path.join("sprites", "Elementos", "bordermap.png")
PATH_SONIDO_GANAR = path.join("sounds", "stageClear.wav")
PATH_SONIDO_PERDER = path.join("sounds", "gameOver.wav")

# Mapas del juego -> Mapas vacio y bordes del mapa
LISTA_MAPAS =[i.split(".")[0] for i in listdir(path.join("mapas"))]
BORDES_MAPA = [
    [f"(0, {i})"  for i in range(ANCHO_GRILLA)],
    [f"(15, {i})"  for i in range(ANCHO_GRILLA)],
    [f"({i}, 0)"  for i in range(LARGO_GRILLA)],
    [f"({i}, 10)"  for i in range(LARGO_GRILLA)]   
]
LISTA_BORDES = [k for i in BORDES_MAPA for k in i]
CASILLAS_VACIAS = [f"{i, k}" for i in range(LARGO_GRILLA) for k in range(ANCHO_GRILLA)]
MAPA_VACIO = [
    ["-"] * (ANCHO_GRILLA - 2) for i in range(LARGO_GRILLA - 2)
]

# Movimientos invalidos
MOVIMIENTOS_INVALIDOS = ["H", "R", "P", "O", "S", "F", "W", "V"]

# Popup
POPUP_ERROR_CONSTRUCTOR = "No se puede iniciar el juego.\nAgrega a Luigi o una estrella."