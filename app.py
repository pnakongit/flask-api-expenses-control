from flask import Flask, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
