from os import listdir, path
from os.path import exists
from sys import exit
from random import choice
import functions as fun
import parametros as pr
import objects as ob



class Torneo: # Clase en donde interactuan los objetos del archivo objects.py

    def __init__(self, arena, eventos, equipo, mochila, excavacion, dias, tipo_arena) -> None:
        self.arena: list = arena 
        self.eventos: list = eventos
        self.equipo: list = equipo
        self.mochila: list = mochila
        self.__metros_excavados: tuple = round((float(excavacion[0])), 2)
        self.metros_totales: tuple = round(float((excavacion[1])), 2)
        self.__dia_actual: tuple = int(dias[0])
        self.dias_totales: tuple = int(dias[1])
        self.tipo_arena: str = tipo_arena
        self.dificultad_arena: float = 0
        self.juego_terminado: bool = False


    @property
    def metros_excavados(self) -> float:
        return self.__metros_excavados
    

    @metros_excavados.setter # Property que se encarga de verificar si se alcanzo la meta
    def metros_excavados(self, metros: float) -> None: 
        terminado: bool = not self.juego_terminado
        if metros >= self.metros_totales and self.dia_actual <= self.dias_totales and terminado:
            self.juego_terminado = True
            metros_totales = f"{round(metros, 1)} / {self.metros_totales}"
            print(75 * "_")
            print(f"\nFELICIDADES!!!, HAS GANADO EL TORNEO\nExcavaste: ({metros_totales}) metros")

        elif metros <= 0: # Utilizado para el evento derrumbe
            self.__metros_excavados = 0

        else:
            self.__metros_excavados = metros
    
    
    @property
    def dia_actual(self) -> int:
        return self.__dia_actual
    

    @dia_actual.setter # Property que se encarga de verificar los dias transcurridos
    def dia_actual(self, dia: int) -> None:
        terminado: bool = not self.juego_terminado
        if dia > self.dias_totales and self.metros_excavados <= self.metros_totales and terminado:
            self.juego_terminado = True
            metros_totales = f"{round(self.metros_excavados, 2)} / {self.metros_totales}"
            print("\n" + 75 * "_")
            print(f"\nLO SENTIMOS, HAS PERDIDO EL TORNEO\nExcavaste: ({metros_totales}) metros")

        else:
            self.__dia_actual = dia


    def mostrar_estado(self) -> None: # Muestra el estado del torneo
        dias_torneo: tuple = (self.dia_actual, self.dias_totales)
        estado_excavacion: tuple = (self.metros_excavados, self.metros_totales)
        fun.estado_torneo(self.equipo, pr.strings, dias_torneo, self.tipo_arena, estado_excavacion)


    def ver_mochila(self) -> None: # Muestra los items de la mochila
        opcion_jugador = fun.mostrar_items(self.mochila, pr.strings)
        if opcion_jugador != "x": # Si la opcion es != x, se aplica un item en la partida
            if self.mochila[opcion_jugador].tipo == "consumible":
                self.usar_consumible(self.mochila.pop(opcion_jugador))

            elif self.mochila[opcion_jugador].tipo == "tesoro":
                self.abrir_tesoros(self.mochila.pop(opcion_jugador))
        

    def usar_consumible(self, consumible) -> None: # Aplica el efecto de un consumible
        for i in self.equipo:
            i.consumir_item(consumible)
        print(f"\nSe ha aplicado {consumible.nombre} en el equipo")


    def abrir_tesoros(self, tesoro) -> None: # Aplica el efecto de un tesoro
        tesoro_abierto = tesoro.efecto() 
        if "Excavador" in str(type(tesoro_abierto)):
            self.equipo.append(tesoro_abierto) # Se agrega el nuevo excavador al equipo
            print(f"\nSe ha agregado {tesoro_abierto.nombre} al equipo")

        elif "Arena" in str(type(tesoro_abierto)):
            self.arena = tesoro_abierto
            self.tipo_arena = tesoro_abierto.tipo  # Se cambia el tipo de arena
            print(f"\nSe ha cambiado la arena a {self.tipo_arena}")


    def simular_dia(self) -> None:
        item_encontrados = [] # Lista de items encontrados en el dia
        total_excavado = 0 # Quiero que por cada dia se setee en 0
        if self.arena.tipo != "magnetica":
            self.dificultad_arena = self.arena.dificultad_arena()

        elif self.arena.tipo == "magnetica":
            self.dificultad_arena = self.arena.efecto_arena()[0]
            
        print("_" * 30 + f" Dia actual: {self.dia_actual} " + "_" * 30 + "\n")
        excavadores_durmiendo = [i for i in self.equipo if i.energia == 0]
    
        for i in self.equipo: # Simular excavacion
            if i.energia > 0 and i.tipo != "tareo":
                i.habilidad_docencio()
                excavado_excavador = i.excavar(self.arena.dificultad_arena())
                total_excavado += excavado_excavador

                if self.arena.tipo == "magnetica":
                    self.mochila.append(item := self.arena.efecto_arena()[1])
                    str_aux = f"{i.nombre} ha encontrado un {item.nombre} de tipo {item.tipo}"
                    item_encontrados.append(str_aux)

                elif self.arena.tipo == "mojada":
                    self.mochila.append(item := self.arena.efecto_arena())
                    str_aux = f"{i.nombre} ha encontrado un {item.nombre} de tipo {item.tipo}"
                    item_encontrados.append(str_aux)
                
                else:
                    item_encontrado = fun.probabilidad_item(i.encontrar_item())
                    if item_encontrado == "consumible":
                        self.mochila.append(item := choice(self.arena.consumibles))
                        str_aux = f"{i.nombre} ha encontrado un {item.nombre} de tipo {item.tipo}"
                        item_encontrados.append(str_aux)
            
                    elif item_encontrado == "tesoro":
                        self.mochila.append(item := choice(self.arena.tesoros))
                        str_aux = f"{i.nombre} ha encontrado un {item.nombre} de tipo {item.tipo}"
                        item_encontrados.append(str_aux)

                    elif item_encontrado == "ninguno":
                        item_encontrados.append(f"{i.nombre} no ha encontrado nada")
                print(f"{i.nombre} ha excavado {excavado_excavador} metros")
        
            elif i.energia > 0:
                excavado_excavador = i.excavar(self.arena.dificultad_arena())
                total_excavado += excavado_excavador
                if self.arena.tipo == "magnetica":
                    self.mochila.append(item := self.arena.efecto_arena()[1])
                    str_aux = f"{i.nombre} ha encontrado un {item.nombre} de tipo {item.tipo}"
                    item_encontrados.append(str_aux)

                elif self.arena.tipo == "mojada":
                    self.mochila.append(item := self.arena.efecto_arena())
                    str_aux = f"{i.nombre} ha encontrado un {item.nombre} de tipo {item.tipo}"
                    item_encontrados.append(str_aux)
                
                else:
                    item_encontrado = fun.probabilidad_item(i.encontrar_item())
                    if item_encontrado == "consumible":
                        self.mochila.append(item := choice(self.arena.consumibles))
                        str_aux = f"{i.nombre} ha encontrado un {item.nombre} de tipo {item.tipo}"
                        item_encontrados.append(str_aux)
            
                    elif item_encontrado == "tesoro":
                        self.mochila.append(item := choice(self.arena.tesoros))
                        str_aux = f"{i.nombre} ha encontrado un {item.nombre} de tipo {item.tipo}"
                        item_encontrados.append(str_aux)

                    elif item_encontrado == "ninguno":
                        item_encontrados.append(f"{i.nombre} no ha encontrado nada")
                print(f"{i.nombre} ha excavado {excavado_excavador} metros")
            else:
                item_encontrados.append(f"{i.nombre} no ha encontrado nada")
        string_1 = f"\nHoy se ha excavado {round(total_excavado, 2)} metros, de"
        string_2 = f" un total de {round(self.metros_excavados + total_excavado, 2)} metros"
        print(string_1 + string_2 + pr.strings["descanso"] + "\n")
        if excavadores_durmiendo != []: # Si hay alguien durmiendo
            for i in excavadores_durmiendo:
                if i.dias_descanzo > 0:
                    print(f"{i.nombre} se fue a dormir ({i.dias_descanzo} dias)")
                    i.dias_descanzo -= 1 # Se le quita un dia, ya que terminaron de excavar
                else:
                    print(f"{i.nombre} ha despertado")
                    i.energia = 100
        else:
            print("No hay nadie durmiendo")
        
        print(pr.strings["items"])
        print(*item_encontrados, sep = "\n")
        prob_evento = fun.probabilidad_evento() # Se simula un evento
        print(pr.strings["evento"])
        self.metros_excavados += total_excavado

        if prob_evento == "lluvia" and not self.juego_terminado:
            print(f"Ha ocurrido un evento: {prob_evento}")
            self.iniciar_evento(prob_evento)
            for i in self.equipo:
                i.felicidad -= pr.FELICIDAD_PERDIDA
            print("El equipo ha perdido felicidad por la lluvia")

        elif prob_evento == "terremoto" and not self.juego_terminado:
            print(f"Ha ocurrido un evento: {prob_evento}")
            self.iniciar_evento(prob_evento)            
            for i in self.equipo:
                i.felicidad -= pr.FELICIDAD_PERDIDA
            print("El equipo ha perdido felicidad por el terremoto")

        elif prob_evento == "derrumbe" and not self.juego_terminado:
            print(f"Ha ocurrido un evento: {prob_evento}")
            for i in self.equipo:
                i.felicidad -= pr.FELICIDAD_PERDIDA
            print("El equipo ha perdido felicidad por el derrumbe")
            self.iniciar_evento(prob_evento)
            

        elif prob_evento != pr.eventos  and not self.juego_terminado:
            print("No ha ocurrido ningun evento")
        # Se registran los metros excavados en el dia
        self.dia_actual += 1


    def iniciar_evento(self, evento: str) -> None:
        arenas_obj = [ob.ArenaNormal, ob.ArenaMojada, ob.ArenaRocosa, ob.ArenaMagnetica] 
        if evento == self.eventos[0]:
            if self.tipo_arena == "normal":
                self.tipo_arena = "mojada"
                self.arena = fun.instanciar_arena(*arenas_obj, self.tipo_arena)
                self.arena.items(fun.items_iniciales(ob.Tesoro, ob.Consumibles))
                print(f"La arena se ha convertido en {self.tipo_arena}")               

            elif self.tipo_arena == "rocosa":
                self.tipo_arena = "magnetica"
                self.arena = fun.instanciar_arena(*arenas_obj, self.tipo_arena)
                self.arena.items(fun.items_iniciales(ob.Tesoro, ob.Consumibles))
                print(f"La arena se ha convertido en {self.tipo_arena}")
            
            else:
                print("No se ha producido ningun cambio en la arena")

        elif evento == self.eventos[1]:
            if self.tipo_arena == "normal":
                self.tipo_arena = "rocosa"
                self.arena = fun.instanciar_arena(*arenas_obj, self.tipo_arena)
                self.arena.items(fun.items_iniciales(ob.Tesoro, ob.Consumibles))
                print(f"La arena se ha convertido en {self.tipo_arena}")


            elif self.tipo_arena == "mojada":
                self.tipo_arena = "magnetica"
                self.arena = fun.instanciar_arena(*arenas_obj, self.tipo_arena)
                self.arena.items(fun.items_iniciales(ob.Tesoro, ob.Consumibles))
                print(f"La arena se ha convertido en {self.tipo_arena}")
            
            else:
                print("No se ha producido ningun cambio en la arena")
            
        elif evento == self.eventos[2]: # Aqui se cambia el tipo de arena
            self.tipo_arena = "normal"
            self.arena = fun.instanciar_arena(*arenas_obj, self.tipo_arena)
            self.arena.items(fun.items_iniciales(ob.Tesoro, ob.Consumibles))
            self.metros_excavados -= pr.METROS_PERDIDOS_DERRUMBE
            metros_excavados = round(self.metros_excavados, 2)
            print(f"Se ha producido un derrumbe, se ha retrocedido a los {metros_excavados}")
         

    def __str__(self) -> str: # Se encarga de convertir la partida en un string
        arena_str = self.arena.__str__()
        equipo_str = "%3#@".join([i.__str__() for i in self.equipo])
        mochila_str = "%3#@".join([i.__str__() for i in self.mochila])
        excavado_str = f"{self.metros_excavados},{self.metros_totales}"
        dia_str = f"{self.dia_actual},{self.dias_totales}"
        tipo_str = f"{self.tipo_arena}"
        return "$23*".join([arena_str, equipo_str, mochila_str, excavado_str, dia_str, tipo_str])


