"""Read and write the expenses file."""
import csv
import os
from decimal import Decimal

FIELDS = ["date", "amount", "category", "note"]


def db_path():
    """Return the expenses file path: $TALLY_DB, or expenses.csv here."""
    return os.environ.get("TALLY_DB", "expenses.csv")


def load(path=None):
    """Load every expense, in file order."""
    with open(path or db_path(), newline="") as f:
        return [dict(r, amount=Decimal(r["amount"])) for r in csv.DictReader(f)]


def append(row, path=None):
    """Append one expense, writing the header first if the file is new."""
    p = path or db_path()
    new = not os.path.exists(p)
    with open(p, "a", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        if new:
            w.writeheader()
        w.writerow(dict(row, amount="%.2f" % Decimal(row["amount"])))
