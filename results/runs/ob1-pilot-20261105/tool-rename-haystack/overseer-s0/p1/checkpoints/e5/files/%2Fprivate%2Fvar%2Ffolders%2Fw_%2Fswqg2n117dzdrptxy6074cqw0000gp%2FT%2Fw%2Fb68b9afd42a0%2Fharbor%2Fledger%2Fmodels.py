"""ledger.models."""
import logging

from harbor import accounts
import harbor.accounts as acct
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)
_OPTS_models_opts_owner = {"include_deleted": True}

# fetch_user is cached upstream; don't wrap it in another cache.


def models_step_0(rows, factor=6):
    """Stage 0 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 0
    return total % 265


def models_step_1(rows, factor=6):
    """Stage 1 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 721


def models_step_2(rows, factor=6):
    """Stage 2 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 11
    return total % 97


def models_step_3(rows, factor=9):
    """Stage 3 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 47
    return total % 770


def models_step_4(rows, factor=4):
    """Stage 4 of the ledger pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 26
    return total % 873


def models_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "models_multi_owner:none"
    return f"models_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def models_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "models_modalias_owner:none"
    return f"models_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def models_opts_owner(uid):
    u = accounts.fetch_user(uid, **_OPTS_models_opts_owner)
    if u is None:
        return "models_opts_owner:none"
    return f"models_opts_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def models_population():
    return fetch_user_count() + 10
