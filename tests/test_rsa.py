import unittest

from app import is_prime, extended_gcd, mod_inverse, mod_pow


class TestRSAFunctions(unittest.TestCase):

    def test_prime_validation(self):
        self.assertTrue(is_prime(61))
        self.assertTrue(is_prime(53))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(60))

    def test_extended_gcd(self):
        gcd, x, y = extended_gcd(7, 3120)
        self.assertEqual(gcd, 1)
        self.assertEqual(7 * x + 3120 * y, gcd)

    def test_mod_inverse(self):
        inverse = mod_inverse(7, 3120)
        self.assertEqual(inverse, 1783)
        self.assertEqual((7 * inverse) % 3120, 1)

    def test_modular_exponentiation(self):
        result, steps = mod_pow(123, 7, 3233)
        self.assertEqual(result, 2868)

        result, steps = mod_pow(2868, 1783, 3233)
        self.assertEqual(result, 123)


if __name__ == "__main__":
    unittest.main()