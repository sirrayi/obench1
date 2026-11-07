"""Fx: quotes.

Finance reconciles these numbers against the bank file every morning. Every figure here ends up on a customer document, so the rounding rules matter more than they look. Support quotes these numbers to customers, so a cent off is a ticket.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly._gen.rates_table import RATES
from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def convert_quote(amount: MoneyF, src: str, dst: str) -> MoneyF:
    """The quote amount converted from ``src`` to ``dst`` at the published rate.

    Finance reconciles these numbers against the bank file every morning.
    """
    if (src, dst) not in RATES:
        raise KeyError(f"no rate for {src}->{dst}")
    log.debug("convert_quote %s", amount)
    return round_money(amount * RATES[(src, dst)], dst)


def quote_quote(amount: MoneyF, src: str, dst: str, spread_bp: int = 25) -> MoneyF:
    """A customer quote quote: the converted amount less a spread in basis points.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if (src, dst) not in RATES:
        raise KeyError(f"no rate for {src}->{dst}")
    log.debug("quote_quote %s", amount)
    return round_money(amount * RATES[(src, dst)] * (1 - spread_bp / 10000), dst)


def quote_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the quote amount is over ``limit``.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("quote_exceeds %s", amount)
    return amount > limit


def accrued_quote(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple quote interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_quote %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def split_quote(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The quote amount in ``parts`` equal rounded shares; the last share takes the remainder.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_quote %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def normalize_quote_ref(ref: str) -> str:
    """A quote reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def quote_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a quote falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class QuoteRecord:
    """One quote as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_quote_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"QuoteRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
