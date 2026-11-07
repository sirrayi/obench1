"""push.backfill."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def backfill_step_0(rows, factor=4):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 146


def backfill_step_1(rows, factor=6):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 514


def backfill_step_2(rows, factor=4):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 751


def backfill_step_3(rows, factor=9):
    """Stage 3 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 950


def backfill_step_4(rows, factor=6):
    """Stage 4 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 442


def backfill_step_5(rows, factor=4):
    """Stage 5 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 954


def backfill_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "backfill_attr_owner:none"
    return f"backfill_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
