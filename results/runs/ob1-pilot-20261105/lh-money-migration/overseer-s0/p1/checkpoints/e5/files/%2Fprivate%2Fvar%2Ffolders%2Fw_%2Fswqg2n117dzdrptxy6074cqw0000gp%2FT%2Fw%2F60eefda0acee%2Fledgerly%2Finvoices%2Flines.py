"""Invoices: lines.

Support quotes these numbers to customers, so a cent off is a ticket. The nightly batch and the API share these helpers; keep them free of I/O. These functions are pure: same inputs, same outputs, no clock and no database.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def net_line(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The line gross amount less ``pct`` percent of it. Only the deduction is rounded.

    Finance reconciles these numbers against the bank file every morning.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_line %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def line_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the line amount is over ``limit``.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    log.debug("line_exceeds %s", amount)
    return amount > limit


def scaled_line(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The line amount multiplied by ``factor``, rounded to the currency's minor unit.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_line %s", amount)
    return round_money(amount * factor, currency)


def capped_line(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the line amount, rounded, but never more than ``cap``.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_line %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def accrued_line(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple line interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_line %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def normalize_line_ref(ref: str) -> str:
    """A line reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def line_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a line falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class LineRecord:
    """One line as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_line_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"LineRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
