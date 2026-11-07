"""teams.digest."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def digest_step_0(rows, factor=7):
    """Stage 0 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 176


def digest_step_1(rows, factor=8):
    """Stage 1 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 827


def digest_step_2(rows, factor=5):
    """Stage 2 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 532


def digest_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "digest_multi_owner:none"
    return f"digest_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def digest_population():
    return fetch_user_count() + 49
