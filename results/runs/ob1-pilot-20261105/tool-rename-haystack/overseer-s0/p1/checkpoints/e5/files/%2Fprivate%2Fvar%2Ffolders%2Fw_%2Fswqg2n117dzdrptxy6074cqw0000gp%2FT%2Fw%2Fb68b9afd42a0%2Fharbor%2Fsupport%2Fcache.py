"""support.cache."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def cache_step_0(rows, factor=2):
    """Stage 0 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 680


def cache_step_1(rows, factor=4):
    """Stage 1 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 498


def cache_step_2(rows, factor=5):
    """Stage 2 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 594


def cache_step_3(rows, factor=4):
    """Stage 3 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 260


def cache_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        return "cache_attr_owner:none"
    return f"cache_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
