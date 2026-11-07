"""Interest: penalties.

Support quotes these numbers to customers, so a cent off is a ticket. Amounts arrive already validated by the API layer; these functions only check their own preconditions. Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def capped_penalty(amount: MoneyF, pct: Rate, cap: MoneyF, currency: str) -> MoneyF:
    """``pct`` percent of the penalty amount, rounded, but never more than ``cap``.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("capped_penalty %s", amount)
    return min(round_money(amount * pct / 100, currency), cap)


def penalty_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the penalty has been paid in full.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    log.debug("penalty_settled %s", paid)
    return abs(paid - due) < 0.005


def net_penalty(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The penalty gross amount less ``pct`` percent of it. Only the deduction is rounded.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_penalty %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def format_penalty(amount: MoneyF, currency: str) -> str:
    """The penalty amount as display text, e.g. ``12.30 USD``.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("format_penalty %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def penalty_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the penalty amount is over ``limit``.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    log.debug("penalty_exceeds %s", amount)
    return amount > limit


def normalize_penalty_ref(ref: str) -> str:
    """A penalty reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def penalty_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a penalty falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class PenaltyRecord:
    """One penalty as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_penalty_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"PenaltyRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