class MenuJuego:

    def __init__(self, Torneo, Arenas, Excavadores, Items, Parametros) -> None:
        self.Torneo: object = Torneo
        self.Arenas: list = Arenas
        self.Excavadores: list = Excavadores
        self.Items: list = Items
        self.parametros: list = Parametros


    def menu_inicio(self) -> None: # Se encarga de mostrar las opciones del menu 
        print(*pr.strings["menu_inicio"], sep = "\n") # Se descomprime el diccionario
        opcion_jugador = input("\nPor favor, ingrese una opcion: ")
        fun.clear()  
        self.opciones_inicio(opcion_jugador) # Se envia a opciones_inicio


    def opciones_inicio(self, opcion_jugador) -> None: # Metodo que maneja las opciones del menu
        fun.clear()
        if opcion_jugador == "1": # Iniciar nueva partida
            arena_obj = fun.instanciar_arenas(*self.Arenas, *self.Items) #Lista con objetos arena
            arena_obj.items(fun.items_iniciales(*self.Items))
            equipo_obj = fun.instanciar_excavadores(*self.Excavadores)
            self.Torneo = Torneo(arena_obj, pr.eventos, equipo_obj, [], *self.parametros)
            self.menu_principal() # Se muestra el menu principal 

        elif opcion_jugador == "2":
            if fun.verificar_carpeta() and listdir(pr.strings["path"]) != []: # Existen carpetas
                nombre_archivo = fun.mostrar_archivos(listdir(pr.strings["path"]))
                print(f"Se ha seleccionado: {nombre_archivo}")
                input("\nPresione enter para continuar...")
                if exists(path.join(pr.strings["path"],  nombre_archivo)):
                    arenas_obj = [self.Arenas, self.Excavadores, self.Items]
                    self.Torneo = Torneo(*fun.leer_partida(nombre_archivo, *arenas_obj))
                    self.menu_principal()

                elif nombre_archivo == "x":
                    fun.clear()
                    self.menu_inicio()  
                
                else:
                    fun.clear()
                    self.opciones_inicio("2")
                                        
            else:
                print("No hay partidas guardadas...\n") 
                self.menu_inicio() 
    
        elif opcion_jugador == "x":
            exit("El programa ha finalizado...")
        return self.menu_inicio() # Si el input no es valido, se vuelve a mostrar el menu


    # Menu que se muestra luego de iniciar una partida
    def menu_principal(self) -> None:
        fun.clear()

        print(*pr.strings["menu_principal1"], sep = "\n")
        print(f"Dia acual: {self.Torneo.dia_actual}")
        print(f"Tipo de arena: {self.Torneo.tipo_arena}")
        print(*pr.strings["menu_principal2"], sep = "\n")
        opcion_jugador = input("\nPor favor, ingrese una opcion: ") 
        self.opciones_principal(opcion_jugador)
    
    
    def opciones_principal(self, opcion_jugador: str) -> None:
        fun.clear()
        if opcion_jugador == "1":
            self.Torneo.simular_dia()
            input("\nPresione enter para continuar...")

        elif opcion_jugador == "2": # Muestra el estado del torneo
            self.Torneo.mostrar_estado()
            input("\nPresione enter para continuar...")
            
        elif opcion_jugador == "3":
            self.Torneo.ver_mochila()
            input("\nPresione enter para continuar...")

        elif opcion_jugador == "4":
            nombre_partida = input("Ingrese un nombre para su partida (x Volver menu principal): ")
            if nombre_partida == "x":
                fun.clear()
                return self.menu_principal()
            else:
                fun.guardar_partida(self.Torneo, nombre_partida)
                print(f"La partida {nombre_partida} se ha guardado con exito...")
                input("\nPresione enter para continuar...")

        elif opcion_jugador == "5":
            return self.menu_inicio()
        
        elif opcion_jugador == "x":
            exit("El programa ha finalizado...")

        if self.Torneo.juego_terminado: # Verificar si el juego ha terminado
            input("\nPresione enter para crear una nueva partida...")
            fun.clear()
            return self.menu_inicio()
        fun.clear()
        return self.menu_principal()

