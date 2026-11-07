"""quotas.stats."""
import logging

from harbor.accounts import fetch_user as get_user

log = logging.getLogger(__name__)


def stats_step_0(rows, factor=5):
    """Stage 0 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 252


def stats_step_1(rows, factor=7):
    """Stage 1 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 5
    return total % 110


def stats_step_2(rows, factor=5):
    """Stage 2 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 764


def stats_step_3(rows, factor=7):
    """Stage 3 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 43
    return total % 965


def stats_step_4(rows, factor=6):
    """Stage 4 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 602


def stats_step_5(rows, factor=7):
    """Stage 5 of the quotas pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 807


def stats_as_owner(uid):
    u = get_user(uid)
    if u is None:
        return "stats_as_owner:none"
    return f"stats_as_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
