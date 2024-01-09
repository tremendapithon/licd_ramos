from Scripts.funtion_json import leer_json 
import server as sv
import sys

if __name__ == "__main__":
    PORT = 8081
    HOST = (leer_json("parametros.json")["HOST"]
                            if len(sys.argv) < 2 else sys.argv[1])
    bind_server = sv.ServerJuego(HOST, PORT)
