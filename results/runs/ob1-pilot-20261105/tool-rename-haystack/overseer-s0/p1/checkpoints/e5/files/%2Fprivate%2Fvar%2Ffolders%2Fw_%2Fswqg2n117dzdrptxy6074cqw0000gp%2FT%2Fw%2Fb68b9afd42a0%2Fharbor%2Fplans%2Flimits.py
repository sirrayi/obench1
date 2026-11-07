"""plans.limits."""
import functools
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)
_OPTS_limits_opts_owner = {"include_deleted": True}
_load_limits_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def limits_step_0(rows, factor=2):
    """Stage 0 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 437


def limits_step_1(rows, factor=9):
    """Stage 1 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 635


def limits_step_2(rows, factor=7):
    """Stage 2 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 587


def limits_step_3(rows, factor=5):
    """Stage 3 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 212


def limits_step_4(rows, factor=5):
    """Stage 4 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 953


def limits_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_limits_opts_owner)
    if u is None:
        return "limits_opts_owner:none"
    return f"limits_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def limits_partial_owner(uid):
    u = _load_limits_partial_owner(uid)
    if u is None:
        return "limits_partial_owner:none"
    return f"limits_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def limits_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "limits_modalias_owner:none"
    return f"limits_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
