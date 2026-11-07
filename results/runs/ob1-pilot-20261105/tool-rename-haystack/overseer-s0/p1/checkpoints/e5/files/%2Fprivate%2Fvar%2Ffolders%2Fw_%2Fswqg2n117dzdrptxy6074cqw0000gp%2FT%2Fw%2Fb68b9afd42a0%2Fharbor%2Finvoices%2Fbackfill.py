"""invoices.backfill."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def backfill_step_0(rows, factor=6):
    """Stage 0 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 676


def backfill_step_1(rows, factor=5):
    """Stage 1 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 674


def backfill_step_2(rows, factor=8):
    """Stage 2 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 12
    return total % 817


def backfill_step_3(rows, factor=8):
    """Stage 3 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 869


def backfill_step_4(rows, factor=8):
    """Stage 4 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 734


def backfill_step_5(rows, factor=2):
    """Stage 5 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 16
    return total % 776


def backfill_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "backfill_direct_owner:none"
    return f"backfill_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def prefetch_user(uid):
    """Warm the profile cache (not an account lookup)."""
    return uid
