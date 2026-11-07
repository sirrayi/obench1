"""Reader for the EU ledger export (semicolon-separated)."""
from decimal import Decimal

from meridian import text


def read_feed(path):
    """Read an EU feed: a list of {date, account, amount} rows."""
    rows = []
    with open(path, encoding="utf-8") as f:
        lines = [x for x in f.read().splitlines() if x and not x.startswith("#")]
    for line in lines[1:]:
        date, account, amount = line.split(";")
        rows.append({"date": date, "account": account, "amount": Decimal(text.clean_number(amount))})
    return rows
