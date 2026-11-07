"""Reports: summaries.

Finance reconciles these numbers against the bank file every morning. When in doubt about a figure, the ledger is the source of truth, not these helpers. These functions are pure: same inputs, same outputs, no clock and no database.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def capped_summary(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the summary amount, rounded, but never more than ``cap``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_summary %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def net_summary(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The summary gross amount less ``pct`` percent of it. Only the deduction is rounded.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_summary %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def summary_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the summary has been paid in full.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    log.debug("summary_settled %s", paid)
    return abs(paid - due) < 0.005


def summary_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the summary amount is over ``limit``.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    log.debug("summary_exceeds %s", amount)
    return amount > limit


def scaled_summary(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The summary amount multiplied by ``factor``, rounded to the currency's minor unit.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_summary %s", amount)
    return round_money(amount * factor, currency)


def normalize_summary_ref(ref: str) -> str:
    """A summary reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def summary_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a summary falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class SummaryRecord:
    """One summary as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_summary_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"SummaryRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
