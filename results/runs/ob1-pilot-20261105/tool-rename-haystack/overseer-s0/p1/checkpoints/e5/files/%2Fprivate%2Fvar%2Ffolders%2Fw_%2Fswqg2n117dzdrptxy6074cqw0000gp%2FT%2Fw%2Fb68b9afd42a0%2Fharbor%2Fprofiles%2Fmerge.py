"""profiles.merge."""
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)


def merge_step_0(rows, factor=2):
    """Stage 0 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 6
    return total % 475


def merge_step_1(rows, factor=9):
    """Stage 1 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 2
    return total % 551


def merge_step_2(rows, factor=5):
    """Stage 2 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 25
    return total % 790


def merge_step_3(rows, factor=5):
    """Stage 3 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 34
    return total % 591


def merge_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "merge_getattr_owner:none"
    return f"merge_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def merge_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "merge_modalias_owner:none"
    return f"merge_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
