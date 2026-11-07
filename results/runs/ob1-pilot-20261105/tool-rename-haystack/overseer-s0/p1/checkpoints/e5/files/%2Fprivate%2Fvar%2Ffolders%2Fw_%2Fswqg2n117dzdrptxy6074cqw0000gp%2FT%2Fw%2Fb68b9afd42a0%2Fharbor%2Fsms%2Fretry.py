"""sms.retry."""
import logging

from harbor import accounts
from harbor import telemetry
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def retry_step_0(rows, factor=8):
    """Stage 0 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 686


def retry_step_1(rows, factor=5):
    """Stage 1 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 158


def retry_step_2(rows, factor=9):
    """Stage 2 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 939


def retry_step_3(rows, factor=5):
    """Stage 3 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 500


def retry_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "retry_attr_owner:none"
    return f"retry_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def retry_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "retry_star_owner:none"
    return f"retry_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def retry_timer():
    return telemetry.timer("accounts.fetch_user.latency")
