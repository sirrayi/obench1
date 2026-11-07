"""Fx: spreads.

When in doubt about a figure, the ledger is the source of truth, not these helpers. Support quotes these numbers to customers, so a cent off is a ticket. The nightly batch and the API share these helpers; keep them free of I/O.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly._gen.rates_table import RATES
from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def convert_spread(amount: MoneyF, src: str, dst: str) -> MoneyF:
    """The spread amount converted from ``src`` to ``dst`` at the published rate.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if (src, dst) not in RATES:
        raise KeyError(f"no rate for {src}->{dst}")
    log.debug("convert_spread %s", amount)
    return round_money(amount * RATES[(src, dst)], dst)


def quote_spread(amount: MoneyF, src: str, dst: str, spread_bp: int = 25) -> MoneyF:
    """A customer spread quote: the converted amount less a spread in basis points.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if (src, dst) not in RATES:
        raise KeyError(f"no rate for {src}->{dst}")
    log.debug("quote_spread %s", amount)
    return round_money(amount * RATES[(src, dst)] * (1 - spread_bp / 10000), dst)


def scaled_spread(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The spread amount multiplied by ``factor``, rounded to the currency's minor unit.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_spread %s", amount)
    return round_money(amount * factor, currency)


def capped_spread(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the spread amount, rounded, but never more than ``cap``.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_spread %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def format_spread(amount: MoneyF, currency: str) -> str:
    """The spread amount as display text, e.g. ``12.30 USD``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("format_spread %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def normalize_spread_ref(ref: str) -> str:
    """A spread reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def spread_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a spread falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class SpreadRecord:
    """One spread as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_spread_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"SpreadRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
