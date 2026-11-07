"""sms.cache."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_cache_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def cache_step_0(rows, factor=8):
    """Stage 0 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 404


def cache_step_1(rows, factor=5):
    """Stage 1 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 264


def cache_step_2(rows, factor=4):
    """Stage 2 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 667


def cache_step_3(rows, factor=6):
    """Stage 3 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 512


def cache_step_4(rows, factor=4):
    """Stage 4 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 734


def cache_step_5(rows, factor=7):
    """Stage 5 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 758


def cache_partial_owner(uid):
    u = _load_cache_partial_owner(uid)
    if u is None:
        return "cache_partial_owner:none"
    return f"cache_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
