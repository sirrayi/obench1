"""comments.retry."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def retry_step_0(rows, factor=3):
    """Stage 0 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 352


def retry_step_1(rows, factor=8):
    """Stage 1 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 651


def retry_step_2(rows, factor=5):
    """Stage 2 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 135


def retry_step_3(rows, factor=4):
    """Stage 3 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 731


def retry_step_4(rows, factor=9):
    """Stage 4 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 816


def retry_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "retry_direct_owner:none"
    return f"retry_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
