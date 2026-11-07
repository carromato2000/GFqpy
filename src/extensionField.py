from src import FiniteField, FiniteFieldElement
from src import rabin
from src import Polynomial

class ExtensionField(FiniteField):
    def __init__(self, base_field: FiniteField, poly: Polynomial):
        if not rabin(poly):
            raise ValueError("Polynomial is not irreducible")
        self.base_field = base_field
        self.poly = poly
        self.order = base_field.get_order() ** poly.degree()

    def proyect(self, a):
        """
        Toma un polinomio con coeficientes en el cuerpo base y lo proyecta al cuerpo de extensio

        Args:
            a : Polinomio a proyectar
        """
        return a % self.poly

    # Elements are polynomials 
    def add(self, a, b):
        """
        Suma dos elementos del cuerpo de extensión

        Args:
            a : Elemento del cuerpo de extensión
            b : Elemento del cuerpo de extensión
        """
        return (a.value + b.value) % self.poly

    def subtract(self, a, b):
        """
        Resta dos elementos del cuerpo de extensión

        Args:
            a : Elemento del cuerpo de extensión
            b : Elemento del cuerpo de extensión
        """
        return (a.value - b.value) % self.poly

    def multiply(self, a, b):
        """
        Multiplica dos elementos del cuerpo de extensión
        Tambien funciona si a o b son elementos del cuerpo base

        Args:
            a : Elemento del cuerpo de extensión
            b : Elemento del cuerpo de extensión
        """
        return (a.value * b.value) % self.poly

    
    def power(self, a, exponent):
        """
        Calcula la potencia de un elemento del cuerpo de extensión

        Args:
            a : Elemento del cuerpo de extensión
            exponent : Exponente
        """
        # Resultado trivial
        if exponent == 0:
            return self.base_field.one
        if exponent < 0:
            a = self.inverse(a)
            exponent = -exponent
        for _ in range(exponent):
            a = self.multiply(a, a)
        return a

    def inverse(self, a):
        """
        Calcula el inverso multiplicativo de un elemento del cuerpo de extensión
        Se puede usar el algoritmo extendido de Euclides para polinomios,
        otra 
        """
        # Resultado trivial
        if a.value == 0:
            raise ValueError("Cannot invert zero")
        return self.power(a, self.order - 2)

    def divide(self, a, b):
        return a.value * self.inverse(b)

    def equal(self, a, b):
        return a.value == b.value


    def get_order(self):
        """
        Devuelve el orden del cuerpo de extensión
        """
        return self.order


class ExtensionFieldElement(FiniteFieldElement):
    def __init__(self, value: Polynomial, field: ExtensionField):
        pass

    def order(self):
        """
        Devuelve el orden del elemento en el grupo multiplicativo del cuerpo de extensión
        """
        # Resultado trivial
        return 1
        




    