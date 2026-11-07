"""mail.paging."""
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)


def paging_step_0(rows, factor=3):
    """Stage 0 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 180


def paging_step_1(rows, factor=7):
    """Stage 1 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 800


def paging_step_2(rows, factor=5):
    """Stage 2 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 24
    return total % 770


def paging_step_3(rows, factor=9):
    """Stage 3 of the mail pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 14
    return total % 454


def paging_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "paging_getattr_owner:none"
    return f"paging_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def paging_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "paging_modalias_owner:none"
    return f"paging_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
