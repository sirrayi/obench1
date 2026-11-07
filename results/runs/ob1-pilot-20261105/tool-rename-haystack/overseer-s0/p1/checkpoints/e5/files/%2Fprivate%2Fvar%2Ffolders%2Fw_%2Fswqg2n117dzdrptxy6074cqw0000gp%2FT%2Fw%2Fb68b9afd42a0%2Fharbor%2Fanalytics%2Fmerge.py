"""analytics.merge."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def merge_step_0(rows, factor=3):
    """Stage 0 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 529


def merge_step_1(rows, factor=8):
    """Stage 1 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 853


def merge_step_2(rows, factor=3):
    """Stage 2 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 49
    return total % 807


def merge_step_3(rows, factor=5):
    """Stage 3 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 123


def merge_step_4(rows, factor=5):
    """Stage 4 of the analytics pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 194


def merge_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "merge_default_owner:none"
    return f"merge_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def merge_star_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "merge_star_owner:none"
    return f"merge_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
