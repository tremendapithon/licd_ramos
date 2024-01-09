from objects_1 import MenuJuego, Torneo
import objects as obj
import parametros as pr

# Objectos que van a interacturar con MenuJuego
arenas_obj = [obj.ArenaNormal, obj.ArenaMojada, obj.ArenaRocosa, obj.ArenaMagnetica]
excavadores_obj = [obj.ExcavadorDocencio, obj.ExcavadorTareo, obj.ExcavadorHibrido]
items_obj = [obj.Tesoro, obj.Consumibles]
parametros_defecto = [pr.metros, pr.DIAS_TORNEO, pr.ARENA_INICIAL]

# Se crea el objeto MenuJuego, que es el que va a interactuar con el usuario
torneo_dccavacava = MenuJuego(Torneo, arenas_obj, excavadores_obj, items_obj, parametros_defecto)
torneo_dccavacava.menu_inicio() # Inicia el juego

