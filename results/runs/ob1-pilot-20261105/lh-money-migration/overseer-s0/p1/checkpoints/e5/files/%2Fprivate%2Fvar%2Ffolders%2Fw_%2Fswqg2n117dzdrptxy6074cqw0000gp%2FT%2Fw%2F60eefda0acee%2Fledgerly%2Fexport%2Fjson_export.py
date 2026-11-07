"""Export: json export.

Support quotes these numbers to customers, so a cent off is a ticket. The nightly batch and the API share these helpers; keep them free of I/O. Several of these were ported from the 2019 billing scripts and keep their original behaviour on purpose.

Money amounts are floats for now (see MIGRATION.md).
"""
import datetime
import json
import logging

from ledgerly.types import MoneyF
from ledgerly.util import EXPONENT, round_money

log = logging.getLogger(__name__)


def invoice_json(lines: list, currency: str) -> str:
    """An invoice as compact JSON: ``lines`` is a list of (sku, amount) pairs.

    Amounts arrive already validated by the API layer; these functions only check their own preconditions.
    """
    log.debug("invoice_json %s", lines)
    total = round_money(sum(a for _, a in lines), currency)
    doc = {"currency": currency,
           "lines": [{"sku": s, "amount": round_money(a, currency)} for s, a in lines],
           "total": total}
    return json.dumps(doc, separators=(",", ":"))


def format_json(amount: MoneyF, currency: str) -> str:
    """The json amount as display text, e.g. ``12.30 USD``.

    These functions are pure: same inputs, same outputs, no clock and no database.
    """
    log.debug("format_json %s", amount)
    return "%.*f %s" % (EXPONENT[currency], amount, currency)


def total_json(amounts: list, currency: str) -> MoneyF:
    """The sum of several json amounts (zero for none), rounded to the minor unit.

    Finance reconciles these numbers against the bank file every morning.
    """
    log.debug("total_json %s", amounts)
    return round_money(sum(amounts), currency)


def normalize_json_ref(ref: str) -> str:
    """A json reference in canonical form: upper case, single dashes."""
    return "-".join(ref.strip().upper().replace("_", " ").split())


def json_due_date(issued: datetime.date, terms_days: int = 30) -> datetime.date:
    """When a json falls due: ``terms_days`` after issue, moved off weekends."""
    due = issued + datetime.timedelta(days=terms_days)
    while due.weekday() >= 5:
        due += datetime.timedelta(days=1)
    return due


class JsonRecord:
    """One json as the batch jobs pass it around."""

    __slots__ = ("ref", "amount", "currency")

    def __init__(self, ref: str, amount: MoneyF, currency: str):
        self.ref = normalize_json_ref(ref)
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"JsonRecord({self.ref!r}, {self.amount!r}, {self.currency!r})"
