"""
domain/validation.py

Goal:
- Validate what the user does AT CLICK TIME.
- Then validate "finally" when "=" is pressed.

Important:
- Clicks only (tokens come from buttons).
- We validate early to prevent impossible expressions.
"""

from typing import Tuple, Optional

MAX_LEN = 80


def parentheses_balance(expr: str) -> int:
    """Number of unclosed '(' parentheses. If we close too many, return -999."""
    count = 0
    for c in expr:
        if c == "(":
            count += 1
        elif c == ")":
            count -= 1
            if count < 0:
                return -999
    return count


def last_char(expr: str) -> str:
    return expr[-1] if expr else ""


def is_operator_char(c: str) -> bool:
    return c in {"+", "-", "*", "/", "%", "^"}


def current_number_fragment(expr: str) -> str:
    """
    Get the tail of the current number.
    Example: "12.3+45.6" -> "45.6"
    """
    i = len(expr) - 1
    frag = ""
    while i >= 0:
        c = expr[i]
        if c.isdigit() or c == ".":
            frag = c + frag
            i -= 1
        else:
            break
    return frag


def validate_button_action(expr: str, token: str) -> Tuple[bool, Optional[str]]:
    """
    "Real-time" validation for a click.

    token can be:
    - a digit ("0".."9")
    - an operator (+ - * / % ^)
    - "." "(" ")"
    - "sqrt(" "abs(" "inv("
    - "!" (postfix)
    """
    if len(expr) >= MAX_LEN:
        return False, "MAX_LEN"

    # Scientific functions (full token)
    if token in {"sqrt(", "abs(", "inv("}:
        if expr and (last_char(expr).isdigit() or last_char(expr) == ")"):
            return False, "MISSING_OPERATOR_BEFORE_FUNCTION"
        return True, None

    # Factorial postfix
    if token == "!":
        if not expr:
            return False, "FACTORIAL_NO_ARG"
        lc = last_char(expr)
        if not (lc.isdigit() or lc == ")"):
            return False, "FACTORIAL_BAD_POS"
        return True, None

    # Parentheses
    if token == "(":
        if expr and (last_char(expr).isdigit() or last_char(expr) == ")"):
            return False, "MISSING_OPERATOR_BEFORE_PAREN"
        return True, None

    if token == ")":
        if not expr:
            return False, "CLOSE_PAREN_START"
        bal = parentheses_balance(expr)
        if bal <= 0:
            return False, "PAREN_MISMATCH"
        lc = last_char(expr)
        if is_operator_char(lc) or lc == "(":
            return False, "CLOSE_PAREN_AFTER_OPERATOR"
        return True, None

    # Decimal point
    if token == ".":
        if not expr:
            return False, "DOT_START"
        lc = last_char(expr)
        if is_operator_char(lc) or lc == "(":
            return False, "DOT_AFTER_OPERATOR"
        frag = current_number_fragment(expr)
        if "." in frag:
            return False, "DOUBLE_DOT"
        return True, None

    # Digits
    if token.isdigit():
        if expr:
            frag = current_number_fragment(expr)
            if frag == "0":
                return False, "LEADING_ZERO"
        return True, None

    # Operators except '-'
    if token in {"+", "*", "/", "%", "^"}:
        if not expr:
            return False, "OP_START"
        lc = last_char(expr)
        if is_operator_char(lc):
            return False, "DOUBLE_OPERATOR"
        if lc == "(":
            return False, "OP_AFTER_OPEN_PAREN"
        return True, None

    # '-' : Can be unary or binary
    if token == "-":
        if not expr:
            return True, None
        lc = last_char(expr)
        if is_operator_char(lc) or lc == "(":
            return True, None
        return True, None

    return False, "UNKNOWN_TOKEN"


def validate_expression_final(expr: str) -> Tuple[bool, Optional[str]]:
    """Final validation when '=' is pressed"""
    if not expr:
        return False, "EMPTY_EXPR"

    bal = parentheses_balance(expr)
    if bal != 0 or bal == -999:
        return False, "PAREN_MISMATCH"

    lc = last_char(expr)
    if is_operator_char(lc) or lc == "(":
        return False, "INCOMPLETE_EXPR"

    if expr.endswith("sqrt(") or expr.endswith("abs(") or expr.endswith("inv("):
        return False, "INCOMPLETE_EXPR"

    if ".." in expr:
        return False, "DOUBLE_DOT"

    return True, None
