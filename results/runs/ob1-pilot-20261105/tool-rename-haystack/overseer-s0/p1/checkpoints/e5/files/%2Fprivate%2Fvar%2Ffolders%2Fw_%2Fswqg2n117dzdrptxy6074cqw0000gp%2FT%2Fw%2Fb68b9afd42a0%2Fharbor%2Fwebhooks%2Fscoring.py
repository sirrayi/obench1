"""webhooks.scoring."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def scoring_step_0(rows, factor=3):
    """Stage 0 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 971


def scoring_step_1(rows, factor=2):
    """Stage 1 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 722


def scoring_step_2(rows, factor=7):
    """Stage 2 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 908


def scoring_step_3(rows, factor=7):
    """Stage 3 of the webhooks pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 523


def scoring_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "scoring_default_owner:none"
    return f"scoring_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
