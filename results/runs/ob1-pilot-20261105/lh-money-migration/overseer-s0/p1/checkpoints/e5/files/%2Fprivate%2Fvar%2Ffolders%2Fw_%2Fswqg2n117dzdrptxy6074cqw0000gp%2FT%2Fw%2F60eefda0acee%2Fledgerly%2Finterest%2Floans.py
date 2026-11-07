"""Interest: loans.

Amounts arrive already validated by the API layer; these functions only check their own preconditions. Finance reconciles these numbers against the bank file every morning. Support quotes these numbers to customers, so a cent off is a ticket.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def percent_of_loan(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the loan amount, rounded to the currency's minor unit.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_loan %s", amount)
    return round_money(amount * pct / 100, currency)


def capped_loan(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the loan amount, rounded, but never more than ``cap``.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_loan %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def scaled_loan(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The loan amount multiplied by ``factor``, rounded to the currency's minor unit.

    The nightly batch and the API share these helpers; keep them free of I/O.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_loan %s", amount)
    return round_money(amount * factor, currency)


def loan_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the loan amount is over ``limit``.

    Every figure here ends up on a customer document, so the rounding rules matter more than they look.
    """
    log.debug("loan_exceeds %s", amount)
    return amount > limit


def split_loan(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The loan amount in ``parts`` equal rounded shares; the last share takes the remainder.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_loan %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def normalize_loan_ref(ref: str) -> str:
    """A loan reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def loan_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a loan falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class LoanRecord:
    """One loan as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_loan_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"LoanRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
