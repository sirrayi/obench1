"""Interest: accrual.

When in doubt about a figure, the ledger is the source of truth, not these helpers. Support quotes these numbers to customers, so a cent off is a ticket. Finance reconciles these numbers against the bank file every morning.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def total_accrual(amounts: list, currency: str) -> MoneyF:
    """The sum of several accrual amounts (zero for none), rounded to the minor unit.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    log.debug("total_accrual %s", amounts)
    return round_money(sum(amounts), currency)


def percent_of_accrual(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the accrual amount, rounded to the currency's minor unit.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_accrual %s", amount)
    return round_money(amount * pct / 100, currency)


def capped_accrual(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the accrual amount, rounded, but never more than ``cap``.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_accrual %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def scaled_accrual(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The accrual amount multiplied by ``factor``, rounded to the currency's minor unit.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_accrual %s", amount)
    return round_money(amount * factor, currency)


def accrual_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the accrual has been paid in full.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    log.debug("accrual_settled %s", paid)
    return abs(paid - due) < 0.005


def normalize_accrual_ref(ref: str) -> str:
    """A accrual reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def accrual_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a accrual falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class AccrualRecord:
    """One accrual as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_accrual_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"AccrualRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
