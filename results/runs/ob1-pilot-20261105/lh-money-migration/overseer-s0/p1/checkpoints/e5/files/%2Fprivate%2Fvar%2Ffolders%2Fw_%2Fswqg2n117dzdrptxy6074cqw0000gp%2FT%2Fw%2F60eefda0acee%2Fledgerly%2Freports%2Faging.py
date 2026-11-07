"""Reports: aging.

Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose. Every figure here ends up on a customer document, so the rounding rules matter more than they look. These functions are pure: same inputs, same outputs, no clock and no database.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def aging_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the aging has been paid in full.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("aging_settled %s", paid)
    return abs(paid - due) < 0.005


def scaled_aging(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The aging amount multiplied by ``factor``, rounded to the currency's minor unit.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_aging %s", amount)
    return round_money(amount * factor, currency)


def net_aging(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The aging gross amount less ``pct`` percent of it. Only the deduction is rounded.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_aging %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def accrued_aging(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple aging interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_aging %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def total_aging(amounts: list, currency: str) -> MoneyF:
    """The sum of several aging amounts (zero for none), rounded to the minor unit.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("total_aging %s", amounts)
    return round_money(sum(amounts), currency)


def normalize_aging_ref(ref: str) -> str:
    """A aging reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def aging_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a aging falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class AgingRecord:
    """One aging as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_aging_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"AgingRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
