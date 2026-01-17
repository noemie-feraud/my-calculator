"""
domain/scientific.py

Goal:
- Scientific functions WITHOUT the math module.
- Return None if impossible (helps with error handling).
"""

from typing import Optional


def abs_value(x: float) -> float:
    """Absolute value"""
    return x if x >= 0 else -x


def inv_value(x: float) -> Optional[float]:
    """Reciprocal 1/x. None if x == 0"""
    if x == 0:
        return None
    return 1.0 / x


def is_integer_value(x: float) -> bool:
    """True if x is exactly an integer (e.g., 5.0)"""
    return x == int(x)


def factorial_int(x: float) -> Optional[float]:
    """
    Factorial :
    - integer
    - >= 0
    """
    if not is_integer_value(x):
        return None
    n = int(x)
    if n < 0:
        return None

    res = 1
    i = 1
    while i <= n:
        res *= i
        i += 1
    return float(res)


def pow_int(a: float, b: float) -> Optional[float]:
    """
    Power a^b with integer b.
    - None if b is not an integer
    - None if 0^negative
    """
    if not is_integer_value(b):
        return None

    n = int(b)
    if n == 0:
        return 1.0

    if n < 0:
        if a == 0:
            return None
        pos = pow_int(a, float(-n))
        if pos is None or pos == 0:
            return None
        return 1.0 / pos

    # simple : multiplications
    res = 1.0
    i = 0
    while i < n:
        res *= a
        i += 1
    return res


def sqrt_newton(x: float, iterations: int = 25) -> Optional[float]:
    """
    Square root approximated using Newton's method.
    - None if x < 0
    """
    if x < 0:
        return None
    if x == 0:
        return 0.0

    guess = x
    i = 0
    while i < iterations:
        guess = (guess + x / guess) / 2.0
        i += 1
    return guess


def mod_int(a: float, b: float) -> Optional[float]:
    """
    Modulo :
    - a and b integers
    - b != 0
    """
    if b == 0:
        return None
    if not is_integer_value(a) or not is_integer_value(b):
        return None
    return float(int(a) % int(b))
