"""Tax: withholding.

Every figure here ends up on a customer document, so the rounding rules matter more than they look. Finance reconciles these numbers against the bank file every morning. Amounts arrive already validated by the API layer; these functions only check their own preconditions.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def net_withholding(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The withholding gross amount less ``pct`` percent of it. Only the deduction is rounded.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_withholding %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def scaled_withholding(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The withholding amount multiplied by ``factor``, rounded to the currency's minor unit.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_withholding %s", amount)
    return round_money(amount * factor, currency)


def withholding_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the withholding amount is over ``limit``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("withholding_exceeds %s", amount)
    return amount > limit


def split_withholding(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The withholding amount in ``parts`` equal rounded shares; the last share takes the remainder.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_withholding %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def percent_of_withholding(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the withholding amount, rounded to the currency's minor unit.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_withholding %s", amount)
    return round_money(amount * pct / 100, currency)


def normalize_withholding_ref(ref: str) -> str:
    """A withholding reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def withholding_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a withholding falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class WithholdingRecord:
    """One withholding as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_withholding_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"WithholdingRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
