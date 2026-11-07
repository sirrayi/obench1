"""plans.merge."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_merge_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def merge_step_0(rows, factor=7):
    """Stage 0 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 704


def merge_step_1(rows, factor=8):
    """Stage 1 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 322


def merge_step_2(rows, factor=4):
    """Stage 2 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 855


def merge_partial_owner(uid):
    u = _load_merge_partial_owner(uid)
    if u is None:
        return "merge_partial_owner:none"
    return f"merge_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
