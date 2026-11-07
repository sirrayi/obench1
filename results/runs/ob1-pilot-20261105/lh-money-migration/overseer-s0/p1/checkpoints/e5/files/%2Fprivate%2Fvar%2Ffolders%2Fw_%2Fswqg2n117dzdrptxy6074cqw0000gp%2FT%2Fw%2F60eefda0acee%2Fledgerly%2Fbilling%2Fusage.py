"""Billing: usage.

The nightly batch and the API share these helpers; keep them free of I/O. Amounts arrive already validated by the API layer; these functions only check their own preconditions. Support quotes these numbers to customers, so a cent off is a ticket.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def usage_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the usage amount is over ``limit``.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    log.debug("usage_exceeds %s", amount)
    return amount > limit


def split_usage(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The usage amount in ``parts`` equal rounded shares; the last share takes the remainder.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_usage %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def scaled_usage(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The usage amount multiplied by ``factor``, rounded to the currency's minor unit.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_usage %s", amount)
    return round_money(amount * factor, currency)


def percent_of_usage(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the usage amount, rounded to the currency's minor unit.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_usage %s", amount)
    return round_money(amount * pct / 100, currency)


def format_usage(amount: MoneyF, currency: str) -> str:
    """The usage amount as display text, e.g. ``12.30 USD``.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("format_usage %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def normalize_usage_ref(ref: str) -> str:
    """A usage reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def usage_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a usage falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class UsageRecord:
    """One usage as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_usage_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"UsageRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
