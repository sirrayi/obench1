"""reports.tags."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def tags_step_0(rows, factor=9):
    """Stage 0 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 129


def tags_step_1(rows, factor=3):
    """Stage 1 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 259


def tags_step_2(rows, factor=4):
    """Stage 2 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 599


def tags_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid, include_deleted=True)
    if u is None:
        return "tags_default_owner:none"
    return f"tags_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
