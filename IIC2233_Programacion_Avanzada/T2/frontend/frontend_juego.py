from frontend import elementos_graficos as eg
from backend import funciones as fn
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QPushButton
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSound
from time import sleep
import sys
import parametros as pa


class VentanaJuego(QWidget):
    # Senales para comunicarse con el backend
    senal_keypress_mov = pyqtSignal(str, int, int)
    senal_keypress_pausa = pyqtSignal(str)
    senal_crear_juego = pyqtSignal(int, int, list)
    senal_eliminar_fantasmas = pyqtSignal(int, int)
    senal_eliminar_luigi = pyqtSignal(int, int)
    senal_volver_jugar = pyqtSignal()
    senal_modificar_vida = pyqtSignal(int)
    senal_modificar_mov = pyqtSignal(int)
    senal_mostrar_popup = pyqtSignal(float, str, str)
    senal_cuadro_nombre = pyqtSignal(str)
    senal_modificar_mapa = pyqtSignal(list)

    # Nombre usuario y posicion inicial
    nom_usr = ''
    pos_x, pos_y = 0, 0 # Posicion inicial
    vidas_utilizadas = 1

    # Mapa del juego
    mapa_grilla, lugar_enemigos, mapa_leido = {}, [], [] # Mapas que son enviados al backend

    # Properties
    __vidas_luigi = pa.CANTIDAD_VIDAS
    __tiempo_rest = pa.TIEMPO_CUENTA_REGRESIVA

    # Variables que se encargan de los eventos del usuario
    partida_pausa: bool = False
    partida_ganada: bool = False
    juego_iniciado: bool = False
    keypress_l, keypress_i, keypress_k = False, False, False
    keypress_i1, keypress_n, keypress_f = False, False, False
    keypress_g = False
    

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs) # Constructor de la clase padre
        # Configuracion ventana
        self.setWindowTitle(f"Partida de DDCCazafantasmas")
        self.setWindowIcon(QIcon(pa.PATH_SPRITES[1]))
        self.setFixedSize(600, 680)
        self.mostrar_elementos()
        self.conecciones_juego()
        self.__cheatcode_kill, self.__cheatcode_life = False, False
        self.qt_reloj = QTimer()
        self.qt_reloj.timeout.connect(self.actualizar_tiempo)
    
    # Properties
    @property
    def vidas_luigi(self) -> int:
        return self.__vidas_luigi
    
    @vidas_luigi.setter # Se encarga de mostrar el fin de la partida por vidas
    def vidas_luigi(self, value) -> None:
        if value <= 0 and not self.cheatcode_life:
            self.label_vida.setText(f"Vida: 0")
            self.sonido_perder = QSound(pa.PATH_SONIDO_PERDER)
            self.sonido_perder.play()
            self.senal_mostrar_popup.emit(0, self.nom_usr, "perdido por quedarte sin vidas")
            self.volver_jugar() # Resetear el juego
        else:
            self.__vidas_luigi = value
            self.label_vida.setText(f"Vida: {self.vidas_luigi}")
            self.vidas_utilizadas += 1
            
    @property
    def tiempo_rest(self) -> int:
        return self.__tiempo_rest
    
    @tiempo_rest.setter # Se encarga de mostrar el fin de la partida por tiempo
    def tiempo_rest(self, value) -> None:
        if value <= 0:
            self.tiempo_partida.setText(f"Tiempo: {0}:{0}")
            self.sonido_perder = QSound(pa.PATH_SONIDO_PERDER)
            self.sonido_perder.play()
            self.senal_mostrar_popup.emit(0, self.nom_usr,
            "perdido por quedarte sin tiempo")
            self.volver_jugar()
        else:
            self.__tiempo_rest = value

    @property
    def chea__cheatcode_kill(self) -> bool:
        return self.__cheatcode_kill
    
    @chea__cheatcode_kill.setter # Hacer valido el cheatcode
    def chea__cheatcode_kill(self, value) -> None:
        if value:
            [self.eliminar_fantasmas(i) for i in self.lugar_enemigos]
            self.lugar_enemigos.clear()
            self.mostrar_cheat.setText("Cheat enemigos")
        else:
            self.__cheatcode_kill = value

    @property
    def cheatcode_life(self) -> bool:
        return self.__cheatcode_life
    
    @cheatcode_life.setter # Hacer valido el cheatcode de vida y tiempo infinitos
    def cheatcode_life(self, value) -> None:
        if value: # int((pa.MULTIPLICADOR_PUNTAJE * self.tiempo_rest) / self.vidas_luigi)
            self.vidas_luigi = 9999
            self.qt_reloj.stop() # Detener el reloj
            puntaje_jugador = pa.MULTIPLICADOR_PUNTAJE * self.tiempo_rest
            self.puntaje_jugador = puntaje_jugador / self.vidas_utilizadas
            self.mostrar_cheat.setText("Cheat inf")
        else:
            self.__cheatcode_life = value

    # Elementos graficos de la ventana de juego
    def mostrar_elementos(self) -> None:
        self.label_vida = QLabel(f"Vida: {self.vidas_luigi}", self)
        self.label_vida.setGeometry(30, 150, 120, 35)
        self.label_vida.setStyleSheet("border: 1px solid black; background-color: white;")
        self.label_vida.setAlignment(Qt.AlignCenter)

        self.boton_pausa = QPushButton("Pausa", self)
        self.boton_pausa.setGeometry(30, 260, 120, 40)
        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.setGeometry(30, 320, 120, 40)

        boton_limpiar = QPushButton("Limpiar", self)
        boton_limpiar.setGeometry(30, 560, 120, 40)
        boton_limpiar.setEnabled(False)
        boton_jugar = QPushButton("Jugar", self)
        boton_jugar.setGeometry(30, 620, 120, 40)
        boton_jugar.setEnabled(False)

        self.texto_estado = QLabel("Estado:", self)
        self.texto_estado.setGeometry(290, 10, 50, 35)
        self.cuadro_estado = QLabel("", self)
        self.cuadro_estado.setGeometry(370, 10, 170, 35)
        self.cuadro_estado.setStyleSheet("border: 1px solid black; background-color: white;")

        self.texto_cheat = QLabel("Cheat:", self)
        self.texto_cheat.setGeometry(30, 10, 50, 35)
        self.mostrar_cheat = QLabel("", self)
        self.mostrar_cheat.setGeometry(100, 10, 150, 35)
        self.mostrar_cheat.setStyleSheet("border: 1px solid black; background-color: white;")

        self.tiempo_partida = QLabel("", self)
        self.tiempo_partida.setGeometry(30, 100, 120, 35)
        self.tiempo_partida.setStyleSheet("border: 1px solid black; background-color: white;")
        self.tiempo_partida.setAlignment(Qt.AlignCenter)

    def mostrar_grilla(self, mapa_leido: list, nom_usr) -> None: # Setear los iconos en la grilla
        self.nom_usr = nom_usr
        self.mapa_grilla = eg.mostrar_grilla(self) # Obtener grilla
        self.mapa_leido = mapa_leido # Respaldo del mapa
        self.iniciar_partida() # Iniciar el juego
        for i in range(14):
            for k in range(9):
                if (path_icon := fn.verificar_icono(mapa_leido[i][k])) != None:
                    self.mapa_grilla[f"({i + 1}, {k + 1})"].setIcon(QIcon(path_icon))
                    arg_icon = self.mapa_grilla[f"({i + 1}, {k + 1})"].size()
                    self.mapa_grilla[f"({i + 1}, {k + 1})"].setIconSize(arg_icon)
                if mapa_leido[i][k] == "L": # Posicion inicial de luigi
                    self.pos_x, self.pos_y = i + 1, k + 1
                    self.pos_inicial = (i + 1, k + 1)
                if mapa_leido[i][k] == "H" or mapa_leido[i][k] == "V": # Posicion de los fantasmas
                    self.lugar_enemigos.append((i + 1, k + 1))
              
        self.senal_crear_juego.emit(i + 1, k + 1, mapa_leido) # Mandar ubicacion de luigi
        self.show() # Mostrar ventana
                
    # Eventos del usuario
    def keyPressEvent(self, event: QKeyEvent) -> None: # SALA DE AYUDA
        # Movimiento del personaje y los eventos con el teclado
        if event.key() == Qt.Key_A:
            self.senal_keypress_mov.emit("izquierda", self.pos_x, self.pos_y)
        elif event.key() == Qt.Key_W:
            self.senal_keypress_mov.emit("arriba", self.pos_x, self.pos_y)
        elif event.key() == Qt.Key_D:
            self.senal_keypress_mov.emit("derecha", self.pos_x, self.pos_y)
        elif event.key() == Qt.Key_S:
            self.senal_keypress_mov.emit("abajo", self.pos_x, self.pos_y)
        elif event.key() == Qt.Key_P and not event.isAutoRepeat():
            self.pausar_partida()
        elif event.key() == Qt.Key_L:
            self.keypress_l = True
        elif event.key() == Qt.Key_I:
            self.keypress_i = True
            self.keypress_i1 = True
        elif event.key() == Qt.Key_K:
            self.keypress_k = True
        elif event.key() == Qt.Key_N:
            self.keypress_n = True
        elif event.key() == Qt.Key_F:
            self.keypress_f = True
        elif event.key() == Qt.Key_G and self.partida_ganada:
            self.keypress_g = True
            puntaje_partida = (pa.MULTIPLICADOR_PUNTAJE * self.tiempo_rest)
            self.puntaje_jugador = int(puntaje_partida / self.vidas_utilizadas)
            self.ganar_partida() # Ganar la partida
        # Activar los codigos nucleares del juego
        if self.keypress_l and self.keypress_k and self.keypress_i:
            self.chea__cheatcode_kill = True
        if self.keypress_i1 and self.keypress_n and self.keypress_f:
            self.cheatcode_life = True
        sleep(pa.AJUSTAR_VELOCIDAD) # Velocidad con la que se mueve luigi

    # Conecciones del juego
    def conecciones_juego(self) -> None:
        self.boton_pausa.clicked.connect(self.pausar_partida)
        self.boton_salir.clicked.connect(sys.exit)

    # Funciones del juego
    def eliminar_fantasmas(self, key: tuple) -> None:
        self.mapa_grilla[f"({key[0]}, {key[1]})"].setIcon(QIcon(""))
        self.senal_eliminar_fantasmas.emit(key[0], key[1])

    def mover_roca(self, pos_x, pos_y, dir):
        self.mapa_grilla[f"({pos_x + 1}, {pos_y + 1})"].setIcon(QIcon(pa.PATH_SPRITES[3]))
        set_icon = self.mapa_grilla[f"({pos_x + 1}, {pos_y + 1})"].size()
        self.mapa_grilla[f"({pos_x + 1}, {pos_y + 1})"].setIconSize(set_icon)
        self.senal_keypress_mov.emit(dir, self.pos_x, self.pos_y)
        
    def iniciar_partida(self) -> None:
        self.juego_iniciado = True
        self.qt_reloj.start(1000)
        self.tiempo_partida.setText(f"Tiempo : {fn.tiempo_str(self.tiempo_rest)}")

    def actualizar_tiempo(self) -> None:
        self.tiempo_rest -= 1
        self.tiempo_partida.setText(f"Tiempo : {fn.tiempo_str(self.tiempo_rest)}")

    def actualizar_vida(self, dano: int) -> None:
        self.vidas_luigi = dano
        self.mapa_grilla[f"({self.pos_x}, {self.pos_y})"].setIcon(QIcon(""))
        set_icon = QIcon(pa.PATH_SPRITES[0])
        self.mapa_grilla[f"({self.pos_inicial[0]}, {self.pos_inicial[1]})"].setIcon(set_icon)
        self.senal_eliminar_luigi.emit(self.pos_x, self.pos_y)
        self.pos_x, self.pos_y = self.pos_inicial[0], self.pos_inicial[1]
        self.cuadro_estado.setText("Perdiste una vida")
        for i in range(14):
            for k in range(9):
                if (path_icon := fn.verificar_icono(self.mapa_leido[i][k])) != None:
                    self.mapa_grilla[f"({i + 1}, {k + 1})"].setIcon(QIcon(path_icon))
                    arg_icon = self.mapa_grilla[f"({i + 1}, {k + 1})"].size()
                    self.mapa_grilla[f"({i + 1}, {k + 1})"].setIconSize(arg_icon)
                else:
                    self.mapa_grilla[f"({i + 1}, {k + 1})"].setIcon(QIcon(""))

                if self.mapa_leido[i][k] == "L":
                    self.pos_x, self.pos_y = i + 1, k + 1
                    self.pos_inicial = (i + 1, k + 1)
                if self.mapa_leido[i][k] == "H" or self.mapa_leido[i][k] == "V":
                    self.lugar_enemigos.append((i + 1, k + 1))
        self.senal_modificar_mapa.emit(self.mapa_leido)

    def mover_luigi(self, animacion, pos_x, pos_y, movimiento) -> None:
        self.mapa_grilla[f"({pos_x}, {pos_y})"].setIcon(QIcon(animacion[movimiento]))
        set_icon = self.mapa_grilla[f"({pos_x}, {pos_y})"].size()
        self.mapa_grilla[f"({pos_x}, {pos_y})"].setIconSize(set_icon)
        self.mapa_grilla[f"({self.pos_x}, {self.pos_y})"].setIcon(QIcon(""))
        self.pos_x, self.pos_y = pos_x, pos_y

    def ganar_partida(self) -> None:
        self.partida_ganada = True
        self.cuadro_estado.setText("Presiona G para ganar")
        self.blockSignals(True)
        if self.keypress_g:
            self.blockSignals(False)
            self.sonido_ganar = QSound(pa.PATH_SONIDO_GANAR)
            self.sonido_ganar.play()
            self.senal_mostrar_popup.emit(self.puntaje_jugador, self.nom_usr, "ganado la partida")
            self.volver_jugar()
            
    def pausar_partida(self) -> None:
        if not self.partida_pausa:
            self.blockSignals(True)
            self.partida_pausa = True
            self.qt_reloj.stop()
        elif self.partida_pausa:
            self.blockSignals(False)
            self.partida_pausa = False
            self.qt_reloj.start(1000)

    def volver_jugar(self) -> None:
        self.blockSignals(False) # Desbloquear senales
        # Setear las variables graficas por default
        self.qt_reloj.stop()
        self.cuadro_estado.setText("")
        self.mostrar_cheat.setText("")
        self.vidas_luigi = pa.CANTIDAD_VIDAS
        self.tiempo_rest = pa.TIEMPO_CUENTA_REGRESIVA
        self.tiempo_partida.setText(f"Tiempo: {fn.tiempo_str(self.tiempo_rest)}")
        self.puntaje_jugador = 0
        # Setear los eventos por default
        self.keypress_l, self.keypress_i, self.keypress_k = False, False, False
        self.keypress_i1, self.keypress_n, self.keypress_f = False, False, False
        self.keypress_g = False
        self.cheatcode_kill = False
        self.cheatcode_life = False
        self.partida_ganada = False
        self.puntaje_jugador = 0
        self.vidas_utilizadas = 1
        # Senales y los qtimer por default
        self.senal_modificar_vida.emit(self.vidas_luigi)
        self.senal_cuadro_nombre.emit("") # Setear a "" el cuadro del inicio
        # Ocultar la ventana, para mostrar la ventana de inicio
        self.hide()

