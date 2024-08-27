from urllib import request

from flask import Flask, jsonify, Response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.exceptions import NotFound

app = Flask(__name__)

app.config.from_mapping(SQLALCHEMY_DATABASE_URI="sqlite:///project.db")


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Expense(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]


@app.route("/", methods=["GET", ])
def index() -> (Response, int):
    return jsonify({"message": "Hello World!"}), 200


@app.route("/expenses/", methods=["GET", ])
def expenses_list() -> (Response, int):
    expenses = Expense.query.all()
    return jsonify(
        [{"id": expense.id, "title": expense.title} for expense in expenses]
    ), 200


@app.route("/expenses/<int:expense_id>/", methods=["GET", ])
def expense_detail(expense_id: int) -> (Response, int):
    expense = db.get_or_404(Expense, expense_id)
    return jsonify({"id": expense.id, "title": expense.title}), 200


@app.route("/expenses/", methods=["POST", ])
def expense_create() -> (Response, int):
    new_expense = Expense(title=request.json["title"])
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"id": new_expense.id, "title": new_expense.title}), 201


@app.route("/expenses/<int:expense_id>/", methods=["PUT", ])
def expense_update(expense_id: int) -> (Response, int):
    expense = db.get_or_404(Expense, expense_id)
    data = request.json
    expense.title = data.get("title", expense.title)
    db.session.add(expense)
    db.session.commit()

    return jsonify({"id": expense.id, "title": expense.title}), 201


@app.route("/expenses/<int:expense_id>/", methods=["DELETE", ])
def expense_delete(expense_id: int) -> (Response, int):
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
