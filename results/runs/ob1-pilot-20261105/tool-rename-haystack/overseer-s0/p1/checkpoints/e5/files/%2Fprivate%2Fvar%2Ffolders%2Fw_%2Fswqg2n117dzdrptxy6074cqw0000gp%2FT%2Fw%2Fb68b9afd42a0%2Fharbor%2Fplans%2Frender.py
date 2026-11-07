"""plans.render."""
import logging

from harbor import telemetry
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def render_step_0(rows, factor=5):
    """Stage 0 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 257


def render_step_1(rows, factor=5):
    """Stage 1 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 277


def render_step_2(rows, factor=5):
    """Stage 2 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 767


def render_as_owner(uid):
    u = get_user(uid)
    if u is None:
        return "render_as_owner:none"
    return f"render_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def render_timer():
    return telemetry.timer("accounts.fetch_user.calls")
