"""invoices.events."""
import functools
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)
_load_events_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def events_step_0(rows, factor=3):
    """Stage 0 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 839


def events_step_1(rows, factor=9):
    """Stage 1 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 136


def events_step_2(rows, factor=7):
    """Stage 2 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 521


def events_partial_owner(uid):
    u = _load_events_partial_owner(uid)
    if u is None:
        return "events_partial_owner:none"
    return f"events_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def events_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "events_multi_owner:none"
    return f"events_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def events_population():
    return fetch_user_count() + 31
