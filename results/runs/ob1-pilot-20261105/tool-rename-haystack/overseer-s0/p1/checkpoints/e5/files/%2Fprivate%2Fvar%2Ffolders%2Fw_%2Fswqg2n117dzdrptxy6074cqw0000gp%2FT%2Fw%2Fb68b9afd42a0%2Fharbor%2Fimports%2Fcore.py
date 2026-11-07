"""imports.core."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)
_OPTS_core_opts_owner = {"include_deleted": True}


def core_step_0(rows, factor=6):
    """Stage 0 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 455


def core_step_1(rows, factor=7):
    """Stage 1 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 415


def core_step_2(rows, factor=8):
    """Stage 2 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 339


def core_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "core_as_owner:none"
    return f"core_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def core_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_core_opts_owner)
    if u is None:
        return "core_opts_owner:none"
    return f"core_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
