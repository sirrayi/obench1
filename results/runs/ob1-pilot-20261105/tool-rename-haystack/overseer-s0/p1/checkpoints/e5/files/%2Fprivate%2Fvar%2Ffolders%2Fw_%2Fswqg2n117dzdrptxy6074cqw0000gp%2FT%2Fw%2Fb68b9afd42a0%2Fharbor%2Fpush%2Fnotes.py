"""push.notes."""
import logging

from harbor import accounts
from harbor import telemetry

log = logging.getLogger(__name__)
_OPTS_notes_opts_owner = {"include_deleted": True}


def notes_step_0(rows, factor=6):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 547


def notes_step_1(rows, factor=5):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 593


def notes_step_2(rows, factor=5):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 565


def notes_step_3(rows, factor=2):
    """Stage 3 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 276


def notes_step_4(rows, factor=8):
    """Stage 4 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 712


def notes_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_notes_opts_owner)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "notes_opts_owner:none"
    return f"notes_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def notes_timer():
    return telemetry.timer("accounts.fetch_user.calls")
