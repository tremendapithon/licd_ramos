from os import path
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from random import random
from time import sleep
import parametros as pa


class LogicaInicio(QObject):
    # Senales que se conectan con el main y el backend
    senal_conectar_constructor = pyqtSignal()
    senal_conectar_juego = pyqtSignal(str)
    senal_conectar_popup = pyqtSignal(str)
    condicion_car = pa.CONDICION_CARACTERES

    def nombre_valido(self, texto, mapa_seleccionado) -> pyqtSignal:
        extension_valida = self.condicion_car[0] <= len(texto) <= self.condicion_car[1]
        if texto != "" and texto.isalnum() and extension_valida:
            if mapa_seleccionado == "nuevo mapa":
                return self.senal_conectar_constructor.emit()
            else:
                return self.senal_conectar_juego.emit(mapa_seleccionado + ".txt")
            
        elif texto == "":
            return self.senal_conectar_popup.emit("no hay caracteres")
        
        elif not extension_valida:
            return self.senal_conectar_popup.emit("no cumple con la extension")
        
        elif not texto.isalnum():
            return self.senal_conectar_popup.emit("hay caracteres no alfanumericos")
        

class LuigiJuego(QObject):
    # Senales que modifican los elementos que se muestran en el frontend
    senal_dano_luigi = pyqtSignal(int)
    senal_movimiento_lugi = pyqtSignal(list, int, int, int)
    senal_vida_actual = pyqtSignal(int)
    senal_ganar_partida = pyqtSignal()
    senal_actualizar_pos = pyqtSignal(int, int, str)
    senal_mover_roca = pyqtSignal(int, int, str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__movimiento_arriba = 0
        self.__movimiento_abajo = 0
        self.__movimiento_izquierda = 0
        self.__movimiento_derecha = 0
        self.__vidas_luigi: int = pa.CANTIDAD_VIDAS
    
    @property
    def vidas_luigi(self) -> int:
        return self.__vidas_luigi
    
    @vidas_luigi.setter
    def vidas(self, value) -> None:
        if value <= 0:
            self.senal_perdida_partida.emit() # Se emite que se se perdio la partida

    @property
    def movimiento_arriba(self) -> int:
        return self.__movimiento_arriba
    
    @movimiento_arriba.setter
    def movimiento_arriba(self, value):
        if value > 2:
            self.__movimiento_arriba = 0
        else:
            self.__movimiento_arriba = value

    @property
    def movimiento_abajo(self) -> int:
        return self.__movimiento_abajo
    
    @movimiento_abajo.setter
    def movimiento_abajo(self, value):
        if value > 2:
            self.__movimiento_abajo = 0
        else:
            self.__movimiento_abajo = value

    @property
    def movimiento_izquierda(self) -> int:
        return self.__movimiento_izquierda
    
    @movimiento_izquierda.setter
    def movimiento_izquierda(self, value):
        if value > 2:
            self.__movimiento_izquierda = 0
        else:
            self.__movimiento_izquierda = value
    
    @property
    def movimiento_derecha(self) -> int:
        return self.__movimiento_derecha
    
    @movimiento_derecha.setter
    def movimiento_derecha(self, value):
        if value > 2:
            self.__movimiento_derecha = 0
        else:
            self.__movimiento_derecha = value
    
    def recibir_mov(self, num):
        self.movimiento_arriba = num

    def modificar_mapa(self, mapa_juego: list) -> None:
        self.mapa_juego = mapa_juego

    def modificar_vida(self, vida: int) -> None:
        self.__vidas_luigi = vida 

    def inicializar_clase(self, pos_x: int, pos_y: int, mapa_juego: list) -> None:
        self.pos_inicial = (pos_x, pos_y)
        self.mapa_juego = mapa_juego

    def guardar_movimiento(self, pos_x, pos_y, ant_x, ant_y) -> None:
        self.mapa_juego[pos_x][pos_y] = "L"
        self.mapa_juego[ant_x][ant_y] = "-"

    def dano_enemigo(self, pos_x, pos_y) -> str:
        casilla = self.mapa_juego[pos_x][pos_y]
        if casilla in ["F", "V", "H"]:
            self.__vidas_luigi -= 1
            return "damage"
        
        elif casilla in ["O", "S"]:
            return "win"
        
        elif casilla == "R":
            return "rock"
        
        return "none"

    def movimiento_personaje(self, event, pos_x, pos_y) -> None:
        casilla_ocupada = False
        senal_emit = [
            [pa.ANIMACIONES_LUIGI["LUIGI_ARRIBA"], pos_x - 1, pos_y, self.movimiento_arriba],
            [pa.ANIMACIONES_LUIGI["LUIGI_ABAJO"], pos_x + 1, pos_y, self.movimiento_abajo],
            [pa.ANIMACIONES_LUIGI["LUIGI_IZQUIERDA"], pos_x, pos_y - 1,
            self.movimiento_izquierda],
            [pa.ANIMACIONES_LUIGI["LUIGI_DERECHA"], pos_x, pos_y + 1, self.movimiento_derecha]
        ]
        if event == "arriba" and pos_x > 1 and self.mapa_juego[pos_x - 2][pos_y - 1] == "-":
            self.senal_movimiento_lugi.emit(*senal_emit[0])
            self.movimiento_arriba += 1
            self.guardar_movimiento(pos_x - 2, pos_y - 1, pos_x - 1, pos_y - 1)

        elif event == "abajo" and pos_x < 14 and self.mapa_juego[pos_x][pos_y - 1] == "-":
            self.senal_movimiento_lugi.emit(*senal_emit[1])
            self.movimiento_abajo += 1
            self.guardar_movimiento(pos_x, pos_y - 1, pos_x - 1, pos_y - 1)

        elif event == "izquierda" and pos_y > 1 and self.mapa_juego[pos_x - 1][pos_y - 2] == "-":
            self.senal_movimiento_lugi.emit(*senal_emit[2])
            self.movimiento_izquierda += 1
            self.guardar_movimiento(pos_x - 1, pos_y - 2, pos_x - 1, pos_y - 1)

        elif event == "derecha" and pos_y < 9 and self.mapa_juego[pos_x - 1][pos_y] == "-":
            self.senal_movimiento_lugi.emit(*senal_emit[3])
            self.movimiento_derecha += 1
            self.guardar_movimiento(pos_x - 1, pos_y, pos_x - 1, pos_y - 1)
        else:
            casilla_ocupada = True
# animacion, pos_x, pos_y, movimiento
        if event == "derecha" and pos_y < 9 and casilla_ocupada:
            if self.dano_enemigo(pos_x - 1, pos_y) == "damage":
                self.senal_dano_luigi.emit(self.vidas_luigi)
            elif self.dano_enemigo(pos_x - 1, pos_y) == "win":
                self.senal_ganar_partida.emit()
                self.senal_movimiento_lugi.emit(*senal_emit[3])

            elif self.dano_enemigo(pos_x - 1, pos_y) == "rock":
                self.movimiento_roca(pos_x - 1, pos_y, "derecha")

        elif event == "izquierda" and pos_y > 1 and casilla_ocupada:
            if self.dano_enemigo(pos_x - 1, pos_y - 2) == "damage":
                self.senal_dano_luigi.emit(self.vidas_luigi)
            elif self.dano_enemigo(pos_x - 1, pos_y - 2) == "win":
                self.senal_ganar_partida.emit()
                self.senal_movimiento_lugi.emit(*senal_emit[2])
                
            elif self.dano_enemigo(pos_x - 1, pos_y - 2) == "rock":
                self.movimiento_roca(pos_x - 1, pos_y - 2, "izquierda")
        
        elif event == "arriba" and pos_x > 1 and casilla_ocupada:
            if self.dano_enemigo(pos_x - 2, pos_y - 1) == "damage":
                self.senal_dano_luigi.emit(self.vidas_luigi)
            elif self.dano_enemigo(pos_x - 2, pos_y - 1) == "win":
                self.senal_ganar_partida.emit()
                self.senal_movimiento_lugi.emit(*senal_emit[0])

            elif self.dano_enemigo(pos_x - 2, pos_y - 1) == "rock":
                self.movimiento_roca(pos_x - 2, pos_y - 1, "arriba")
        
        elif event == "abajo" and pos_x < 14 and casilla_ocupada:
            if self.dano_enemigo(pos_x, pos_y - 1) == "damage":
                self.senal_dano_luigi.emit(self.vidas_luigi)
            elif self.dano_enemigo(pos_x, pos_y - 1) == "win":
                self.senal_ganar_partida.emit()
                self.senal_movimiento_lugi.emit(*senal_emit[1])

            elif self.dano_enemigo(pos_x, pos_y - 1) == "rock":
                self.movimiento_roca(pos_x, pos_y - 1, "abajo")

    def movimiento_roca(self, pos_x, pos_y, dir):
        if dir == "derecha" and pos_y < 8 and self.mapa_juego[pos_x][pos_y + 1] == "-":
            self.eliminar_roca(pos_x, pos_y + 1, pos_x, pos_y, dir)

        elif dir == "izquierda" and pos_y > 0 and self.mapa_juego[pos_x][pos_y - 1] == "-":
            self.eliminar_roca(pos_x, pos_y - 1, pos_x, pos_y, dir)

        elif dir == "arriba" and pos_x > 0 and self.mapa_juego[pos_x - 1][pos_y] == "-":
            self.eliminar_roca(pos_x - 1, pos_y, pos_x, pos_y, dir)

        elif dir == "abajo" and pos_x < 13 and self.mapa_juego[pos_x + 1][pos_y] == "-":
            self.eliminar_roca(pos_x + 1, pos_y, pos_x, pos_y, dir)
    
    def eliminar_roca(self, pos_x, pos_y, ant_x, ant_y, dir):
        self.mapa_juego[ant_x][ant_y] = "-"
        self.mapa_juego[pos_x][pos_y] = "R"
        self.senal_mover_roca.emit(pos_x, pos_y, dir) # Emitir senal para modificar estado
        
    def eliminar_fantasmas(self, pos_x, pos_y) -> None: # Implementado para el cheat code
        self.mapa_juego[pos_x - 1][pos_y - 1] = "-"

    def eliminar_luigi(self, pos_x, pos_y) -> None: # Simulacion del movimiento de luigi
        self.mapa_juego[pos_x - 1][pos_y - 1] = "-"


class GhostJuego(QObject):
    senal_movimiento_fantasma = pyqtSignal(int, int)

    def __init__(self, pos_x, pos_y, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ponderador_velocidad_fantasmas = pa.PONDERADOR_VELOCIDAD_FANTASMAS
        self.pos_x = pos_x
        self.pos_y = pos_y

    def tiempo_movimiento(self) -> float: # En seguntos
        return (1 / self.ponderador_velocidad_fantasmas)
    
class GhostVertical(GhostJuego):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.qt_movimiento = QTimer()
        self.qt_movimiento.timeout.connect(self.movimiento_fantasma)

    def movimiento_fantasma(self, mapa_juego) -> None:
        sleep(self.tiempo_movimiento())
        if 0 < self.pos_x < 13:
            pass


    
