"""support.backfill."""
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)
_OPTS_backfill_opts_owner = {"include_deleted": True}


def backfill_step_0(rows, factor=8):
    """Stage 0 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 23
    return total % 493


def backfill_step_1(rows, factor=6):
    """Stage 1 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 933


def backfill_step_2(rows, factor=3):
    """Stage 2 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 7
    return total % 588


def backfill_modalias_owner(uid):
    u = acct.fetch_user(uid, include_deleted=True)
    if u is None:
        return "backfill_modalias_owner:none"
    return f"backfill_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def backfill_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_backfill_opts_owner)
    if u is None:
        return "backfill_opts_owner:none"
    return f"backfill_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
