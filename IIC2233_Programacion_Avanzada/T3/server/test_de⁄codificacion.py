from Scripts.funtions import codificar_mensaje, decodificar_mensaje


def test_codificar_mensaje():
    msg = ""
    N = 100
    msg_codificado = codificar_mensaje(msg, N)
    msg_decodificado = decodificar_mensaje(msg_codificado.copy(), N)
    assert msg_decodificado == msg
    print("Test 1: OK")

def test_codificar_mensaje_2():
    dict_msg = {
        "nombre": "Juan",
        "apellido": "Perez",
        "edad": 20,
        "mensaje": "Hola mundo",
        "lista": ["Hola", "mundo", "lista"],
        "tupla": ("Hola", "mundo", "tupla"),
        "diccionario": {
            "nombre": "Juan",
            "apellido": "Perez"
        },
        "set": {"Hola", "mundo", "set"},
        "bytes": b"Hola mundo",
        "bytearray": bytearray(b"Hola mundo"),
        "bool": True,
        "none": None,
        "float": 3.1416,
        "int": 1001,
        "array": [1, 2, 3, 4, 5],
        "array2": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "apellido": "Perez"
    }
    N = 100 # PONDERADOR_ENCRIPCION
    msg_codificado = codificar_mensaje(dict_msg, N)
    msg_decodificado = decodificar_mensaje(msg_codificado, N)
    # Crea test para verifacar si el mensaje codificado es igual al mensaje decodificado
    assert dict_msg == msg_decodificado
    print("Test 2: OK")

# llama a los test
test_codificar_mensaje()
test_codificar_mensaje_2()
