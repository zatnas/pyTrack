import db

TABLE_NAME = "CategoryGroup"


def add(
    name,
    color,
    icon,
):
    column_values = {
        "name": name,
        "color": color,
        "icon": icon,
    }
    return db.insert(TABLE_NAME, column_values)


def get_all():
    return db.select(TABLE_NAME)
