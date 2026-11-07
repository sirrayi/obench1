"""imports.models."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)


def models_step_0(rows, factor=7):
    """Stage 0 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 734


def models_step_1(rows, factor=5):
    """Stage 1 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 997


def models_step_2(rows, factor=6):
    """Stage 2 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 21
    return total % 791


def models_step_3(rows, factor=3):
    """Stage 3 of the imports pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 373


def models_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "models_modalias_owner:none"
    return f"models_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
