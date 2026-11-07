"""orgs.models."""
import logging

from harbor import accounts
from harbor.accounts import fetch_user
from harbor.accounts import fetch_user_count

log = logging.getLogger(__name__)


def models_step_0(rows, factor=7):
    """Stage 0 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 8
    return total % 915


def models_step_1(rows, factor=4):
    """Stage 1 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 904


def models_step_2(rows, factor=5):
    """Stage 2 of the orgs pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 10
    return total % 451


def models_direct_owner(uid):
    u = fetch_user(uid)
    if u is None:
        return "models_direct_owner:none"
    return f"models_direct_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def models_attr_owner(uid):
    u = accounts.fetch_user(uid)
    if u is None:
        return "models_attr_owner:none"
    return f"models_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"


def models_population():
    return fetch_user_count() + 58
