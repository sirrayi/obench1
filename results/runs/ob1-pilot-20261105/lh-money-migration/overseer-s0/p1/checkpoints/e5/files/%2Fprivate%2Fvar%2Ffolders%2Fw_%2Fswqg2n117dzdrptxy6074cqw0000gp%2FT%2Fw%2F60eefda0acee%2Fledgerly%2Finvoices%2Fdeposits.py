"""Invoices: deposits.

Finance reconciles these numbers against the bank file every morning. These functions are pure: same inputs, same outputs, no clock and no database. Support quotes these numbers to customers, so a cent off is a ticket.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def capped_deposit(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the deposit amount, rounded, but never more than ``cap``.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_deposit %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def deposit_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the deposit amount is over ``limit``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("deposit_exceeds %s", amount)
    return amount > limit


def accrued_deposit(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple deposit interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_deposit %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def format_deposit(amount: MoneyF, currency: str) -> str:
    """The deposit amount as display text, e.g. ``12.30 USD``.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("format_deposit %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def deposit_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the deposit has been paid in full.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("deposit_settled %s", paid)
    return abs(paid - due) < 0.005


def normalize_deposit_ref(ref: str) -> str:
    """A deposit reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def deposit_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a deposit falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class DepositRecord:
    """One deposit as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_deposit_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"DepositRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
