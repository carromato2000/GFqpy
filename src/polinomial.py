from math import inf
from src import IntegerRing, Ring

class PolynomialRing(Ring):
    def __init__(self, letter='x', ring : Ring = IntegerRing()):
        self.letter = letter
        self.ring = ring

    @property
    def one(self):
        return Polynomial({0: self.ring.one}, self)

    @property
    def characteristic(self):
        return self.ring.characteristic

    def compatible(self, other: Ring) -> bool:
        if not isinstance(other, PolynomialRing):
            return self.ring.compatible(other)
        return self.ring.compatible(other.ring)

    def convert(self, item):
        # Si convert es un polinomio comprobamos la compatibilidad de los anillos de polinomios
        if isinstance(item, Polynomial):
            return item if (self.compatible(item.poly_ring) and self.letter == item.letter) else None
        else:
            # Si convert no es un polinomio, delegamos la conversion al anillo de coeficientes
            item = self.ring.convert(item)
            return Polynomial({0: item}, self) if item is not None else None

    def random_element(self, degree: int | float, size: int = 1024):
        if isinstance(degree, float):
            if degree == -inf:
                coeffs = {}
            else:
                raise ValueError(f"Invalid degree: {degree}")
        else:
            if degree < 0:
                raise ValueError(f"Invalid degree: {degree}")
            coeffs = {i: self.ring.random_element(size) for i in range(degree+1)}        
        return Polynomial(coeffs, self, self.letter)


    def gen(self):
        return Polynomial({1: self.ring.one}, self, self.letter)
        
class Polynomial():
    # Convención: 
    # {} = polinomio nulo
    # {0: c} = polinomio constante c != 0
    # {1: c} = polinomio lineal c != 0
    # {n: c} = monomio de grado n con coeficiente c != 0
    # Los items del diccionario cuyo valor es 0, se eliminan
    # Se escribe explicitamente 0, que es un elemento universal en cualquier anillo

    def __init__(self, coeffs, poly_ring=PolynomialRing()):
        # En anillo de polinomios por defecto, es el anillo de polinomios sobre los enteros
        self.poly_ring = poly_ring
        # Posibilidad de cambiar la letra del polinomio, si se pasa como argumento
        self.letter = poly_ring.letter
        self._terms = {}
        if isinstance(coeffs, dict):
            self._terms = {k: v for k, v in coeffs.items() if v != 0}
            self.degree = max(self._terms, default=-inf)
        else: 
            raise ValueError("Coefficients must be a dictionary")

    def monic(self):
        if self.degree < 0:
            return Polynomial({}, self.poly_ring)
        leading_coeff = self._terms[self.degree]
        if leading_coeff == 1:
            return self
        coeffs = {
            degree: coeff / leading_coeff
            for degree, coeff in self._terms.items()
        }
        return Polynomial(coeffs, self.poly_ring)

    def __add__(self, other):
        # Si other no es un polinomio, encargamos al anillo de polinomios que lo convierta en uno si puede
        other = self.poly_ring.convert(other)
        if other is None:
            return NotImplemented
        if isinstance(other, Polynomial):
            coeffs = self._terms.copy()
            # La suma se define en terminos de los métodos __add__ y __radd__ de los coeficientes
            for degree, coefficient in other._terms.items():
                coeffs[degree] = coeffs.get(degree, 0) + coefficient
            return Polynomial(coeffs, self.poly_ring)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = self.poly_ring.convert(other)
        if other is None:
            return NotImplemented
        coeffs = self._terms.copy()
        # La resta se define en terminos de los métodos __sub__ y __rsub__ de los coeficientes
        for degree, coefficient in other._terms.items():
            coeffs[degree] = coeffs.get(degree, 0) - coefficient
        return Polynomial(coeffs, self.poly_ring)

    def __neg__(self):
        # Delegamos la negación a la implementación  de __neg__ de los coeficientes
        return Polynomial({degree: -coefficient for degree, coefficient in self._terms.items()}, self.poly_ring)

    def __rsub__(self, other):
        return (-self).__add__(other)

    def __mul__(self, other):
        other = self.poly_ring.convert(other)
        if other is None:
            return NotImplemented
        degree = self.degree + other.degree 
        if degree < 0:
            return Polynomial({}, self.poly_ring)
        coeffs = {}
        for i, coefficient1 in self._terms.items():
            for j, coefficient2 in other._terms.items():
                degree = i + j
                coeffs[degree] = (
                    coeffs.get(degree, 0) + coefficient1 * coefficient2
                )
        return Polynomial(coeffs, self.poly_ring)
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, other):
        if isinstance(other, int):
            if other < 0:
                raise ValueError("Negative exponent not supported for polynomials")
            result = Polynomial({0: self.poly_ring.ring.one}, self.poly_ring)
            for _ in range(other):
                result *= self
            return result
        return NotImplemented

    def __divmod__(self, other):
        other = self.poly_ring.convert(other)
        if other is None:
            return NotImplemented
        if other.degree < 0:
            raise ZeroDivisionError("Polynomial division by zero")
        if self.degree < 0:
            # 0 = 0 * other + 0
            return Polynomial({}, self.poly_ring), Polynomial({}, self.poly_ring)
        quotient_coeffs = {}
        # Algoritmo de la división de polinomios
        remainder = Polynomial(self._terms, self.poly_ring)
        while remainder.degree >= other.degree:
            degree = remainder.degree - other.degree
            coefficient = remainder[remainder.degree] / other[other.degree]
            quotient_coeffs[degree] = coefficient
            remainder -= Polynomial({degree: coefficient}, self.poly_ring) * other
        return Polynomial(quotient_coeffs, self.poly_ring), remainder

    def __floordiv__(self, other):
        return divmod(self, other)[0]

    def __mod__(self, other):
        return divmod(self, other)[1]

    def __eq__(self, other):
        other = self.poly_ring.convert(other)
        if other is None:
            return NotImplemented
        if other.letter != self.letter:
            if self.degree < 1 and other.degree < 1:
                return self._terms == other._terms
            else:
                return False
        return self._terms == other._terms

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self._terms)

    def __getitem__(self, index):
        if not isinstance(index, int) or index < 0:
            raise IndexError("Index must be a non-negative integer")
        return self._terms.get(index, 0)
    
    def __gcd__(self, other):
        other = self.poly_ring.convert(other)
        if other is None:
            return NotImplemented
        a, b = self, other
        while b.degree >= 0:
            _, r = divmod(a, b)
            a, b = b, r
        return a.monic()

    def __str__(self):
        terms = []
        for i in sorted(self._terms):
            coeff = self._terms[i]
            if i == 0:
                terms.append(f"{coeff}")
            elif i == 1:
                terms.append(f"{coeff}{self.letter}")
            else:
                terms.append(f"{coeff}{self.letter}^{i}")
        return " + ".join(terms) if terms else "0"
