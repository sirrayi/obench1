"""presence.queue."""
import functools
import logging

from harbor import accounts
from harbor import telemetry
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)
_load_queue_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def queue_step_0(rows, factor=8):
    """Stage 0 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 895


def queue_step_1(rows, factor=4):
    """Stage 1 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 653


def queue_step_2(rows, factor=4):
    """Stage 2 of the presence pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 815


def queue_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "queue_direct_owner:none"
    return f"queue_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def queue_partial_owner(uid):
    u = _load_queue_partial_owner(uid)
    if u is None:
        return "queue_partial_owner:none"
    return f"queue_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def queue_timer():
    return telemetry.timer("accounts.fetch_user.calls")
