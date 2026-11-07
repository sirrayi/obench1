"""Fx: cross rates.

These functions are pure: same inputs, same outputs, no clock and no database. Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose. Support quotes these numbers to customers, so a cent off is a ticket.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly._gen.rates_table import RATES
from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def convert_cross(amount: MoneyF, src: str, dst: str) -> MoneyF:
    """The cross amount converted from ``src`` to ``dst`` at the published rate.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if (src, dst) not in RATES:
        raise KeyError(f"no rate for {src}->{dst}")
    log.debug("convert_cross %s", amount)
    return round_money(amount * RATES[(src, dst)], dst)


def quote_cross(amount: MoneyF, src: str, dst: str, spread_bp: int = 25) -> MoneyF:
    """A customer cross quote: the converted amount less a spread in basis points.

    Finance reconciles these numbers against the bank file every morning.
    """
    if (src, dst) not in RATES:
        raise KeyError(f"no rate for {src}->{dst}")
    log.debug("quote_cross %s", amount)
    return round_money(amount * RATES[(src, dst)] * (1 - spread_bp / 10000), dst)


def accrued_cross(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple cross interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_cross %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def net_cross(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The cross gross amount less ``pct`` percent of it. Only the deduction is rounded.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_cross %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def percent_of_cross(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the cross amount, rounded to the currency's minor unit.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_cross %s", amount)
    return round_money(amount * pct / 100, currency)


def normalize_cross_ref(ref: str) -> str:
    """A cross reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def cross_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a cross falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class CrossRecord:
    """One cross as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_cross_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"CrossRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
