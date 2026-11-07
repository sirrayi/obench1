"""Totals and breakdowns."""
from decimal import Decimal


def month_key(value):
    """Return the YYYY-MM key of an ISO date or month, or None if it has none."""
    parts = value.split("-")
    if len(parts) < 2:
        return None
    year, month = parts[0], parts[1]
    if not (year.isdigit() and month.isdigit()):
        return None
    if len(year) != 4 or not 1 <= int(month) <= 12:
        return None
    return "%04d-%02d" % (int(year), int(month))


def total(rows, month=None, category=None):
    """Sum the amounts, optionally for one month (YYYY-MM) and one category."""
    wanted = month_key(month) if month else None
    if month and wanted is None:
        raise ValueError("not a month as YYYY-MM: %r" % month)
    out = Decimal("0")
    for r in rows:
        if wanted and month_key(r["date"]) != wanted:
            continue
        if category and r["category"] != category:
            continue
        out += r["amount"]
    return out


def by_category(rows):
    """Total each category, biggest first."""
    acc = {}
    for r in rows:
        acc[r["category"]] = acc.get(r["category"], Decimal("0")) + r["amount"]
    return sorted(acc.items(), key=lambda kv: (-kv[1], kv[0]))


def top(rows, n):
    """Return the n largest expenses, biggest first, ties by earlier date."""
    if n <= 0:
        return []
    return sorted(rows, key=lambda r: (-r["amount"], r["date"]))[:n]
