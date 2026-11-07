"""export.summary."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def summary_step_0(rows, factor=5):
    """Stage 0 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 489


def summary_step_1(rows, factor=4):
    """Stage 1 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 512


def summary_step_2(rows, factor=9):
    """Stage 2 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 167


def summary_step_3(rows, factor=3):
    """Stage 3 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 345


def summary_step_4(rows, factor=7):
    """Stage 4 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 572


def summary_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "summary_as_owner:none"
    return f"summary_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
