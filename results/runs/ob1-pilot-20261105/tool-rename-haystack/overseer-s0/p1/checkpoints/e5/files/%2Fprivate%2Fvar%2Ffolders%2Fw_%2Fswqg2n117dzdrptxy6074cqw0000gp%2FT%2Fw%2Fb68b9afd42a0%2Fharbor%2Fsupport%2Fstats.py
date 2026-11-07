"""support.stats."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def stats_step_0(rows, factor=5):
    """Stage 0 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 531


def stats_step_1(rows, factor=5):
    """Stage 1 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 970


def stats_step_2(rows, factor=8):
    """Stage 2 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 609


def stats_step_3(rows, factor=6):
    """Stage 3 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 196


def stats_step_4(rows, factor=8):
    """Stage 4 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 488


def stats_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "stats_default_owner:none"
    return f"stats_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
