"""Fx: convert.

Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose. Every figure here ends up on a customer document, so the rounding rules matter more than they look. These functions are pure: same inputs, same outputs, no clock and no database.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly._gen.rates_table import RATES
from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def convert_conversion(amount: MoneyF, src: str, dst: str) -> MoneyF:
    """The conversion amount converted from ``src`` to ``dst`` at the published rate.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if (src, dst) not in RATES:
        raise KeyError(f"no rate for {src}->{dst}")
    log.debug("convert_conversion %s", amount)
    return round_money(amount * RATES[(src, dst)], dst)


def quote_conversion(amount: MoneyF, src: str, dst: str, spread_bp: int = 25) -> MoneyF:
    """A customer conversion quote: the converted amount less a spread in basis points.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if (src, dst) not in RATES:
        raise KeyError(f"no rate for {src}->{dst}")
    log.debug("quote_conversion %s", amount)
    return round_money(amount * RATES[(src, dst)] * (1 - spread_bp / 10000), dst)


def net_conversion(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The conversion gross amount less ``pct`` percent of it. Only the deduction is rounded.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_conversion %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def scaled_conversion(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The conversion amount multiplied by ``factor``, rounded to the currency's minor unit.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_conversion %s", amount)
    return round_money(amount * factor, currency)


def total_conversion(amounts: list, currency: str) -> MoneyF:
    """The sum of several conversion amounts (zero for none), rounded to the minor unit.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    log.debug("total_conversion %s", amounts)
    return round_money(sum(amounts), currency)


def convert_float(amount: float, src: str, dst: str) -> float:
    """v1 compatibility shim: float in, float out. legacy/ depends on it; keep its signature and results.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    log.debug("convert_float %s", amount)
    return round(amount * RATES[(src, dst)], EXPONENT[dst])


def normalize_conversion_ref(ref: str) -> str:
    """A conversion reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def conversion_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a conversion falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class ConversionRecord:
    """One conversion as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_conversion_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"ConversionRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
