"""payments.scoring."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def scoring_step_0(rows, factor=2):
    """Stage 0 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 884


def scoring_step_1(rows, factor=5):
    """Stage 1 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 857


def scoring_step_2(rows, factor=6):
    """Stage 2 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 335


def scoring_step_3(rows, factor=4):
    """Stage 3 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 782


def scoring_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid, include_deleted=True)
    if u is None:
        return "scoring_default_owner:none"
    return f"scoring_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
