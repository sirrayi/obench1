"""Tax: reverse charge.

Support quotes these numbers to customers, so a cent off is a ticket. Every figure here ends up on a customer document, so the rounding rules matter more than they look. These functions are pure: same inputs, same outputs, no clock and no database.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def accrued_reverse_charge(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple reverse charge interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_reverse_charge %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def reverse_charge_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the reverse charge has been paid in full.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    log.debug("reverse_charge_settled %s", paid)
    return abs(paid - due) < 0.005


def capped_reverse_charge(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the reverse charge amount, rounded, but never more than ``cap``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_reverse_charge %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def split_reverse_charge(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The reverse charge amount in ``parts`` equal rounded shares; the last share takes the remainder.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_reverse_charge %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def reverse_charge_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the reverse charge amount is over ``limit``.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("reverse_charge_exceeds %s", amount)
    return amount > limit


def normalize_reverse_charge_ref(ref: str) -> str:
    """A reverse charge reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def reverse_charge_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a reverse charge falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class ReverseChargeRecord:
    """One reverse charge as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_reverse_charge_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"ReverseChargeRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
