import db
from util import Validate

TABLE_NAME = "Account"
REQUIRED_PARAMS = {
    "name": True,
    "color": True,
}


def validate(params):
    return Validate(REQUIRED_PARAMS, params)


def add(column_values):
    return db.insert(TABLE_NAME, column_values)


def get_all():
    return db.select(TABLE_NAME)
