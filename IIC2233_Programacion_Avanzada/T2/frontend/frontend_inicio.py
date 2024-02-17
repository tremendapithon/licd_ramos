from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon
from os import path
from PyQt5.QtCore import pyqtSignal
from backend.funciones import leer_partida
from frontend import elementos_graficos as eg
import sys
import parametros as pa

window_name, base_class = uic.loadUiType(pa.PATH_QTDESIGNER) # Cargar archivo .ui


class VentanaInicio(window_name, base_class):
    # Senales que se conectan con el main y el backend
    senal_click_inicio = pyqtSignal(str, str)
    senal_iniciar_constructor = pyqtSignal()
    senal_iniciar_juego = pyqtSignal(list, str)
    senal_nombre_jugador = pyqtSignal(str)
    nom_usr = ""

    def __init__(self, mapas_guardados: list) -> None:
        super().__init__() # Constructor de la clase padre
        # Configuracion ventana 
        self.setupUi(self)
        self.mapas_guardados = mapas_guardados
        self.setWindowTitle("Inicio DCCazafantasmas")
        self.setWindowIcon(QIcon(pa.PATH_SPRITES[2])) 
        self.setFixedSize(600, 680)
        self.elementos_ventana()
        self.conecciones_botones()
            
    # Elementos graficos de la ventana
    def elementos_ventana(self) -> None:
        background_fondo = QPixmap(pa.PATH_BACKGROUND)  ###CITAR README
        set_palette = self.palette()
        set_palette.setBrush(QPalette.Background, QBrush(background_fondo))
        self.setPalette(set_palette)
        self.MainLogo.setPixmap(QPixmap(pa.PATH_LOGO))
        self.label.setStyleSheet("QLabel {color: white;}")
        self.MenuOpcion.addItems(self.mapas_guardados)
        self.MenuOpcion.addItem("nuevo mapa")
        
    # Conecciones y senales de la ventana
    def conecciones_botones(self) -> None:
        self.MainInicio.clicked.connect(self.click_jugar)
        self.MainSalir.clicked.connect(self.click_salir)

    def click_jugar(self) -> None: # Click para jugar
        self.nom_usr = self.MainNombre.text()
        self.senal_click_inicio.emit(self.MainNombre.text(), self.MenuOpcion.currentText())

    def click_salir(self): # Click para salir
        sys.exit()

    def abrir_constructor(self) -> None:
        self.senal_iniciar_constructor.emit()
        self.senal_nombre_jugador.emit(self.nom_usr)
        self.hide()

    def abrir_juego(self, mapa_seleccionado: str) -> None:
        self.senal_iniciar_juego.emit(leer_partida(path.join("mapas", mapa_seleccionado)), 
                                self.nom_usr)
        self.MainNombre.setText("")
        self.hide()

    # Funciones de la ventana
    def warning_popup(self, tipo_error) -> None: 
        eg.mostrar_popup(f"El nombre de usario no es valido, porque {tipo_error}.",
                        "Error: Nombre de usuario no valido")
 
