"""Payouts: fees.

These functions are pure: same inputs, same outputs, no clock and no database. Amounts arrive already validated by the API layer; these functions only check their own preconditions. Finance reconciles these numbers against the bank file every morning.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def fee_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the fee has been paid in full.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    log.debug("fee_settled %s", paid)
    return abs(paid - due) < 0.005


def split_fee(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The fee amount in ``parts`` equal rounded shares; the last share takes the remainder.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_fee %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def capped_fee(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the fee amount, rounded, but never more than ``cap``.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_fee %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def scaled_fee(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The fee amount multiplied by ``factor``, rounded to the currency's minor unit.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_fee %s", amount)
    return round_money(amount * factor, currency)


def net_fee(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The fee gross amount less ``pct`` percent of it. Only the deduction is rounded.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_fee %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def normalize_fee_ref(ref: str) -> str:
    """A fee reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def fee_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a fee falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class FeeRecord:
    """One fee as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_fee_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"FeeRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
