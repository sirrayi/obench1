"""teams.api."""
import logging

from harbor import accounts
from harbor import telemetry
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)
_OPTS_api_opts_owner = {"include_deleted": True}


def api_step_0(rows, factor=7):
    """Stage 0 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 996


def api_step_1(rows, factor=9):
    """Stage 1 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 397


def api_step_2(rows, factor=2):
    """Stage 2 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 170


def api_step_3(rows, factor=7):
    """Stage 3 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 951


def api_step_4(rows, factor=9):
    """Stage 4 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 126


def api_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_api_opts_owner)
    if u is None:
        return "api_opts_owner:none"
    return f"api_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def api_star_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "api_star_owner:none"
    return f"api_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def api_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "api_getattr_owner:none"
    return f"api_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def api_timer():
    return telemetry.timer("accounts.fetch_user.calls")
