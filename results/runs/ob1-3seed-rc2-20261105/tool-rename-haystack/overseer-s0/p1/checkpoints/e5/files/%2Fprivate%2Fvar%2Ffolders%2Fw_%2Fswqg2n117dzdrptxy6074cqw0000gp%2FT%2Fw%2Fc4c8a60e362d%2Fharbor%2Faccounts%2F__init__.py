"""Accounts: the account store."""

__all__ = ["fetch_user", "fetch_user_count", "account_tiers"]

TIERS = ("free", "pro", "team")


def fetch_user(user_id, *, include_deleted=False):
    """The account for user_id, or None if it was deleted (unless deleted ones are asked for)."""
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError(f"bad user id: {user_id!r}")
    deleted = user_id % 7 == 0
    if deleted and not include_deleted:
        return None
    return {"id": user_id, "name": f"user{user_id}", "tier": TIERS[user_id % 3], "deleted": deleted}


def fetch_user_count():
    """How many accounts exist."""
    return 4242


def account_tiers():
    return list(TIERS)
