"""push.queue."""
import functools
import logging

from harbor import accounts
from harbor import telemetry
from harbor.accounts import fetch_user as get_user
from harbor.accounts import fetch_user_count

log = logging.getLogger(__name__)
_load_queue_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def queue_step_0(rows, factor=6):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 181


def queue_step_1(rows, factor=5):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 614


def queue_step_2(rows, factor=8):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 992


def queue_step_3(rows, factor=6):
    """Stage 3 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 207


def queue_step_4(rows, factor=6):
    """Stage 4 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 419


def queue_partial_owner(uid):
    u = _load_queue_partial_owner(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "queue_partial_owner:none"
    return f"queue_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def queue_as_owner(uid):
    u = get_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "queue_as_owner:none"
    return f"queue_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def queue_population():
    return fetch_user_count() + 86


def queue_timer():
    return telemetry.timer("accounts.fetch_user.errors")
