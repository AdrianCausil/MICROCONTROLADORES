from array import array


# Creamos un array de tipo 'f' para representar la matriz numérica
f = array('f', [1, 2, 3, 4, 5, 6, 7, 8, 9])

def obtener_numero_por_posicion(array_f, fila, columna):
    if fila < 0 or fila > 2 or columna < 0 or columna > 2:
        print("Las posiciones de fila y columna deben estar en el rango de 0 a 2.")
        return None
    indice = fila * 3 + columna
    return array_f[indice]

# Ejemplo de uso:
print("Array 'f' original:", f)
fila = int(input("Ingrese la fila (0-2): "))
columna = int(input("Ingrese la columna (0-2): "))
numero = obtener_numero_por_posicion(f, fila, columna)
if numero is not None:
    print(f"El número en la fila {fila} y columna {columna} es: {numero}")


def array_a_matriz_3x3(array):
    matriz = [array[i:i+3] for i in range(0, 9, 3)]
    return matriz

def intercambiar_filas(matriz, fila1, fila2):
    matriz[fila1], matriz[fila2] = matriz[fila2], matriz[fila1]
    return matriz

def multiplicar_fila_por_escalar(matriz, fila, escalar):
    matriz[fila] = [elemento * escalar for elemento in matriz[fila]]
    return matriz

def sumar_multiplo_de_fila(matriz, fila_destino, fila_origen, escalar):
    for i in range(len(matriz[fila_destino])):
        matriz[fila_destino][i] += matriz[fila_origen][i] * escalar
    return matriz

def restar_multiplo_de_fila(matriz, fila_destino, fila_origen, escalar):
    for i in range(len(matriz[fila_destino])):
        matriz[fila_destino][i] -= matriz[fila_origen][i] * escalar
    return matriz

# Ejemplo de uso:
matriz = array_a_matriz_3x3(f)

print("Matriz original:")
for fila in matriz:
    print(fila)

# Intercambiar la fila 1 y la fila 2
matriz = intercambiar_filas(matriz, 0, 1)
print("\nMatriz luego de intercambiar la fila 1 y la fila 2:")
for fila in matriz:
    print(fila)

# Multiplicar la fila 3 por 2
matriz = multiplicar_fila_por_escalar(matriz, 2, 2)
print("\nMatriz luego de multiplicar la fila 3 por 2:")
for fila in matriz:
    print(fila)

# Sumar 3 veces la fila 2 a la fila 1
matriz = sumar_multiplo_de_fila(matriz, 0, 1, 3)
print("\nMatriz luego de sumar 3 veces la fila 2 a la fila 1:")
for fila in matriz:
    print(fila)

# Restar 2 veces la fila 1 a la fila 3
matriz = restar_multiplo_de_fila(matriz, 2, 0, 2)
print("\nMatriz luego de restar 2 veces la fila 1 a la fila 3:")
for fila in matriz:
    print(fila)
