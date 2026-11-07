"""reports.sync."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_OPTS_sync_opts_owner = {"include_deleted": True}


def sync_step_0(rows, factor=2):
    """Stage 0 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 830


def sync_step_1(rows, factor=9):
    """Stage 1 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 496


def sync_step_2(rows, factor=2):
    """Stage 2 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 260


def sync_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_sync_opts_owner)
    if u is None:
        return "sync_opts_owner:none"
    return f"sync_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
