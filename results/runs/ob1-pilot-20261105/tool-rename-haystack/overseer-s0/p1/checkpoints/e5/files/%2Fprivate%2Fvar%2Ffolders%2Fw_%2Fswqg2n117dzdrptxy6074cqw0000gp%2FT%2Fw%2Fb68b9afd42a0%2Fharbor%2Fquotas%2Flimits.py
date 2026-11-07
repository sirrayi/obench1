"""quotas.limits."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_limits_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def limits_step_0(rows, factor=9):
    """Stage 0 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 924


def limits_step_1(rows, factor=6):
    """Stage 1 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 854


def limits_step_2(rows, factor=4):
    """Stage 2 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 225


def limits_step_3(rows, factor=4):
    """Stage 3 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 715


def limits_step_4(rows, factor=9):
    """Stage 4 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 861


def limits_partial_owner(uid):
    u = _load_limits_partial_owner(uid)
    if u is None:
        return "limits_partial_owner:none"
    return f"limits_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
