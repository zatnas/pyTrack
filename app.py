"""
.
"""
from dataclasses import dataclass
from datetime import timedelta, timezone, datetime
import csv
import re
import logging
from io import StringIO
from flask import abort, jsonify
from flask import Flask
from flask import Response, request
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg://admin:admin@postgresql:5432/expense_tracker"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(
    app,
    model_class=Base,
    engine_options={
        "connect_args": {
            "connect_timeout": 60
        }
    }
)


@dataclass
class Account(db.Model):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    currency: Mapped[str] = mapped_column(
            nullable=True
    )
    total_amount: Mapped[float]
    name: Mapped[str]


@dataclass
class Category(db.Model):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"),
        nullable=True
    )
    name: Mapped[str]


@dataclass
class Transaction(db.Model):
    __tablename__ = "transaction"
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float]
    details: Mapped[str]
    datetime: Mapped[int]
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))


with app.app_context():
    db.create_all()
    accounts = [
        "My Account",
        "Account 1",
        "Account 2",
    ]
    for a in accounts:
        db.session.add(Account(name=a, total_amount=0))
    db.session.add(Category(name="Unknown"))
    db.session.commit()


@app.route("/category", methods=["GET"])
def category_read():
    return jsonify(
        db.session.execute(
            db.select(Category)
        ).scalars().all()
    )


@app.route("/category/new", methods=["POST"])
def category_create():
    if not request.form["name"]:
        abort(400)
    category = Category(name=request.form["name"])
    db.session.add(category)
    db.session.commit()
    return Response(status=204)


@app.route("/account", methods=["GET"])
def account_read_all():
    accounts = db.session.execute(
        db.select(Account)
    ).scalars().all()
    return jsonify(accounts)


@app.route("/account/<int:account_id>", methods=["GET"])
def account_read_one(account_id: int):
    account = db.session.execute(
        db.select(Account)
        .where(Account.id == account_id)
    ).scalars().one()
    return jsonify(account)


@app.route("/account/new", methods=["POST"])
def account_create():
    if not request.form["name"]:
        abort(400)
    account = Account(name=request.form["name"])
    db.session.add(account)
    db.session.commit()
    return Response(status=204)


@app.route("/account/<int:account_id>/transaction", methods=["GET"])
def transaction_read(account_id: int):
    transactions = db.session.execute(
        db.select(Transaction)
        .where(Transaction.account_id == account_id)
    ).scalars().all()
    return jsonify(transactions)


@app.route("/account/<int:account_id>/transaction/new", methods=["POST"])
def transaction_create(account_id: int):
    if not request.form["amount"]:
        abort(400)
    if not request.form["datetime"]:
        abort(400)
    transaction = Transaction(
        account_id=account_id,
        amount=request.form["amount"],
        datetime=request.form["datetime"],
    )
    insert_transaction([transaction])
    return Response(status=204)


@app.route("/account/<int:account_id>/import/<string:bank_name>", methods=["POST"])
def transaction_import(account_id: int, bank_name: str):
    if not bank_name:
        print("missing bank_name")
        abort(400)
    if not 'file' in request.files:
        print("missing file")
        abort(400)
    file = request.files['file']
    bank_name = bank_name.lower()
    if bank_name == "cimb":
        cimb_csv_io = StringIO(file.read().decode("utf-8"))
        transaction_list = cimb_import_parser(account_id, cimb_csv_io)
        insert_transaction(transaction_list)
        return jsonify({
            "result": "success",
            "msg": "transactions have been imported"
        })

    return Response(status=500)


def insert_transaction(transaction_list: list[Transaction]):
    account_total_added = {}
    for transaction in transaction_list:
        if not transaction.account_id in account_total_added:
            account_total_added[transaction.account_id] = 0
        account_total_added[transaction.account_id] += transaction.amount
        db.session.add(transaction)
    for account_id, total_added in account_total_added.items():
        account = Account.query.get(account_id)
        account.total_amount += total_added
    db.session.commit()


def cimb_import_parser(account_id, csvfile):
    cimb_csv = csv.DictReader(csvfile, delimiter=',')
    transaction_list = []
    for row in cimb_csv:
        date_time = datetime.strptime(row['Date'], "%d-%b-%Y")
        date_time_localized = date_time.replace(
            tzinfo=timezone(timedelta(hours=8))
        )
        date_time_utc = date_time.astimezone(tz=timezone.utc)
        epoch = date_time_utc.timestamp()
        details = row['Transaction Details'].strip().replace('|', '\n')
        if row['Money In']:
            currency, amount = re.fullmatch(
                r"(?P<currency>\w+)\s+(?P<amount>[0-9.]+)",
                row['Money In']
            ).groups()
            amount = float(amount)
        elif row['Money Out']:
            currency, amount = re.fullmatch(
                r"(?P<currency>\w+)\s+(?P<amount>[0-9.]+)",
                row['Money Out']
            ).groups()
            amount = -float(amount)
        else:
            logging.debug(row)
            logging.error("No money in or out")
            raise Exception("No money in or out")
        transaction_list.append(
            Transaction(
                account_id=account_id,
                category_id=1,
                amount=amount,
                details=details,
                datetime=epoch,
            )
        )
    return transaction_list


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
    )
