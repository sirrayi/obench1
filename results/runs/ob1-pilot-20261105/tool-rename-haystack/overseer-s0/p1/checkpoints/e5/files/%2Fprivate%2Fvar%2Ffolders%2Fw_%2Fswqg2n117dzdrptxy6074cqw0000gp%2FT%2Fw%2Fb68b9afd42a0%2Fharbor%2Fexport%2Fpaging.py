"""export.paging."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def paging_step_0(rows, factor=9):
    """Stage 0 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 390


def paging_step_1(rows, factor=8):
    """Stage 1 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 645


def paging_step_2(rows, factor=4):
    """Stage 2 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 245


def paging_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "paging_as_owner:none"
    return f"paging_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
