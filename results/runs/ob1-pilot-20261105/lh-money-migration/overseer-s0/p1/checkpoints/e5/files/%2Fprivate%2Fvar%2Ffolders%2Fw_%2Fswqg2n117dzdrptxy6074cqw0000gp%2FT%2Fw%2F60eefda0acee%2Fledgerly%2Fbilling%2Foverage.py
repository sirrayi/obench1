"""Billing: overage.

Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose. Finance reconciles these numbers against the bank file every morning. These functions are pure: same inputs, same outputs, no clock and no database.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def overage_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the overage has been paid in full.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    log.debug("overage_settled %s", paid)
    return abs(paid - due) < 0.005


def split_overage(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The overage amount in ``parts`` equal rounded shares; the last share takes the remainder.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_overage %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def percent_of_overage(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the overage amount, rounded to the currency's minor unit.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_overage %s", amount)
    return round_money(amount * pct / 100, currency)


def overage_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the overage amount is over ``limit``.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    log.debug("overage_exceeds %s", amount)
    return amount > limit


def total_overage(amounts: list, currency: str) -> MoneyF:
    """The sum of several overage amounts (zero for none), rounded to the minor unit.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    log.debug("total_overage %s", amounts)
    return round_money(sum(amounts), currency)


def normalize_overage_ref(ref: str) -> str:
    """A overage reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def overage_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a overage falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class OverageRecord:
    """One overage as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_overage_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"OverageRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
