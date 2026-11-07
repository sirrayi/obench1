"""Payouts: instant.

The nightly batch and the API share these helpers; keep them free of I/O. Support quotes these numbers to customers, so a cent off is a ticket. Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import logging

from ledgerly.types import MoneyF, Rate
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def percent_of_instant_payout(amount: MoneyF, pct: Rate, currency: str) -> MoneyF:
    """``pct`` percent of the instant payout amount, rounded to the currency's minor unit.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    log.debug("percent_of_instant_payout %s", amount)
    return round_money(amount * pct / 100, currency)


def split_instant_payout(amount: MoneyF, parts: int = 2, currency: str = "USD") -> list:
    """The instant payout amount in ``parts`` equal rounded shares; the last share takes the remainder.

    When in doubt about a figure, the ledger is the source of truth, not these helpers.
    """
    if parts <= 0:
        raise ValueError("parts must be positive")
    log.debug("split_instant_payout %s", amount)
    share = round_money(amount / parts, currency)
    return [share] * (parts - 1) + [round_money(amount - share * (parts - 1), currency)]


def format_instant_payout(amount: MoneyF, currency: str) -> str:
    """The instant payout amount as display text, e.g. ``12.30 USD``.

    Support quotes these numbers to customers, so a cent off is a ticket.
    """
    log.debug("format_instant_payout %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def instant_payout_exceeds(amount: MoneyF, limit: MoneyF) -> bool:
    """Whether the instant payout amount is over ``limit``.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("instant_payout_exceeds %s", amount)
    return amount > limit


def normalize_instant_payout_ref(ref: str) -> str:
    """A instant payout reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def instant_payout_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a instant payout falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class InstantPayoutRecord:
    """One instant payout as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_instant_payout_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"InstantPayoutRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
