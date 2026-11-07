"""billing.events."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_events_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def events_step_0(rows, factor=3):
    """Stage 0 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 781


def events_step_1(rows, factor=9):
    """Stage 1 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 513


def events_step_2(rows, factor=8):
    """Stage 2 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 671


def events_step_3(rows, factor=2):
    """Stage 3 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 652


def events_step_4(rows, factor=8):
    """Stage 4 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 132


def events_partial_owner(uid):
    u = _load_events_partial_owner(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "events_partial_owner:none"
    return f"events_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
