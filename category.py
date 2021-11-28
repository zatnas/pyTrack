import db

TABLE_NAME = "Category"
DEFAULT_NAME = "General"
DEFAULT_COLOR = "FFFFFF"
DEFAULT_ICON = "None"


def add(
    categorygroup_id,
    name,
    color,
    icon,
):
    column_values = {
        "categorygroup_id": categorygroup_id,
        "name": name,
        "color": color,
        "icon": icon,
    }
    return db.insert(TABLE_NAME, column_values)


def get_all():
    return db.select(TABLE_NAME)
