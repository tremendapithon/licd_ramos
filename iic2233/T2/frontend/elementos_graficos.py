from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from sys import exit
import parametros as pa


# Clase que modela las casillas del mapa
class BotonGrilla(QPushButton): # citar en readme
    senal_boton_grilla = pyqtSignal(str, tuple)

    def __init__(self, nombre, pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre: str = nombre
        self.pos: tuple = pos
        self.nombre_icon = ''

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.senal_boton_grilla.emit(self.nombre, self.pos)

    def name_icon(self, nombre):
        self.nombre_icon: str = nombre


# Clase que representa las imagenes de los personajes
class BotonPersonaje(QPushButton):
    senal_boton_personaje = pyqtSignal(str)

    def __init__(self, nombre, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.nombre: str = nombre

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        self.senal_boton_personaje.emit(self.nombre)
        
    def set_icon(self) -> str: # Setear el icono en la casilla
        return pa.PATH_SPRITES[pa.LISTA_PERSONAJES.index(self.nombre)]
    
class VentanaResultado(QWidget):
    senal_volver_jugar = pyqtSignal()
    senal_salir = pyqtSignal()
    senal_ocultar_ventana = pyqtSignal()
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def mostrar_texto(self, puntaje, nom_usr, resultado):
        self.setWindowTitle(f"Puntaje: Haz {resultado}")
        self.setStyleSheet("background-color: #1f1f1f;")
        self.setWindowIcon(QIcon(pa.PATH_SPRITES[5]))
        self.setFixedSize(320, 200)
        label_text = QLabel(self)
        label_text.setText(f"{nom_usr}\nTu puntaje es: {puntaje}\nHaz {resultado}")
        label_text.setStyleSheet("color: white;")
        label_text.setGeometry(20, 20, 300, 80)
        label_text.setAlignment(Qt.AlignCenter)
        boton_aceptar = QPushButton("Volver a jugar", self)
        boton_aceptar.setGeometry(100, 100, 100, 40)
        boton_aceptar.setStyleSheet("background-color: #1f1f1f; color: white;")
        boton_salir =  QPushButton("Salir", self)
        boton_salir.setGeometry(100, 150, 100, 40)
        boton_salir.setStyleSheet("background-color: #1f1f1f; color: white;")
        boton_aceptar.clicked.connect(self.mostrar_anuncio)
        boton_salir.clicked.connect(self.senal_salir.emit)
        self.show()

    def mostrar_anuncio(self):
        self.senal_ocultar_ventana.emit()
        self.senal_volver_jugar.emit()
 
# Funcion para mostrar los pop-up durante el juego
def mostrar_popup(mensaje, titulo) -> None:
    mensaje_error = QMessageBox()
    mensaje_error.setWindowTitle(titulo)
    mensaje_error.setText(mensaje)
    mensaje_error.setIcon(QMessageBox.Information)
    mensaje_error.setFixedSize(320, 500)
    mensaje_error.setStandardButtons(QMessageBox.Ok)
    mensaje_error.show()
    mensaje_error.exec_()

# Funcion que crea el mapa
def mostrar_grilla(self) -> None:
    mapa_grilla = {}
    for largo in range(pa.LARGO_GRILLA):
        for ancho in range(pa.ANCHO_GRILLA):
            casilla_grilla = BotonGrilla(f"({largo}, {ancho})", (largo, ancho), self)
            casilla_grilla.setGeometry(180 + ancho * 35, 80 + largo * 35, 35, 35)
            casilla_grilla.setStyleSheet("border: 1px solid black; background-color: #1f1f1f;")
            if largo == 0 or ancho == 0 or largo == 15 or ancho == 10:
                casilla_grilla.setIcon(QIcon(pa.PATH_BORDERMAP))
                casilla_grilla.setIconSize(casilla_grilla.size())
            mapa_grilla[f"({largo}, {ancho})"] = casilla_grilla
    return mapa_grilla
    




