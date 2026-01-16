"""
domain/scientific.py

But :
- Fonctions scientifiques SANS module math.
- On renvoie None si impossible (ça aide à gérer les erreurs).
"""

from typing import Optional


def abs_value(x: float) -> float:
    """Valeur absolue."""
    return x if x >= 0 else -x


def inv_value(x: float) -> Optional[float]:
    """Inverse 1/x. None si x == 0."""
    if x == 0:
        return None
    return 1.0 / x


def is_integer_value(x: float) -> bool:
    """Vrai si x est exactement un entier (ex: 5.0)."""
    return x == int(x)


def factorial_int(x: float) -> Optional[float]:
    """
    Factorielle :
    - entier
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
    Puissance a^b avec b entier.
    - None si b non entier
    - None si 0^négatif
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
    Racine carrée approximée par Newton.
    - None si x < 0
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
    - a et b entiers
    - b != 0
    """
    if b == 0:
        return None
    if not is_integer_value(a) or not is_integer_value(b):
        return None
    return float(int(a) % int(b))
