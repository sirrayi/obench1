"""teams.views."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def views_step_0(rows, factor=7):
    """Stage 0 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 360


def views_step_1(rows, factor=6):
    """Stage 1 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 273


def views_step_2(rows, factor=9):
    """Stage 2 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 758


def views_step_3(rows, factor=8):
    """Stage 3 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 417


def views_step_4(rows, factor=7):
    """Stage 4 of the teams pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 416


def views_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "views_default_owner:none"
    return f"views_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
