import db

TABLE_NAME = "Tag"


def add(
    name,
    color,
):
    column_values = {
        "name": name,
        "color": color,
    }
    return db.insert(TABLE_NAME, column_values)


def get_all():
    return db.select(TABLE_NAME)
