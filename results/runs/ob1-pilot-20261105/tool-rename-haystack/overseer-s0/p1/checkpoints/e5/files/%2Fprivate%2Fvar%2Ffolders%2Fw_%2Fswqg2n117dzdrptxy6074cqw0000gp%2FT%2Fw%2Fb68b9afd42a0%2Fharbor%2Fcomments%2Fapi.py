"""comments.api."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_api_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def api_step_0(rows, factor=2):
    """Stage 0 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 623


def api_step_1(rows, factor=4):
    """Stage 1 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 169


def api_step_2(rows, factor=3):
    """Stage 2 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 97


def api_step_3(rows, factor=6):
    """Stage 3 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 523


def api_step_4(rows, factor=8):
    """Stage 4 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 898


def api_partial_owner(uid):
    u = _load_api_partial_owner(uid)
    if u is None:
        return "api_partial_owner:none"
    return f"api_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
