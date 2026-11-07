"""Tax: sales tax.

When in doubt about a figure, the ledger is the source of truth, not these helpers. Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose. The nightly batch and the API share these helpers; keep them free of I/O.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def sales_tax_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the sales tax has been paid in full.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    log.debug("sales_tax_settled %s", paid)
    return abs(paid - due) < 0.005


def net_sales_tax(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The sales tax gross amount less ``pct`` percent of it. Only the deduction is rounded.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_sales_tax %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def format_sales_tax(amount: MoneyF, currency: str) -> str:
    """The sales tax amount as display text, e.g. ``12.30 USD``.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("format_sales_tax %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def accrued_sales_tax(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple sales tax interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_sales_tax %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def scaled_sales_tax(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The sales tax amount multiplied by ``factor``, rounded to the currency's minor unit.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_sales_tax %s", amount)
    return round_money(amount * factor, currency)


def normalize_sales_tax_ref(ref: str) -> str:
    """A sales tax reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def sales_tax_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a sales tax falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class SalesTaxRecord:
    """One sales tax as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_sales_tax_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"SalesTaxRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
