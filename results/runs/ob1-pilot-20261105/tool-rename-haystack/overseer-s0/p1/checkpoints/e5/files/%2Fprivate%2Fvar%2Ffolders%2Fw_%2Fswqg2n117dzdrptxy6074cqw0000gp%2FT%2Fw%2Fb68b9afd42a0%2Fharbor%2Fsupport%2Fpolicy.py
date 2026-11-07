"""support.policy."""
import functools
import logging

from harbor import accounts
from harbor.accounts import (
    fetch_user,
    fetch_user_count,
)

log = logging.getLogger(__name__)
_load_policy_partial_owner = functools.partial(accounts.fetch_user, include_deleted=True)


def policy_step_0(rows, factor=8):
    """Stage 0 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 38
    return total % 869


def policy_step_1(rows, factor=8):
    """Stage 1 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 372


def policy_step_2(rows, factor=6):
    """Stage 2 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 3
    return total % 610


def policy_step_3(rows, factor=9):
    """Stage 3 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 31
    return total % 970


def policy_step_4(rows, factor=8):
    """Stage 4 of the support pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 35
    return total % 782


def policy_partial_owner(uid):
    u = _load_policy_partial_owner(uid)
    if u is None:
        return "policy_partial_owner:none"
    return f"policy_partial_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def policy_multi_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "policy_multi_owner:none"
    return f"policy_multi_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def policy_population():
    return fetch_user_count() + 15
