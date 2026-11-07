"""ledger.render."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_render_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def render_step_0(rows, factor=3):
    """Stage 0 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 828


def render_step_1(rows, factor=2):
    """Stage 1 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 771


def render_step_2(rows, factor=9):
    """Stage 2 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 964


def render_partial_owner(uid):
    u = _load_render_partial_owner(uid)
    if u is None:
        return "render_partial_owner:none"
    return f"render_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
