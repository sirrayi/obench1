"""Small helpers shared across packages."""

EXPONENT = {"USD": 2, "EUR": 2, "GBP": 2, "CHF": 2, "JPY": 0, "KWD": 3}


def round_money(x: float, currency: str) -> float:
    """A float amount rounded to the currency's minor unit (float era)."""
    return round(x, EXPONENT[currency])
