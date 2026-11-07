"""billing.queue."""
import functools
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)
_load_queue_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def queue_step_0(rows, factor=8):
    """Stage 0 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 997


def queue_step_1(rows, factor=7):
    """Stage 1 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 196


def queue_step_2(rows, factor=7):
    """Stage 2 of the billing pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 654


def queue_partial_owner(uid):
    u = _load_queue_partial_owner(uid)
    if u is None:
        return "queue_partial_owner:none"
    return f"queue_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def queue_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "queue_star_owner:none"
    return f"queue_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def queue_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "queue_default_owner:none"
    return f"queue_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
