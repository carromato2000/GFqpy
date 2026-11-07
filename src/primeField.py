from src import FiniteField, FiniteFieldElement, millerRabin, IntegerRing
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

    def compatible(self, other):
        if isinstance(other, IntegerRing):
            return True
        if isinstance(other, 'PrimeField'):
            return self.p == other.p

    def random_element(self, size: int = 0):
        return PrimeFieldElement(self, randint(0, self.p - 1))

    def convert(self, element):
        if isinstance(element, PrimeFieldElement):
            return element
        if isinstance(element, int):
            return PrimeFieldElement(self, element)
        return None

class PrimeFieldElement(FiniteFieldElement):
    def __init__(self, field: PrimeField, value: int):
        self.value = value % field.p
        super().__init__(field)

    def __add__(self, other):
        other = self.field.convert(other)
        if other is None:
            return NotImplemented
        return PrimeFieldElement(self.field, (self.value + other.value % self.field.p))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = self.field.convert(other)
        if other is None:
            return NotImplemented
        return PrimeFieldElement(self.field, (self.value - other.value % self.field.p))

    def __rsub__(self, other):
        return self.__sub__(other)
        
    def __mul__(self, other):
        other = self.field.convert(other)
        if other is None:
            return NotImplemented
        return PrimeFieldElement(self.field, (self.value * other.value % self.field.p))

    def __rmul__(self, other):
        return self.__mul__(other)

    @property
    def inverse(self):
        return PrimeFieldElement(self.field, pow(self.value, -1, self.field.p))

    def __truediv__(self, other):
        other = self.field.convert(other)
        if other is None:
            return NotImplemented
        return self.__mul__(other.inverse)

    def __rtruediv__(self, other):
        return self.inverse.__mul__(other)

    def __eq__(self, other):
        other = self.field.convert(other)
        if other is None:
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __neg__(self):
        return PrimeFieldElement(self.field, -self.value)

    def __pow__(self, exponent):
        if not isinstance(exponent, int):
            raise ValueError(f"exponent: {exponent} is not an integer")
        if exponent > 0:
            res = 1
            for _ in range(exponent):
                res *= self.value
                res %= self.field.p
            return PrimeFieldElement(self.field, res)
        elif exponent < 0:
            self.inverse.__pow__(-exponent)
        else:
            return self.field.one
    @property
    def order(self):
        if self.value == 0:
            return 
        return self.field.p - 1

    def __str__(self):
        return f"({self.value} mod {self.field.p})"

    def __repr__(self):
        return f"PrimeFieldElement: {self.__str__()}"
    