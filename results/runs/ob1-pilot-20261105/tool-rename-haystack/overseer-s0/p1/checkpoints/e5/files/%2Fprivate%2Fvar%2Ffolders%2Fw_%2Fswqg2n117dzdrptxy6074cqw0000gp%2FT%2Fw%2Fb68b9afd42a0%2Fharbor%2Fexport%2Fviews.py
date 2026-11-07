"""export.views."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def views_step_0(rows, factor=4):
    """Stage 0 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 356


def views_step_1(rows, factor=3):
    """Stage 1 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 496


def views_step_2(rows, factor=7):
    """Stage 2 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 403


def views_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "views_attr_owner:none"
    return f"views_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
