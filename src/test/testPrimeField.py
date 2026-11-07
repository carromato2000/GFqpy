import unittest
from src import PrimeField, PrimeFieldElement

class TestPrimeField(unittest.TestCase):
    def setUp(self):
        self.field = PrimeField(7)

    def test_addition(self):
        cases = [
            (3, 5, 1, 7),  # (3 + 5) % 7 = 1
            (2, 4, 6, 11),  # (2 + 4) % 11 = 6
        ]
        for a_val, b_val, expected, prime in cases:
            with self.subTest(a=a_val, b=b_val, expected=expected, prime=prime):
                self.field = PrimeField(prime)  
                a = PrimeFieldElement(field = self.field, value = a_val)
                b = PrimeFieldElement(field = self.field, value = b_val)
                result = a + b
                self.assertEqual(result, expected)
                result = b + a
                self.assertEqual(result, expected)  # Commutativity
                result = a + b_val
                self.assertEqual(result, expected)  # Commutativity with int
                result = b_val + a
                self.assertEqual(result, expected)  # Commutativity with int

    def test_multiplication(self):
        cases = [
            (3, 5, 1, 7),  # (3 * 5) % 7 = 1
            (2, 4, 8, 11),  # (2 * 4) % 11 = 8
        ]
        for a_val, b_val, expected, prime in cases:
            with self.subTest(a=a_val, b=b_val, expected=expected, prime=prime):
                self.field = PrimeField(prime)  
                a = PrimeFieldElement(field = self.field, value = a_val)
                b = PrimeFieldElement(field = self.field, value = b_val)
                result = a * b
                self.assertEqual(result, expected)
                result = b * a
                self.assertEqual(result, expected)  # Commutativity
                result = a * b_val
                self.assertEqual(result, expected) 
                result = b_val * a
                self.assertEqual(result, expected)  # Commutativity with int

    def test_inverse(self):
        cases = [
            (3, 5, 7),  # Inverse of 3 mod 7 is 5
        ]
        for a_val, expected_inverse, prime in cases:
            with self.subTest(a=a_val, expected_inverse=expected_inverse, prime=prime):
                self.field = PrimeField(prime)  
                a = PrimeFieldElement(field = self.field, value = a_val)
                inverse_a = self.field.inverse(a)
                self.assertEqual(inverse_a, expected_inverse)

    def test_subtraction(self):
        cases = [
            (3, 5, 5, 7),  # (3 - 5) % 7 = 5
            (2, 4, 9, 11),  # (2 - 4) % 11 = 9
        ]
        for a_val, b_val, expected, prime in cases:
            with self.subTest(a=a_val, b=b_val, expected=expected, prime=prime):
                self.field = PrimeField(prime)  
                a = PrimeFieldElement(field = self.field, value = a_val)
                b = PrimeFieldElement(field = self.field, value = b_val)
                result = a - b
                self.assertEqual(result, expected)
                result = a - b_val
                self.assertEqual(result, expected)

    def test_division(self):
        cases = [
            (3, 5, 2, 7),  # (3 / 5) % 7 = 2
        ]
        for a_val, b_val, expected, prime in cases:
            with self.subTest(a=a_val, b=b_val, expected=expected, prime=prime):
                self.field = PrimeField(prime)
                a = PrimeFieldElement(field = self.field, value = a_val)
                b = PrimeFieldElement(field = self.field, value = b_val)
                result = a / b 
                expected = PrimeFieldElement(field = self.field, value = expected)
                self.assertEqual(result, expected)

    def test_power(self):
        cases = [
            (3, 2, 2, 7),  # (3^2) % 7 = 2
            (2, 3, 8, 11),  # (2^3) % 11 = 8
        ]
        for a_val, exponent, expected, prime in cases:
            with self.subTest(a=a_val, exponent=exponent, expected=expected, prime=prime):
                self.field = PrimeField(prime)
                a = PrimeFieldElement(field = self.field, value = a_val)
                result = self.field.power(a.value, exponent)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    import unittest
    unittest.main()