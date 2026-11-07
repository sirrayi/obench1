"""Tax: vat.

Finance reconciles these numbers against the bank file every morning. Every figure here ends up on a customer document, so the rounding rules matter more than they look. Amounts arrive already validated by the API layer; these functions only check their own preconditions.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def format_vat(amount: MoneyF, currency: str) -> str:
    """The vat amount as display text, e.g. ``12.30 USD``.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    log.debug("format_vat %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def capped_vat(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the vat amount, rounded, but never more than ``cap``.

    Finance reconciles these numbers against the bank file every morning.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_vat %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def vat_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the vat amount is over ``limit``.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    log.debug("vat_exceeds %s", amount)
    return amount > limit


def total_vat(amounts: list, currency: str) -> MoneyF:
    """The sum of several vat amounts (zero for none), rounded to the minor unit.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    log.debug("total_vat %s", amounts)
    return round_money(sum(amounts), currency)


def split_vat(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The vat amount in ``parts`` equal rounded shares; the last share takes the remainder.

    Finance reconciles these numbers against the bank file every morning.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_vat %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def normalize_vat_ref(ref: str) -> str:
    """A vat reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def vat_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a vat falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class VatRecord:
    """One vat as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_vat_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"VatRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
