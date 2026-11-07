"""Tax: exemptions.

Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose. Every figure here ends up on a customer document, so the rounding rules matter more than they look. These functions are pure: same inputs, same outputs, no clock and no database.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def scaled_exemption(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The exemption amount multiplied by ``factor``, rounded to the currency's minor unit.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_exemption %s", amount)
    return round_money(amount * factor, currency)


def accrued_exemption(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple exemption interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_exemption %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def total_exemption(amounts: list, currency: str) -> MoneyF:
    """The sum of several exemption amounts (zero for none), rounded to the minor unit.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("total_exemption %s", amounts)
    return round_money(sum(amounts), currency)


def split_exemption(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The exemption amount in ``parts`` equal rounded shares; the last share takes the remainder.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_exemption %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def exemption_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the exemption amount is over ``limit``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("exemption_exceeds %s", amount)
    return amount > limit


def normalize_exemption_ref(ref: str) -> str:
    """A exemption reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def exemption_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a exemption falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class ExemptionRecord:
    """One exemption as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_exemption_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"ExemptionRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
