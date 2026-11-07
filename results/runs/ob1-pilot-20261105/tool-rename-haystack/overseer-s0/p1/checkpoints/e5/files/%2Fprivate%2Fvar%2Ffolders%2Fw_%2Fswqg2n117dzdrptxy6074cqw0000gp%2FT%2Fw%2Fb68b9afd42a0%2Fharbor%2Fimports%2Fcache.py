"""imports.cache."""
import functools
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)
_load_cache_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def cache_step_0(rows, factor=3):
    """Stage 0 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 532


def cache_step_1(rows, factor=2):
    """Stage 1 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 208


def cache_step_2(rows, factor=3):
    """Stage 2 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 655


def cache_step_3(rows, factor=6):
    """Stage 3 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 97


def cache_step_4(rows, factor=8):
    """Stage 4 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 843


def cache_partial_owner(uid):
    u = _load_cache_partial_owner(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "cache_partial_owner:none"
    return f"cache_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cache_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "cache_modalias_owner:none"
    return f"cache_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
