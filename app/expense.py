from flask import jsonify, request, Response, Blueprint

from app.db import Expense, db

bp = Blueprint("expense", __name__, url_prefix="/expenses")


@bp.route("/", methods=["GET", ])
def expenses_list() -> (Response, int):
    """
    Return a list of all expenses.
    ---
    tags:
      - "expenses"
    responses:
      200:
        description: OK
        schema:
          type: array
          items:
            $ref: "#/definitions/ExpenseOut"

    """
    expenses = Expense.query.all()
    return jsonify(
        [{"id": expense.id, "title": expense.title} for expense in expenses]
    ), 200


@bp.route("/<int:expense_id>/", methods=["GET", ])
def expense_detail(expense_id: int) -> (Response, int):
    """
    Return a specific expense.
    ---
    tags:
      - "expenses"
    parameters:
      - in: path
        name: expense_id
        description: ID of the expense
        required: true
    responses:
      200:
        description: OK
        schema:
          $ref: "#/definitions/ExpenseOut"
      404:
        description: Not found

    """
    expense = db.get_or_404(Expense, expense_id)
    return jsonify({"id": expense.id, "title": expense.title}), 200


@bp.route("/", methods=["POST", ])
def expense_create() -> (Response, int):
    """
    Create a new expense.
    ---
    tags:
      - "expenses"
    parameters:
      - in: body
        name: expense
        required: true
        schema:
          $ref: '#/definitions/ExpenseIn'
    responses:
      201:
        description: Created.
        schema:
          $ref: '#/definitions/ExpenseOut'

    """

    new_expense = Expense(title=request.json["title"])
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"id": new_expense.id, "title": new_expense.title}), 201


@bp.route("/<int:expense_id>/", methods=["PUT", ])
def expense_update(expense_id: int) -> (Response, int):
    """
    Update an existing expense.
    ---
    tags:
      - "expenses"
    parameters:
      - in: path
        name: expense_id
        type: integer
        required: true
        description: The ID of the expense to retrieve
      - in: body
        name: expense
        required: true
        schema:
          $ref: '#/definitions/ExpenseIn'
    responses:
      201:
        description: Created.
        schema:
          $ref: '#/definitions/ExpenseOut'
      404:
        description: Not found.
    """
    expense = db.get_or_404(Expense, expense_id)
    data = request.json
    expense.title = data.get("title", expense.title)
    db.session.add(expense)
    db.session.commit()

    return jsonify({"id": expense.id, "title": expense.title}), 201


@bp.route("/<int:expense_id>/", methods=["DELETE", ])
def expense_delete(expense_id: int) -> (Response, int):
    """
    Delete an existing expense.
    ---
    tags:
      - "expenses"
    parameters:
      - in: path
        name: expense_id
        type: integer
        required: true
        description: The ID of the expense to delete.
    responses:
      204:
        description: No content.
      404:
        description: Not found.
    """
    expense = db.get_or_404(Expense, expense_id)
    db.session.delete(expense)
    db.session.commit()

    return jsonify(), 204
