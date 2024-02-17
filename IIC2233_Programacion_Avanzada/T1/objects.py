from abc import ABC, abstractmethod # Para crear clases abstractas
from random import choice, randint, random
import functions as fun
import parametros as pr


# Clase abstracta que representa a las arenas
class Arena(ABC):
    
    def __init__(self, nombre, tipo, rareza, humedad, dureza, estatica) -> None:
        self.nombre: str = nombre
        self.tipo: str = tipo
        self.rareza: int = int(rareza)
        self.humedad: int = int(humedad)
        self.dureza: int = int(dureza)
        self.estatica: int = int(estatica)
        self.tesoros: list = []
        self.consumibles: list= []


    def dificultad_arena(self) -> float: # Metodo que calcula la dificultad de la arena
        formula_arena = ((self.rareza + self.humedad + self.dureza + self.estatica) / 40)
        return round(formula_arena, 2)


    def items(self, items: list) -> object: # Metodo que agrega items a la clase
        self.tesoros = [i for i in items[0]]
        self.consumibles = [i for i in items[1]]
    

    def item_aleatorio(self) -> object:
        item_aleatorio = choice([choice(self.consumibles), choice(self.tesoros)])
        return item_aleatorio


    @abstractmethod
    def efecto_arena(self) -> None:
        pass


    def __str__(self) -> str: # Metodo que retorna un string con los atributos de la clase
        string_1 = f"{self.nombre},{self.tipo},{self.rareza},"
        string_2 = f"{self.humedad},{self.dureza},{self.estatica}"
        return string_1 + string_2 # Se utiliza para guardar los datos de la arena


# Clases que heredan de Arena
class ArenaNormal(Arena):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ponderacion_arena: float = pr.POND_ARENA_NORMAL


    def efecto_arena(self) -> float:
        return round(self.dificultad_arena() * self.ponderacion_arena, 2)


class ArenaMojada(Arena):

    def __init__(self, *args, **kwargs) -> None: # Herencia de la arena
        super().__init__(*args, **kwargs)


    def efecto_arena(self) -> object: # Retornar un objeto aleatorio
        item_aleatorio = choice([choice(self.consumibles), choice(self.tesoros)]) 
        return item_aleatorio

        
class ArenaRocosa(Arena):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


    def efecto_arena(self) -> float:
        formula_arena = ((self.rareza + self.humedad + (2 * self.dureza) + self.estatica) / 50)
        return round(formula_arena, 2)


class ArenaMagnetica(ArenaMojada, ArenaRocosa):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dificultad_excavacion: float = 0


    def efecto_arena(self) -> list:
        self.humedad = randint(1, 10)
        self.dureza = randint(1, 10)
        self.dificultad_excavacion = ArenaRocosa.efecto_arena(self) 
        item_aleatorio = ArenaMojada.efecto_arena(self)
        return [self.dificultad_excavacion, item_aleatorio] 
        

# Clase que representa a los excavadores
class Excavador:
    
    def __init__(self, nombre, tipo, edad, energia, fuerza, suerte, felicidad) -> None:
        self.nombre: str = nombre
        self.tipo: str = tipo
        self.__edad: int = int(edad)
        self.__energia: int = int(energia)
        self.__fuerza: int = int(fuerza)
        self.__suerte: int = int(suerte)
        self.__felicidad: int = int(felicidad)
        self.dias_descanzo: int = 0

    # Properties que se encargan de manejar los atributos privados
    @property
    def edad(self):
        return self.__edad
    

    @edad.setter
    def edad(self, edad) -> None: # La edad es una property que verifica que sea entre 18 y 60
        if 18 <= edad <= 60:
            self.__edad = edad
        
        elif edad > 60:
            self.__edad = 60

        else:
            self.__edad = 18 # Si no se cumple la condicion, se le asigna 18 años


    @property # Property que verifica que la energia sea entre 0 y 100
    def energia(self) -> int:
        return self.__energia
    

    @energia.setter
    def energia(self, energia) -> None:
        if 100 >= energia > 0 and self.tipo != "hibrido": #
            self.__energia = energia

        elif energia > 100:
            self.__energia = 100     

        elif (energia >= 20 ) and self.tipo == "hibrido": # Caso excabador hibrido
            self.__energia = energia

        elif energia < 20 and self.tipo == "hibrido":
            self.__energia = 20

        else: # Si la energia es menor o igual a 0, el excavador descanza 
            self.descanzar()
            self.__energia = 0
    

    @property # Property que verifica que la fuerza sea entre 1 y 10
    def fuerza(self) -> int:
        return self.__fuerza


    @fuerza.setter
    def fuerza(self, fuerza) -> None:
        if 10 >= fuerza > 0:
            self.__fuerza = fuerza
        
        elif fuerza > 10:
            self.__fuerza = 10
        
        elif fuerza <= 0:
            self.__fuerza = 1


    @property # Property que verifica que la suerte sea entre 1 y 10
    def suerte(self) -> int:
        return self.__suerte


    @suerte.setter
    def suerte(self, suerte) -> None:
        if 10 >= suerte > 0:
            self.__suerte = suerte
        
        elif suerte > 10:
            self.__suerte = 10
        
        elif suerte <= 0:
            self.__suerte = 1


    @property # Property que verifica que la felicidad sea entre 1 y 10
    def felicidad(self) -> int:
        return self.__felicidad
    

    @felicidad.setter
    def felicidad(self, felicidad) -> None:
        if 10 >= felicidad > 0:
            self.__felicidad = felicidad
        
        elif felicidad > 10:
            self.__felicidad = 10
        
        elif felicidad <= 0:
            self.__felicidad = 1


    def excavar(self, dificultad_arena) -> float:
        formula_1 = (30 / self.edad) + (((self.felicidad) + (2 * self.fuerza)) / 10)
        formula_2 = (1 / (10 * dificultad_arena))
        self.gastar_energia()
        return round(formula_1 * formula_2, 2)


    def descanzar(self) -> None: # Metodo que se encarga de descanzar al excavador
        self.dias_descanzo = int(self.edad / 20)


    def encontrar_item(self) -> float:
        return (self.suerte * (1 / 10)) * pr.PROB_ENCONTRAR_ITEM


    def gastar_energia(self) -> None:
        self.energia -= int((10 / self.fuerza) + (self.edad / 6))


    def consumir_item(self, item: object) -> None:
        self.energia += item.energia
        self.fuerza += item.fuerza
        self.suerte += item.suerte
        self.felicidad += item.felicidad
        self.consumio_item = True


    def __str__(self) -> str: # Metodo que devuelve un string con los atributos del excavador
        string_1 = f"{self.nombre},{self.tipo},{self.edad},{self.energia},"
        string_2 = f"{self.fuerza},{self.suerte},{self.felicidad}"
        return string_1 + string_2 # Se utiliza para el guardado de los excavadores
            

