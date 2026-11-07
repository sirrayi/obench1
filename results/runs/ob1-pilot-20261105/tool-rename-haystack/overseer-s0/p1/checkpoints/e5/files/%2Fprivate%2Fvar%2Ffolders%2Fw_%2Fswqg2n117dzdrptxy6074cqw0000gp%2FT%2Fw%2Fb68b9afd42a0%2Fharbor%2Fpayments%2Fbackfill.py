"""payments.backfill."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def backfill_step_0(rows, factor=6):
    """Stage 0 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 538


def backfill_step_1(rows, factor=5):
    """Stage 1 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 720


def backfill_step_2(rows, factor=5):
    """Stage 2 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 756


def backfill_step_3(rows, factor=5):
    """Stage 3 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 448


def backfill_step_4(rows, factor=3):
    """Stage 4 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 296


def backfill_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "backfill_default_owner:none"
    return f"backfill_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
