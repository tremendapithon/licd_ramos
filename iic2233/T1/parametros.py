from os import path


# Inicio de la partida
ARENA_INICIAL = "mojada"
DIAS_INICALES_TORNEO = 1
DIAS_TOTALES_TORNEO = 120
DIAS_TORNEO = (DIAS_INICALES_TORNEO, DIAS_TOTALES_TORNEO)
METROS_INICIALES = 0
METROS_META = 2000
metros = (METROS_INICIALES, METROS_META)
CANTIDAD_EXCAVADORES_INICIALES = 10
# Parametro de arena
POND_ARENA_NORMAL = 0.8

# Probabilidades de los items
PROB_ENCONTRAR_ITEM = 0.5
PROB_ENCONTRAR_TESORO = 0.4
PROB_ENCONTRAR_CONSUMIBLE = 0.6


# Probabilidad de evento
PROB_INICIAR_EVENTO = 0.8
PROB_LLUVIA = 0.1
PROB_TERREMOTO = 0.5
PROB_DERRUMBE = 0.4
METROS_PERDIDOS_DERRUMBE = 10 
FELICIDAD_PERDIDA = 2

# Parametros de los excavadores
FELICIDAD_ADICIONAL_DOCENCIO = 5
FUERZA_ADICIONAL_DOCENCIO = 5
ENERGIA_PERDIDA_DOCENCIO = 50
ENERGIA_ADICIONAL_TAREO = 10
SUERTE_ADICIONAL_TAREO = 6
EDAD_ADICIONAL_TAREO = 10
FELICIDAD_PERDIDA_TAREO = 5



eventos = ["lluvia", "terremoto", "derrumbe"]

# Diccionarios con todos los strings necesarios para el programa
strings = {
    "menu_inicio" : [
    "** Menu Inicio **",
    "-----------------",
    "[1] Nueva Partida",
    "[2] Cargar Partida",
    "[x] Salir",
     "-----------------"
                ],
    "menu_principal1" : [ 
    "** Menu Principal **",
    "--------------------------"
            ],

    "menu_principal2" : [
    "\n[1] Simular dia torneo",
    "[2] Ver estado torneo",
    "[3] Ver items",
    "[4] Guardar partida",
    "[5] Volver",
    "[x] Salir del programa",
    "--------------------------"
            ],

    "estado_torneo" : 
    "_" * 26 + "*** ESTADO DEL TORNEO ***" + "_" * 27,

    "mostrar_archivos":[
     "_" * 8 + "      *** ARCHIVOS GUARDADOS ***    " + "_" * 8 + "\n",
    "|N*  |Nombre de la partida               |Extencion|" + "\n" + "-" * 52,
    ],

    "excavadores" : 
    "|N*    |Nombe               |Tipo      |Energía |Fuerza |Suerte |Felicidad |",

    "path" : 
    path.join("Partidas"),
    "nombre_archivo" : [ 
    "arenas.csv",
    "excavadores.csv",
    "tesoros.csv",
    "consumibles.csv",
    ],

    "estado_items" : [
    "_" * 51 +"*** ESTADO DE LOS ITEMS ***" + "_" * 51 + "\n",
    "-" * 129,
    "|N*  |Nombre                                  |Tipo       |Descripción" + " " * 59 + "|",
    "-" * 129,
            ],

    "opcion_salida" :[
    "|x   |Volver al menu                          |           |           " + " " * 59 + "|",
    "|x   |Volver al menu                     |         |" + "\n" + "-" * 52 + "\n"
    ],

    "descanso" : "\n" + "\n" + "_" * 25 +" Excavadores descansando " + "_" * 24 + "\n",
    "items": "\n" + "_" * 19 + " Resultados de la busqueda de items " + "_" * 19 + "\n",
    "evento" : "\n" + "_" * 26 + " Resultados del evento " + "_" * 26 + "\n",
                }

