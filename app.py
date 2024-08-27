from flask import Flask, jsonify, Response
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


@app.route("/expenses", methods=["GET", ])
def expenses_list() -> (Response, int):
    expenses = Expense.query.all()
    return jsonify(
        [{"id": expense.id, "title": expense.title} for expense in expenses]
    ), 200


@app.route("/expenses/<int:expense_id>", methods=["GET", ])
def expense_detail(expense_id: int) -> (Response, int):
    expense = db.get_or_404(Expense, expense_id)
    return jsonify({"id": expense.id, "title": expense.title}), 200


@app.errorhandler(404)
def resource_not_found(e: NotFound) -> (Response, int):
    return jsonify(error=str(e)), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
