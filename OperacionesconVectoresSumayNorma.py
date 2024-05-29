def suma_vectores(v1, v2):
    """
    Suma dos vectores de la misma longitud.

    Args:
        v1 (list): Primer vector.
        v2 (list): Segundo vector.

    Returns:
        list: Vector resultante de la suma.
        str: Mensaje de error si los vectores no tienen la misma longitud.
    """
    if len(v1) != len(v2):
        return "Error: Los vectores no tienen la misma longitud"
    
    suma = [v1[i] + v2[i] for i in range(len(v1))]  # Usando una lista por comprensión para la suma de vectores
    return suma

def norma_vector(lista):
    """
    Calcula la norma (magnitud) de un vector.

    Args:
        lista (list): Vector representado como una lista de números.

    Returns:
        float: Norma del vector.
    """
    suma_cuadrados = sum(x ** 2 for x in lista)  # Usando una lista por comprensión para calcular la suma de cuadrados
    norma = suma_cuadrados ** 0.5  # Calculamos la raíz cuadrada de la suma de los cuadrados para obtener la norma
    return norma  # Devolvemos la norma calculada