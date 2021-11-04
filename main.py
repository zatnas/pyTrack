from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from datetime import timedelta
import sqlite3
import os

DATABASE_NAME = "track.db"

def load_database():
    if not os.path.isfile(f"./{DATABASE_NAME}"):
        init_database()

def init_database():
    db = sqlite3.connect(DATABASE_NAME)
    db.cursor().execute("""
                        CREATE TABLE 'transaction' (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        datetime INTEGER NOT NULL,
                        amount REAL NOT NULL
                        )""")
    db.commit()
    db.close()

def database_execute(a=None,b=None):
    db = sqlite3.connect(DATABASE_NAME)
    r = db.cursor().execute(a,b)
    db.commit()
    db.close()
    return r

if os.path.isfile(DATABASE_NAME):
    os.remove(DATABASE_NAME)

if not os.path.isfile(DATABASE_NAME):
    init_database()

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=3)

@app.route("/transaction", methods=["GET"])
def transaction():
    return render_template("transaction.html")

@app.route("/api/v1/transaction", methods=["GET","POST"])
def api_transaction():
    if request.method == "GET":
        db = sqlite3.connect(DATABASE_NAME)
        c = db.cursor()
        c.execute("SELECT * FROM 'transaction'")
        transaction_history = c.fetchall()
        db.close()
        return jsonify(transaction_history)
    elif request.method == "POST":
        datetime = request.form["datetime"]
        amount = request.form["amount"]
        db = sqlite3.connect(DATABASE_NAME)
        db.cursor().execute("INSERT INTO 'transaction' (datetime, amount) VALUES (?, ?)", (datetime, amount))
        db.commit()
        db.close()
        return jsonify({})
    return f"Unsupported method:{request.method}"

if __name__ == "__main__":
    app.run( debug=True )