class ExcavadorDocencio(Excavador):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


    def habilidad_docencio(self) -> None:
        self.felicidad += pr.FELICIDAD_ADICIONAL_DOCENCIO
        self.fuerza += pr.FUERZA_ADICIONAL_DOCENCIO
        self.energia -= pr.ENERGIA_PERDIDA_DOCENCIO
        print(f"{self.nombre} del tipo {self.tipo} ha aplicado su habilidad Docencio")


class ExcavadorTareo(Excavador):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__consumio_item: bool = False


    # Property que se encarga de manejar el atributo privado consumio_item y la habilidad tareo
    @property
    def consumio_item(self) -> bool:
        return self.__consumio_item
    
    
    @consumio_item.setter
    def consumio_item(self, consumo) -> None:
        if consumo:
            self.habilidad_tareo()
            self.__consumio_item: bool = False


    def habilidad_tareo(self) -> None:
        self.energia += pr.ENERGIA_ADICIONAL_TAREO
        self.suerte += pr.SUERTE_ADICIONAL_TAREO
        self.edad += pr.EDAD_ADICIONAL_TAREO
        self.felicidad -= pr.FELICIDAD_PERDIDA_TAREO
        print(f"{self.nombre} de tipo {self.tipo} ha aplicado su habilidad Tareo")


class ExcavadorHibrido(ExcavadorTareo, ExcavadorDocencio):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


# Clase que se encarga de manejar los items
class Item:

    def __init__(self, nombre, tipo, descripcion) -> None:
        self.nombre: str = nombre
        self.tipo: str = tipo
        self.descripcion: str = descripcion


    def efecto(self): # Metodo que se encarga de aplicar el efecto del item
        pass


class Tesoro(Item):
    
    def __init__(self, nombre, tipo, descripcion, calidad, cambio) -> None:
        super().__init__(nombre, tipo, descripcion)
        self.calidad: str = calidad
        self.cambio: str = cambio


    def efecto(self) -> object: # Metodo que devuelve un objeto de tipo Arena o Excavador
        if self.calidad == "1": # Se agrega un excavador
            objetos_excavadores = [ExcavadorDocencio, ExcavadorTareo, ExcavadorHibrido]  
            return fun.instanciar_excavador(*objetos_excavadores, self.cambio)            

        elif self.calidad == "2": # Se cambia el campo
            objetos_arenas = [ArenaNormal, ArenaMojada, ArenaRocosa, ArenaMagnetica]
            cambio_arena = fun.instanciar_arena(*objetos_arenas, self.cambio)
            cambio_arena.items(fun.items_iniciales(Tesoro, Consumibles))
            return cambio_arena
        

    def __str__(self) -> str: # Metodo que devuelve un string con los atributos del tesoro
        return f"{self.nombre},{self.tipo},{self.descripcion},{self.calidad},{self.cambio}"
        
    
class Consumibles(Item):
        
    def __init__(self, nombre, tipo, descripcion, energia, fuerza, suerte, felicidad) -> None:
        super().__init__(nombre, tipo, descripcion)
        self.energia: int = int(energia)
        self.fuerza: int = int(fuerza)
        self.suerte: int = int(suerte) 
        self.felicidad: int = int(felicidad)


    def __str__(self):
        string_1 = f"{self.nombre},{self.tipo},{self.descripcion},{self.energia},"
        string_2 = f"{self.fuerza},{self.suerte},{self.felicidad}"
        return string_1 + string_2 # Se utiliza para el guardado de los consumibles
    
