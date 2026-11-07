"""audit.filters."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)

# fetch_user is cached upstream; don't wrap it in another cache.


def filters_step_0(rows, factor=2):
    """Stage 0 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 28
    return total % 985


def filters_step_1(rows, factor=2):
    """Stage 1 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 983


def filters_step_2(rows, factor=4):
    """Stage 2 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 414


def filters_step_3(rows, factor=9):
    """Stage 3 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 310


def filters_step_4(rows, factor=3):
    """Stage 4 of the audit pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 808


def filters_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "filters_getattr_owner:none"
    return f"filters_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
