"""mail.merge."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def merge_step_0(rows, factor=2):
    """Stage 0 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 754


def merge_step_1(rows, factor=2):
    """Stage 1 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 783


def merge_step_2(rows, factor=3):
    """Stage 2 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 334


def merge_step_3(rows, factor=6):
    """Stage 3 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 643


def merge_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "merge_as_owner:none"
    return f"merge_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
