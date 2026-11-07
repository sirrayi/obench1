"""Fx: revaluation.

Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose. Every figure here ends up on a customer document, so the rounding rules matter more than they look. The nightly batch and the API share these helpers; keep them free of I/O.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly._gen.rates_table import RATES
from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def convert_revaluation(amount: MoneyF, src: str, dst: str) -> MoneyF:
    """The revaluation amount converted from ``src`` to ``dst`` at the published rate.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if (src, dst) not in RATES:
        raise KeyError(f"no rate for {src}->{dst}")
    log.debug("convert_revaluation %s", amount)
    return round_money(amount * RATES[(src, dst)], dst)


def quote_revaluation(amount: MoneyF, src: str, dst: str, spread_bp: int = 25) -> MoneyF:
    """A customer revaluation quote: the converted amount less a spread in basis points.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if (src, dst) not in RATES:
        raise KeyError(f"no rate for {src}->{dst}")
    log.debug("quote_revaluation %s", amount)
    return round_money(amount * RATES[(src, dst)] * (1 - spread_bp / 10000), dst)


def net_revaluation(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The revaluation gross amount less ``pct`` percent of it. Only the deduction is rounded.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_revaluation %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def accrued_revaluation(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple revaluation interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_revaluation %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def split_revaluation(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The revaluation amount in ``parts`` equal rounded shares; the last share takes the remainder.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_revaluation %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def normalize_revaluation_ref(ref: str) -> str:
    """A revaluation reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def revaluation_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a revaluation falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class RevaluationRecord:
    """One revaluation as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_revaluation_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"RevaluationRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
