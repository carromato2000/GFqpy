from sage.all import GF, gcd, PolynomialRing
from src.alfabet import Alfabet

class BCHcode():
    def __init__(self, alfabet: Alfabet, n: int, d: int):
        q = alfabet.len
        if gcd(q, n) != 1:
            raise ValueError("blocklength n and alfabet length q must be coprime")
        else:
            m = 1
            while (q**m-1)%n != 0:
                m += 1
            self.m = m
        self.base_field = GF(q)
        self.poly_ring = PolynomialRing(self.base_field)

    def get_primitive_poly(self):
        # Busca un polinomio primitivo de grado q**m para construir la extensión
        pass

    



    




