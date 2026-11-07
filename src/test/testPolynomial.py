import unittest
from math import inf

from src import Polynomial


class TestPolinomial(unittest.TestCase):
    def test_01_creation(self):
        cases = [
            ({0: 1, 1: 2, 2: 3}, {0: 1, 1: 2, 2: 3}, 2),
            ({}, {}, -inf),
            ({0: 5, 2: 1}, {0: 5, 2: 1}, 2),
            ({0: 1}, {0: 1}, 0),
            ({1: 1}, {1: 1}, 1),
        ]
        for coeffs, expected_terms, degree in cases:
            with self.subTest(coeffs=coeffs):
                polynomial = Polynomial(coeffs)
                self.assertEqual(polynomial._terms, expected_terms)
                self.assertEqual(polynomial.degree, degree)

    def test_sparse_high_degree(self):
        polynomial = Polynomial({1_000_000: 7})

        self.assertEqual(polynomial.degree, 1_000_000)
        self.assertEqual(polynomial[1_000_000], 7)
        self.assertEqual(polynomial[0], 0)
        self.assertEqual(len(polynomial._terms), 1)

    def test_02_equality(self):
        cases = [
            ({0: 1, 1: 2, 2: 3}, {0: 1, 1: 2, 2: 3}, True),
            ({}, {}, True),
            ({0: 5, 2: 1}, {0: 5, 2: 1}, True),
            ({0: 1}, {0: 1}, True),
            ({1: 1}, {1: 1}, True),
            ({0: 1, 1: 2}, {0: 2, 1: 1}, False),
            ({0: 1, 1: 2, 2: 3}, {0: 1, 1: 2}, False),
        ]
        for coeffs1, coeffs2, expected in cases:
            with self.subTest(coeffs1=coeffs1, coeffs2=coeffs2):
                self.assertEqual(Polynomial(coeffs1) == Polynomial(coeffs2), expected)

    def test_03_monic(self):
        cases = [
            ({0: 1, 1: 2, 2: 3}, {0: 1 / 3, 1: 2 / 3, 2: 1}),
            ({}, {}),
            ({0: 5, 2: 1}, {0: 5, 2: 1}),
            ({0: 1}, {0: 1}),
            ({1: 1}, {1: 1}),
        ]
        for coeffs, expected_terms in cases:
            with self.subTest(coeffs=coeffs):
                self.assertEqual(Polynomial(coeffs).monic()._terms, expected_terms)

    def test_03_addition(self):
        cases = [
            ({0: 1, 1: 2, 2: 3}, {0: 4, 1: 5}, {0: 5, 1: 7, 2: 3}),
            ({}, {}, {}),
            ({0: 5, 2: 1}, {0: 1, 1: 2}, {0: 6, 1: 2, 2: 1}),
            ({0: 1}, {1: 1}, {0: 1, 1: 1}),
            ({1: 1}, {0: 1}, {0: 1, 1: 1}),
        ]
        for coeffs1, coeffs2, expected in cases:
            with self.subTest(coeffs1=coeffs1, coeffs2=coeffs2):
                self.assertEqual((Polynomial(coeffs1) + Polynomial(coeffs2))._terms, expected)

    def test_04_subtraction(self):
        cases = [
            ({0: 1, 1: 2, 2: 3}, {0: 4, 1: 5}, {0: -3, 1: -3, 2: 3}),
            ({}, {}, {}),
            ({0: 5, 2: 1}, {0: 1, 1: 2}, {0: 4, 1: -2, 2: 1}),
            ({0: 1}, {1: 1}, {0: 1, 1: -1}),
            ({1: 1}, {0: 1}, {0: -1, 1: 1}),
        ]
        for coeffs1, coeffs2, expected in cases:
            with self.subTest(coeffs1=coeffs1, coeffs2=coeffs2):
                self.assertEqual((Polynomial(coeffs1) - Polynomial(coeffs2))._terms, expected)

    def test_04_multiplication(self):
        cases = [
            ({0: 1, 1: 2}, {0: 3, 1: 4}, {0: 3, 1: 10, 2: 8}),
            ({}, {}, {}),
            ({0: 5}, {0: 1, 1: 2}, {0: 5, 1: 10}),
            ({0: 1}, {1: 1}, {1: 1}),
            ({1: 1}, {0: 1}, {1: 1}),
        ]
        for coeffs1, coeffs2, expected in cases:
            with self.subTest(coeffs1=coeffs1, coeffs2=coeffs2):
                self.assertEqual((Polynomial(coeffs1) * Polynomial(coeffs2))._terms, expected)

    def test_05_scalar_multiplication(self):
        cases = [
            ({0: 1, 1: 2, 2: 3}, 2, {0: 2, 1: 4, 2: 6}),
            ({}, 5, {}),
            ({0: 5, 2: 1}, -1, {0: -5, 2: -1}),
            ({0: 1}, 3, {0: 3}),
            ({1: 1}, 4, {1: 4}),
        ]
        for coeffs, scalar, expected in cases:
            with self.subTest(coeffs=coeffs):
                polynomial = Polynomial(coeffs)
                self.assertEqual((polynomial * scalar)._terms, expected)
                self.assertEqual((scalar * polynomial)._terms, expected)

    def test_06_power(self):
        cases = [
            ({0: 1, 1: 2}, 2, {0: 1, 1: 4, 2: 4}),
            ({}, 3, {}),
            ({0: 5}, 2, {0: 25}),
            ({0: 1}, 5, {0: 1}),
            ({1: 1}, 3, {3: 1}),
        ]
        for coeffs, exponent, expected in cases:
            with self.subTest(coeffs=coeffs):
                self.assertEqual((Polynomial(coeffs) ** exponent)._terms, expected)

    def test_04_division(self):
        cases = [
            ({0: 1, 1: 3, 2: 3}, {0: 1, 1: 1}, {1: 3}, {0: 1}),
            ({}, {}, {}, {}),
            ({}, {0: 1}, {}, {}),
            (
                {0: 1, 1: -7, 2: 4, 4: 1, 5: 6},
                {0: -3, 1: 1, 2: 2},
                {0: -2, 1: 5, 2: -1, 3: 3},
                {0: -5, 1: 10},
            ),
        ]
        for coeffs1, coeffs2, expected_q, expected_r in cases:
            with self.subTest(coeffs1=coeffs1, coeffs2=coeffs2):
                if not coeffs2:
                    with self.assertRaises(ZeroDivisionError):
                        divmod(Polynomial(coeffs1), Polynomial(coeffs2))
                else:
                    quotient, remainder = divmod(Polynomial(coeffs1), Polynomial(coeffs2))
                    self.assertEqual(quotient._terms, expected_q)
                    self.assertEqual(remainder._terms, expected_r)

    def test_07_gcd(self):
        cases = [
            ({0: -1, 2: 1}, {0: -1, 1: 1}, {0: -1, 1: 1}),
            ({2: 1}, {1: 1, 2: 1}, {1: 1}),
            ({0: 1, 1: 2, 2: 1}, {0: 1, 1: 1}, {0: 1, 1: 1}),
            ({}, {}, {}),
            ({1: 1}, {}, {1: 1}),
            ({1: 1}, {1: 1}, {1: 1}),
            ({0: 1, 1: 1, 2: 1}, {0: 1, 1: 1, 2: 1}, {0: 1, 1: 1, 2: 1}),
        ]
        for coeffs1, coeffs2, expected in cases:
            with self.subTest(coeffs1=coeffs1, coeffs2=coeffs2):
                self.assertEqual(Polynomial(coeffs1).__gcd__(Polynomial(coeffs2))._terms, expected)


if __name__ == "__main__":
    unittest.main()
