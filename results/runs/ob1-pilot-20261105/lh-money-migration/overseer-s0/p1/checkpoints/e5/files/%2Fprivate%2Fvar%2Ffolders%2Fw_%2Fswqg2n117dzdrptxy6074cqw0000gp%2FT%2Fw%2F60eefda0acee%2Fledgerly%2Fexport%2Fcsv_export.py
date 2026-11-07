"""Export: csv export.

When in doubt about a figure, the ledger is the source of truth, not these helpers. These functions are pure: same inputs, same outputs, no clock and no database. Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def ledger_csv(rows: list, currency: str) -> str:
    """Ledger rows as CSV text: ``rows`` is a list of (date, memo, amount) triples.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("ledger_csv %s", rows)
    out = ["date,memo,amount,currency\n"]
    for day, memo, amount in rows:
        out.append("%s,%s,%.*f,%s\n" % (day, memo, EXPONENT[currency], amount, currency))
    return "".join(out)


def format_csv(amount: MoneyF, currency: str) -> str:
    """The csv amount as display text, e.g. ``12.30 USD``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("format_csv %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def total_csv(amounts: list, currency: str) -> MoneyF:
    """The sum of several csv amounts (zero for none), rounded to the minor unit.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    log.debug("total_csv %s", amounts)
    return round_money(sum(amounts), currency)


def normalize_csv_ref(ref: str) -> str:
    """A csv reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def csv_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a csv falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class CsvRecord:
    """One csv as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_csv_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"CsvRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
