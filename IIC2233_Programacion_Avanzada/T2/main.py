from frontend import frontend_inicio as fi
from frontend import frontend_constructor as fc
from frontend import frontend_juego as fj
from frontend import elementos_graficos as eg
from backend import backend_juego as bkj

from PyQt5.QtWidgets import QApplication
from os import listdir, path
import parametros as pa
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Frontend
    ventana_inicio = fi.VentanaInicio(pa.LISTA_MAPAS) # Mapas guardados
    ventana_constructor = fc.VentanaConstructor() # Ventana constructor
    ventana_juego = fj.VentanaJuego() # Juego desde el inicio

    # Backend
    logica_inicio = bkj.LogicaInicio() # Comunicacion con el backend
    logica_juego = bkj.LuigiJuego() # Comunicacion con el backend
    #logica_fantasmas = bkj.GhostJuego()
    resultado_partida = eg.VentanaResultado()

    # Senales de la ventana de inicio
    ventana_inicio.senal_click_inicio.connect(logica_inicio.nombre_valido) # Verificar nombre
    ventana_inicio.senal_iniciar_constructor.connect(ventana_constructor.show) # Mostrar constructor
    ventana_inicio.senal_iniciar_juego.connect(ventana_juego.mostrar_grilla) # Mostrar juego
    ventana_inicio.senal_nombre_jugador.connect(ventana_constructor.agregar_nombre)

    ventana_constructor.senal_conectar_juego.connect(ventana_juego.mostrar_grilla) # Pasamos el mapa
    
    # Senales de la ventana del juego
    ventana_juego.senal_crear_juego.connect(logica_juego.inicializar_clase) # Pasamos el mapa
    ventana_juego.senal_keypress_mov.connect(logica_juego.movimiento_personaje)
    ventana_juego.senal_eliminar_fantasmas.connect(logica_juego.eliminar_fantasmas)
    ventana_juego.senal_eliminar_luigi.connect(logica_juego.eliminar_luigi)
    ventana_juego.senal_volver_jugar.connect(ventana_inicio.show)
    ventana_juego.senal_volver_jugar.connect(ventana_constructor.eliminar_mapa)
    ventana_juego.senal_modificar_vida.connect(logica_juego.modificar_vida)
    ventana_juego.senal_cuadro_nombre.connect(ventana_inicio.MainNombre.setText)
    ventana_juego.senal_mostrar_popup.connect(resultado_partida.mostrar_texto)
    ventana_juego.senal_modificar_mapa.connect(logica_juego.modificar_mapa)

    # Senales de la logica del juego
    logica_juego.senal_movimiento_lugi.connect(ventana_juego.mover_luigi) # Mov luigi
    logica_juego.senal_dano_luigi.connect(ventana_juego.actualizar_vida)
    logica_juego.senal_ganar_partida.connect(ventana_juego.ganar_partida)
    logica_juego.senal_mover_roca.connect(ventana_juego.mover_roca)

    # Senales que verifican la pestana de inicio
    logica_inicio.senal_conectar_popup.connect(ventana_inicio.warning_popup) # Mostrar popup
    logica_inicio.senal_conectar_constructor.connect(ventana_inicio.abrir_constructor) 
    logica_inicio.senal_conectar_juego.connect(ventana_inicio.abrir_juego) # Pasamos el mapa
    
    resultado_partida.senal_volver_jugar.connect(ventana_inicio.show)
    resultado_partida.senal_ocultar_ventana.connect(resultado_partida.hide)
    resultado_partida.senal_salir.connect(sys.exit)
    
    # Inicio del juego
    ventana_inicio.show()
    sys.exit(app.exec_())
