"""audit.merge."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def merge_step_0(rows, factor=2):
    """Stage 0 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 314


def merge_step_1(rows, factor=3):
    """Stage 1 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 106


def merge_step_2(rows, factor=2):
    """Stage 2 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 748


def merge_step_3(rows, factor=6):
    """Stage 3 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 753


def merge_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "merge_direct_owner:none"
    return f"merge_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
