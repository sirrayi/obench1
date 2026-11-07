"""mail.worker."""
import logging

from harbor.accounts import fetch_user

log = logging.getLogger(__name__)


def worker_step_0(rows, factor=6):
    """Stage 0 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 623


def worker_step_1(rows, factor=6):
    """Stage 1 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 708


def worker_step_2(rows, factor=9):
    """Stage 2 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 603


def worker_step_3(rows, factor=9):
    """Stage 3 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 27
    return total % 238


def worker_step_4(rows, factor=8):
    """Stage 4 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 363


def worker_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "worker_direct_owner:none"
    return f"worker_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
