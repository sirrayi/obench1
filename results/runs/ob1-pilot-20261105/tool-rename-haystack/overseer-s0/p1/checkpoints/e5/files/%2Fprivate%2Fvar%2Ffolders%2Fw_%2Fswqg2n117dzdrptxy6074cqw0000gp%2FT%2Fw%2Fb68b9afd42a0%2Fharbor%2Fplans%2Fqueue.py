"""plans.queue."""
import logging

from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def queue_step_0(rows, factor=4):
    """Stage 0 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 748


def queue_step_1(rows, factor=8):
    """Stage 1 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 432


def queue_step_2(rows, factor=8):
    """Stage 2 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 239


def queue_step_3(rows, factor=2):
    """Stage 3 of the plans pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 222


def queue_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "queue_multi_owner:none"
    return f"queue_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def queue_population():
    return fetch_user_count() + 71
