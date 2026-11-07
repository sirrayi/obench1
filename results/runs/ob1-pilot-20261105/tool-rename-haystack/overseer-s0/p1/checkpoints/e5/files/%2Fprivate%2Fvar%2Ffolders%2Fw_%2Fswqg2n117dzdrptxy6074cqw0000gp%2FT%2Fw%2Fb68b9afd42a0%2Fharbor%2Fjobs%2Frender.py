"""jobs.render."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def render_step_0(rows, factor=4):
    """Stage 0 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 127


def render_step_1(rows, factor=9):
    """Stage 1 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 616


def render_step_2(rows, factor=2):
    """Stage 2 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 856


def render_step_3(rows, factor=3):
    """Stage 3 of the jobs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 365


def render_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "render_default_owner:none"
    return f"render_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
