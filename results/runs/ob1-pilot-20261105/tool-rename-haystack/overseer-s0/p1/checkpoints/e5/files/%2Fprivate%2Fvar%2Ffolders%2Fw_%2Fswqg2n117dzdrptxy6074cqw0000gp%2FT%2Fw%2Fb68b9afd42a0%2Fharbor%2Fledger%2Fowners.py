"""ledger.owners."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def owners_step_0(rows, factor=7):
    """Stage 0 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 13
    return total % 117


def owners_step_1(rows, factor=7):
    """Stage 1 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 740


def owners_step_2(rows, factor=2):
    """Stage 2 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 15
    return total % 102


def owners_step_3(rows, factor=3):
    """Stage 3 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 42
    return total % 852


def owners_step_4(rows, factor=8):
    """Stage 4 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 797


def owners_step_5(rows, factor=3):
    """Stage 5 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 346


def owners_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid, include_deleted=True)
    if u is None:
        return "owners_getattr_owner:none"
    return f"owners_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
