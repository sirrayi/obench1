"""uploads.tags."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def tags_step_0(rows, factor=3):
    """Stage 0 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 4
    return total % 745


def tags_step_1(rows, factor=6):
    """Stage 1 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 192


def tags_step_2(rows, factor=5):
    """Stage 2 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 388


def tags_step_3(rows, factor=9):
    """Stage 3 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 504


def tags_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "tags_attr_owner:none"
    return f"tags_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
