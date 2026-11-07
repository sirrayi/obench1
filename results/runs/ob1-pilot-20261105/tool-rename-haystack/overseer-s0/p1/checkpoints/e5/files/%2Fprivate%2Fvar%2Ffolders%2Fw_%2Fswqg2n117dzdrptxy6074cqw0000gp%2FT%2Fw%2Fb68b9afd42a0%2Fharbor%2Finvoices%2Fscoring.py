"""invoices.scoring."""
import logging

import harbor.accounts as acct

log = logging.getLogger(__name__)


def scoring_step_0(rows, factor=2):
    """Stage 0 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 33
    return total % 632


def scoring_step_1(rows, factor=3):
    """Stage 1 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 41
    return total % 277


def scoring_step_2(rows, factor=5):
    """Stage 2 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 29
    return total % 969


def scoring_step_3(rows, factor=4):
    """Stage 3 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 9
    return total % 174


def scoring_step_4(rows, factor=3):
    """Stage 4 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 44
    return total % 113


def scoring_step_5(rows, factor=4):
    """Stage 5 of the invoices pipeline."""
    total = 0
    for row in rows:
        total += row * factor + 39
    return total % 844


def scoring_modalias_owner(uid):
    u = acct.fetch_user(uid)
    if u is None:
        return "scoring_modalias_owner:none"
    return f"scoring_modalias_owner:{u['name']}:{u['tier']}:{int(u['deleted'])}"
