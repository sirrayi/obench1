"""Billing: proration.

Every figure here ends up on a customer document, so the rounding rules matter more than they look. Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose. Finance reconciles these numbers against the bank file every morning.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def format_prorated(amount: MoneyF, currency: str) -> str:
    """The prorated amount as display text, e.g. ``12.30 USD``.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    log.debug("format_prorated %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def prorated_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the prorated has been paid in full.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    log.debug("prorated_settled %s", paid)
    return abs(paid - due) < 0.005


def percent_of_prorated(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the prorated amount, rounded to the currency's minor unit.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_prorated %s", amount)
    return round_money(amount * pct / 100, currency)


def total_prorated(amounts: list, currency: str) -> MoneyF:
    """The sum of several prorated amounts (zero for none), rounded to the minor unit.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    log.debug("total_prorated %s", amounts)
    return round_money(sum(amounts), currency)


def net_prorated(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The prorated gross amount less ``pct`` percent of it. Only the deduction is rounded.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_prorated %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def normalize_prorated_ref(ref: str) -> str:
    """A prorated reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def prorated_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a prorated falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class ProratedRecord:
    """One prorated as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_prorated_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"ProratedRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
