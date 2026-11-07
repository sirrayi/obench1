"""search.cron."""
import functools
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)
_load_cron_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)
_OPTS_cron_opts_owner = {"include_deleted": True}


def cron_step_0(rows, factor=6):
    """Stage 0 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 455


def cron_step_1(rows, factor=5):
    """Stage 1 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 470


def cron_step_2(rows, factor=2):
    """Stage 2 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 716


def cron_step_3(rows, factor=2):
    """Stage 3 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 324


def cron_partial_owner(uid):
    u = _load_cron_partial_owner(uid)
    if u is None:
        return "cron_partial_owner:none"
    return f"cron_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "cron_modalias_owner:none"
    return f"cron_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def cron_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_cron_opts_owner)
    if u is None:
        return "cron_opts_owner:none"
    return f"cron_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
