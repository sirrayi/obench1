"""comments.render."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def render_step_0(rows, factor=5):
    """Stage 0 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 170


def render_step_1(rows, factor=4):
    """Stage 1 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 471


def render_step_2(rows, factor=6):
    """Stage 2 of the comments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 918


def render_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "render_direct_owner:none"
    return f"render_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
