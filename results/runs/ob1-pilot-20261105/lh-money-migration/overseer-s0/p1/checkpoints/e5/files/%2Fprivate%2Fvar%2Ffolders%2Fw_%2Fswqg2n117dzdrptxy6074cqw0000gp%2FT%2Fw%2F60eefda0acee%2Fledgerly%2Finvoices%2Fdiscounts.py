"""Invoices: discounts.

Support quotes these numbers to customers, so a cent off is a ticket. Amounts arrive already validated by the API layer; these functions only check their own preconditions. When in doubt about a figure, the ledger is the source of truth, not these helpers.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def scaled_discount(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The discount amount multiplied by ``factor``, rounded to the currency's minor unit.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_discount %s", amount)
    return round_money(amount * factor, currency)


def capped_discount(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the discount amount, rounded, but never more than ``cap``.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_discount %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def discount_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the discount amount is over ``limit``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("discount_exceeds %s", amount)
    return amount > limit


def split_discount(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The discount amount in ``parts`` equal rounded shares; the last share takes the remainder.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_discount %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def discount_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the discount has been paid in full.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    log.debug("discount_settled %s", paid)
    return abs(paid - due) < 0.005


def normalize_discount_ref(ref: str) -> str:
    """A discount reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def discount_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a discount falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class DiscountRecord:
    """One discount as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_discount_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"DiscountRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
