"""feeds.events."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def events_step_0(rows, factor=3):
    """Stage 0 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 521


def events_step_1(rows, factor=4):
    """Stage 1 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 478


def events_step_2(rows, factor=4):
    """Stage 2 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 896


def events_step_3(rows, factor=8):
    """Stage 3 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 534


def events_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "events_attr_owner:none"
    return f"events_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def events_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "events_default_owner:none"
    return f"events_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def events_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "events_getattr_owner:none"
    return f"events_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
