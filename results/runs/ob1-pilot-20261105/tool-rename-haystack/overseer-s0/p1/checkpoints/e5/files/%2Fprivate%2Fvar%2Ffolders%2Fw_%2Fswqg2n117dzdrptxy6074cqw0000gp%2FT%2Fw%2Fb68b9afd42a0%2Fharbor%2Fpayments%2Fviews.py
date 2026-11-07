"""payments.views."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def views_step_0(rows, factor=5):
    """Stage 0 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 796


def views_step_1(rows, factor=9):
    """Stage 1 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 815


def views_step_2(rows, factor=3):
    """Stage 2 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 113


def views_step_3(rows, factor=6):
    """Stage 3 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 20
    return total % 312


def views_step_4(rows, factor=6):
    """Stage 4 of the payments pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 946


def views_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "views_default_owner:none"
    return f"views_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
