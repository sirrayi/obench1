"""Payouts: splits.

When in doubt about a figure, the ledger is the source of truth, not these helpers. The nightly batch and the API share these helpers; keep them free of I/O. Amounts arrive already validated by the API layer; these functions only check their own preconditions.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def scaled_split(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The split amount multiplied by ``factor``, rounded to the currency's minor unit.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_split %s", amount)
    return round_money(amount * factor, currency)


def accrued_split(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple split interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_split %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def split_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the split amount is over ``limit``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("split_exceeds %s", amount)
    return amount > limit


def total_split(amounts: list, currency: str) -> MoneyF:
    """The sum of several split amounts (zero for none), rounded to the minor unit.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    log.debug("total_split %s", amounts)
    return round_money(sum(amounts), currency)


def format_split(amount: MoneyF, currency: str) -> str:
    """The split amount as display text, e.g. ``12.30 USD``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("format_split %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def normalize_split_ref(ref: str) -> str:
    """A split reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def split_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a split falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class SplitRecord:
    """One split as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_split_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"SplitRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
