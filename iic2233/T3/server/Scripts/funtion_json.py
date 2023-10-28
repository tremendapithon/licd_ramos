from os import path
from json import load

def leer_json(ruta: str) -> dict:
    with open(path.join(ruta), "r") as archivo:
        diccionario = load(archivo)
    return diccionario