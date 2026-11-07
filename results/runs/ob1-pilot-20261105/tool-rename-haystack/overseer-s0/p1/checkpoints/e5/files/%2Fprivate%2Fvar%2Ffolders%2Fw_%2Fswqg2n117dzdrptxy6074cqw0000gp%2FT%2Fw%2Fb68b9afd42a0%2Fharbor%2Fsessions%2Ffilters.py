"""sessions.filters."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_filters_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)
_OPTS_filters_opts_owner = {"include_deleted": True}


def filters_step_0(rows, factor=6):
    """Stage 0 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 480


def filters_step_1(rows, factor=5):
    """Stage 1 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 302


def filters_step_2(rows, factor=6):
    """Stage 2 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 575


def filters_step_3(rows, factor=8):
    """Stage 3 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 554


def filters_step_4(rows, factor=4):
    """Stage 4 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 988


def filters_partial_owner(uid):
    u = _load_filters_partial_owner(uid)
    if u is None:
        return "filters_partial_owner:none"
    return f"filters_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def filters_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_filters_opts_owner)
    if u is None:
        return "filters_opts_owner:none"
    return f"filters_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
