# Modulo encargado de codificar y decodificar los mensajes
from pickle import dumps, loads, PicklingError, UnpicklingError
from Scripts.cripto import encriptar, desencriptar
from Scripts.cripto import encriptar, desencriptar
from os import system
import sys

def codificar_mensaje(msg: any, N: int) -> bytearray: # CODIFICAR
    try:
        msg_codificado = bytearray(encriptar(bytearray(dumps(msg)), N))
        len_codificado = bytearray(len(msg_codificado).to_bytes(4, byteorder="little"))
        numero_bloques =  (len_msg := len(msg_codificado)) // 128
        
        if numero_bloques == 0: # Caso len(msg) < 128
            msg_codificado += bytearray(b"\x00") * (128 - len_msg)
            return (len_codificado + bytearray(numero_bloques.to_bytes(4, byteorder="big")) 
                        + msg_codificado)
            
        elif numero_bloques != 0: # Caso len(msg) > 128
            new_bytearray = bytearray()
            for i in range(numero_bloques):
                new_bytearray += i.to_bytes(4, byteorder="big") # Numero de bloque
                new_bytearray += msg_codificado[i * (128): (i + 1) * 128]
            new_bytearray += numero_bloques.to_bytes(4, byteorder="big")
            new_bytearray += (msg_codificado[(i + 1) * 128:] + bytearray(b"\x00") * (128 - len_msg))
            return (len_codificado + new_bytearray)
    except (IndexError, ValueError, TypeError, PicklingError):
        pass
    
def decodificar_mensaje(msg: bytearray, N: int) -> any: # DECODIFICA HASTA 256 BYTES
    try:
        len_msg = int.from_bytes(msg[0: 4], byteorder="little")
        if len_msg < 128:
            msg = msg[8: len_msg + 8]
            return loads(desencriptar(msg, N))
            
        elif len_msg == 128:
            msg = msg[8:]
            return loads(desencriptar(msg, N))
            
        elif len_msg > 128:
            new_bytearray = bytearray()
            numero_bloques, largo_msg = len_msg // 128, len_msg % 128
            msg = msg[4:] # Elimina el largo del mensaje

            for i in range(numero_bloques):
                new_bytearray += msg[4 + (i * 132): 132 * (i + 1)]

            if largo_msg == 0:
                return loads(desencriptar(new_bytearray, N))
                
            elif largo_msg != 0:
                new_bytearray += msg[4 + (numero_bloques * 132):]
                return loads(desencriptar(new_bytearray, N))
    except (IndexError, TypeError, ValueError, UnpicklingError):
        pass  

def ajustar_label(num: int, pond: int) -> tuple:
    if num == 0:
        return (256 + round(pond / 4), 50 + pond, 90, 90)
    elif num == 1:
        return (64 + round(pond / 4), 150 + pond, 90, 90)
    elif num == 2:
        return (450 + round(pond / 4), 150 + pond, 90, 90)
    else:
        return (256 + round(pond / 4), 300 + pond, 90, 90)
    
def verificar_pos(num) -> int:
    if num == 0:
        return num
    elif num == 3:
        return 1
    else:
        return num + 1

class RunAgain:
    def __init__(self, args) -> None:
        self.args = args

    def run_again(self):
        system(f"python3 main.py {self.args}")
        sys.exit()

    
