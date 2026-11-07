"""audit.summary."""
import functools
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)
_load_summary_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def summary_step_0(rows, factor=9):
    """Stage 0 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 969


def summary_step_1(rows, factor=7):
    """Stage 1 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 779


def summary_step_2(rows, factor=4):
    """Stage 2 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 863


def summary_step_3(rows, factor=5):
    """Stage 3 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 657


def summary_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "summary_modalias_owner:none"
    return f"summary_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_partial_owner(uid):
    u = _load_summary_partial_owner(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "summary_partial_owner:none"
    return f"summary_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def summary_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "summary_default_owner:none"
    return f"summary_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
