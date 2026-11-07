from sage.all import *
from src.alfabet import Alfabet

class PrimitiveBCH():
    def __init__(self, alfabet: Alfabet, m: int, d: int):
        self.alfabet = alfabet
        q = alfabet.len
        self.q = q
        self.m = m
        self.d = d
        self.base_field = GF(q)
        self.base_polynomial_ring= PolynomialRing(self.base_field,  'x')
        self.extension_field = GF(q**m)
        self.apha = self.extension_field.multiplicative_generator()
        self.extension_polynomial_ring = PolynomialRing(self.extension_field, 'x')
        x = self.base_polynomial_ring.gen()
        self.p = x**(q**m-1)-1
        self.generator = self.compute_generator_polynomial()
        self.n = q**m-1
        self.k = self.n - self.generator.degree()

    def minimal_polynomal(self, beta):
        """
        Calcula el polinomio mínimo del elemento de la extensión respecto del cuerpo base

        Args:
            beta : Elemento de la extensión del cual calcular su polinomio mínimo
        """
        if beta not in self.extension_field:
            raise ValueError()
        x = self.extension_polynomial_ring.gen()
        f_beta = x - beta
        i = 1
        next = beta**(self.q**i)
        while next != beta:
            f_beta = f_beta * (x-next)
            i += 1
            next = beta**(self.q**i)
        coefficients = [
            self.base_field(c) for c in f_beta.list()
        ]
        return self.base_polynomial_ring(coefficients)

    def compute_generator_polynomial(self):
        """
        Calcula y devuelve el polinómio generador del código BCH
        """
        minimal_polynomials = set()
        for i in range(1, self.d):
            minimal_polynomials.add(self.minimal_polynomal(self.apha**i))
        generator = self.base_polynomial_ring.one()
        for f in minimal_polynomials:
            generator *= f
        return generator.monic()

    def dataword_str_to_GF_list(self, dataword: str):
        if len(dataword) != self.k:
            raise ValueError("dataword has no appropiate length")
        datawordGF = []
        for sym in dataword:
            index = self.alfabet.sym_to_index.get(sym)
            if index is None:
                raise ValueError("dataword has unkown symbols")
            datawordGF.append(self.base_field.from_integer(index))
        return datawordGF

    def GF_list_to_polynomial(self, GF_list):
        return self.base_polynomial_ring(list(reversed(GF_list)))

    def dataword_to_polynomial(self, dataword):
        GF_list = self.dataword_str_to_GF_list(dataword)
        return self.GF_list_to_polynomial(GF_list)

    def GF_list_to_codeword(self, GF_list):
        codeword = []
        for item in GF_list:
            codeword.append(self.alfabet.alfabet_str[item._integer_representation()])
        return ''.join(codeword)

    def polynomial_to_GF_list(self, cx):
        codeword_coefficients = cx.list()
        codeword_coefficients.extend(
            [self.base_field.zero()] * (self.n - len(codeword_coefficients))
        )
        return list(reversed(codeword_coefficients))


    def polynomial_to_codeword(self, cx):
        GF_list = self.polynomial_to_GF_list(cx)
        return self.GF_list_to_codeword(GF_list)

    
    def non_systematic_codification(self, dataword):
        ax = self.dataword_to_polynomial(dataword)
        return self.polynomial_to_codeword(*self.generator)

    def systematic_codification(self, dataword):
        ax = self.dataword_to_polynomial(dataword)
        x = self.base_polynomial_ring.gen()
        shifted = x**(self.n-self.k) * ax
        remainder = shifted.quo_rem(self.generator)[1]
        codeword = shifted - remainder

        return self.polynomial_to_codeword(codeword)