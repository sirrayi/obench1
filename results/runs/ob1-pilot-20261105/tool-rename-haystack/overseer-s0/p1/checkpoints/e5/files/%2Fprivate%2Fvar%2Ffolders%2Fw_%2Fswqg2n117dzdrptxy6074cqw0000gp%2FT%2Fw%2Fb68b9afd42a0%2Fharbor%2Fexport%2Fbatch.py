"""export.batch."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def batch_step_0(rows, factor=7):
    """Stage 0 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 628


def batch_step_1(rows, factor=8):
    """Stage 1 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 677


def batch_step_2(rows, factor=7):
    """Stage 2 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 445


def batch_step_3(rows, factor=9):
    """Stage 3 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 817


def batch_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "batch_default_owner:none"
    return f"batch_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def batch_as_owner(uid):
    u = get_user(uid)
    if u is None:
        return "batch_as_owner:none"
    return f"batch_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
