#!/usr/bin/env python
from flask import Flask, render_template
from datetime import timedelta
import os

from api import api_bp
import config
import db

if os.path.isfile(config.DATABASE_NAME):
    os.remove(config.DATABASE_NAME)

if not os.path.isfile(config.DATABASE_NAME):
    db.init()

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.register_blueprint(api_bp, url_prefix="/api/v1")
app.permanent_session_lifetime = timedelta(days=3)


@app.route("/transaction", methods=["GET"])
def transaction():
    return render_template("transaction.html")


if __name__ == "__main__":
    app.run(debug=True)
