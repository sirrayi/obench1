"""Reader for the APAC ledger export (pipe-separated)."""
from decimal import Decimal


def _strip_grouping(raw):
    # APAC exports group thousands with spaces and use a decimal comma: "1 234,56"
    return raw.strip().replace(" ", "").replace(".", "").replace(",", ".")


def load(path):
    """Read an APAC feed: a list of {date, account, amount} rows."""
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#") or line.startswith("date|"):
                continue
            date, account, amount = line.split("|")
            out.append({"date": date, "account": account, "amount": Decimal(_strip_grouping(amount))})
    return out
