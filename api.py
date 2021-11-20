
from flask import Blueprint, request, jsonify
import db

api_bp = Blueprint('api_bp', __name__)

@api_bp.route("/transaction", methods=["GET","POST"])
def api_transaction():
    if request.method == "GET":
        return jsonify(
            db.execute("SELECT * FROM 'Transaction'")
        )
    elif request.method == "POST":
        account_id = request.form["account_id"]
        category_id = request.form["category_id"]
        datetime = request.form["datetime"]
        amount = request.form["amount"]
        db.insert("Transaction", {
            "account_id": account_id,
            "category_id": category_id,
            "datetime": datetime,
            "amount": amount,
            })
        return jsonify({
            "status": "success"
        })
    return f"Unsupported method:{ request.method }"

@api_bp.route("/account", methods=["GET","POST"])
def api_account():
    if request.method == "GET":
        return jsonify(
            db.execute("SELECT * FROM 'Account'")
        )
    elif request.method == "POST":
        name = request.form["name"]
        color = request.form["color"]
        db.insert("Account", {
            "name": name,
            "color": color,
            })
        return jsonify({
            "status": "success"
        })
    return f"Unsupported method:{ request.method }"

@api_bp.route("/categorygroup", methods=["GET","POST"])
def api_categorygroup():
    if request.method == "GET":
        return jsonify(
            db.execute("SELECT * FROM 'CategoryGroup'")
        )
    elif request.method == "POST":
        name = request.form["name"]
        color = request.form["color"]
        icon = request.form["icon"]
        categorygroup_id = db.insert("CategoryGroup", {
            "name": name,
            "color": color,
            "icon": icon,
            })
        db.insert("Category", {
            "categorygroup_id": categorygroup_id,
            "name": name,
            "color": color,
            "icon": icon,
            })
        return jsonify({
            "status": "success"
        })
    return f"Unsupported method:{ request.method }"

@api_bp.route("/category", methods=["GET","POST"])
def api_category():
    if request.method == "GET":
        return jsonify(
            db.execute("SELECT * FROM 'Category'")
        )
    elif request.method == "POST":
        categorygroup_id = request.form["categorygroup_id"]
        name = request.form["name"]
        color = request.form["color"]
        icon = request.form["icon"]
        db.insert("Category", {
            "categorygroup_id": categorygroup_id,
            "name": name,
            "color": color,
            "icon": icon,
            })
        return jsonify({
            "status": "success"
        })
    return f"Unsupported method:{ request.method }"
