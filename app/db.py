from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Expense(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
