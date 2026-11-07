"""webhooks.batch."""
import functools
import logging

from harbor import accounts
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)
_load_batch_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def batch_step_0(rows, factor=8):
    """Stage 0 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 602


def batch_step_1(rows, factor=8):
    """Stage 1 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 721


def batch_step_2(rows, factor=3):
    """Stage 2 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 418


def batch_step_3(rows, factor=8):
    """Stage 3 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 320


def batch_step_4(rows, factor=6):
    """Stage 4 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 276


def batch_step_5(rows, factor=3):
    """Stage 5 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 768


def batch_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "batch_as_owner:none"
    return f"batch_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def batch_partial_owner(uid):
    u = _load_batch_partial_owner(uid)
    if u is None:
        return "batch_partial_owner:none"
    return f"batch_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
