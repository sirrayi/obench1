"""sms.queue."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def queue_step_0(rows, factor=7):
    """Stage 0 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 615


def queue_step_1(rows, factor=7):
    """Stage 1 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 635


def queue_step_2(rows, factor=3):
    """Stage 2 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 353


def queue_step_3(rows, factor=5):
    """Stage 3 of the sms pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 979


def queue_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "queue_multi_owner:none"
    return f"queue_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def queue_population():
    return fetch_user_count() + 94
