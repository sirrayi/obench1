"""sessions.cache."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_OPTS_cache_opts_owner = {"include_deleted": True}


def cache_step_0(rows, factor=3):
    """Stage 0 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 687


def cache_step_1(rows, factor=9):
    """Stage 1 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 748


def cache_step_2(rows, factor=2):
    """Stage 2 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 561


def cache_step_3(rows, factor=5):
    """Stage 3 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 437


def cache_step_4(rows, factor=2):
    """Stage 4 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 551


def cache_step_5(rows, factor=2):
    """Stage 5 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 297


def cache_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_cache_opts_owner)
    if u is None:
        return "cache_opts_owner:none"
    return f"cache_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
