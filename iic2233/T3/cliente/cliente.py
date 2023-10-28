from PyQt5.QtCore import pyqtSignal, QObject
from Scripts.funtions import codificar_mensaje, decodificar_mensaje
from Scripts.funtion_json import leer_json
from math import ceil
from time import sleep
import pickle
import socket
import threading


# Crear un socket TCP/IP
class ConexionCliente(QObject):

    N_PONDERADOR = leer_json("parametros.json")["N_PONDERADOR"]
    
    senal_nombre_usuario = pyqtSignal(str)
    senal_mostrar_ventana = pyqtSignal()
    senal_mostrar_problema = pyqtSignal()
    senal_caida_servidor = pyqtSignal()
    senal_sala_llena = pyqtSignal(str)
    senal_partida_curso = pyqtSignal(str)
    
    senal_iniciar_juego = pyqtSignal()
    senal_enviar_nombre = pyqtSignal(str)
    senal_volver_jugar = pyqtSignal()
    senal_ocultar_ventana = pyqtSignal() 
    senal_actualizar_jugadores = pyqtSignal(dict)
    senal_actualizar_label = pyqtSignal(str, str)
    senal_dados_juego = pyqtSignal(dict)

    nombre_asignado = False

    def __init__(self, host_name: str, port_user: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.host_name = host_name
        self.port_user = port_user
        self.id_jugador = ''
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conexion_establecida = False
        self.log_console("Connecting to server...", f"{self.host_name} : {self.port_user}")

        try:
            self.socket_cliente.connect((self.host_name, self.port_user))
            self.conexion_establecida = True
            self.log_console("Connection established!", f"{self.host_name} : {self.port_user}")
            self.listen()

        except ConnectionError:
            self.log_console("Connection failed...", f"{self.host_name} : {self.port_user}")
            self.senal_mostrar_problema.emit()
            self.socket_cliente.close() # Cerrar el socket

    def listen(self):
        self.log_console("Listening...", f"{self.host_name} : {self.port_user}")
        thread = threading.Thread(target=self.thread_escuchar, args=(self.socket_cliente, ), 
                                daemon=True)
        thread.start()

    def thread_escuchar(self, socket_cliente: socket) -> None: # CITAR README
        while True:
            try:
                mensaje = self.recibir_mensaje(socket_cliente)
                self.procesar_mensaje(mensaje)
                if len(mensaje) == 0 :
                    self.log_console("Server disconnected", "removed from server")
                    self.senal_caida_servidor.emit()
                    break

            except (TypeError, ConnectionResetError) :
                self.log_console("Server disconnected", "removed from server")
                sleep(0.1) # Para que el main pueda capturar la señal
                self.senal_caida_servidor.emit()
                break
            
    def enviar_mensaje(self, mensaje: any) -> None:
        msg_codificado = codificar_mensaje(mensaje, self.N_PONDERADOR)
        self.socket_cliente.sendall(msg_codificado[0:4])
        self.socket_cliente.sendall(msg_codificado)

    def recibir_mensaje(self, socket_cliente: socket) -> any:
        try:
            largo_mensaje = int.from_bytes(bytearray(socket_cliente.recv(4)), "little")
            cantidad_recivir = lambda num: ceil(num / 128)
            mensaje_cod = bytearray(socket_cliente.recv(136 * cantidad_recivir(largo_mensaje)))
            return decodificar_mensaje(mensaje_cod, self.N_PONDERADOR)
        except pickle.UnpicklingError as e:
            pass
    
    def procesar_mensaje(self, mensaje: any) -> None:
        sleep(0.1)
        if "id_usuario" in mensaje and not(self.nombre_asignado):
            self.nombre_asignado = True
            self.id_jugador = mensaje["id_usuario"]
            self.senal_nombre_usuario.emit(mensaje["id_usuario"])

        elif "sala_espera" == mensaje:
            self.senal_sala_llena.emit("La sala esta ocupada, intente mas tarde...")

        elif "sala_llena" == mensaje:
            self.senal_partida_curso.emit("Partida en curso, intente mas tarde...")

        elif "iniciar_juego" == mensaje:
            self.senal_iniciar_juego.emit()
            self.senal_enviar_nombre.emit(self.id_jugador)
        
        elif "clientes_conectados" in mensaje:
            self.senal_actualizar_jugadores.emit(mensaje)
            if len(mensaje["clientes_conectados"]) == 4 and not(self.nombre_asignado):
                self.senal_sala_llena.emit("La sala esta ocupada, intente mas tarde...")

        elif "actualizar_id" in mensaje:
            self.id_jugador = mensaje["actualizar_id"]
            self.senal_enviar_nombre.emit(self.id_jugador)

        elif "actualizar_label" in mensaje:
            if mensaje["actualizar_label"] == "valor_anunciado":
                self.senal_actualizar_label.emit(str(mensaje["mensaje"]),
                                                mensaje["actualizar_label"])
            
            elif mensaje["actualizar_label"] == "turno_jugador":
                self.senal_actualizar_label.emit(f"Turno de: {mensaje['mensaje']}", 
                                                mensaje["actualizar_label"])
                
            elif mensaje["actualizar_label"] == "actualizar_turno":
                self.senal_actualizar_label.emit(f"{mensaje['mensaje']}", 
                                                "actualizar_turno")
            elif mensaje["actualizar_label"] == "movimiento_invalido":
                self.senal_actualizar_label.emit(mensaje["mensaje"],
                                                "movimiento_invalido")
            elif mensaje["actualizar_label"] == "dados_jugador":
                self.senal_dados_juego.emit(mensaje["mensaje"])

        elif "dados" in mensaje:
            self.senal_dados_juego.emit(mensaje["dados"])

        elif "sala_disponible" == mensaje:
            self.senal_volver_jugar.emit()
            
    def mostrar_ventana(self): # Mostrar la ventana del cliente
        if self.conexion_establecida:
            self.senal_mostrar_ventana.emit()
        else:
            self.senal_mostrar_problema.emit() # Cerrar el programa
            self.socket_cliente.close() # Cerrar el socket

    def init_juego(self):
        self.enviar_mensaje("iniciar_juego")

    def cerrar_conexion(self):
        self.log_console("Closing connection...", f"{self.host_name} : {self.port_user}")
        self.enviar_mensaje("cerrar_conexion")

    def log_console(self, msg: str, address: str) -> None:
        expacios_log = "|{:<25}|{:<20}|"
        print(expacios_log.format(msg, f"{address}"))
