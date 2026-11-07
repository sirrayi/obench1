"""Billing: coupons.

Amounts arrive already validated by the API layer; these functions only check their own preconditions. Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose. These functions are pure: same inputs, same outputs, no clock and no database.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def format_coupon(amount: MoneyF, currency: str) -> str:
    """The coupon amount as display text, e.g. ``12.30 USD``.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    log.debug("format_coupon %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def coupon_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the coupon has been paid in full.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    log.debug("coupon_settled %s", paid)
    return abs(paid - due) < 0.005


def scaled_coupon(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The coupon amount multiplied by ``factor``, rounded to the currency's minor unit.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_coupon %s", amount)
    return round_money(amount * factor, currency)


def split_coupon(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The coupon amount in ``parts`` equal rounded shares; the last share takes the remainder.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_coupon %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def net_coupon(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The coupon gross amount less ``pct`` percent of it. Only the deduction is rounded.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_coupon %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def normalize_coupon_ref(ref: str) -> str:
    """A coupon reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def coupon_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a coupon falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class CouponRecord:
    """One coupon as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_coupon_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"CouponRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
