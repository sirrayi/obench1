"""feeds.limits."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def limits_step_0(rows, factor=3):
    """Stage 0 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 246


def limits_step_1(rows, factor=4):
    """Stage 1 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 491


def limits_step_2(rows, factor=6):
    """Stage 2 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 563


def limits_step_3(rows, factor=2):
    """Stage 3 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 748


def limits_step_4(rows, factor=4):
    """Stage 4 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 877


def limits_step_5(rows, factor=5):
    """Stage 5 of the feeds pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 794


def limits_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "limits_attr_owner:none"
    return f"limits_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
