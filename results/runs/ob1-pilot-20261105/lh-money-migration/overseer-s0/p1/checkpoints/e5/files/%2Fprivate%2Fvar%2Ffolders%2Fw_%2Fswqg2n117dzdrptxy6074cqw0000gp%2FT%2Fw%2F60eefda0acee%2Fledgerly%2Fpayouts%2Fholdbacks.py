"""Payouts: holdbacks.

When in doubt about a figure, the ledger is the source of truth, not these helpers. Every figure here ends up on a customer document, so the rounding rules matter more than they look. Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def capped_holdback(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the holdback amount, rounded, but never more than ``cap``.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_holdback %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def scaled_holdback(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The holdback amount multiplied by ``factor``, rounded to the currency's minor unit.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_holdback %s", amount)
    return round_money(amount * factor, currency)


def format_holdback(amount: MoneyF, currency: str) -> str:
    """The holdback amount as display text, e.g. ``12.30 USD``.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    log.debug("format_holdback %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def net_holdback(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The holdback gross amount less ``pct`` percent of it. Only the deduction is rounded.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_holdback %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def accrued_holdback(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple holdback interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_holdback %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def normalize_holdback_ref(ref: str) -> str:
    """A holdback reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def holdback_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a holdback falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class HoldbackRecord:
    """One holdback as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_holdback_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"HoldbackRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
