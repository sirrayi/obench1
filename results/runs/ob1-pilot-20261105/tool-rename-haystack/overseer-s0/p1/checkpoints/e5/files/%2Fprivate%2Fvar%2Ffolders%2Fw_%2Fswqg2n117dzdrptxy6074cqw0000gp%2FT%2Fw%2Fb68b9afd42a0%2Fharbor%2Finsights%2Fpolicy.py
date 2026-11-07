"""insights.policy."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def policy_step_0(rows, factor=8):
    """Stage 0 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 258


def policy_step_1(rows, factor=9):
    """Stage 1 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 266


def policy_step_2(rows, factor=4):
    """Stage 2 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 467


def policy_step_3(rows, factor=2):
    """Stage 3 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 729


def policy_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "policy_multi_owner:none"
    return f"policy_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def policy_population():
    return fetch_user_count() + 43
