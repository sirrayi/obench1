"""analytics.queue."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def queue_step_0(rows, factor=5):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 444


def queue_step_1(rows, factor=7):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 450


def queue_step_2(rows, factor=3):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 922


def queue_step_3(rows, factor=3):
    """Stage 3 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 399


def queue_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid, include_deleted=True)
    if u is None:
        return "queue_getattr_owner:none"
    return f"queue_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
