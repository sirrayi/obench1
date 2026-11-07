"""search.summary."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def summary_step_0(rows, factor=7):
    """Stage 0 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 151


def summary_step_1(rows, factor=3):
    """Stage 1 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 584


def summary_step_2(rows, factor=5):
    """Stage 2 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 119


def summary_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "summary_direct_owner:none"
    return f"summary_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
