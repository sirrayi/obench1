"""reports.paging."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def paging_step_0(rows, factor=6):
    """Stage 0 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 522


def paging_step_1(rows, factor=3):
    """Stage 1 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 405


def paging_step_2(rows, factor=7):
    """Stage 2 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 567


def paging_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "paging_default_owner:none"
    return f"paging_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
