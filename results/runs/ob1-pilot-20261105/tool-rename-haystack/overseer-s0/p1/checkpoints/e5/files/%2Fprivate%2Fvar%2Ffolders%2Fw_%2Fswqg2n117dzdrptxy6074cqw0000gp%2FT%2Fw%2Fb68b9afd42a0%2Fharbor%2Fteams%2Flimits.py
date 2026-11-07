"""teams.limits."""
import functools
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)
_load_limits_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def limits_step_0(rows, factor=3):
    """Stage 0 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 493


def limits_step_1(rows, factor=4):
    """Stage 1 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 308


def limits_step_2(rows, factor=5):
    """Stage 2 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 984


def limits_step_3(rows, factor=7):
    """Stage 3 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 513


def limits_step_4(rows, factor=4):
    """Stage 4 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 348


def limits_step_5(rows, factor=9):
    """Stage 5 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 892


def limits_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "limits_modalias_owner:none"
    return f"limits_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def limits_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid, include_deleted=True)
    if u is None:
        return "limits_getattr_owner:none"
    return f"limits_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def limits_partial_owner(uid):
    u = _load_limits_partial_owner(uid)
    if u is None:
        return "limits_partial_owner:none"
    return f"limits_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
