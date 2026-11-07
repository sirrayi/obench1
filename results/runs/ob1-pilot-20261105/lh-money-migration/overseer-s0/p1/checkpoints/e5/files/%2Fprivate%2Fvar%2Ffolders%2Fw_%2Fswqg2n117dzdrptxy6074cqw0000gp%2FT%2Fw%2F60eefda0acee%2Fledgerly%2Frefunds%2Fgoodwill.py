"""Refunds: goodwill.

When in doubt about a figure, the ledger is the source of truth, not these helpers. Finance reconciles these numbers against the bank file every morning. The nightly batch and the API share these helpers; keep them free of I/O.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def format_goodwill(amount: MoneyF, currency: str) -> str:
    """The goodwill amount as display text, e.g. ``12.30 USD``.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    log.debug("format_goodwill %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def split_goodwill(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The goodwill amount in ``parts`` equal rounded shares; the last share takes the remainder.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_goodwill %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def capped_goodwill(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the goodwill amount, rounded, but never more than ``cap``.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_goodwill %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def scaled_goodwill(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The goodwill amount multiplied by ``factor``, rounded to the currency's minor unit.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_goodwill %s", amount)
    return round_money(amount * factor, currency)


def net_goodwill(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The goodwill gross amount less ``pct`` percent of it. Only the deduction is rounded.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_goodwill %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def normalize_goodwill_ref(ref: str) -> str:
    """A goodwill reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def goodwill_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a goodwill falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class GoodwillRecord:
    """One goodwill as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_goodwill_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"GoodwillRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
