"""Refunds: partial.

Support quotes these numbers to customers, so a cent off is a ticket. The nightly batch and the API share these helpers; keep them free of I/O. These functions are pure: same inputs, same outputs, no clock and no database.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def partial_refund_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the partial refund amount is over ``limit``.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    log.debug("partial_refund_exceeds %s", amount)
    return amount > limit


def capped_partial_refund(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the partial refund amount, rounded, but never more than ``cap``.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_partial_refund %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def net_partial_refund(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The partial refund gross amount less ``pct`` percent of it. Only the deduction is rounded.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_partial_refund %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def percent_of_partial_refund(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the partial refund amount, rounded to the currency's minor unit.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_partial_refund %s", amount)
    return round_money(amount * pct / 100, currency)


def split_partial_refund(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The partial refund amount in ``parts`` equal rounded shares; the last share takes the remainder.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_partial_refund %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def normalize_partial_refund_ref(ref: str) -> str:
    """A partial refund reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def partial_refund_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a partial refund falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class PartialRefundRecord:
    """One partial refund as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_partial_refund_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"PartialRefundRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
