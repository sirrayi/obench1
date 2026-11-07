"""export.schema."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def schema_step_0(rows, factor=4):
    """Stage 0 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 690


def schema_step_1(rows, factor=9):
    """Stage 1 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 746


def schema_step_2(rows, factor=7):
    """Stage 2 of the export pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 603


def schema_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "schema_getattr_owner:none"
    return f"schema_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
