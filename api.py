from flask import Blueprint, request, jsonify, g

import account
import attachment
import category
import categorygroup
import tag
import transaction
import transactiongroup

api_bp = Blueprint('api_bp', __name__)


def success_response():
    return jsonify({
        "status": "success",
    })


def api_validate(api_class, request_form):
    invalid, invalid_msg = api_class.validate(request_form)
    if invalid:
        return (True, lambda: jsonify({
            "status": "failed",
            "msg": invalid_msg
        }))
    else:
        return (False, None)


@api_bp.before_request
def before_request():
    if request.method == "POST":
        form = request.form
        g.form = form
        g.form_dict = form.to_dict(flat=True)


@api_bp.route("/transactiongroup", methods=["POST"])
def api_transactiongroup():
    if request.method == "POST":
        transactiongroup.add()
    return f"Unsupported method:{ request.method }"


@api_bp.route("/tag", methods=["POST"])
def api_tag():
    if request.method == "POST":
        tag.add()
    return f"Unsupported method:{ request.method }"


@api_bp.route("/attachment", methods=["POST"])
def api_attachment():
    if request.method == "POST":
        attachment.add()
    return f"Unsupported method:{ request.method }"


@api_bp.route("/transaction", methods=["GET", "POST"])
def api_transaction():
    if request.method == "GET":
        return jsonify(transaction.get_all())
    elif request.method == "POST":
        invalid, flask_response = api_validate(transaction, g.form)
        if invalid:
            return flask_response()
        transaction.add(g.form_dict)
        return success_response()
    return f"Unsupported method:{ request.method }"


@api_bp.route("/account", methods=["GET", "POST"])
def api_account():
    if request.method == "GET":
        return jsonify(account.get_all())
    elif request.method == "POST":
        invalid, flask_response = api_validate(account, g.form)
        if invalid:
            return flask_response()
        account.add(g.form_dict)
        return success_response()
    return f"Unsupported method:{ request.method }"


@api_bp.route("/categorygroup", methods=["GET", "POST"])
def api_categorygroup():
    if request.method == "GET":
        return jsonify(categorygroup.get_all())
    elif request.method == "POST":
        invalid, flask_response = api_validate(categorygroup, g.form)
        if invalid:
            return flask_response()
        categorygroup_id = categorygroup.add(g.form_dict)
        category.add({
            "categorygroup_id": categorygroup_id,
            **g.form_dict
        })
        return success_response()
    return f"Unsupported method:{ request.method }"


@api_bp.route("/category", methods=["GET", "POST"])
def api_category():
    if request.method == "GET":
        return jsonify(category.get_all())
    elif request.method == "POST":
        invalid, flask_response = api_validate(category, g.form)
        if invalid:
            return flask_response()
        category.add(g.form_dict)
        return success_response()
    return f"Unsupported method:{ request.method }"
