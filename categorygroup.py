import db
from util import Validate

TABLE_NAME = "CategoryGroup"
REQUIRED_PARAMS = {
    "name": True,
    "color": True,
    "icon": True,
}


def validate(params):
    return Validate(REQUIRED_PARAMS, params)


def add(column_values):
    return db.insert(TABLE_NAME, column_values)


def get_all():
    return db.select(TABLE_NAME)
