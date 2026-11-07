"""ledger.schema."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def schema_step_0(rows, factor=7):
    """Stage 0 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 50
    return total % 558


def schema_step_1(rows, factor=3):
    """Stage 1 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 22
    return total % 873


def schema_step_2(rows, factor=2):
    """Stage 2 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 317


def schema_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "schema_getattr_owner:none"
    return f"schema_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
