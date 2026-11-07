"""Refunds: returns.

When in doubt about a figure, the ledger is the source of truth, not these helpers. Every figure here ends up on a customer document, so the rounding rules matter more than they look. Support quotes these numbers to customers, so a cent off is a ticket.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def scaled_return(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The return amount multiplied by ``factor``, rounded to the currency's minor unit.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_return %s", amount)
    return round_money(amount * factor, currency)


def accrued_return(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple return interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_return %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def format_return(amount: MoneyF, currency: str) -> str:
    """The return amount as display text, e.g. ``12.30 USD``.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    log.debug("format_return %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def net_return(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The return gross amount less ``pct`` percent of it. Only the deduction is rounded.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_return %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def total_return(amounts: list, currency: str) -> MoneyF:
    """The sum of several return amounts (zero for none), rounded to the minor unit.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    log.debug("total_return %s", amounts)
    return round_money(sum(amounts), currency)


def normalize_return_ref(ref: str) -> str:
    """A return reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def return_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a return falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class ReturnRecord:
    """One return as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_return_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"ReturnRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
