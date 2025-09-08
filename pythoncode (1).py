import random

# ======= Funciones de generación de llaves =======

def fs(p, s):
    return (p ^ s) & ((1 << 64) - 1)

def fg(p0, q):
    return (p0 * q) & ((1 << 64) - 1)

def fm(s, q):
    return ((s << 3) ^ q) & ((1 << 64) - 1)

def generar_tabla_claves(p, q, s, n=8):
    tabla = []
    for _ in range(n):
        p0 = fs(p, s)
        k = fg(p0, q)
        tabla.append(k)
        s = fm(s, q)
    return tabla

# ======= Funciones reversibles =======

def f1(x, k):  # XOR
    return x ^ k

def f2(x, k):  # rotación a la izquierda
    return ((x << 5) | (x >> (64 - 5))) & ((1 << 64) - 1)

def f3(x, k):  # suma modular
    return (x + k) & ((1 << 64) - 1)

def f4(x, k):  # rotación a la derecha
    return ((x >> 7) | (x << (64 - 7))) & ((1 << 64) - 1)

FUNCIONES = [f1, f2, f3, f4]

# ======= Funciones inversas para descifrado =======

def f1_inv(x, k):  # XOR (es su propia inversa)
    return x ^ k

def f2_inv(x, k):  # inversa de rotación izquierda
    return ((x >> 5) | (x << (64 - 5))) & ((1 << 64) - 1)

def f3_inv(x, k):  # inversa de suma modular
    return (x - k) & ((1 << 64) - 1)

def f4_inv(x, k):  # inversa de rotación derecha
    return ((x << 7) | (x >> (64 - 7))) & ((1 << 64) - 1)

FUNCIONES_INV = [f1_inv, f2_inv, f3_inv, f4_inv]

# ======= Cifrado y descifrado de bloques =======

def encriptar_bloque(bloque, claves, psn):
    x = bloque
    for i in range(len(FUNCIONES)):
        idx = (psn + i) % len(FUNCIONES)
        f = FUNCIONES[idx]
        k = claves[i % len(claves)]
        x = f(x, k)
    return x

def desencriptar_bloque(bloque, claves, psn):
    x = bloque
    for i in reversed(range(len(FUNCIONES))):
        idx = (psn + i) % len(FUNCIONES)
        f = FUNCIONES_INV[idx]  
        k = claves[i % len(claves)]
        x = f(x, k)
    return x

def texto_a_bloques(texto):
    """Convierte string en lista de enteros de 64 bits"""
    data = texto.encode("utf-8")
    bloques = []
    for i in range(0, len(data), 8):
        bloque = data[i:i+8]
        bloque = bloque.ljust(8, b'\0')  
        bloques.append(int.from_bytes(bloque, "big"))
    return bloques

def bloques_a_texto(bloques):
    """Convierte lista de enteros de 64 bits en string"""
    data = b''.join([b.to_bytes(8, "big") for b in bloques])
    return data.rstrip(b'\0').decode("utf-8", errors="ignore")

def encriptar_texto(texto, claves, psn):
    bloques = texto_a_bloques(texto)
    cifrados = [encriptar_bloque(b, claves, psn) for b in bloques]
    return cifrados

def desencriptar_texto(cifrados, claves, psn):
    bloques = [desencriptar_bloque(c, claves, psn) for c in cifrados]
    return bloques_a_texto(bloques)

def select_initial_psn(data):
    """Selecciona un PSN inicial basado en los datos"""
    if len(data) == 0:
        return random.randint(0, 15)
    return sum(data) % 16














# === funcion para generar llaves de endpoints ===

def generar_llaves_endpoints():
    # Cliente A
    P_A, Q_A, S_A = 104729, 1299709, 9876543210123456789
    tabla_A = generar_tabla_claves(P_A, Q_A, S_A, n=8)

    # Servidor B
    P_B, Q_B, S_B = 104759, 1299721, 123456789876543210
    tabla_B = generar_tabla_claves(P_B, Q_B, S_B, n=8)

    print("\n=== LLAVES CLIENTE A ===")
    for i, k in enumerate(tabla_A, 1):
        print("Subclave {}: {}".format(i, hex(k)))

    print("\n=== LLAVES SERVIDOR B ===")
    for i, k in enumerate(tabla_B, 1):
        print("Subclave {}: {}".format(i, hex(k)))

    return tabla_A, tabla_B


# --- evaluación por endpoint (bits y duplicados) ---
def evaluar_llaves(tabla, nombre):
    print("\n=== EVALUACIÓN DE LLAVES {} ===".format(nombre))
    seen = set()
    duplicados = False

    for i, k in enumerate(tabla, 1):
        bin_k = format(k, "064b")      # binario en 64 bits
        count_1 = bin_k.count("1")
        count_0 = 64 - count_1
        print("Subclave {}: {} | Bits 1: {} | Bits 0: {}".format(i, hex(k), count_1, count_0))
        if k in seen:
            duplicados = True
        seen.add(k)

    print("¿Duplicados? {}".format("Si" if duplicados else "NO"))


# --- comparación entre endpoints (para evitar llaves identicas) ---
def comparar_endpoints(tabla_A, tabla_B):
    inter = set(tabla_A).intersection(tabla_B)
    print("\n=== COMPARACION ENTRE ENDPOINTS ===")
    if inter:
        print("Subclaves identicas entre A y B: {}".format([hex(x) for x in inter]))
    else:
        print("No hay subclaves identicas entre A y B.")

     










# ======= Programa principal =======

def main():
    P = 104729   
    Q = 1299709  
    S = 1234567890123456789 

    tabla = generar_tabla_claves(P, Q, S, n=8)
    
    print("=== SISTEMA DE CIFRADO ===")
    mensaje = input("Escribe el mensaje que quieras cifrar: ")
    psn = select_initial_psn(mensaje.encode('utf-8'))
    
    cifrado = encriptar_texto(mensaje, tabla, psn)
    descifrado = desencriptar_texto(cifrado, tabla, psn)
    
    print("\n=== RESULTADOS ===")
    print("Mensaje original :", mensaje)
    print("PSN inicial      :", psn)
    print("Bloques cifrados :", [hex(c) for c in cifrado])
    print("Mensaje descifrado:", descifrado)
    
    # Verificación
    if mensaje == descifrado:
        print("✓ Cifrado/descifrado exitoso!")  
    else:
        print("✗ Error en el cifrado/descifrado")

# ======= Ejecución =======

if __name__ == "__main__":
    main()  

    # genera, muestra y guarda las tablas
    tabla_A, tabla_B = generar_llaves_endpoints()

    # evalua calidad (bits y duplicados) y compara A vs B
    evaluar_llaves(tabla_A, "CLIENTE A")
    evaluar_llaves(tabla_B, "SERVIDOR B")
    comparar_endpoints(tabla_A, tabla_B)

    input("\nPresiona ENTER para salir...")