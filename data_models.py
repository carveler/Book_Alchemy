from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.String)
    date_of_death = db.Column(db.String)

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name}, birth_date={self.birth_date}, date_of_death={self.date_of_death})"

    def __str__(self):
        return f"Author(id={self.id}, name={self.name}, birth_date={self.birth_date}, date_of_death={self.date_of_death})"


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String)
    title = db.Column(db.String)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))

    def __repr__(self):
        return f"Book(id={self.id}, title={self.title}, author_id={self.author_id})"

    def __str__(self):
        return f"Book(id={self.id}, title={self.title}, author_id={self.author_id})"
