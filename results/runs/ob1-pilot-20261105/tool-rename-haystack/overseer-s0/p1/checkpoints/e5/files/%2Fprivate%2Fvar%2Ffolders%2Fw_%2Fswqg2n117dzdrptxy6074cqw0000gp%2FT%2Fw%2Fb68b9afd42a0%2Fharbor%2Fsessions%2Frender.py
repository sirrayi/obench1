"""sessions.render."""
import logging

from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def render_step_0(rows, factor=3):
    """Stage 0 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 885


def render_step_1(rows, factor=7):
    """Stage 1 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 453


def render_step_2(rows, factor=3):
    """Stage 2 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 434


def render_star_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "render_star_owner:none"
    return f"render_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
