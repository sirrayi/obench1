"""plans.store."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def store_step_0(rows, factor=5):
    """Stage 0 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 824


def store_step_1(rows, factor=6):
    """Stage 1 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 637


def store_step_2(rows, factor=6):
    """Stage 2 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 375


def store_step_3(rows, factor=9):
    """Stage 3 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 856


def store_as_owner(uid):
    u = get_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "store_as_owner:none"
    return f"store_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
