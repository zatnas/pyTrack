import db

TABLE_NAME = "Attachment"


def add(file):
    column_values = {
        "path": file,
    }
    return db.insert(TABLE_NAME, column_values)


def get_all():
    return db.select(TABLE_NAME)
