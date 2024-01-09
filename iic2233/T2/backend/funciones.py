from os import path
import parametros as pa

def leer_partida(nombre_archivo):
    with open (path.join(nombre_archivo), "r", encoding="utf-8") as archivo:
        contenido = archivo.readlines()
        return [[k for k in i] for i in [i.strip() for i in contenido]]

def verificar_icono(casilla_mapa):
    if casilla_mapa == "L":
        return pa.PATH_SPRITES[0]
    elif casilla_mapa == "V":
        return pa.PATH_SPRITES[1]
    elif casilla_mapa == "H":
        return pa.PATH_SPRITES[2]
    elif casilla_mapa == "R":
        return pa.PATH_SPRITES[3]
    elif casilla_mapa == "P" or casilla_mapa == "W":
        return pa.PATH_SPRITES[4]
    elif casilla_mapa == "O" or casilla_mapa == "S":
        return pa.PATH_SPRITES[5]
    elif casilla_mapa == "F":
        return pa.PATH_SPRITES[6]
    
def tiempo_str(tiempo) -> str:
    tiempo_menor = f"0{tiempo % 60}"
    tiempo_segundos = tiempo % 60 if tiempo % 60 >= 10 else tiempo_menor
    return f"{tiempo // 60}:{tiempo_segundos}"
    
