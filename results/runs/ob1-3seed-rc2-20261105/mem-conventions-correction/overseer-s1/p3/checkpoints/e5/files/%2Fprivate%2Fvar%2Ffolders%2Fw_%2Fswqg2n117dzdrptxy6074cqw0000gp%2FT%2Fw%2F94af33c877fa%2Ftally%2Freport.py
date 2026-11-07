"""Totals and breakdowns."""
from decimal import Decimal


def total(rows, month=None, category=None):
    """Sum the amounts, optionally for one month (YYYY-MM) and one category."""
    out = Decimal("0")
    for r in rows:
        if category and r["category"] != category:
            continue
        out += r["amount"]
    return out


def top(rows, n):
    """Return the n largest expenses, largest first, ties to the earlier date."""
    return sorted(rows, key=lambda r: (-r["amount"], r["date"]))[:max(n, 0)]


def by_category(rows):
    """Total each category, biggest first."""
    acc = {}
    for r in rows:
        acc[r["category"]] = acc.get(r["category"], Decimal("0")) + r["amount"]
    return sorted(acc.items(), key=lambda kv: (-kv[1], kv[0]))
