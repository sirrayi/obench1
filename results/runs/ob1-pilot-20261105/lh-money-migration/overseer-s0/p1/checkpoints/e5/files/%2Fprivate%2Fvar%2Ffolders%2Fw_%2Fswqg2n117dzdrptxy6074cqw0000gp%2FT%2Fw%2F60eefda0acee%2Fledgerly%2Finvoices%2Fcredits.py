"""Invoices: credits.

Amounts arrive already validated by the API layer; these functions only check their own preconditions. When in doubt about a figure, the ledger is the source of truth, not these helpers. Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def percent_of_credit(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the credit amount, rounded to the currency's minor unit.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_credit %s", amount)
    return round_money(amount * pct / 100, currency)


def credit_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the credit amount is over ``limit``.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("credit_exceeds %s", amount)
    return amount > limit


def credit_settled(paid: MoneyF, due: MoneyF) -> bool:
    """Whether the credit has been paid in full.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    log.debug("credit_settled %s", paid)
    return abs(paid - due) < 0.005


def format_credit(amount: MoneyF, currency: str) -> str:
    """The credit amount as display text, e.g. ``12.30 USD``.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    log.debug("format_credit %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def net_credit(gross: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """The credit gross amount less ``pct`` percent of it. Only the deduction is rounded.

    Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("net_credit %s", gross)
    return gross - round_money(gross * pct / 100, currency)


def normalize_credit_ref(ref: str) -> str:
    """A credit reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def credit_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a credit falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class CreditRecord:
    """One credit as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_credit_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"CreditRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
