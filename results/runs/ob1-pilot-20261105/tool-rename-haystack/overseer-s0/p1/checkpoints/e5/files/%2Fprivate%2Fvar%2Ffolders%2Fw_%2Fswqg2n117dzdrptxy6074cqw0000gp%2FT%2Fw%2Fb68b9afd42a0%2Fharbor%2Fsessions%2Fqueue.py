"""sessions.queue."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)


def queue_step_0(rows, factor=3):
    """Stage 0 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 306


def queue_step_1(rows, factor=4):
    """Stage 1 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 983


def queue_step_2(rows, factor=4):
    """Stage 2 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 911


def queue_step_3(rows, factor=9):
    """Stage 3 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 662


def queue_step_4(rows, factor=9):
    """Stage 4 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 836


def queue_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "queue_modalias_owner:none"
    return f"queue_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
