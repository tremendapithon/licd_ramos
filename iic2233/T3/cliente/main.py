from PyQt5.QtWidgets import QApplication
from frontend import elementos_frontend, ventana_inicio, ventana_juego
from Scripts.funtions import RunAgain
from Scripts.funtion_json import leer_json
import cliente as cl
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Se define el puerto y el host
    PORT = 8081
    HOST = leer_json("parametros.json")["HOST"] if len(sys.argv) < 2 else sys.argv[1]
    
    # Elementos front-end
    ventana_inicio = ventana_inicio.VentanaInicio()
    ventana_juego = ventana_juego.VentanaJuego()
    ventana_error = elementos_frontend.InicioError()
    server_error = elementos_frontend.ServerError()
    informacion_cliente = elementos_frontend.InformacionCliente()

    popup_volver = elementos_frontend.VolverIntentar()
    volver_a_correr = RunAgain(HOST)
    # Cliente
    conexion_servidor = cl.ConexionCliente(HOST, PORT)

    # Senales entre el cliente y el frontend
    conexion_servidor.senal_mostrar_ventana.connect(ventana_inicio.show) #ok
    conexion_servidor.senal_mostrar_problema.connect(ventana_error.show) #ok
    conexion_servidor.senal_caida_servidor.connect(server_error.show) #ok
    conexion_servidor.senal_caida_servidor.connect(ventana_inicio.hide) #ok
    conexion_servidor.senal_caida_servidor.connect(ventana_juego.hide) #ok
    conexion_servidor.mostrar_ventana() # ok
    conexion_servidor.senal_sala_llena.connect(informacion_cliente.init_popup) #ok
    conexion_servidor.senal_partida_curso.connect(informacion_cliente.init_popup)
    conexion_servidor.senal_ocultar_ventana.connect(ventana_inicio.hide)
    conexion_servidor.senal_iniciar_juego.connect(ventana_juego.show)
    conexion_servidor.senal_iniciar_juego.connect(ventana_inicio.hide)
    conexion_servidor.senal_nombre_usuario.connect(ventana_juego.set_user)
    conexion_servidor.senal_actualizar_jugadores.connect(ventana_inicio.actualizar_jugadores)
    conexion_servidor.senal_actualizar_jugadores.connect(ventana_juego.actualizar_jugadores)
    conexion_servidor.senal_actualizar_label.connect(ventana_juego.actualizar_label)
    conexion_servidor.senal_dados_juego.connect(ventana_juego.actualizar_dados)
    conexion_servidor.senal_volver_jugar.connect(popup_volver.init_popup)

    popup_volver.senal_volver_intentar.connect(ventana_inicio.hide)
    popup_volver.senal_volver_intentar.connect(ventana_juego.hide)
    popup_volver.senal_volver_intentar.connect(ventana_error.hide)
    popup_volver.senal_volver_intentar.connect(server_error.hide)
    popup_volver.senal_volver_intentar.connect(informacion_cliente.hide)
    popup_volver.senal_volver_intentar.connect(conexion_servidor.cerrar_conexion)
    popup_volver.senal_volver_intentar.connect(popup_volver.hide)
    popup_volver.senal_volver_intentar.connect(volver_a_correr.run_again)

    ventana_inicio.senal_ingresar_juego.connect(conexion_servidor.init_juego)

    ventana_juego.senal_click_button.connect(ventana_juego.procesar_click)
    ventana_juego.senal_boton_presionado.connect(conexion_servidor.enviar_mensaje)

    informacion_cliente.senal_ocultar_ventanas.connect(informacion_cliente.hide)

    sys.exit(app.exec_())
    
  


