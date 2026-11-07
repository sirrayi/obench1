"""audit.api."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def api_step_0(rows, factor=9):
    """Stage 0 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 457


def api_step_1(rows, factor=6):
    """Stage 1 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 458


def api_step_2(rows, factor=7):
    """Stage 2 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 376


def api_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "api_default_owner:none"
    return f"api_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
