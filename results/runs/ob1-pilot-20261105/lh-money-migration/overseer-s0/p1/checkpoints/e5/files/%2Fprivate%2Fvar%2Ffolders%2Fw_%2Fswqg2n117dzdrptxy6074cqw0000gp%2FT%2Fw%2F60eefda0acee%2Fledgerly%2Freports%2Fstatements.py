"""Reports: statements.

When in doubt about a figure, the ledger is the source of truth, not these helpers. Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose. Support quotes these numbers to customers, so a cent off is a ticket.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def total_statement(amounts: list, currency: str) -> MoneyF:
    """The sum of several statement amounts (zero for none), rounded to the minor unit.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    log.debug("total_statement %s", amounts)
    return round_money(sum(amounts), currency)


def statement_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the statement has been paid in full.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    log.debug("statement_settled %s", paid)
    return abs(paid - due) < 0.005


def statement_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the statement amount is over ``limit``.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    log.debug("statement_exceeds %s", amount)
    return amount > limit


def split_statement(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The statement amount in ``parts`` equal rounded shares; the last share takes the remainder.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_statement %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def net_statement(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The statement gross amount less ``pct`` percent of it. Only the deduction is rounded.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_statement %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def normalize_statement_ref(ref: str) -> str:
    """A statement reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def statement_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a statement falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class StatementRecord:
    """One statement as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_statement_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"StatementRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
