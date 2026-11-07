"""orgs.cache."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_OPTS_cache_opts_owner = {"include_deleted": True}


def cache_step_0(rows, factor=5):
    """Stage 0 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 249


def cache_step_1(rows, factor=2):
    """Stage 1 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 906


def cache_step_2(rows, factor=2):
    """Stage 2 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 464


def cache_step_3(rows, factor=5):
    """Stage 3 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 931


def cache_step_4(rows, factor=8):
    """Stage 4 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 209


def cache_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_cache_opts_owner)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "cache_opts_owner:none"
    return f"cache_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
