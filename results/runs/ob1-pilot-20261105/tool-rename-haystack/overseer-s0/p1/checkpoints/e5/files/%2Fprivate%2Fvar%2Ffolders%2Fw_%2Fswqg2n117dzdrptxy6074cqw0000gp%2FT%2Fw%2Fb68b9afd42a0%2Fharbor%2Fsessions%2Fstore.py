"""sessions.store."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def store_step_0(rows, factor=2):
    """Stage 0 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 635


def store_step_1(rows, factor=5):
    """Stage 1 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 40
    return total % 189


def store_step_2(rows, factor=7):
    """Stage 2 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 460


def store_step_3(rows, factor=3):
    """Stage 3 of the sessions pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 560


def store_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "store_attr_owner:none"
    return f"store_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
