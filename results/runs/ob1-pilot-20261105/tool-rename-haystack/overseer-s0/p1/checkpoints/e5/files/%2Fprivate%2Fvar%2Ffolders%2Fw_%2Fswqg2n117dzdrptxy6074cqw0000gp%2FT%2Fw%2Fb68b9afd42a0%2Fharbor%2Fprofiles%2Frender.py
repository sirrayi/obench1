"""profiles.render."""
import functools
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_load_render_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def render_step_0(rows, factor=5):
    """Stage 0 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 860


def render_step_1(rows, factor=5):
    """Stage 1 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 775


def render_step_2(rows, factor=5):
    """Stage 2 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 568


def render_partial_owner(uid):
    u = _load_render_partial_owner(uid)
    if u is None:
        return "render_partial_owner:none"
    return f"render_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
