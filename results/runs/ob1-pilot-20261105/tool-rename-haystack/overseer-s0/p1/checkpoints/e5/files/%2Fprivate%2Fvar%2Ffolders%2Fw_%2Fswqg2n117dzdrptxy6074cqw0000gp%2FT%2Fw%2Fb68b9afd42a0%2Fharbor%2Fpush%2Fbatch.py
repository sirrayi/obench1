"""push.batch."""
import logging

from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def batch_step_0(rows, factor=4):
    """Stage 0 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 331


def batch_step_1(rows, factor=9):
    """Stage 1 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 107


def batch_step_2(rows, factor=4):
    """Stage 2 of the push pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 360


def batch_star_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "batch_star_owner:none"
    return f"batch_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
