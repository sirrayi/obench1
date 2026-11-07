"""Refunds: cancellations.

Amounts arrive already validated by the API layer; these functions only check their own preconditions. Support quotes these numbers to customers, so a cent off is a ticket. When in doubt about a figure, the ledger is the source of truth, not these helpers.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def cancellation_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the cancellation amount is over ``limit``.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("cancellation_exceeds %s", amount)
    return amount > limit


def cancellation_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the cancellation has been paid in full.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("cancellation_settled %s", paid)
    return abs(paid - due) < 0.005


def accrued_cancellation(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple cancellation interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    Finance reconciles these numbers against the bank file every morning.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_cancellation %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def format_cancellation(amount: MoneyF, currency: str) -> str:
    """The cancellation amount as display text, e.g. ``12.30 USD``.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    log.debug("format_cancellation %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def percent_of_cancellation(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the cancellation amount, rounded to the currency's minor unit.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_cancellation %s", amount)
    return round_money(amount * pct / 100, currency)


def normalize_cancellation_ref(ref: str) -> str:
    """A cancellation reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def cancellation_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a cancellation falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class CancellationRecord:
    """One cancellation as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_cancellation_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"CancellationRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
