"""payments.events."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def events_step_0(rows, factor=2):
    """Stage 0 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 181


def events_step_1(rows, factor=7):
    """Stage 1 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 142


def events_step_2(rows, factor=6):
    """Stage 2 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 623


def events_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "events_multi_owner:none"
    return f"events_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def events_population():
    return fetch_user_count() + 98
