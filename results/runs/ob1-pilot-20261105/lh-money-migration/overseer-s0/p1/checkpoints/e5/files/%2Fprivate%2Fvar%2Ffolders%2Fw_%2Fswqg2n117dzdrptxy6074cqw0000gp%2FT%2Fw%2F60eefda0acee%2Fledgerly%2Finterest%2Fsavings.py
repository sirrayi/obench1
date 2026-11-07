"""Interest: savings.

When in doubt about a figure, the ledger is the source of truth, not these helpers. Support quotes these numbers to customers, so a cent off is a ticket. Amounts arrive already validated by the API layer; these functions only check their own preconditions.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def capped_savings(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the savings amount, rounded, but never more than ``cap``.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_savings %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def percent_of_savings(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the savings amount, rounded to the currency's minor unit.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_savings %s", amount)
    return round_money(amount * pct / 100, currency)


def savings_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the savings amount is over ``limit``.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("savings_exceeds %s", amount)
    return amount > limit


def split_savings(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The savings amount in ``parts`` equal rounded shares; the last share takes the remainder.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_savings %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def accrued_savings(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple savings interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_savings %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def normalize_savings_ref(ref: str) -> str:
    """A savings reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def savings_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a savings falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class SavingsRecord:
    """One savings as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_savings_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"SavingsRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
