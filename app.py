from urllib import request

from flask import Flask, jsonify, Response, request
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.exceptions import NotFound

app = Flask(__name__)

app.config.from_mapping(SQLALCHEMY_DATABASE_URI="sqlite:///project.db")

swaggerui_blueprint = get_swaggerui_blueprint(
    "/api/docs",
    "/spec"
)
app.register_blueprint(swaggerui_blueprint)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Expense(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]


@app.route("/spec/")
def spec() -> Response:
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "My API"
    swag["definitions"] = {
        "ExpenseIn": {
            "type": "object",
            "discriminator": "ExpenseIn",
            "description": "Create an expense",
            "properties": {
                "id": {"type": "integer", "readOnly": True},
                "title": {"type": "string", "required": True},
            },
            "example": {
                "title": "My Expense",
            }
        },
        "ExpenseOut": {
            "allOf": [
                {"$ref": "#/definitions/ExpenseIn"},
                {
                    "type": "object",
                    "description": "Return information about an expense",
                    "example": {
                        "id": 2,
                    }
                }
            ]
        }
    }
    return jsonify(swag)


@app.route("/", methods=["GET", ])
def index() -> (Response, int):
    """
    Send a simple message, like a greeting.
    ---
    tags:
      - "echo endpoint"
    responses:
      200:
        description: OK
        schema:
         type: object
         example:
           { "message" : "Hello World!" }


    """
    return jsonify({"message": "Hello World!"}), 200


@app.route("/expenses/", methods=["GET", ])
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


@app.route("/expenses/<int:expense_id>/", methods=["GET", ])
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


@app.route("/expenses/", methods=["POST", ])
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


@app.route("/expenses/<int:expense_id>/", methods=["PUT", ])
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


@app.route("/expenses/<int:expense_id>/", methods=["DELETE", ])
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


@app.errorhandler(404)
def resource_not_found(e: NotFound) -> (Response, int):
    return jsonify(error=str(e)), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
