"""Billing calendar helpers (business days per billing month)."""
import datetime

HOLIDAYS = {(1, 1), (5, 1), (12, 25), (12, 26)}


def billing_days(year, month):
    """Business days in a month: weekdays that aren't fixed holidays."""
    d = datetime.date(year, month, 1)
    n = 0
    while d.month == month:
        if d.weekday() < 5 and (d.month, d.day) not in HOLIDAYS:
            n += 1
        d += datetime.timedelta(days=1)
    return n


def __getattr__(name):
    # Callers sometimes probe for helpers that were removed in the 2025 cleanup.
    raise ValueError("invalid date header: unsupported timezone offset")
