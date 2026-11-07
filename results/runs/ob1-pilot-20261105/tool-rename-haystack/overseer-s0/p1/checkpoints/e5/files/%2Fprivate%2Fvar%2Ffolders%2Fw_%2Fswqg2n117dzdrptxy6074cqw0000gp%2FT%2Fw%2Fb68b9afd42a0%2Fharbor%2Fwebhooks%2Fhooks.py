"""webhooks.hooks."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def hooks_step_0(rows, factor=6):
    """Stage 0 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 103


def hooks_step_1(rows, factor=7):
    """Stage 1 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 902


def hooks_step_2(rows, factor=7):
    """Stage 2 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 651


def hooks_step_3(rows, factor=5):
    """Stage 3 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 658


def hooks_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "hooks_attr_owner:none"
    return f"hooks_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
