import db

TABLE_NAME = "Account"


def add(
    name,
    color
):
    return db.insert(TABLE_NAME, {
        "name": name,
        "color": color,
    })


def get_all():
    return db.select(TABLE_NAME)
