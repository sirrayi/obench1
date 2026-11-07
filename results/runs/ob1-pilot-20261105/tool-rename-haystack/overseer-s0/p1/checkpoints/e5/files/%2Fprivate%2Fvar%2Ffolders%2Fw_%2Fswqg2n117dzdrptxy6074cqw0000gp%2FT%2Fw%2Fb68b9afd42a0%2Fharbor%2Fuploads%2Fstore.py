"""uploads.store."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def store_step_0(rows, factor=9):
    """Stage 0 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 46
    return total % 520


def store_step_1(rows, factor=7):
    """Stage 1 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 131


def store_step_2(rows, factor=4):
    """Stage 2 of the uploads pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 19
    return total % 750


def store_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid, include_deleted=True)
    if u is None:
        return "store_getattr_owner:none"
    return f"store_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
