from random import randrange
from src import Polynomial

def millerRabin(n: int, k: int =5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    u = n - 1
    s = 0
    while u % 2 == 0:
        u //= 2
        s += 1

    for _ in range(k):
        a = randrange(2, n)
        x = pow(a, u, n)
        if x == 1 or x == n - 1:
            # n pasa el test en base a
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                # n pasa el test en base a
                break
            elif x == 1:
                # Si aparece 1 antes de n-1, n es compuesto
                return False
        else:
            # n es compuesto
            return False
            
    # n pasa el test en todas las bases probadas
    return True

def factorization(n: int):
    factors = dict()
    # Dividir por 2 hasta que n sea impar
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    # Probar con números impares desde 3 hasta la raíz cuadrada de n
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n //= i
    if n > 2:
        factors[n] = factors.get(n, 0) + 1
    return factors

def prime_factors(n: int):
    return list(factorization(n).keys())

def Rabin(poly):
    prime_factors = prime_factors(poly.degree())
    

def generate_irreducible_polynomial(degree: int, field):
    if degree < 1:
        raise ValueError("Degree must be at least 1")
    # Genera un polinomio monico de grado 'degree' con coeficientes aleatorios en el cuerpo finito dado
    coefficients = [0] * (degree + 1)
    coefficients[degree] = field.one()
    while True:
        # El primer coeficiente no puede ser cero para que el polinomio sea irreducible
        coefficients[0] = field.random_element()
        if coefficients[0] != field.zero():
            break
        # Los coeficinetes intermedios pueden ser cualquier elemento del cuerpo finito
        for i in range(1,degree):
            coefficients[i] = field.random_element()
        # Generamos el polinomio y aplicamos el test de Rabin para verificar si es irreducible
        poly = Polynomial(coefficients)
        if Rabin(poly):
            return poly