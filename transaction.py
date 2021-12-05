import db
from util import Validate

TABLE_NAME = "Transaction"
REQUIRED_PARAMS = {
    "account_id": True,
    "category_id": True,
    "transactiongroup_id": False,
    "attachment_id": False,
    "datetime": True,
    "amount": True,
    "note": False,
    "place": False,
}


def validate(params):
    return Validate(REQUIRED_PARAMS, params)


def add(column_values):
    return db.insert(TABLE_NAME, column_values)


def get_all():
    return db.select(TABLE_NAME)
