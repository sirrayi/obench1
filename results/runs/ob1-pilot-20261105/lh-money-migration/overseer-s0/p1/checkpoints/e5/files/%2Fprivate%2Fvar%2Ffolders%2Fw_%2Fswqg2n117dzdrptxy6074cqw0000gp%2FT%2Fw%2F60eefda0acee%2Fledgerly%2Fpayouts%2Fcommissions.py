"""Payouts: commissions.

Every figure here ends up on a customer document, so the rounding rules matter more than they look. These functions are pure: same inputs, same outputs, no clock and no database. The nightly batch and the API share these helpers; keep them free of I/O.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def capped_commission(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the commission amount, rounded, but never more than ``cap``.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_commission %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def total_commission(amounts: list, currency: str) -> MoneyF:
    """The sum of several commission amounts (zero for none), rounded to the minor unit.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    log.debug("total_commission %s", amounts)
    return round_money(sum(amounts), currency)


def format_commission(amount: MoneyF, currency: str) -> str:
    """The commission amount as display text, e.g. ``12.30 USD``.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    log.debug("format_commission %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def accrued_commission(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple commission interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_commission %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def commission_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the commission has been paid in full.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    log.debug("commission_settled %s", paid)
    return abs(paid - due) < 0.005


def normalize_commission_ref(ref: str) -> str:
    """A commission reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def commission_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a commission falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class CommissionRecord:
    """One commission as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_commission_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"CommissionRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
