import unittest
from domain.validation import validate_button_action, validate_expression_final


class TestValidation(unittest.TestCase):
    def test_empty_final(self):
        ok, err = validate_expression_final("")
        self.assertFalse(ok)
        self.assertEqual(err, "EMPTY_EXPR")

    def test_parentheses_mismatch(self):
        ok, err = validate_expression_final("(1+2")
        self.assertFalse(ok)
        self.assertEqual(err, "PAREN_MISMATCH")

    def test_operator_start(self):
        ok, err = validate_button_action("", "+")
        self.assertFalse(ok)
        self.assertEqual(err, "OP_START")

    def test_decimal_start(self):
        ok, err = validate_button_action("", ".")
        self.assertFalse(ok)
        self.assertEqual(err, "DOT_START")


if __name__ == "__main__":
    unittest.main()
