"""Payouts: transfers.

Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose. Amounts arrive already validated by the API layer; these functions only check their own preconditions. Support quotes these numbers to customers, so a cent off is a ticket.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import round_money

log = logging.getLogger(__name__)


def accrued_transfer(balance: MoneyF, annual_rate: Rate, days: int = 30, currency: str = "USD") -> MoneyF:
    """Simple transfer interest on ``balance`` for ``days`` days at ``annual_rate`` percent a year (actual/365), rounded to the minor unit.

    Finance reconciles these numbers against the bank file every morning.
    """
    if days < 0:
        raise ValueError("days must not be negative")
    log.debug("accrued_transfer %s", balance)
    return round_money(balance * annual_rate / 100 * days / 365, currency)


def split_transfer(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The transfer amount in ``parts`` equal rounded shares; the last share takes the remainder.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_transfer %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def percent_of_transfer(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the transfer amount, rounded to the currency's minor unit.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_transfer %s", amount)
    return round_money(amount * pct / 100, currency)


def transfer_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the transfer amount is over ``limit``.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("transfer_exceeds %s", amount)
    return amount > limit


def scaled_transfer(amount: MoneyF, factor: Rate, currency: str) -> MoneyF:
    """The transfer amount multiplied by ``factor``, rounded to the currency's minor unit.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    if factor < 0:
        raise ValueError("factor must not be negative")
    log.debug("scaled_transfer %s", amount)
    return round_money(amount * factor, currency)


def normalize_transfer_ref(ref: str) -> str:
    """A transfer reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def transfer_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a transfer falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class TransferRecord:
    """One transfer as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_transfer_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"TransferRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
