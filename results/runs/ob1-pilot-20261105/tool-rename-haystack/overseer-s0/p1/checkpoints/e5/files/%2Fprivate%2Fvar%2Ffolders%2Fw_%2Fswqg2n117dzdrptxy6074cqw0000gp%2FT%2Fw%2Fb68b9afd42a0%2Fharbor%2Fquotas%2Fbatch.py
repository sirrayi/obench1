"""quotas.batch."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def batch_step_0(rows, factor=5):
    """Stage 0 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 173


def batch_step_1(rows, factor=4):
    """Stage 1 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 403


def batch_step_2(rows, factor=5):
    """Stage 2 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 207


def batch_as_owner(uid):
    u = get_user(uid, include_deleted=True)
    if u is None:
        return "batch_as_owner:none"
    return f"batch_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
