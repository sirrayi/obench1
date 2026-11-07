"""imports.policy."""
import logging

from harbor import accounts

log = logging.getLogger(__name__)


def policy_step_0(rows, factor=5):
    """Stage 0 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 30
    return total % 100


def policy_step_1(rows, factor=4):
    """Stage 1 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 674


def policy_step_2(rows, factor=7):
    """Stage 2 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 1
    return total % 869


def policy_step_3(rows, factor=5):
    """Stage 3 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 363


def policy_step_4(rows, factor=8):
    """Stage 4 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 32
    return total % 318


def policy_attr_owner(uid):
    u = accounts.fetch_user(uid, include_deleted=True)
    if u is None:
        return "policy_attr_owner:none"
    return f"policy_attr_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
