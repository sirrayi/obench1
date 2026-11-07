"""Refunds: chargebacks.

Support quotes these numbers to customers, so a cent off is a ticket. Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose. Amounts arrive already validated by the API layer; these functions only check their own preconditions.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def accrued_chargeback(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple chargeback interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_chargeback %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def split_chargeback(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The chargeback amount in ``parts`` equal rounded shares; the last share takes the remainder.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_chargeback %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def net_chargeback(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The chargeback gross amount less ``pct`` percent of it. Only the deduction is rounded.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_chargeback %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def chargeback_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the chargeback amount is over ``limit``.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    log.debug("chargeback_exceeds %s", amount)
    return amount > limit


def percent_of_chargeback(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the chargeback amount, rounded to the currency's minor unit.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_chargeback %s", amount)
    return round_money(amount * pct / 100, currency)


def normalize_chargeback_ref(ref: str) -> str:
    """A chargeback reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def chargeback_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a chargeback falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class ChargebackRecord:
    """One chargeback as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_chargeback_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"ChargebackRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
