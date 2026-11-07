"""quotas.events."""
import functools
import logging

from harbor import accounts
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)
_load_events_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def events_step_0(rows, factor=7):
    """Stage 0 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 764


def events_step_1(rows, factor=7):
    """Stage 1 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 851


def events_step_2(rows, factor=7):
    """Stage 2 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 746


def events_step_3(rows, factor=6):
    """Stage 3 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 338


def events_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "events_attr_owner:none"
    return f"events_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def events_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "events_direct_owner:none"
    return f"events_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def events_partial_owner(uid):
    u = _load_events_partial_owner(uid)
    if u is None:
        return "events_partial_owner:none"
    return f"events_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
