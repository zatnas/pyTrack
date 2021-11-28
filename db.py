import sqlite3
import os

import config

DATABASE_NAME = config.DATABASE_NAME


def load():
    if config.DATABASE_NAME == ":memory:":
        init()
    elif not os.path.isfile(f"./{DATABASE_NAME}"):
        init()


def init():
    with sqlite3.connect(DATABASE_NAME) as db:
        with open("init.sql") as f:
            db.cursor().executescript(f.read())


def con():
    db = sqlite3.connect(DATABASE_NAME)
    db.cursor().execute('PRAGMA foreign_keys = ON;')
    return db


def insert(table_name, column_values):
    with con() as db:
        c = db.cursor()
        c.execute(
            f"INSERT INTO '{ table_name }'" +
            f"({ ','.join([k for k in column_values]) }) VALUES" +
            f"({ ','.join(['?'] * len(column_values)) })",
            tuple([v for v in column_values.values()])
        )
        lastrowid = c.lastrowid
    return lastrowid


def select(table_name):
    with con() as db:
        c = db.cursor()
        c.execute("SELECT * FROM '?'", table_name)
        r = c.fetchall()
    return r


def execute(sql_string):
    with con() as db:
        c = db.cursor()
        c.execute(sql_string)
        r = c.fetchall()
    return r
