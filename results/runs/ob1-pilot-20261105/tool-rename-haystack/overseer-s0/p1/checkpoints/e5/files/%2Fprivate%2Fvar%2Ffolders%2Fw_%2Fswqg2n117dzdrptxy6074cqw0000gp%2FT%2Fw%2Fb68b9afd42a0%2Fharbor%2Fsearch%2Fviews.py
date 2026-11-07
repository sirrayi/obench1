"""search.views."""
import logging

from harbor import accounts
import harbor.accounts as acct
from harbor.accounts import *  # noqa: F401,F403

log = logging.getLogger(__name__)


def views_step_0(rows, factor=3):
    """Stage 0 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 642


def views_step_1(rows, factor=2):
    """Stage 1 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 922


def views_step_2(rows, factor=3):
    """Stage 2 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 121


def views_step_3(rows, factor=8):
    """Stage 3 of the search pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 529


def views_star_owner(uid):
    u = fetch_user(uid, include_deleted=True)
    if u is None:
        return "views_star_owner:none"
    return f"views_star_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def views_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "views_modalias_owner:none"
    return f"views_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def views_default_owner(uid, loader=accounts.fetch_user):
    u = loader(uid)
    if u is None:
        return "views_default_owner:none"
    return f"views_default_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
