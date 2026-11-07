"""profiles.tags."""
import logging

from harbor import accounts
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def tags_step_0(rows, factor=3):
    """Stage 0 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 802


def tags_step_1(rows, factor=7):
    """Stage 1 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 791


def tags_step_2(rows, factor=5):
    """Stage 2 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 786


def tags_step_3(rows, factor=9):
    """Stage 3 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 713


def tags_step_4(rows, factor=8):
    """Stage 4 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 846


def tags_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "tags_getattr_owner:none"
    return f"tags_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def tags_star_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "tags_star_owner:none"
    return f"tags_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
