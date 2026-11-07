"""notify.tags."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def tags_step_0(rows, factor=8):
    """Stage 0 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 789


def tags_step_1(rows, factor=5):
    """Stage 1 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 667


def tags_step_2(rows, factor=9):
    """Stage 2 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 299


def tags_step_3(rows, factor=9):
    """Stage 3 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 406


def tags_step_4(rows, factor=8):
    """Stage 4 of the notify pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 975


def tags_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "tags_getattr_owner:none"
    return f"tags_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
