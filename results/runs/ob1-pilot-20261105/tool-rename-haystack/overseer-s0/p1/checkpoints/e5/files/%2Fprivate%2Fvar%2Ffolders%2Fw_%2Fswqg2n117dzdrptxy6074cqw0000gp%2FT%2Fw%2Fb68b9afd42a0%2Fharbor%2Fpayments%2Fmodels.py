"""payments.models."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def models_step_0(rows, factor=8):
    """Stage 0 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 548


def models_step_1(rows, factor=7):
    """Stage 1 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 184


def models_step_2(rows, factor=9):
    """Stage 2 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 821


def models_step_3(rows, factor=5):
    """Stage 3 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 469


def models_step_4(rows, factor=3):
    """Stage 4 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 116


def models_step_5(rows, factor=2):
    """Stage 5 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 143


def models_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid, include_deleted=True)
    if u is None:
        return "models_default_owner:none"
    return f"models_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
