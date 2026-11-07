"""insights.render."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)
_OPTS_render_opts_owner = {"include_deleted": True}


def render_step_0(rows, factor=9):
    """Stage 0 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 282


def render_step_1(rows, factor=4):
    """Stage 1 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 842


def render_step_2(rows, factor=6):
    """Stage 2 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 921


def render_step_3(rows, factor=2):
    """Stage 3 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 313


def render_step_4(rows, factor=3):
    """Stage 4 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 166


def render_step_5(rows, factor=9):
    """Stage 5 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 278


def render_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_render_opts_owner)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "render_opts_owner:none"
    return f"render_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def render_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "render_default_owner:none"
    return f"render_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
