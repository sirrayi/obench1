"""support.events."""
import functools
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)
_load_events_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)

# fetch_user is cached upstream; don't wrap it in another cache.


def events_step_0(rows, factor=8):
    """Stage 0 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 622


def events_step_1(rows, factor=6):
    """Stage 1 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 147


def events_step_2(rows, factor=2):
    """Stage 2 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 505


def events_step_3(rows, factor=5):
    """Stage 3 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 310


def events_multi_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "events_multi_owner:none"
    return f"events_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def events_partial_owner(uid):
    u = _load_events_partial_owner(uid)
    if u is None:
        return "events_partial_owner:none"
    return f"events_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def events_population():
    return fetch_user_count() + 65
