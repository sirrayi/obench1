"""insights.notes."""
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def notes_step_0(rows, factor=6):
    """Stage 0 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 228


def notes_step_1(rows, factor=4):
    """Stage 1 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 473


def notes_step_2(rows, factor=6):
    """Stage 2 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 445


def notes_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "notes_multi_owner:none"
    return f"notes_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def notes_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "notes_attr_owner:none"
    return f"notes_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def notes_population():
    return fetch_user_count() + 66
