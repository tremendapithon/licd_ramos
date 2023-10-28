from os import system, path
from msvcrt import getch
import functions # Se importan las funciones del archivo functions.py
import tablero

nombre_archivo = functions.menu_inicio() # Variable que almacena el nombre del archivo
tablero_valido = False

if nombre_archivo != "no_archivo": # Si el usuario ingresa un nombre de archivo valido
    tablero_jugador = functions.cargar_tablero(path.join("Archivos",nombre_archivo))
    while True:
        opcion_jugador = functions.menu_seleccion()
        system("cls")
        if opcion_jugador == "1":
            tablero.imprimir_tablero(tablero_jugador, utf8=True)
        
        elif opcion_jugador == "2":
            bombas_validas = functions.verificar_valor_bombas(tablero_jugador)
            tortugas_validas = functions.verificar_tortugas(tablero_jugador)
            if bombas_validas == tortugas_validas == 0:
                print("El tablero es valido...")
                tablero_valido = True
            else:
                print("El tablero no es valido...")
                tablero_valido = False

        elif opcion_jugador == "3":
            if functions.verificar_bombas_tablero(tablero_jugador) == 0 and tablero_valido:
                print("El tablero es solucionable...")
            else:
                print("El tablero no es solucionable...")
            
        elif opcion_jugador == "4":
            if tablero_valido:
                #Se resuleve el tablero y se guarda como un archivo de solucion
                if "_sol.txt" not in nombre_archivo:
                    archivo_solucion = nombre_archivo.replace(".txt", "_sol.txt") # Archivo de solucion
                    functions.guardar_tablero(archivo_solucion, tablero_jugador)
                else:
                    functions.guardar_tablero(nombre_archivo, tablero_jugador)
                print("La solucion al tablero se ha guardado...")
            else:
                print("El tablero no se puede resolver...")

        elif opcion_jugador == "5":
            print("El programa ha finalizado...")
            break

        print("\nPresione una tecla para continuar...")
        getch()
else:
    print("El programa ha finalizado...")








