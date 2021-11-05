#!/usr/bin/env python
from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from datetime import timedelta
import sqlite3
import os

DATABASE_NAME = "track.db"
SECRET_KEY = "hello"

def load_database():
    if DATABASE_NAME == ":memory:":
        init_database()
    elif not os.path.isfile(f"./{DATABASE_NAME}"):
        init_database()

def init_database():
    with sqlite3.connect(DATABASE_NAME) as db:
        with open("init.sql") as db_f:
            db.cursor().executescript(db_f.read())

def db_con():
    return sqlite3.connect(DATABASE_NAME)

def db_insert(table_name, column_values):
    with db_con() as db:
        c = db.cursor()
        c.execute(
            f"INSERT INTO '{ table_name }'" +
            f"({ ','.join([k for k in column_values]) }) VALUES" +
            f"({ ','.join(['?'] * len(column_values)) })",
            tuple([v for v in column_values.values()])
        )
        lastrowid = c.lastrowid
    return lastrowid

def db_execute(sql_string):
    with db_con() as db:
        c = db.cursor()
        c.execute(sql_string)
        r = c.fetchall()
    return r

if os.path.isfile(DATABASE_NAME):
    os.remove(DATABASE_NAME)

if not os.path.isfile(DATABASE_NAME):
    init_database()

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(days=3)

@app.route("/transaction", methods=["GET"])
def transaction():
    return render_template("transaction.html")

@app.route("/api/v1/transaction", methods=["GET","POST"])
def api_transaction():
    if request.method == "GET":
        return jsonify(
            db_execute("SELECT * FROM 'Transaction'")
        )
    elif request.method == "POST":
        account_id = request.form["account_id"]
        category_id = request.form["category_id"]
        datetime = request.form["datetime"]
        amount = request.form["amount"]
        db_insert("Transaction", {
            "account_id": account_id,
            "category_id": category_id,
            "datetime": datetime,
            "amount": amount,
            })
        return jsonify({
            "status": "success"
        })
    return f"Unsupported method:{ request.method }"

@app.route("/api/v1/account", methods=["GET","POST"])
def api_account():
    if request.method == "GET":
        return jsonify(
            db_execute("SELECT * FROM 'Account'")
        )
    elif request.method == "POST":
        name = request.form["name"]
        color = request.form["color"]
        db_insert("Account", {
            "name": name,
            "color": color,
            })
        return jsonify({
            "status": "success"
        })
    return f"Unsupported method:{ request.method }"

@app.route("/api/v1/categorygroup", methods=["GET","POST"])
def api_categorygroup():
    if request.method == "GET":
        return jsonify(
            db_execute("SELECT * FROM 'CategoryGroup'")
        )
    elif request.method == "POST":
        name = request.form["name"]
        color = request.form["color"]
        icon = request.form["icon"]
        categorygroup_id = db_insert("CategoryGroup", {
            "name": name,
            "color": color,
            "icon": icon,
            })
        db_insert("Category", {
            "categorygroup_id": categorygroup_id,
            "name": name,
            "color": color,
            "icon": icon,
            })
        return jsonify({
            "status": "success"
        })
    return f"Unsupported method:{ request.method }"

@app.route("/api/v1/category", methods=["GET","POST"])
def api_category():
    if request.method == "GET":
        return jsonify(
            db_execute("SELECT * FROM 'Category'")
        )
    elif request.method == "POST":
        categorygroup_id = request.form["categorygroup_id"]
        name = request.form["name"]
        color = request.form["color"]
        icon = request.form["icon"]
        db_insert("Category", {
            "categorygroup_id": categorygroup_id,
            "name": name,
            "color": color,
            "icon": icon,
            })
        return jsonify({
            "status": "success"
        })
    return f"Unsupported method:{ request.method }"

if __name__ == "__main__":
    app.run(debug=True)
