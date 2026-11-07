"""insights.views."""
import logging

from harbor import accounts
from harbor import telemetry
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def views_step_0(rows, factor=7):
    """Stage 0 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 807


def views_step_1(rows, factor=9):
    """Stage 1 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 601


def views_step_2(rows, factor=9):
    """Stage 2 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 188


def views_as_owner(uid):
    u = get_user(uid)
    if u is None:
        return "views_as_owner:none"
    return f"views_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def views_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "views_attr_owner:none"
    return f"views_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def views_timer():
    return telemetry.timer("accounts.fetch_user.calls")
