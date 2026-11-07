"""insights.admin."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def admin_step_0(rows, factor=4):
    """Stage 0 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 397


def admin_step_1(rows, factor=5):
    """Stage 1 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 640


def admin_step_2(rows, factor=5):
    """Stage 2 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 238


def admin_step_3(rows, factor=3):
    """Stage 3 of the insights pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 628


def admin_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "admin_default_owner:none"
    return f"admin_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
