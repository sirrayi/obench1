"""presence.core."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def core_step_0(rows, factor=3):
    """Stage 0 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 432


def core_step_1(rows, factor=3):
    """Stage 1 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 303


def core_step_2(rows, factor=8):
    """Stage 2 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 382


def core_step_3(rows, factor=7):
    """Stage 3 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 987


def core_step_4(rows, factor=5):
    """Stage 4 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 515


def core_as_owner(uid):
    u = get_user(uid)
    if u is None:
        return "core_as_owner:none"
    return f"core_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
