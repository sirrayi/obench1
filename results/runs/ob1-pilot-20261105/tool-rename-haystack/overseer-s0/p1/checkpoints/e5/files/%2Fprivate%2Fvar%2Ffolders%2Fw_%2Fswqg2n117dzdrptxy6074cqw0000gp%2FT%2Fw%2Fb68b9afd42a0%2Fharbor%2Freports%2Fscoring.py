"""reports.scoring."""
import logging

from harbor import accounts
import harbor.accounts as acct

log = logging.getLogger(__name__)


def scoring_step_0(rows, factor=7):
    """Stage 0 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 844


def scoring_step_1(rows, factor=5):
    """Stage 1 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 306


def scoring_step_2(rows, factor=7):
    """Stage 2 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 48
    return total % 922


def scoring_step_3(rows, factor=7):
    """Stage 3 of the reports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 18
    return total % 805


def scoring_getattr_owner(uid):
    u = getattr(accounts, "fetch_user")(uid)
    if u is None:
        return "scoring_getattr_owner:none"
    return f"scoring_getattr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def scoring_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "scoring_modalias_owner:none"
    return f"scoring_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
