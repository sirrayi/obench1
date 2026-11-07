"""push.cache."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def cache_step_0(rows, factor=3):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 900


def cache_step_1(rows, factor=8):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 643


def cache_step_2(rows, factor=8):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 969


def cache_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "cache_direct_owner:none"
    return f"cache_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
