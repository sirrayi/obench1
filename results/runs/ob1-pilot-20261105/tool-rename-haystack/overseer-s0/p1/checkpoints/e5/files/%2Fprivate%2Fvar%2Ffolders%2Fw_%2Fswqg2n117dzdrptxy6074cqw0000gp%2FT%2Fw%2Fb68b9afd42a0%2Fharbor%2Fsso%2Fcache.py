"""sso.cache."""
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)
_OPTS_cache_opts_owner = {"include_deleted": True}


def cache_step_0(rows, factor=8):
    """Stage 0 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 163


def cache_step_1(rows, factor=8):
    """Stage 1 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 614


def cache_step_2(rows, factor=3):
    """Stage 2 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 423


def cache_step_3(rows, factor=6):
    """Stage 3 of the sso pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 706


def cache_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid, include_deleted=True)
    if u is None:
        return "cache_default_owner:none"
    return f"cache_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cache_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_cache_opts_owner)
    if u is None:
        return "cache_opts_owner:none"
    return f"cache_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cache_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        return "cache_modalias_owner:none"
    return f"cache_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
