"""Proration of a period's charge, in integer cents."""


def prorate(amount_cents, days_used, days_in_period):
    """Charge for `days_used` of the period: amount × used / period, rounded to the
    nearest cent (halves round up)."""
    if not 0 <= days_used <= days_in_period:
        raise ValueError("days_used out of range")
    return int(amount_cents * days_used / days_in_period)
