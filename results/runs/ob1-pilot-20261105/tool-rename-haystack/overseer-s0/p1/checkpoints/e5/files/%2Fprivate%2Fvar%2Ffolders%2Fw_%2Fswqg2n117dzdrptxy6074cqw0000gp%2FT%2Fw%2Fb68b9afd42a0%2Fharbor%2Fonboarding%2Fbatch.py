"""onboarding.batch."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def batch_step_0(rows, factor=3):
    """Stage 0 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 516


def batch_step_1(rows, factor=9):
    """Stage 1 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 868


def batch_step_2(rows, factor=5):
    """Stage 2 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 430


def batch_multi_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "batch_multi_owner:none"
    return f"batch_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def batch_population():
    return fetch_user_count() + 76
