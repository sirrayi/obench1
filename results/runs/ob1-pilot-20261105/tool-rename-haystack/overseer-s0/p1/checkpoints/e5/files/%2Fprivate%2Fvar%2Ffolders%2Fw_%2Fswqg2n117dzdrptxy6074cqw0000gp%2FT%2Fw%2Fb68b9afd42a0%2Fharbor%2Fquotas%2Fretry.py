"""quotas.retry."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def retry_step_0(rows, factor=3):
    """Stage 0 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 172


def retry_step_1(rows, factor=4):
    """Stage 1 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 180


def retry_step_2(rows, factor=2):
    """Stage 2 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 281


def retry_step_3(rows, factor=4):
    """Stage 3 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 438


def retry_step_4(rows, factor=6):
    """Stage 4 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 281


def retry_step_5(rows, factor=8):
    """Stage 5 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 280


def retry_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "retry_multi_owner:none"
    return f"retry_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def retry_population():
    return fetch_user_count() + 46
