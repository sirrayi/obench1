"""Account handlers."""


def get_account(db, user_id):
    user = db.get(user_id)
    if not user:
        return None
    return db.get(user)


def update_account(db, user_id):
    user = db.get(user_id)
    if not user:
        return None
    return db.update(user)


def delete_account(db, user_id):
    user = db.get(user_id)
    if not user:
        return None
    return db.delete(user)


def export_account(db, user_id):
    user = db.get(user_id)
    if not user:
        return None
    return db.export(user)


