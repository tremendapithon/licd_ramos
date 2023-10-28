def encriptar(msg: bytearray, N: int) -> bytearray: # ENCRIPTAR
    encriptar_alg = map(lambda x: msg.insert(0, msg.pop(len(msg) - 1)), range(N))
    list(encriptar_alg)
    primer_elemento, n_elemento = msg.pop(0), msg.pop(N % len(msg) - 1)
    msg.insert(0, n_elemento)
    msg.insert(N % len(msg), primer_elemento)
    return msg

def desencriptar(msg: bytearray, N: int) -> bytearray: # DESENCRIPTAR
    primer_elemento, n_elemento = msg.pop(0), msg.pop(N % len(msg) - 1)
    msg.insert(0, n_elemento)
    msg.insert(N % len(msg), primer_elemento)
    desencriptar_alg = map(lambda x: msg.insert(len(msg), msg.pop(0)), range(N))
    list(desencriptar_alg)
    return msg
    

if __name__ == "__main__":
    # Testear encriptar
    N = 1
    msg_original = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04\x05')
    msg_esperado = bytearray(b'\x01\x05\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04')
    msg_encriptado = encriptar(msg_original.copy(), N)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")
    
    # Testear desencriptar
    msg_desencriptado = desencriptar(msg_esperado.copy(), N)
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")