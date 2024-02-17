from PyQt5.QtCore import pyqtSignal
from Scripts import funtion_json as lj
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton, QMainWindow)
from os import path
import sys


class VentanaInicio(QMainWindow):
    senal_ingresar_juego = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(600, 480)
        self.setWindowTitle("En espera...")
        self.init_elements()
        self.init_signals()
    
    def init_elements(self):
        # Background del inicio
        dict_background= lj.leer_json("parametros.json")["PATH_BACKGROUND"]
        path_background = path.join(*(list(map(lambda x: dict_background[x], dict_background))))
        background_fondo = QPixmap(path_background).scaled(self.size(), 1)
        set_palette = self.palette()
        set_palette.setBrush(QPalette.Background, QBrush(background_fondo))
        self.setPalette(set_palette)

        self.label_titulo = QLabel(self)
        self.label_titulo.setText("SALA DE ESPERA...")
        self.label_titulo.setGeometry(150, 50, 380, 50)
        self.label_titulo.setStyleSheet("font-size: 40px; font-family: Bold; color: white;")

        self.boton_ingresar = QPushButton(self)
        self.boton_ingresar.setText("INGRESAR")
        self.boton_ingresar.setGeometry(150, 350, 320, 35)
        self.boton_ingresar.setStyleSheet("font-family: Bold; color: white; font-size: 15px;"
                                    "background-color: #1f1f1f; border-radius: 10px;")
        
        self.boton_salir = QPushButton(self)
        self.boton_salir.setText("SALIR")
        self.boton_salir.setGeometry(150, 400, 320, 35)
        self.boton_salir.setStyleSheet("font-family: Bold; color: white; font-size: 15px;"
                                    "background-color: #1f1f1f; border-radius: 10px;")
        usr_log = lj.leer_json("parametros.json")["PATH_PLAYER"]
        path_userprofile = path.join(*(list(map(lambda x: usr_log[x], usr_log))))

        self.dict_users, self.nom_usrs = {}, {}
        for i in range(4):
            self.dict_users[i] = QLabel(self)
            self.dict_users[i].setPixmap(QPixmap(path_userprofile).scaled(90, 90, 1))
            self.dict_users[i].setGeometry(30 + 150 * (i), 150, 90, 90)
            self.nom_usrs[i] = QLabel(self)
            self.nom_usrs[i].setGeometry(30 + 150 * (i), 250, 100, 30)
            self.nom_usrs[i].setStyleSheet("font-size: 18px; font-family: Bold; color: white;")

    def init_signals(self):
        self.boton_salir.clicked.connect(sys.exit)
        self.boton_ingresar.clicked.connect(self.senal_ingresar_juego.emit)

    def actualizar_jugadores(self, jugadores: dict):
        lista_jugadores = jugadores["clientes_conectados"]
        for i in range(len(lista_jugadores)):
            self.nom_usrs[i].setText(f"   {lista_jugadores[i]}")

        if len(lista_jugadores) < 4:
            for i in range(len(lista_jugadores), 4):
                self.nom_usrs[i].setText(f"   Jugador {i+1}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.exit(app.exec_())