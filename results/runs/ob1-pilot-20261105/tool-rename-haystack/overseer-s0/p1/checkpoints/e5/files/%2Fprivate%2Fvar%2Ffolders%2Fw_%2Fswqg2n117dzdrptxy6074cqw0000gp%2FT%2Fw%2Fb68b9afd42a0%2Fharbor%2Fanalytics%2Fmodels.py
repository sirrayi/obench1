"""analytics.models."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def models_step_0(rows, factor=6):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 610


def models_step_1(rows, factor=5):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 314


def models_step_2(rows, factor=4):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 431


def models_step_3(rows, factor=9):
    """Stage 3 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 250


def models_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "models_as_owner:none"
    return f"models_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
