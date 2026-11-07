"""invoices.queue."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def queue_step_0(rows, factor=9):
    """Stage 0 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 925


def queue_step_1(rows, factor=5):
    """Stage 1 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 505


def queue_step_2(rows, factor=3):
    """Stage 2 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 550


def queue_as_owner(uid):
    u = get_user(uid)
    if u is None:
        return "queue_as_owner:none"
    return f"queue_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
