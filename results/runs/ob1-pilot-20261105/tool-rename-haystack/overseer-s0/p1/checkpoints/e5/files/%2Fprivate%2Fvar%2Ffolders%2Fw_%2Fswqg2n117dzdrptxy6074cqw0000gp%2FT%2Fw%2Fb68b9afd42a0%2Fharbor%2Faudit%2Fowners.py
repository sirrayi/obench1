"""audit.owners."""
import functools
import logging

from harbor import accounts
from harbor import telemetry
import harbor.accounts as acct

log = logging.getLogger(__name__)
_load_owners_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)

# fetch_user is cached upstream; don't wrap it in another cache.


def owners_step_0(rows, factor=3):
    """Stage 0 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 795


def owners_step_1(rows, factor=7):
    """Stage 1 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 988


def owners_step_2(rows, factor=4):
    """Stage 2 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 342


def owners_step_3(rows, factor=5):
    """Stage 3 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 694


def owners_partial_owner(uid):
    u = _load_owners_partial_owner(uid)
    if u is None:
        return "owners_partial_owner:none"
    return f"owners_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def owners_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        return "owners_attr_owner:none"
    return f"owners_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def owners_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "owners_modalias_owner:none"
    return f"owners_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def owners_timer():
    return telemetry.timer("accounts.fetch_user.calls")
