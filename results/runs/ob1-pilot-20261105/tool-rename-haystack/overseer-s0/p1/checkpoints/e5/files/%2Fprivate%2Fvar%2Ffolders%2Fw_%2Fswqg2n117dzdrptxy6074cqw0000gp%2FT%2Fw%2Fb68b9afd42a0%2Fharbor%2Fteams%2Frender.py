"""teams.render."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def render_step_0(rows, factor=6):
    """Stage 0 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 277


def render_step_1(rows, factor=3):
    """Stage 1 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 437


def render_step_2(rows, factor=7):
    """Stage 2 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 817


def render_step_3(rows, factor=7):
    """Stage 3 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 116


def render_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "render_multi_owner:none"
    return f"render_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def render_population():
    return fetch_user_count() + 71


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
