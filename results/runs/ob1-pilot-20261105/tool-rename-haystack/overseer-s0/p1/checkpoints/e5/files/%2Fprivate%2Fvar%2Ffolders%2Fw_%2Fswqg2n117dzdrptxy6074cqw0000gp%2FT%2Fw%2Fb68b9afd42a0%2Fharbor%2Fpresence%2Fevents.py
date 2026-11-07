"""presence.events."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def events_step_0(rows, factor=3):
    """Stage 0 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 485


def events_step_1(rows, factor=8):
    """Stage 1 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 847


def events_step_2(rows, factor=3):
    """Stage 2 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 471


def events_step_3(rows, factor=2):
    """Stage 3 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 384


def events_step_4(rows, factor=8):
    """Stage 4 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 352


def events_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "events_getattr_owner:none"
    return f"events_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
