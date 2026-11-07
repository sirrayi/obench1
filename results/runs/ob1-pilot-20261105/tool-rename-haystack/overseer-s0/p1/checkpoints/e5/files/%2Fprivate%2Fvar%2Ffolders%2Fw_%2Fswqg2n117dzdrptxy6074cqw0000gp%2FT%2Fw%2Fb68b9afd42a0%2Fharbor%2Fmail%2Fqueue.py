"""mail.queue."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)


def queue_step_0(rows, factor=9):
    """Stage 0 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 458


def queue_step_1(rows, factor=7):
    """Stage 1 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 805


def queue_step_2(rows, factor=8):
    """Stage 2 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 644


def queue_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        return "queue_modalias_owner:none"
    return f"queue_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
