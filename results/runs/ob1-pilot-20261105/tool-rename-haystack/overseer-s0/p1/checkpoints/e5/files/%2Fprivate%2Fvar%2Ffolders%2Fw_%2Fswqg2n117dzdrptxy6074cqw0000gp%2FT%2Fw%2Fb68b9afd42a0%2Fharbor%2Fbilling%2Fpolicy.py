"""billing.policy."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def policy_step_0(rows, factor=7):
    """Stage 0 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 865


def policy_step_1(rows, factor=9):
    """Stage 1 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 566


def policy_step_2(rows, factor=5):
    """Stage 2 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 116


def policy_step_3(rows, factor=8):
    """Stage 3 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 896


def policy_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "policy_as_owner:none"
    return f"policy_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
