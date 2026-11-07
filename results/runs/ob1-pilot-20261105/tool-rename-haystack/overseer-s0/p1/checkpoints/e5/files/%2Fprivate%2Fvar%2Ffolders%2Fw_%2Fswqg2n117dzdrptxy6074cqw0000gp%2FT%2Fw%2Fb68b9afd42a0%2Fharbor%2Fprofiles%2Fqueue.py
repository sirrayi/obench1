"""profiles.queue."""
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)
_OPTS_queue_opts_owner = {"include_deleted": True}


def queue_step_0(rows, factor=4):
    """Stage 0 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 339


def queue_step_1(rows, factor=6):
    """Stage 1 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 17
    return total % 157


def queue_step_2(rows, factor=7):
    """Stage 2 of the profiles pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 779


def queue_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "queue_getattr_owner:none"
    return f"queue_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def queue_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "queue_modalias_owner:none"
    return f"queue_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def queue_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_queue_opts_owner)
    if u is None:
        log.warning("fetch_user returned nothing for %s", uid)
        return "queue_opts_owner:none"
    return f"queue_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
