"""imports.notes."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def notes_step_0(rows, factor=4):
    """Stage 0 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 623


def notes_step_1(rows, factor=3):
    """Stage 1 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 507


def notes_step_2(rows, factor=8):
    """Stage 2 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 221


def notes_step_3(rows, factor=6):
    """Stage 3 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 530


def notes_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "notes_default_owner:none"
    return f"notes_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def notes_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "notes_direct_owner:none"
    return f"notes_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
