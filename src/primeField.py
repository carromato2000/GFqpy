from src import FiniteField, FiniteFieldElement, millerRabin
from random import randint

class PrimeField(FiniteField):
    def __init__(self, p: int): 
        if not millerRabin(p):
            raise ValueError(f"{p} is not a prime number")
        self.p = p

    @property
    def one(self):
        return PrimeFieldElement(self, 1)

    @property
    def order(self):
        return self.p

    @property
    def characteristic(self):
        return self.p

    def add(self, a, b):
        return PrimeFieldElement(self, (a.value + b.value) % self.p)

    def subtract(self, a, b):
        return PrimeFieldElement(self, (a.value - b.value) % self.p)

    def equal(self, a, b):
        return a.value == b.value

    def negative(self, a):
        return PrimeFieldElement(self, self.p - a.value)

    def multiply(self, a, b):
        """
        Multiplies two elements in the prime field.
        a and b can be either integers or PrimeFieldElement instances.

        Args:
            a : An element of the prime field (int or PrimeFieldElement)
            b : An element of the prime field (int or PrimeFieldElement)
        Returns:
            A new PrimeFieldElement representing the product of a and b in the prime field.
        """
        return PrimeFieldElement(self, (a.value * b.value) % self.p)

    def inverse(self, a):
        if a.value == 0:
            raise ValueError("Cannot compute inverse of zero")
        # Using Fermat's little theorem for prime fields
        return PrimeFieldElement(self, pow(a.value, self.p - 2, self.p))

    def divide(self, a, b):
        if b.value == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return self.multiply(a, self.inverse(b))

    def power(self, a, exponent: int):
        if isinstance(a, PrimeFieldElement):
            a = a.value
        return pow(a, exponent, self.p)

    def get_order(self, a):
        if isinstance(a, int):
            # Si a es un entero, lo convertimos a un elemento del cuerpo
            a = PrimeFieldElement(self, a)
        if isinstance(a, PrimeFieldElement):
            a = a.value
            if a == 0:
                return 0 
            else:
                return self.p - 1
        else:
            raise ValueError("Argument must be an integer or a PrimeFieldElement")

    def random_element(self):
        return PrimeFieldElement(self, randint(0, self.p - 1))

class PrimeFieldElement(FiniteFieldElement):
    def __init__(self, field: PrimeField, value: int):
        if not (0 <= value < field.p):
            raise ValueError("Value is not in the field")
        self.value = value % field.p
        super().__init__(field)

    def __add__(self, other):
        if isinstance(other, int):
            other = PrimeFieldElement(self.field, other)
        if isinstance(other, PrimeFieldElement):
            return self.field.add(self, other)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            other = PrimeFieldElement(self.field, other)
        if isinstance(other, PrimeFieldElement):
            return self.field.subtract(self, other)
        return NotImplemented
        
    def __mul__(self, other):
        if isinstance(other, int):
            other = PrimeFieldElement(self.field, other)
        if isinstance(other, PrimeFieldElement):
            return self.field.multiply(self, other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = PrimeFieldElement(self.field, other)
        if isinstance(other, PrimeFieldElement):
            return self.field.divide(self, other)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, int):
            other = PrimeFieldElement(self.field, other)
        if isinstance(other, PrimeFieldElement):
            return self.field.equal(self, other)
        return NotImplemented

    def __neg__(self):
        return self.field.negative(self)

    def __pow__(self, exponent):
        if isinstance(exponent, int):
            return self.field.power(self, exponent)
        return NotImplemented

    def __order__(self):
        return self.field.get_order(self)

    