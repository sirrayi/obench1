"""sms.render."""
import functools
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)
_load_render_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def render_step_0(rows, factor=4):
    """Stage 0 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 657


def render_step_1(rows, factor=8):
    """Stage 1 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 636


def render_step_2(rows, factor=3):
    """Stage 2 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 381


def render_step_3(rows, factor=6):
    """Stage 3 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 285


def render_partial_owner(uid):
    u = _load_render_partial_owner(uid)
    if u is None:
        return "render_partial_owner:none"
    return f"render_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def render_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "render_multi_owner:none"
    return f"render_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def render_population():
    return fetch_user_count() + 27
