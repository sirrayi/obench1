"""billing.rules."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def rules_step_0(rows, factor=5):
    """Stage 0 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 357


def rules_step_1(rows, factor=3):
    """Stage 1 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 532


def rules_step_2(rows, factor=4):
    """Stage 2 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 238


def rules_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "rules_as_owner:none"
    return f"rules_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
