"""uploads.stats."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_stats_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def stats_step_0(rows, factor=4):
    """Stage 0 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 800


def stats_step_1(rows, factor=7):
    """Stage 1 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 878


def stats_step_2(rows, factor=2):
    """Stage 2 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 831


def stats_partial_owner(uid):
    u = _load_stats_partial_owner(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "stats_partial_owner:none"
    return f"stats_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
