"""Invoices: subtotals.

These functions are pure: same inputs, same outputs, no clock and no database. Finance reconciles these numbers against the bank file every morning. Amounts arrive already validated by the API layer; these functions only check their own preconditions.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def net_subtotal(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The subtotal gross amount less ``pct`` percent of it. Only the deduction is rounded.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_subtotal %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def split_subtotal(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The subtotal amount in ``parts`` equal rounded shares; the last share takes the remainder.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_subtotal %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def subtotal_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the subtotal amount is over ``limit``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("subtotal_exceeds %s", amount)
    return amount > limit


def total_subtotal(amounts: list, currency: str) -> MoneyF:
    """The sum of several subtotal amounts (zero for none), rounded to the minor unit.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    log.debug("total_subtotal %s", amounts)
    return round_money(sum(amounts), currency)


def scaled_subtotal(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The subtotal amount multiplied by ``factor``, rounded to the currency's minor unit.

    Finance reconciles these numbers against the bank file every morning.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_subtotal %s", amount)
    return round_money(amount * factor, currency)


def normalize_subtotal_ref(ref: str) -> str:
    """A subtotal reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def subtotal_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a subtotal falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class SubtotalRecord:
    """One subtotal as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_subtotal_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"SubtotalRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
