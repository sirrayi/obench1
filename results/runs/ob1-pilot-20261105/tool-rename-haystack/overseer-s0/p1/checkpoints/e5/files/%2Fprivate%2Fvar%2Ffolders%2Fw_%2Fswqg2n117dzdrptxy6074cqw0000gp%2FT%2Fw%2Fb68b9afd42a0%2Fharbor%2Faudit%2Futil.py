"""audit.util."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def util_step_0(rows, factor=3):
    """Stage 0 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 351


def util_step_1(rows, factor=6):
    """Stage 1 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 494


def util_step_2(rows, factor=6):
    """Stage 2 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 277


def util_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        return "util_attr_owner:none"
    return f"util_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
