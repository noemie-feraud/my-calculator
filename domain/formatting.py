"""
domain/formatting.py

But :
- Formater le résultat en texte propre.
Exemples :
- 3.0 -> "3"
- 2.5000 -> "2.5"
- Si c'est trop long : affichage façon "e" (simple, sans math)
"""


def format_result(value: float, max_len: int = 18) -> str:
    """
    Formate un float pour affichage.
    """
    # Cas entier exact
    if value == int(value):
        s = str(int(value))
    else:
        s = str(value)
        if "." in s:
            s = s.rstrip("0").rstrip(".")

    # Si trop long, on passe en "notation scientifique" simple (affichage)
    if len(s) > max_len:
        sign = "-" if s.startswith("-") else ""
        raw = s.lstrip("-")

        # enlève le point
        if "." in raw:
            raw = raw.replace(".", "")

        # enlève les zéros de tête
        raw = raw.lstrip("0") or "0"

        if len(raw) == 1:
            return sign + raw

        mantissa = raw[0] + "." + raw[1:7]
        exp = len(raw) - 1
        return f"{sign}{mantissa}e+{exp}"

    return s
