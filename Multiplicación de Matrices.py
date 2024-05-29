def multiplicar_matrices(matriz_a, matriz_b):
    """
    Multiplica dos matrices.

    Args:
        matriz_a (list): Primera matriz representada como una lista de listas.
        matriz_b (list): Segunda matriz representada como una lista de listas.

    Returns:
        list: Matriz resultante de la multiplicación.
    """
    # Obtener dimensiones de las matrices
    filas_a = len(matriz_a)         # Número de filas de la matriz A
    columnas_a = len(matriz_a[0])    # Número de columnas de la matriz A (y filas de la matriz B)
    columnas_b = len(matriz_b[0])    # Número de columnas de la matriz B

    # Inicializar la matriz resultado con ceros
    matriz_resultante = [[0] * columnas_b for _ in range(filas_a)]

    # Realizar la multiplicación de matrices
    for i in range(filas_a):
        for j in range(columnas_b):
            for k in range(columnas_a):
                matriz_resultante[i][j] += matriz_a[i][k] * matriz_b[k][j]

    return matriz_resultante