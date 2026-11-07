"""webhooks.rules."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def rules_step_0(rows, factor=3):
    """Stage 0 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 456


def rules_step_1(rows, factor=5):
    """Stage 1 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 439


def rules_step_2(rows, factor=2):
    """Stage 2 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 870


def rules_step_3(rows, factor=3):
    """Stage 3 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 834


def rules_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "rules_default_owner:none"
    return f"rules_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
