import unittest
from src import millerRabin

class TestPrimality(unittest.TestCase):
    def test_millerRabin(self):
        # Test known primes
        known_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        for prime in known_primes:
            self.assertTrue(millerRabin(prime))

        # Test known composites
        known_composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18]
        for composite in known_composites:
            self.assertFalse(millerRabin(composite))

if __name__ == '__main__':
    unittest.main()