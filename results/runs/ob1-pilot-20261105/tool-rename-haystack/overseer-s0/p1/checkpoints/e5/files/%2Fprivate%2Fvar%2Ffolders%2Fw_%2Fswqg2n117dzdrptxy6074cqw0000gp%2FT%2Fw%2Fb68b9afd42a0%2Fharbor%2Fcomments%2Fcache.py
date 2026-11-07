"""comments.cache."""
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)


def cache_step_0(rows, factor=4):
    """Stage 0 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 953


def cache_step_1(rows, factor=7):
    """Stage 1 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 883


def cache_step_2(rows, factor=8):
    """Stage 2 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 857


def cache_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "cache_default_owner:none"
    return f"cache_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cache_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        return "cache_modalias_owner:none"
    return f"cache_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
