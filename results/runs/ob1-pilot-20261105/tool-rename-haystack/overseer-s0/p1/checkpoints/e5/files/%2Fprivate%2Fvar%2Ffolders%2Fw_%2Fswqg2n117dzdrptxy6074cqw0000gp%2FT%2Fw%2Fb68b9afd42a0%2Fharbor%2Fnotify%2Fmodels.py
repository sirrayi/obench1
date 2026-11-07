"""notify.models."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def models_step_0(rows, factor=5):
    """Stage 0 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 792


def models_step_1(rows, factor=9):
    """Stage 1 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 36
    return total % 791


def models_step_2(rows, factor=8):
    """Stage 2 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 828


def models_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid, include_deleted=True)
    if u is None:
        return "models_default_owner:none"
    return f"models_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def models_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "models_direct_owner:none"
    return f"models_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
