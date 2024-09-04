from flask import jsonify, request, Response, Blueprint
from marshmallow import ValidationError

from app.db import Expense, db
from app.schemas import expense_schema

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

    return expense_schema.dump(expenses, many=True), 200


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
    return expense_schema.dump(expense), 200


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
    load_data = request.get_json()
    if not load_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        data = expense_schema.load(load_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_expense = Expense(**data)
    db.session.add(new_expense)
    db.session.commit()

    return expense_schema.dump(new_expense), 201


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
    load_data = request.get_json()
    if not load_data:
        return jsonify({'message': 'No input data provided'}), 400

    try:
        data = expense_schema.load(load_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    Expense.query.filter(Expense.id == expense_id).update(data)
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
