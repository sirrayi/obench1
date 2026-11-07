"""search.policy."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def policy_step_0(rows, factor=5):
    """Stage 0 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 113


def policy_step_1(rows, factor=4):
    """Stage 1 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 656


def policy_step_2(rows, factor=5):
    """Stage 2 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 149


def policy_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "policy_attr_owner:none"
    return f"policy_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
