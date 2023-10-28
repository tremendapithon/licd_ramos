from Scripts.funtions import codificar_mensaje, decodificar_mensaje, generar_id
from Scripts.funtion_json import leer_json
from math import ceil
from backend_server import JuegoDCCachos
import socket
import threading


class ServerJuego:
    # Parametros json
    maximo_conexiones = leer_json("parametros.json")["NUMERO_JUGADORES"]
    id_disponibles = leer_json("parametros.json")["ID_JUGADOR"]
    acciones_usuario = leer_json("parametros.json")["ACCIONES_USUARIO"]
    VALOR_PASO = leer_json("parametros.json")["VALOR_PASO"]
    N_PONDERADOR = leer_json("parametros.json")["N_PONDERADOR"] 
    
    # Parametros server
    sockets_clientes = {}
    sockets_espera = {}
    id_asignados = []
    partida_bots = False
    juego_iniciado = False
    
    def __init__(self, host_name: str, port_user: int) -> None: # Server echo
        self.host_name = host_name
        self.port_user = port_user
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.host_name, self.port_user))
        self.socket_server.listen(10)
        self.log_console("EVENT", "STATUS")
        self.log_console("Server started",
                        f"Listening in host: {self.host_name} / port:{self.port_user}")
        self.echo_client = threading.Thread(target=self.thread_conexiones)
        self.echo_client.start()
        self.lock = threading.Lock()

    def thread_conexiones(self) -> None: # Aceptar conexiones
        while True:
            socket_cliente, address = self.socket_server.accept()
            if len(self.sockets_clientes) < self.maximo_conexiones and not(self.juego_iniciado):
                self.sockets_clientes[socket_cliente] = (id_cliente := 
                                            generar_id(self.id_disponibles, self.id_asignados))
                self.id_asignados.append(id_cliente)
                self.enviar_mensaje({"id_usuario" : id_cliente}, socket_cliente)
                self.comunicar_sockets({"clientes_conectados": self.id_asignados})
                self.log_console(f"{id_cliente} has connected", "Waiting for players...")
                listening_client = threading.Thread(target=self.thread_escuchar, 
                args=(socket_cliente, id_cliente, ), daemon=True)
                listening_client.start() # Se crea un thread para escuchar al cliente
            # Si no puede acceder lo dejamos en la sala de espera
            elif len(self.sockets_clientes) > self.maximo_conexiones and not(self.juego_iniciado):
                self.sala_espera(socket_cliente, address, "sala_espera")
            
            elif self.juego_iniciado and len(self.sockets_clientes) < self.maximo_conexiones:
                self.sala_espera(socket_cliente, address, "sala_llena")
            
            else:
                self.sala_espera(socket_cliente, address, "sala_espera")
        
    def thread_escuchar(self, socket_cliente: socket, id_usuario: str) -> None:
        while True: 
            try:
                mensaje_cliente = self.recibir_mensaje(socket_cliente)
                self.procesar_mensaje(mensaje_cliente)
                if len(mensaje_cliente) == 0:
                    self.eliminar_socket(socket_cliente) # Eliminar cliente
                    break
            except (TypeError, ValueError, ConnectionResetError, BrokenPipeError): 
                self.eliminar_socket(socket_cliente, id_usuario)
                break

    def comunicar_sockets(self, msg: any) -> None:
        for k in self.sockets_clientes:
            self.enviar_mensaje(msg, k)
        
    def enviar_mensaje(self, mensaje: any, socket_cliente: socket) -> None:
        msg_codificado = codificar_mensaje(mensaje, self.N_PONDERADOR)
        socket_cliente.sendall(msg_codificado[0: 4])
        socket_cliente.sendall(msg_codificado)

    def recibir_mensaje(self, socket_cliente: socket) -> any:
        largo_mensaje = int.from_bytes(bytearray(socket_cliente.recv(4)), "little")
        cantidad_recivir = lambda num: ceil(num / 128)
        mensaje_cod = bytearray(socket_cliente.recv(136 * cantidad_recivir(largo_mensaje)))
        return decodificar_mensaje(mensaje_cod, self.N_PONDERADOR)
    
    def procesar_mensaje(self, mensaje: any) -> None:
        if mensaje == "iniciar_juego" and not(self.juego_iniciado):
            self.juego_iniciado = True 
            self.log_console("Starting game with players:", "")
            list(map(lambda x: self.log_console(f"{x}", ""), self.sockets_clientes.values()))
            self.juego_dcc = JuegoDCCachos(self.sockets_clientes)
            self.comunicar_sockets("iniciar_juego")
            self.comunicar_sockets({"dados": self.juego_dcc.dict_dados})
            self.comunicar_sockets({"actualizar_label" : "turno_jugador",
                                    "mensaje": self.juego_dcc.turno_jugador})
            self.comunicar_sockets({"actualizar_label" : "actualizar_turno",
                                    "mensaje": self.juego_dcc.numero_turno})
        elif len(mensaje) > 0:
            if mensaje["accion"] == "Anunciar":
                self.juego_dcc.recibir_instrucciones(mensaje)
                if self.juego_dcc.valor_actualizado:
                    self.comunicar_sockets({"actualizar_label" : "valor_anunciado",
                                        "mensaje": self.juego_dcc.valor_anunciado})
                    self.log_console(f"New valor announced by {mensaje['id_usuario']}", 
                                    f"Value: {mensaje['mensaje']}")
                else:
                    self.log_console(f"Invalid value by {mensaje['id_usuario']}", "")
                    self.comunicar_sockets({"actualizar_label" : "movimiento_invalido",
                                        "mensaje": mensaje["id_usuario"]})
            elif mensaje["accion"] == "Dados":
                self.juego_dcc.cambiar_dados(mensaje["id_usuario"])
                self.comunicar_sockets({"dados" : self.juego_dcc.dict_dados})

            elif mensaje["accion"] == "Pasar":
                if (sum(self.juego_dcc.dict_dados[mensaje["id_usuario"]]) == self.VALOR_PASO
                and mensaje["id_usuario"] == self.juego_dcc.turno_jugador):
                    self.log_console(f"Pass by {mensaje['id_usuario']}", "")
                    self.juego_dcc.cambiar_turno(mensaje["id_usuario"])
                    self.comunicar_sockets({"actualizar_label" : "turno_jugador",
                                            "mensaje": self.juego_dcc.turno_jugador})
                    
                else:
                    self.log_console(f"Invalid pass by {mensaje['id_usuario']}", "")
            elif (mensaje["accion"] == "Dudar" and mensaje["id_usuario"] == 
                self.juego_dcc.turno_jugador):
                self.log_console(f"Doubt by {mensaje['id_usuario']}", 
                                f"To user {self.juego_dcc.jugador_anterior}")
            
        
    def eliminar_socket(self, socket_cliente: socket, id_cliente: str) -> None:
        try:
            del self.sockets_clientes[socket_cliente]
            self.id_asignados.remove(id_cliente)
            self.comunicar_sockets({"clientes_conectados": self.id_asignados})
            self.comunicar_espera("sala_disponible")
            self.comunicar_espera({"clientes_conectados": self.id_asignados})
            self.juego_dcc.eliminar_jugador(id_cliente)
            self.comunicar_sockets({"dados" : self.juego_dcc.dict_dados})
            self.comunicar_sockets({"actualizar_label" : "turno_jugador",
                                    "mensaje": self.juego_dcc.turno_jugador})

        except (RuntimeError, BrokenPipeError, ConnectionResetError, AttributeError, ValueError):
            pass

        finally:
            self.log_console(f"{id_cliente} disconnected", "Remove from server!")

    def comunicar_espera(self, mensaje: any) -> None:
        try:
            list(map(lambda x: self.enviar_mensaje(mensaje, x), self.sockets_espera))

        except (RuntimeError, BrokenPipeError, ConnectionResetError):
            self.log_console("Error in the process", "Server online")
        
    def sala_espera(self, socket_cliente: socket, address: str, case: str) -> None:
        self.sockets_espera[socket_cliente] =  (id_cliente := 
                                        f"Cliente {len(self.sockets_espera) + 1}")
        self.enviar_mensaje({"clientes_conectados": self.id_asignados}, socket_cliente)
        self.enviar_mensaje(case, socket_cliente)
        self.log_console(f"{id_cliente} has connected", "Waiting room...")
        echo_espera = threading.Thread(target=self.thread_espera, args=(socket_cliente,
                                    id_cliente, ), daemon=True)
        echo_espera.start()
        
    def thread_espera(self, socket_cliente: socket, id_cliente: str) -> None:
        while True:
            try:
                mensaje_cliente = self.recibir_mensaje(socket_cliente)
                if len(mensaje_cliente) == 0 or mensaje_cliente == "cerrar_conexion":
                    del self.sockets_espera[socket_cliente]
                    self.log_console(f"{id_cliente} disconnected", "Remove from server!")
                    break
            except (TypeError, ValueError, ConnectionResetError):
                del self.sockets_espera[socket_cliente]
                self.log_console(f"{id_cliente} disconnected", "Remove from server!")
                break

    def log_console(self, msg: str, status: str) -> None:
        expacios_log = "|{:<30}|{:<50}|"
        print(expacios_log.format(msg, status))

