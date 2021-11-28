from flask import Blueprint, request, jsonify
import db

import account
import attachment
import category
import categorygroup
import tag
import transaction
import transactiongroup

api_bp = Blueprint('api_bp', __name__)


@api_bp.route("/transactiongroup", methods=["POST"])
def api_transactiongroup():
    if request.method == "POST":
        pass
    return f"Unsupported method:{ request.method }"


@api_bp.route("/transaction", methods=["GET", "POST"])
def api_transaction():
    if request.method == "GET":
        return jsonify(transaction.get_all())
    elif request.method == "POST":
        account_id = request.form["account_id"]
        category_id = request.form["category_id"]
        datetime = request.form["datetime"]
        amount = request.form["amount"]
        transaction.quick_add(
            account_id,
            category_id,
            datetime,
            amount
        )
        return jsonify({
            "status": "success"
        })
    return f"Unsupported method:{ request.method }"


@api_bp.route("/account", methods=["GET", "POST"])
def api_account():
    if request.method == "GET":
        return jsonify(account.get_all())
    elif request.method == "POST":
        name = request.form["name"]
        color = request.form["color"]
        account.add(
            name,
            color
        )
        return jsonify({
            "status": "success"
        })
    return f"Unsupported method:{ request.method }"


@api_bp.route("/categorygroup", methods=["GET", "POST"])
def api_categorygroup():
    if request.method == "GET":
        return jsonify(
            db.execute("SELECT * FROM 'CategoryGroup'")
        )
    elif request.method == "POST":
        name = request.form["name"]
        color = request.form["color"]
        icon = request.form["icon"]
        categorygroup_id = categorygroup.add(
            name,
            color,
            icon,
        )
        category.add(
            categorygroup_id,
            name,
            color,
            icon
        )
        return jsonify({
            "status": "success"
        })
    return f"Unsupported method:{ request.method }"


@api_bp.route("/category", methods=["GET", "POST"])
def api_category():
    if request.method == "GET":
        return jsonify(category.get_all())
    elif request.method == "POST":
        categorygroup_id = request.form["categorygroup_id"]
        name = request.form["name"]
        color = request.form["color"]
        icon = request.form["icon"]
        category.add(
            categorygroup_id,
            name,
            color,
            icon
        )
        return jsonify({
            "status": "success"
        })
    return f"Unsupported method:{ request.method }"
