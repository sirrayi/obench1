"""sessions.notes."""
import logging

from harbor import accounts
import harbor.accounts as acct
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)


def notes_step_0(rows, factor=3):
    """Stage 0 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 686


def notes_step_1(rows, factor=7):
    """Stage 1 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 45
    return total % 489


def notes_step_2(rows, factor=2):
    """Stage 2 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 661


def notes_step_3(rows, factor=5):
    """Stage 3 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 469


def notes_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        return "notes_attr_owner:none"
    return f"notes_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def notes_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "notes_multi_owner:none"
    return f"notes_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def notes_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        return "notes_modalias_owner:none"
    return f"notes_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def notes_population():
    return fetch_user_count() + 10
