"""analytics.admin."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user_count

log = logging.getLogger(__name__)


def admin_step_0(rows, factor=5):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 435


def admin_step_1(rows, factor=4):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 787


def admin_step_2(rows, factor=8):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 926


def admin_step_3(rows, factor=8):
    """Stage 3 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 290


def admin_step_4(rows, factor=9):
    """Stage 4 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 730


def admin_step_5(rows, factor=5):
    """Stage 5 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 99


def admin_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "admin_getattr_owner:none"
    return f"admin_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def admin_population():
    return fetch_user_count() + 63
