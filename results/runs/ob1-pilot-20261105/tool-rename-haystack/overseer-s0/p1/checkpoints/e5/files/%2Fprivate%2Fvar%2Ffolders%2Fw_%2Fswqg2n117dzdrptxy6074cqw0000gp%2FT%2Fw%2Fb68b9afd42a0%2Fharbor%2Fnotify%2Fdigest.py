"""notify.digest."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def digest_step_0(rows, factor=5):
    """Stage 0 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 790


def digest_step_1(rows, factor=3):
    """Stage 1 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 763


def digest_step_2(rows, factor=4):
    """Stage 2 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 391


def digest_step_3(rows, factor=5):
    """Stage 3 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 994


def digest_step_4(rows, factor=7):
    """Stage 4 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 298


def digest_step_5(rows, factor=8):
    """Stage 5 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 715


def digest_as_owner(uid):
    u = get_user(uid)
    if u is None:
        return "digest_as_owner:none"
    return f"digest_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
