import db

TABLE_NAME = "TransactionGroup"


def add(
    attachment_id,
    datetime,
    note,
    place,
):
    column_values = {
        "attachment_id": attachment_id,
        "datetime": datetime,
        "note": note,
        "place": place,
    }
    return db.insert(TABLE_NAME, column_values)


def get_all():
    return db.select(TABLE_NAME)
