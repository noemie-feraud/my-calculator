"""
domain/formatting.py

Goal:
- Format the result into a clean text string.
Examples:
- 3.0 -> "3"
- 2.5000 -> "2.5"
- If it's too long: display using a simple "e"-style notation (no math)
"""


def format_result(value: float, max_len: int = 18) -> str:
    """
    Format a float for display
    """
    # Exact integer case
    if value == int(value):
        s = str(int(value))
    else:
        s = str(value)
        if "." in s:
            s = s.rstrip("0").rstrip(".")

    # If it's too long, switch to a simple "scientific notation" (for display)
    if len(s) > max_len:
        sign = "-" if s.startswith("-") else ""
        raw = s.lstrip("-")

        # Remove the decimal point
        if "." in raw:
            raw = raw.replace(".", "")

        # Remove leading zeros
        raw = raw.lstrip("0") or "0"

        if len(raw) == 1:
            return sign + raw

        mantissa = raw[0] + "." + raw[1:7]
        exp = len(raw) - 1
        return f"{sign}{mantissa}e+{exp}"

    return s
