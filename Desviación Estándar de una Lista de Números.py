import math

def desviacion_vector(lista):
    # Número de elementos en la lista
    n = len(lista)
    
    # Manejar el caso de lista vacía
    if n == 0:
        return 0
    
    # Calcular la media de la lista
    media = sum(lista) / n
    
    # Calcular la suma de los cuadrados de las diferencias con la media
    suma_cuadrados = sum((x - media) ** 2 for x in lista)
    
    # Calcular la varianza dividiendo la suma de cuadrados entre el número de elementos
    varianza = suma_cuadrados / n
    
    # Calcular la desviación estándar tomando la raíz cuadrada de la varianza
    desviacion_estandar = math.sqrt(varianza)
    
    # Retornar la desviación estándar calculada
    return desviacion_estandar