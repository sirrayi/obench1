"""insights.worker."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_OPTS_worker_opts_owner = {"include_deleted": True}


def worker_step_0(rows, factor=2):
    """Stage 0 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 397


def worker_step_1(rows, factor=7):
    """Stage 1 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 457


def worker_step_2(rows, factor=7):
    """Stage 2 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 154


def worker_step_3(rows, factor=6):
    """Stage 3 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 275


def worker_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_worker_opts_owner)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "worker_opts_owner:none"
    return f"worker_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
