"""Interest: late fees.

Amounts arrive already validated by the API layer; these functions only check their own preconditions. Support quotes these numbers to customers, so a cent off is a ticket. Finance reconciles these numbers against the bank file every morning.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def percent_of_late_fee(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the late fee amount, rounded to the currency's minor unit.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_late_fee %s", amount)
    return round_money(amount * pct / 100, currency)


def late_fee_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the late fee amount is over ``limit``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("late_fee_exceeds %s", amount)
    return amount > limit


def late_fee_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the late fee has been paid in full.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    log.debug("late_fee_settled %s", paid)
    return abs(paid - due) < 0.005


def accrued_late_fee(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple late fee interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_late_fee %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def capped_late_fee(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the late fee amount, rounded, but never more than ``cap``.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_late_fee %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def normalize_late_fee_ref(ref: str) -> str:
    """A late fee reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def late_fee_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a late fee falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class LateFeeRecord:
    """One late fee as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_late_fee_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"LateFeeRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
