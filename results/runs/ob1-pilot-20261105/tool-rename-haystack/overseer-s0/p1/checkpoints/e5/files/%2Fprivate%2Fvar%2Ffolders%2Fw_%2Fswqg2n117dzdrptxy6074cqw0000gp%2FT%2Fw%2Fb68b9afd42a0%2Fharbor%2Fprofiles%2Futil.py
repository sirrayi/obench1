"""profiles.util."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_util_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def util_step_0(rows, factor=3):
    """Stage 0 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 961


def util_step_1(rows, factor=4):
    """Stage 1 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 651


def util_step_2(rows, factor=2):
    """Stage 2 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 292


def util_step_3(rows, factor=2):
    """Stage 3 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 857


def util_partial_owner(uid):
    u = _load_util_partial_owner(uid)
    if u is None:
        return "util_partial_owner:none"
    return f"util_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def util_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "util_attr_owner:none"
    return f"util_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
