from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from Scripts.funtion_json import leer_json
import sys


# No se puede acceder al servidor
class InicioError(QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setFixedSize(320, 160)
        self.setWindowTitle("Error de conexión")
        self.setStyleSheet("background-color: #111111;")
        self.label_error = QLabel(self)
        self.label_error.setText("No se pudo conectar con el servidor...")
        self.label_error.setGeometry(30, 0, 270, 80)
        self.label_error.setStyleSheet("font-family: Bold; color: white; font-size: 15px;")
        self.boton_salir = QPushButton(self)
        self.boton_salir.setText("SALIR")
        self.boton_salir.setGeometry(30, 90, 270, 35)
        self.boton_salir.setStyleSheet("font-size: 20px; font-family: Arial; color: white;"
                                       "background-color: #1f1f1f; border-radius: 10px;")
        self.boton_salir.clicked.connect(sys.exit)

# Cuando el servidor se ha caido
class ServerError(QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setFixedSize(320, 160)
        self.setWindowTitle("Error de servidor")
        self.setStyleSheet("background-color: #111111;")
        self.label_error = QLabel(self)
        self.label_error.setText(leer_json("parametros.json")["SERVER_ERROR"])
        self.label_error.setGeometry(30, 10, 270, 80)
        self.label_error.setStyleSheet("font-family: Bold; color: white; font-size: 15px;")
        self.label_error.setWordWrap(True)
        self.label_error.setAlignment(Qt.AlignCenter)
        self.boton_salir = QPushButton(self)
        self.boton_salir.setText("SALIR")
        self.boton_salir.setGeometry(30, 110, 270, 35)
        self.boton_salir.setStyleSheet("font-size: 20px; font-family: Arial; color: white;"
                                       "background-color: #1f1f1f; border-radius: 10px;")
        self.boton_salir.clicked.connect(sys.exit)

# Informacion al cliente
class InformacionCliente(QWidget):
    senal_ocultar_ventanas = pyqtSignal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setFixedSize(320, 200)
        self.setWindowTitle("Información del cliente")
        self.setStyleSheet("background-color: #111111;")
        self.label_aviso = QLabel(self)
        self.boton_salir = QPushButton(self)
        self.boton_salir.setText("SALIR")
        self.boton_salir.setGeometry(30, 90, 270, 35)
        self.boton_salir.setStyleSheet("font-family: Bold; color: white; font-size: 15px;"
                                       "background-color: #2f2f2f; border-radius: 10px;")
        self.boton_salir.clicked.connect(sys.exit)
        self.volver_intentar = QPushButton(self)
        self.volver_intentar.setText("ACEPTAR")
        self.volver_intentar.setGeometry(30, 130, 270, 35)
        self.volver_intentar.setStyleSheet("font-family: Bold; color: #f1f1f1; font-size: 15px;"
                                           "background-color: #2f2f2f; border-radius: 10px;")
        self.volver_intentar.clicked.connect(self.senal_ocultar_ventanas.emit)
        
    def init_popup(self, msg: str) -> None:
        self.label_aviso.setText(msg)
        self.label_aviso.setGeometry(30, 0, 270, 90)
        self.label_aviso.setWordWrap(True)
        self.label_aviso.setAlignment(Qt.AlignCenter)
        self.label_aviso.setStyleSheet("font-family: Bold; color: white; font-size: 15px;")
        self.show()

class VolverIntentar(InformacionCliente):
    senal_volver_intentar = pyqtSignal()
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.volver_intentar.setText("VOLVER A INTENTAR")
        self.volver_intentar.clicked.connect(self.run_again)

    def run_again(self) -> None:
        self.senal_volver_intentar.emit()

    def init_popup(self) -> None:
        super().init_popup("Puede volver a conectarse con el servidor" +
                           ", pulse el botón volver a intentar")

class PushButton(QPushButton):
    senal_click_button = pyqtSignal(str)

    def __init__(self, texto: str, pos: list, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.texto = texto
        self.setText(self.texto)
        self.setGeometry(*pos)
        self.setStyleSheet("font-family: Bold; color: #ffffff; font-size: 15px;"
                           "background-color: #1f1f1f; border-radius: 5px;")

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        self.senal_click_button.emit(self.texto)

        