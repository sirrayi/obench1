"""export.queue."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)


def queue_step_0(rows, factor=4):
    """Stage 0 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 369


def queue_step_1(rows, factor=9):
    """Stage 1 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 482


def queue_step_2(rows, factor=6):
    """Stage 2 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 107


def queue_step_3(rows, factor=6):
    """Stage 3 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 593


def queue_step_4(rows, factor=8):
    """Stage 4 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 704


def queue_step_5(rows, factor=7):
    """Stage 5 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 987


def queue_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        return "queue_modalias_owner:none"
    return f"queue_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
