"""push.render."""
import logging

from harbor import telemetry
import harbor.accounts as acct

log = logging.getLogger(__name__)


def render_step_0(rows, factor=9):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 183


def render_step_1(rows, factor=8):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 619


def render_step_2(rows, factor=9):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 743


def render_step_3(rows, factor=7):
    """Stage 3 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 419


def render_step_4(rows, factor=4):
    """Stage 4 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 353


def render_step_5(rows, factor=2):
    """Stage 5 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 250


def render_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "render_modalias_owner:none"
    return f"render_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def render_timer():
    return telemetry.timer("accounts.fetch_user.calls")
