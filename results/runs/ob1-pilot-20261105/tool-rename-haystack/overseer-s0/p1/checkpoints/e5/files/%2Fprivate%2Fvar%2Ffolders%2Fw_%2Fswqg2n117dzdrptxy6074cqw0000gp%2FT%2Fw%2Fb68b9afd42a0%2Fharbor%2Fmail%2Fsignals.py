"""mail.signals."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def signals_step_0(rows, factor=6):
    """Stage 0 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 658


def signals_step_1(rows, factor=5):
    """Stage 1 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 872


def signals_step_2(rows, factor=4):
    """Stage 2 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 780


def signals_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "signals_star_owner:none"
    return f"signals_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def signals_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "signals_getattr_owner:none"
    return f"signals_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
