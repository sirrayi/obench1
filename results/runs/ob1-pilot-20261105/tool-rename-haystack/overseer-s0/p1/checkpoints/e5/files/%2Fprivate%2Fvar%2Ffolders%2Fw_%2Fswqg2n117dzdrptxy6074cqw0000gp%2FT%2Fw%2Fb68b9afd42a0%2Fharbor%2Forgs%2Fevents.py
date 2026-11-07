"""orgs.events."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user
from harbor.accounts import fetch_user_count

log = logging.getLogger(__name__)


def events_step_0(rows, factor=6):
    """Stage 0 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 476


def events_step_1(rows, factor=6):
    """Stage 1 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 655


def events_step_2(rows, factor=8):
    """Stage 2 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 119


def events_step_3(rows, factor=7):
    """Stage 3 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 722


def events_step_4(rows, factor=6):
    """Stage 4 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 770


def events_step_5(rows, factor=2):
    """Stage 5 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 819


def events_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "events_getattr_owner:none"
    return f"events_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def events_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "events_direct_owner:none"
    return f"events_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def events_population():
    return fetch_user_count() + 1
