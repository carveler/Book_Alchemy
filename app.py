from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from data_models import db, Author, Book
import os


app = Flask(__name__)  # Create an instance of the Flask application

database_path = os.path.join(os.getcwd(), "data", "library.sqlite")
os.makedirs(os.path.dirname(database_path), exist_ok=True)
print(database_path)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"

db.init_app(app)

with app.app_context():
    db.create_all()  # need to run only once


@app.route("/")
def home():
    """
    Render the home page with a list of all books.

    Returns:
        render_template: Rendered HTML for the home page with books data.
    """
    search_query = request.args.get("search", "").strip()

    if search_query:
        books = Book.query.join(Author).filter(
            or_(
                Book.title.ilike(f"%{search_query}%"),
                Author.name.ilike(f"%{search_query}%"),
            )
        ).all()

    else:
        books = Book.query.all()
    authors = Author.query.all()
    authors_dict = {author.id: author for author in authors}
    sort_key = request.args.get("sort", "")
    if sort_key == "title":
        books = sorted(books, key=lambda b: b.title)
    elif sort_key == "author":
        books = sorted(books, key=lambda b: authors_dict[b.author_id].name)
    return render_template("home.html", books=books, authors=authors_dict)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """
    Handle GET and POST requests for adding a new author.

    On GET: Render the add_author form.
    On POST: Process the form data to add a new author to the database.

    Returns:
        On GET: render_template for add_author form.
        On POST success: Redirect to home page.
        On POST failure: Re-render add_author form (implicitly).
    """
    if request.method == "POST":
        print("Form data received:")
        name = request.form.get("name")
        birth_date = request.form.get("birth_date")
        date_of_death = request.form.get("date_of_death")
        new_author = Author(
            name=name, birth_date=birth_date, date_of_death=date_of_death
        )
        print(f"New author before commit: {new_author}")
        try:
            db.session.add(new_author)
            db.session.commit()
            print(f"New author after commit: {new_author}")
            return redirect(url_for("home"))
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {str(e)}")
    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """
    Handle GET and POST requests for adding a new book.

    On GET: Render the add_book form.
    On POST: Process the form data to add a new book to the database.

    Returns:
        On GET: render_template for add_book form.
        On POST success: Redirect to home page.
        On POST failure: Re-render add_book form (implicitly).
    """
    if request.method == "POST":
        print("Form data received:")
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        publication_year = request.form.get("publication_year")
        author_id = request.form.get("author_id")
        new_book = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            author_id=author_id,
        )
        print(f"New book before commit: {new_book}")
        try:
            db.session.add(new_book)
            db.session.commit()
            print(f"New book after commit: {new_book}")
            return redirect(url_for("home"))
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {str(e)}")

    return render_template("add_book.html")
