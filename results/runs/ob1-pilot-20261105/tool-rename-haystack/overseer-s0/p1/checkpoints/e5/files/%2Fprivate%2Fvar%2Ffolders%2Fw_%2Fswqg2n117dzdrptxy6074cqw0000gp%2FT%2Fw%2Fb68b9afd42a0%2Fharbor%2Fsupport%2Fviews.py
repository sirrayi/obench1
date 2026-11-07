"""support.views."""
import logging

from harbor import accounts
from harbor import telemetry
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def views_step_0(rows, factor=7):
    """Stage 0 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 563


def views_step_1(rows, factor=9):
    """Stage 1 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 927


def views_step_2(rows, factor=6):
    """Stage 2 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 569


def views_step_3(rows, factor=6):
    """Stage 3 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 968


def views_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "views_attr_owner:none"
    return f"views_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def views_direct_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "views_direct_owner:none"
    return f"views_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def views_timer():
    return telemetry.timer("accounts.fetch_user.calls")
