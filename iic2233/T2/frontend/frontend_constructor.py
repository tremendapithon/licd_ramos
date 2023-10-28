from PyQt5.QtWidgets import (QLabel, QWidget, QPushButton, QComboBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from frontend import elementos_graficos as eg
import parametros as pa


class VentanaConstructor(QWidget):
    senal_conectar_juego = pyqtSignal(object, str)
    senal_boton_grilla = pyqtSignal(str)
    
    cantidad_elementos: list = pa.CANTIDAD_ELEMENTOS.copy() # Cantidad predeterminada del mapa
    mapa_guardado: list = pa.MAPA_VACIO.copy()
    condicion_juego = 0 # Condicion para que pueda iniciar el juego
    personaje_seleccionado: bool = None
    boton_presionado: bool = False
    nom_usr = ''

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs) # Constructor de la clase padre
        # Configuracion ventana
        self.setWindowTitle("Constructor DCCazafantasmas")
        self.setFixedSize(600, 680)
        self.setWindowIcon(QIcon(pa.PATH_SPRITES[5]))
        self.mostrar_personajes()
        self.mostrar_grilla()
        self.conexion_botones()

    def agregar_nombre(self, nombre):
        self.nom_usr = nombre
    
    # Mostrar elementos graficos en la ventana
    def mostrar_personajes(self) -> None:
        # Botones con los personajes y bloques
        self.dict_botones: dict = {}
        for personajes in pa.LISTA_PERSONAJES:
            self.dict_botones[personajes] = eg.BotonPersonaje(personajes, self)

        # Agregar imagenes a los botones
        for personajes, path, num, pos_x in zip(pa.LISTA_PERSONAJES, pa.PATH_SPRITES,
                                        self.cantidad_elementos, range(7)):
            self.dict_botones[personajes].setIcon(QIcon(path))
            self.dict_botones[personajes].setText(f"  ({str(num)})")
            self.dict_botones[personajes].setGeometry(30, 120 + pos_x * 60, 100, 60)
            self.dict_botones[personajes].setStyleSheet(":pressed {background: transparent;}")
            self.dict_botones[personajes].setIconSize(self.dict_botones[personajes].size())

        # Botones extras en la pantalla
        self.seleccionar_personajes = QComboBox(self)
        self.seleccionar_personajes.setGeometry(30, 50, 100, 35)
        self.seleccionar_personajes.addItems(["Todos", "Bloques", "Entidades"])
        self.dict_botones["limpiar"] = QPushButton("Limpiar", self)
        self.dict_botones["limpiar"].setGeometry(30, 560, 100, 40)
        self.dict_botones["jugar"] = QPushButton("Jugar", self)
        self.dict_botones["jugar"].setGeometry(30, 620, 100, 40)

        # Mostrar personaje seleccionado -> Almacenar personaje
        self.texto_label = QLabel("Seleccionado:", self)
        self.texto_label.setGeometry(30, 10, 150, 35)
        self.texto_estado = QLabel("Estado:", self)
        self.texto_estado.setGeometry(290, 10, 50, 35)
        self.cuadro_estado = QLabel("", self)
        self.cuadro_estado.setGeometry(370, 10, 170, 35)
        self.cuadro_estado.setStyleSheet("border: 1px solid black; background-color: white;")
        self.mostrar_personaje = QLabel("", self)
        self.mostrar_personaje.setGeometry(160, 10, 100, 35)
        self.mostrar_personaje.setStyleSheet("border: 1px solid black; background-color: white;")

    def mostrar_grilla(self) -> None:
        self.mapa_grilla = eg.mostrar_grilla(self)

    # Senales y conexiones
    def conexion_botones(self) -> None:
        self.seleccionar_personajes.currentIndexChanged.connect(self.combobox_changed)
        self.dict_botones["jugar"].clicked.connect(self.click_jugar)
        self.dict_botones["limpiar"].clicked.connect(self.restablecer_mapa)

        conexion_botones: dict = {} # Dict con las conexiones de los botones
        for i in pa.LISTA_PERSONAJES:
            boton_conectar = self.dict_botones[i].senal_boton_personaje.connect(self.click_boton)
            conexion_botones[i] = boton_conectar

        conexion_grilla: dict = {} # Dict con las conexiones de la grilla
        for i in self.mapa_grilla:
            boton_conectar = self.mapa_grilla[i].senal_boton_grilla.connect(self.click_grilla)
            conexion_grilla[i] = boton_conectar

    def click_boton(self, nombre: str) -> None:
        self.cuadro_estado.setText("Se puede agregar")
        if self.boton_presionado == False:
            arg_funcion = [nombre, self.cantidad_elementos[pa.LISTA_PERSONAJES.index(nombre)]]
            self.actualizar_boton(*arg_funcion)
            self.desactivar_botones(*arg_funcion)
            self.personaje_seleccionado = self.dict_botones[nombre]
            self.boton_presionado = True

    def click_grilla(self, nombre: str, pos: tuple) -> None:
        casilla_libre = self.mapa_grilla[f"{nombre}"].nombre_icon == ''
        casilla_borde = nombre not in pa.LISTA_BORDES
        personaje_seleccionado = self.personaje_seleccionado
        boton_presionado = self.boton_presionado

        if personaje_seleccionado != None and casilla_libre and casilla_borde and boton_presionado:
            print(self.personaje_seleccionado.nombre)
            if personaje_seleccionado.nombre not in ["ghost_v", "ghost_h"]:
                guardar_personaje = personaje_seleccionado.nombre[0].upper()
                self.mapa_guardado[pos[0] - 1][pos[1] - 1] = guardar_personaje
                if personaje_seleccionado.nombre in ["luigi", "osstar"]:
                    self.condicion_juego += 1
            else:
                guardar_personaje = personaje_seleccionado.nombre[6].upper()
                self.mapa_guardado[pos[0] - 1][pos[1] - 1] = guardar_personaje

            self.mapa_grilla[f"{nombre}"].setIcon(QIcon(self.personaje_seleccionado.set_icon()))
            self.mapa_grilla[f"{nombre}"].setIconSize(self.mapa_grilla[f"{nombre}"].size())
            self.mapa_grilla[f"{nombre}"].name_icon(self.personaje_seleccionado.nombre)
            self.personaje_seleccionado = None
            self.boton_presionado = False
            self.mostrar_personaje.setText("")

        else:
            self.cuadro_estado.setText("No se puede agregar")
    
    def click_jugar(self) -> None:
        if self.condicion_juego == 2:
            self.senal_conectar_juego.emit(self.mapa_guardado, self.nom_usr)
            self.eliminar_mapa()
            self.hide()
        else:
            eg.mostrar_popup(pa.POPUP_ERROR_CONSTRUCTOR, "Error")

    # Funciones de la ventana
    def actualizar_boton(self, nombre, cantidad_elementos) -> None:
        if self.personaje_seleccionado == None and cantidad_elementos > 0:
            self.cantidad_elementos[pa.LISTA_PERSONAJES.index(nombre)] -= 1
            self.dict_botones[nombre].setText(f"  ({cantidad_elementos - 1})")
            self.mostrar_personaje.setText(nombre)

    def desactivar_botones(self, nombre, cantidad_elementos) -> None:
        if cantidad_elementos <= 1:
            self.dict_botones[nombre].setEnabled(False)

    def restablecer_mapa(self) -> None:
        eg.mostrar_popup("El mapa se ha eliminado", "Mapa eliminado")
        self.eliminar_mapa()

    def eliminar_mapa(self) -> None:
        self.condicion_juego = 0
        self.cantidad_elementos = pa.CANTIDAD_ELEMENTOS.copy()
        self.mostrar_personaje.setText("")
        self.cuadro_estado.setText("Mapa restablecido")
        self.mapa_guardado = [["-"] * (pa.ANCHO_GRILLA - 2) for i in range(pa.LARGO_GRILLA - 2)]
        self.personaje_seleccionado = None

        for key, num in zip(self.dict_botones, self.cantidad_elementos):
            self.dict_botones[key].setEnabled(True)
            self.dict_botones[key].setText(f"  ({num})")

        for key in self.mapa_grilla:
            if key not in pa.LISTA_BORDES:
                self.mapa_grilla[key].setIcon(QIcon(""))
                self.mapa_grilla[key].setIconSize(self.mapa_grilla[key].size())
                self.mapa_grilla[key].name_icon("")

    def combobox_changed(self, value) -> None: # Citar readme
        # Metodo que ajusta la visibilidad de los botones
        if value == 0:
            for personaje, num in zip(pa.LISTA_PERSONAJES, range(7)):
                self.dict_botones[personaje].show()
                self.dict_botones[personaje].setGeometry(30, 120 + (num) * 60, 100, 60)

        elif value == 1:
            for personaje, num in zip(pa.LISTA_PERSONAJES, range(7)):
                self.dict_botones[personaje].hide()
                if num >= 3:
                    self.dict_botones[personaje].setGeometry(30, 120 + (num - 3) * 60, 100, 60)
                    self.dict_botones[personaje].show()

        else:
            for personaje, num in zip(pa.LISTA_PERSONAJES, range(7)):
                self.dict_botones[personaje].hide()
                if num < 3:
                    self.dict_botones[personaje].show()

