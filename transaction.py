import db

TABLE_NAME = "Transaction"


def add(
    account_id,
    category_id,
    transactiongroup_id,
    attachment_id,
    datetime,
    amount,
    note,
    place,
):
    column_values = {
        "account_id": account_id,
        "category_id": category_id,
        "datetime": datetime,
        "amount": amount,
    }
    if transactiongroup_id is not None:
        column_values["transactiongroup_id"] = transactiongroup_id
    if attachment_id is not None:
        column_values["attachment_id"] = attachment_id
    if note is not None:
        column_values["note"] = note
    if place is not None:
        column_values["place"] = place
    return db.insert(TABLE_NAME, column_values)


def quick_add(
    account_id,
    category_id,
    datetime,
    amount,
):
    column_values = {
        "account_id": account_id,
        "category_id": category_id,
        "datetime": datetime,
        "amount": amount,
    }
    return db.insert(TABLE_NAME, column_values)


def get_all():
    return db.select(TABLE_NAME)
