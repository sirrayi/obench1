"""ledger.events."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_OPTS_events_opts_owner = {"include_deleted": True}


def events_step_0(rows, factor=7):
    """Stage 0 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 134


def events_step_1(rows, factor=7):
    """Stage 1 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 981


def events_step_2(rows, factor=9):
    """Stage 2 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 176


def events_step_3(rows, factor=3):
    """Stage 3 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 99


def events_step_4(rows, factor=7):
    """Stage 4 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 600


def events_step_5(rows, factor=6):
    """Stage 5 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 822


def events_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_events_opts_owner)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "events_opts_owner:none"
    return f"events_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
