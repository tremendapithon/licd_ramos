from random import choice, randint

class JuegoDCCachos:
    __ganador_dccachos = False
    turno_jugador = ''
    valor_anunciado = 0
    valor_actualizado = False
    numero_turno = 1
    dados_cambiados = []

    def __init__(self, lista_jugadores: list) -> None:
        self.lista_jugadores = lista_jugadores
        self.__numero_jugadores = len(lista_jugadores)
        self.id_jugadores = list(map(lambda x: lista_jugadores[x], lista_jugadores))
        self.turno_jugador = choice(self.id_jugadores)
        self.jugador_anterior = self.turno_jugador
        self.dict_dados = self.repartir_dados(self.id_jugadores)

    def repartir_dados(self, lista_jugadores) -> dict:
        dict_dados = {}
        for i in lista_jugadores:
            dict_dados[i] = ((randint(1, 6), randint(1, 6)))
        return dict_dados
    
    def cambiar_dados(self, id_jugador):
        if self.turno_jugador == id_jugador and id_jugador not in self.dados_cambiados:
            self.dict_dados[id_jugador] = ((randint(1, 6), randint(1, 6)))
            self.dados_cambiados.append(id_jugador)
    
    @property
    def numero_jugadores(self) -> int:
        return self.__numero_jugadores
    
    @numero_jugadores.setter
    def numero_jugadores(self, numero_jugadores: int) -> None:
        if numero_jugadores == 0:
            self.ganador_dccachos = True

    @property
    def ganador_dccachos(self) -> bool:
        return self.__ganador_dccachos
    
    @ganador_dccachos.setter
    def ganador_dccachos(self, ganador_dccachos: bool) -> None:
        if ganador_dccachos == True:
            pass

    def recibir_instrucciones(self, instruccion: dict) -> None:
        if instruccion["accion"] == "Anunciar":
            if (instruccion["mensaje"] > self.valor_anunciado and instruccion["id_usuario"]
                == self.turno_jugador):
                self.valor_anunciado = instruccion["mensaje"]
                self.valor_actualizado = True
            else:
                self.valor_actualizado = False

    def cambiar_turno(self, id_jugador: str) -> None:
        self.dados_cambiados = []
        if self.jugador_anterior in self.id_jugadores:
            self.jugador_anterior = self.turno_jugador

        if (index_id := self.id_jugadores.index(id_jugador)) == len(self.id_jugadores) - 1:
            self.turno_jugador = self.id_jugadores[0]
        elif index_id < len(self.id_jugadores) - 1:
            self.turno_jugador = self.id_jugadores[index_id + 1]
        elif index_id > len(self.id_jugadores) - 1:
            self.turno_jugador = self.id_jugadores[0]


    def eliminar_jugador(self, id_jugador: str) -> None:
        self.cambiar_turno(id_jugador)
        self.id_jugadores.remove(id_jugador)
        self.numero_jugadores = len(self.id_jugadores)
        del self.dict_dados[id_jugador]


