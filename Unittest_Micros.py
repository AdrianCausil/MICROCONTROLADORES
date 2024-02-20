import numpy as np
import unittest
from array import array

class MatrizManipulator:
    def __init__(self, f):
        """
        Inicializa el objeto con un array 'f' de 9 elementos.
        'f' debe ser un array de longitud 9.
        """
        if len(f) != 9:
            raise ValueError("El array 'f' debe tener 9 elementos.")
        self.matriz = np.array(f, dtype=np.float32).reshape((3, 3))

    def multiplicar_primera_fila_por_2(self):
        """
        Multiplica el primer renglón de la matriz por 2.
        """
        self.matriz[0] *= 2

    def intercambiar_primer_y_segundo_renglon(self):
        """
        Intercambia el primer y segundo renglón de la matriz.
        """
        self.matriz[[0, 1]] = self.matriz[[1, 0]]

    def sumar_multiplo_del_tercer_renglon_al_segundo(self, factor):
        """
        Suma un múltiplo del tercer renglón al segundo renglón de la matriz.
        El factor indica el múltiplo.
        """
        self.matriz[1] += factor * self.matriz[2]

    def mostrar_matriz(self):
        """
        Muestra la matriz actual.
        """
        print(self.matriz)

    def add_elementwise(self, other):
        """
        Suma elemento a elemento la matriz actual con otra matriz.
        """
        self.matriz += other

    def scalar_multiply_elementwise(self, scalar):
        """
        Multiplica elemento a elemento la matriz actual por un escalar.
        """
        self.matriz *= scalar

    def elementwise_multiply(self, other):
        """
        Multiplica elemento a elemento la matriz actual por otra matriz.
        """
        self.matriz *= other

class TestMatrizManipulator(unittest.TestCase):
    def setUp(self):
        self.matriz = MatrizManipulator(array('f', [1, 2, 3, 4, 5, 6, 7, 8, 9]))

    def test_add_elementwise(self):
        self.matriz.add_elementwise(np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.float32))
        self.assertTrue((self.matriz.matriz == np.array([[2, 3, 4], [5, 6, 7], [8, 9, 10]], dtype=np.float32)).all())

    def test_scalar_multiply_elementwise(self):
        self.matriz.scalar_multiply_elementwise(2)
        self.assertTrue((self.matriz.matriz == np.array([[2, 4, 6], [8, 10, 12], [14, 16, 18]], dtype=np.float32)).all())

    def test_elementwise_multiply(self):
        self.matriz.elementwise_multiply(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.float32))
        self.assertTrue((self.matriz.matriz == np.array([[1, 4, 9], [16, 25, 36], [49, 64, 81]], dtype=np.float32)).all())

if __name__ == '__main__':
    unittest.main()
