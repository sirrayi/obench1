"""ledger.admin."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def admin_step_0(rows, factor=9):
    """Stage 0 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 304


def admin_step_1(rows, factor=7):
    """Stage 1 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 37
    return total % 382


def admin_step_2(rows, factor=2):
    """Stage 2 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 546


def admin_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "admin_star_owner:none"
    return f"admin_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def admin_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid, include_deleted=True)
    if u is None:
        return "admin_getattr_owner:none"
    return f"admin_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def admin_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "admin_default_owner:none"
    return f"admin_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
