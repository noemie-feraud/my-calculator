import unittest
from domain.engine import evaluate_expression


class TestEngineStandard(unittest.TestCase):
    def test_add(self):
        ok, v, e = evaluate_expression("1+2")
        self.assertTrue(ok)
        self.assertEqual(v, 3.0)

    def test_priority(self):
        ok, v, e = evaluate_expression("2+3*4")
        self.assertTrue(ok)
        self.assertEqual(v, 14.0)

    def test_parentheses(self):
        ok, v, e = evaluate_expression("(2+3)*4")
        self.assertTrue(ok)
        self.assertEqual(v, 20.0)

    def test_div_zero(self):
        ok, v, e = evaluate_expression("3/0")
        self.assertFalse(ok)
        self.assertEqual(e, "DIV_ZERO")

    def test_unary_minus(self):
        ok, v, e = evaluate_expression("-3+5")
        self.assertTrue(ok)
        self.assertEqual(v, 2.0)


if __name__ == "__main__":
    unittest.main()
