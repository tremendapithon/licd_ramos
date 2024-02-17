from Scripts.funtion_json import leer_json
from Scripts.funtions import ajustar_label, verificar_pos
from frontend.elementos_frontend import PushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from os import path



class VentanaJuego(QWidget):
    maximo_jugadores = leer_json("parametros.json")["MAXIMO_JUGADORES"]
    pos_botones = leer_json("parametros.json")["POS_BOTONES"]
    nombre_botones = leer_json("parametros.json")["NOMBRE_BOTONES"]
    VIDA_JUGADOR = leer_json("parametros.json")["NUMERO_VIDAS"]
    senal_boton_presionado = pyqtSignal(dict)
    senal_click_button = pyqtSignal(str)
    id_usuario = ''
    socket_cliente = None
    cantidad_jugadores = 0
    primera_vez = True

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(600, 480)
        self.label_user()
        self.init_gui()
        
    def init_gui(self):
        dict_background= leer_json("parametros.json")["PATH_BACKGROUND_GAME"]
        path_background = path.join(*(list(map(lambda x: dict_background[x], dict_background))))
        background_fondo = QPixmap(path_background).scaled(self.size(), 1)
        set_palette = self.palette()
        set_palette.setBrush(QPalette.Background, QBrush(background_fondo))
        self.setPalette(set_palette)
        self.dict_users, self.nom_usrs = {}, {}
        dict_usrlog = leer_json("parametros.json")["PATH_PLAYER"]
        path_userprofile = path.join(*(list(map(lambda x: dict_usrlog[x], dict_usrlog))))

        for i in range(self.maximo_jugadores):
            self.dict_users[i] = QLabel(self)
            self.dict_users[i].setPixmap(QPixmap(path_userprofile).scaled(90, 90, 1))
            self.dict_users[i].setGeometry(*ajustar_label(i, 0))
            self.nom_usrs[i] = QLabel(self)
            self.nom_usrs[i].setGeometry(*ajustar_label(i, 60))
            self.nom_usrs[i].setStyleSheet("color: white; font-size: 15px; font-family: Arial")
            self.nom_usrs[i].setBuddy(self.dict_users[i])
            self.label_vida[i] = QLabel(f"Vida: {self.VIDA_JUGADOR}", self)
            self.label_vida[i].setGeometry(*ajustar_label(i, 80))
            self.label_vida[i].setStyleSheet("color: white; font-size: 15px; font-family: Arial")

        dict_logo = leer_json("parametros.json")["PATH_LOGO_DCCACHOS"]
        path_logo = path.join(*(list(map(lambda x: dict_logo[x], dict_logo))))
        self.dcc_logo = QLabel(self)

        self.dcc_logo.setPixmap(QPixmap(path_logo).scaled(250, 120, 1))
        self.dcc_logo.setGeometry(390, 350, 250, 120)

    def label_user(self):
        self.botones_juego, self.dados_label, self.label_vida = {}, {}, {}
        self.path_dado = path.join(*leer_json("parametros.json")["PATH_DADO_TOP"])

        for i, k in zip(self.pos_botones, self.nombre_botones):
            self.botones_juego[k] = PushButton(k, i, self)
            self.botones_juego[k].senal_click_button.connect(self.procesar_click)

        for k in range(self.maximo_jugadores):
            for i in range(2):
                self.dados_label[(k, i)] = QLabel(self)
                self.dados_label[(k, i)].setPixmap(QPixmap(self.path_dado).scaled(40, 40, 1))
                self.dados_label[(k, i)].setGeometry(*leer_json("parametros.json")
                                                    [f"POS_DADOS_P{k + 1}"][i])

        self.turno_jugador = QLabel("Turno de: ", self)
        self.turno_jugador.setGeometry(210, 10, 180, 30)
        self.turno_jugador.setStyleSheet("background-color: #1f1f1f; border-radius: 5px"
                                         ";color: white; font-size: 15px; font-family: Arial")
        self.valor_anunciar = QLabel("Valor anunciado 0", self)
        self.valor_anunciar.setGeometry(10, 10, 160, 30)
        self.valor_anunciar.setStyleSheet("background-color: #1f1f1f; border-radius: 5px"
                                          ";color: white; font-size: 15px; font-family: Arial")
        self.numero_turno = QLabel("Turno: ", self)
        self.numero_turno.setGeometry(450, 10, 100, 30)
        self.numero_turno.setStyleSheet("background-color: #1f1f1f; border-radius: 5px"
                                          ";color: white; font-size: 15px; font-family: Arial")
        self.texto_anunciar = QLineEdit("", self)
        self.texto_anunciar.setGeometry(110, 330, 75, 30)
        self.texto_anunciar.setStyleSheet("border-radius: 5px")
        
    def actualizar_label(self, msg: any, accion: str):
        if accion == "turno_jugador":
            self.turno_jugador.setText(msg)

        elif accion == "valor_anunciado":
            self.valor_anunciar.setText(f"Valor anunciado: {msg}")

        elif accion == "actualizar_turno":
            self.numero_turno.setText(f"Turno: {msg}")

        elif accion == "movimiento_invalido":
            if msg == self.id_usuario:
                self.texto_anunciar.setText("Invalido")

    def actualizar_dados(self, dados: dict):
        n_label = 0
        pos_label = 0
        for k in dados:
            if k == self.id_usuario:
                dado_1 = leer_json("parametros.json")[f"PATH_DADO_{dados[self.id_usuario][0]}"]
                dado_2 = leer_json("parametros.json")[f"PATH_DADO_{dados[self.id_usuario][1]}"]
                pos_label = verificar_pos(n_label)
                self.dados_label[(pos_label, 0)].setPixmap(QPixmap(path.join(*dado_1))
                                                        .scaled(40, 40, 1))
                self.dados_label[(pos_label, 1)].setPixmap(QPixmap(path.join(*dado_2))
                                                        .scaled(40, 40, 1))
            n_label += 1

        for i in range(4):
            if i != pos_label:
                self.dados_label[(i, 0)].setPixmap(QPixmap(self.path_dado).scaled(40, 40, 1))
                self.dados_label[(i, 1)].setPixmap(QPixmap(self.path_dado).scaled(40, 40, 1))
            
    def procesar_click(self, senal: str):
        if senal == "Anunciar":
            if self.texto_anunciar.text() != "" and self.texto_anunciar.text().isdigit():
                senal_emitir = {
                    "accion" : senal,
                    "id_usuario": self.id_usuario,
                    "mensaje" : int(self.texto_anunciar.text())
                }
                self.senal_boton_presionado.emit(senal_emitir)
            self.texto_anunciar.setText("")
        else:
            senal_emitir = {
                "accion" : senal,
                "id_usuario": self.id_usuario
            }
            self.senal_boton_presionado.emit(senal_emitir)

    def enviar_senal(self, senal):
        self.senal_boton_presionado.emit(senal)

    def actualizar_jugadores(self, jugadores: dict):
        self.cantidad_jugadores = len(jugadores["clientes_conectados"])
        lista_jugadores = jugadores["clientes_conectados"]
        for i in range(len(lista_jugadores)):
            self.nom_usrs[i].setText(lista_jugadores[i])

        if len(lista_jugadores) < 4:
            for i in range(len(lista_jugadores), 4):
                self.nom_usrs[i].setText(f"Jugador {i+1}")

    def set_user(self, id_usuario: str):
        self.id_usuario = id_usuario
        self.setWindowTitle(f"Ventana Juego de {self.id_usuario}")

