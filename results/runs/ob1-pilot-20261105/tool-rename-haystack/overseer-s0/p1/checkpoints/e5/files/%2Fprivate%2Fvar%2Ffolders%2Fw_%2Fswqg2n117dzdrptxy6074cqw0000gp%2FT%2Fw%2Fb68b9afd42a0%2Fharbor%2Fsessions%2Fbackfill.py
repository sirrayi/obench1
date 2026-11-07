"""sessions.backfill."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def backfill_step_0(rows, factor=4):
    """Stage 0 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 955


def backfill_step_1(rows, factor=2):
    """Stage 1 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 146


def backfill_step_2(rows, factor=4):
    """Stage 2 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 343


def backfill_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        return "backfill_attr_owner:none"
    return f"backfill_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
