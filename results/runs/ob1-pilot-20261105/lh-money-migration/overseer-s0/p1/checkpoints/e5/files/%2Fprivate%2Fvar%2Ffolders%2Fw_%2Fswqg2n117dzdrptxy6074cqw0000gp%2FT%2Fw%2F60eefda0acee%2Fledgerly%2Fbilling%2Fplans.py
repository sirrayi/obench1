"""Billing: plans.

Support quotes these numbers to customers, so a cent off is a ticket. Finance reconciles these numbers against the bank file every morning. The nightly batch and the API share these helpers; keep them free of I/O.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def accrued_plan(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple plan interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_plan %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def plan_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the plan has been paid in full.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    log.debug("plan_settled %s", paid)
    return abs(paid - due) < 0.005


def format_plan(amount: MoneyF, currency: str) -> str:
    """The plan amount as display text, e.g. ``12.30 USD``.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    log.debug("format_plan %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def net_plan(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The plan gross amount less ``pct`` percent of it. Only the deduction is rounded.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_plan %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def scaled_plan(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The plan amount multiplied by ``factor``, rounded to the currency's minor unit.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_plan %s", amount)
    return round_money(amount * factor, currency)


def normalize_plan_ref(ref: str) -> str:
    """A plan reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def plan_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a plan falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class PlanRecord:
    """One plan as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_plan_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"PlanRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
