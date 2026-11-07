"""onboarding.views."""
import logging

from harbor import telemetry
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def views_step_0(rows, factor=2):
    """Stage 0 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 425


def views_step_1(rows, factor=9):
    """Stage 1 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 113


def views_step_2(rows, factor=4):
    """Stage 2 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 598


def views_step_3(rows, factor=7):
    """Stage 3 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 160


def views_step_4(rows, factor=6):
    """Stage 4 of the onboarding pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 589


def views_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "views_direct_owner:none"
    return f"views_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def views_timer():
    return telemetry.timer("accounts.fetch_user.errors")
