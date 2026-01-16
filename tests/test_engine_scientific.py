import unittest
from domain.engine import evaluate_expression


class TestEngineScientific(unittest.TestCase):
    def test_pow_int(self):
        ok, v, e = evaluate_expression("2^3")
        self.assertTrue(ok)
        self.assertEqual(v, 8.0)

    def test_pow_not_int(self):
        ok, v, e = evaluate_expression("2^2.5")
        self.assertFalse(ok)
        self.assertEqual(e, "POW_EXP_NOT_INT")

    def test_sqrt(self):
        ok, v, e = evaluate_expression("sqrt(9)")
        self.assertTrue(ok)
        self.assertTrue(abs(v - 3.0) < 0.001)

    def test_factorial(self):
        ok, v, e = evaluate_expression("5!")
        self.assertTrue(ok)
        self.assertEqual(v, 120.0)

    def test_abs(self):
        ok, v, e = evaluate_expression("abs(-7)")
        self.assertTrue(ok)
        self.assertEqual(v, 7.0)

    def test_inv(self):
        ok, v, e = evaluate_expression("inv(4)")
        self.assertTrue(ok)
        self.assertEqual(v, 0.25)


if __name__ == "__main__":
    unittest.main()
