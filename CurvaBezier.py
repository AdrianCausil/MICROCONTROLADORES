import math
import matplotlib.pyplot as plt

# Definición de puntos para la curva de Bezier
p0 = [1, 0]
p1 = [1, -2]
p2 = [6, 3]
p3 = [3, 3]

# Lista para almacenar las velocidades del motor
Lista = []

# Parámetros para el cálculo
b = 2   # Distancia del motor al centro de gravedad
T = 5   # Tiempo de llegar de un punto a otro
r = 1   # Radio de las ruedas
t = 5   # Cantidad de pasos

# Listas para graficar
Bx1_list = []
By1_list = []
Bx2_list = []
By2_list = []

# Bucle para calcular los puntos de la curva de Bezier y las velocidades de los motores
for i in range(t):  # Error corregido: Agregar paréntesis para evitar errores de sintaxis

    # Lista temporal para almacenar las velocidades de los motores
    Lista2 = []

    # Calcular parámetro de la curva de Bezier de 0 a 1
    m1 = i / t
    z1 = (1 - m1)

    # Calcular puntos de la curva de Bezier en el paso actual
    Bx1 = z1 ** 3 * p0[0] + 3 * z1 ** 2 * m1 * p1[0] + 3 * z1 * m1 ** 2 * p2[0] + m1 ** 3 * p3[0]
    By1 = z1 ** 3 * p0[1] + 3 * z1 ** 2 * m1 * p1[1] + 3 * z1 * m1 ** 2 * p2[1] + m1 ** 3 * p3[1]

    # Almacenar puntos para graficar
    Bx1_list.append(Bx1)
    By1_list.append(By1)

    # Calcular parámetro de la curva de Bezier para el siguiente paso
    m2 = (i + 1) / t
    z2 = (1 - m2)

    # Calcular puntos de la curva de Bezier para el siguiente paso
    Bx2 = z2 ** 3 * p0[0] + 3 * z2 ** 2 * m2 * p1[0] + 3 * z2 * m2 ** 2 * p2[0] + m2 ** 3 * p3[0]
    By2 = z2 ** 3 * p0[1] + 3 * z2 ** 2 * m2 * p1[1] + 3 * z2 * m2 ** 2 * p2[1] + m2 ** 3 * p3[1]

    # Almacenar puntos para graficar
    Bx2_list.append(Bx2)
    By2_list.append(By2)

    # Calcular ángulos de orientación
    Gama1 = math.atan2(By1, Bx1)
    Gama2 = math.atan2(By2, Bx2)

    # Calcular diferencia de tiempo
    DTau1 = (T / t) * i
    DTau2 = (T / t) * (i + 1)
    DTauTotal = DTau2 - DTau1

    # Calcular componentes de velocidad y orientación
    Ux = Bx2 - Bx1
    Uy = By2 - By1
    E = math.sqrt(Ux ** 2 + Uy ** 2)
    V = E / DTauTotal
    wi = (Gama2 - Gama1) / DTauTotal

    # Calcular velocidades de los motores
    MotorD = (1 / r) * (V + b * wi)
    MotorI = (1 / r) * (V - b * wi)

    # Almacenar velocidades de los motores en una lista temporal
    Lista2.append(MotorD)
    Lista2.append(MotorI)

    # Almacenar velocidades de los motores como tupla en la lista principal
    VELOCIDADES = (MotorD, MotorI)
    Lista.append(VELOCIDADES)

print("Lista de velocidades de los motores:", Lista)

# Graficar puntos de la curva de Bezier
plt.plot(Bx1_list, By1_list, label='Bx1, By1')
plt.plot(Bx2_list, By2_list, label='Bx2, By2')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Gráficas de Bx1, By1 y Bx2, By2')
plt.legend()
plt.grid(True)
plt.show()

