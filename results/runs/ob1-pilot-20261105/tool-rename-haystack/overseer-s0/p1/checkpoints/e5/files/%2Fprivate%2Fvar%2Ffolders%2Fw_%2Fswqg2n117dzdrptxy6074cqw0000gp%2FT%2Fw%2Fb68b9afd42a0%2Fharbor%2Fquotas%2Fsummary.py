"""quotas.summary."""
import functools
import logging

from harbor import accounts
from harbor.accounts import fetch_user_count

log = logging.getLogger(__name__)
_load_summary_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def summary_step_0(rows, factor=7):
    """Stage 0 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 712


def summary_step_1(rows, factor=5):
    """Stage 1 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 693


def summary_step_2(rows, factor=8):
    """Stage 2 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 315


def summary_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid, include_deleted=True)
    if u is None:
        return "summary_default_owner:none"
    return f"summary_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_partial_owner(uid):
    u = _load_summary_partial_owner(uid)
    if u is None:
        return "summary_partial_owner:none"
    return f"summary_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_population():
    return fetch_user_count() + 18
