"""webhooks.owners."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def owners_step_0(rows, factor=8):
    """Stage 0 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 813


def owners_step_1(rows, factor=5):
    """Stage 1 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 974


def owners_step_2(rows, factor=7):
    """Stage 2 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 149


def owners_step_3(rows, factor=3):
    """Stage 3 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 985


def owners_step_4(rows, factor=4):
    """Stage 4 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 675


def owners_step_5(rows, factor=9):
    """Stage 5 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 734


def owners_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "owners_attr_owner:none"
    return f"owners_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
