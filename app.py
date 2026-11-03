from flask import Flask, render_template, request, redirect, url_for, flash
from database import (
    create_table,
    get_all_books,
    add_book,
    delete_book,
    update_status,
    get_statistics
)

app = Flask(__name__)
app.secret_key = "library-project-secret-key"

create_table()


@app.route("/")
def home():
    search = request.args.get("search", "").strip()

    books = get_all_books()

    if search:
        books = [
            book for book in books
            if search.lower() in book["title"].lower()
            or search.lower() in book["author"].lower()
            or search.lower() in (book["isbn"] or "").lower()
        ]

    stats = get_statistics()

    return render_template(
        "index.html",
        books=books,
        stats=stats,
        search=search
    )


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    isbn = request.form.get("isbn", "").strip()
    category = request.form.get("category", "").strip()

    if not title or not author:
        flash("Book title and author are required.", "error")
        return redirect(url_for("home"))

    try:
        add_book(title, author, isbn, category)
        flash("Book added successfully!", "success")
    except Exception:
        flash("Could not add book. Check whether the ISBN already exists.", "error")

    return redirect(url_for("home"))


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete(book_id):
    delete_book(book_id)
    flash("Book deleted successfully.", "success")
    return redirect(url_for("home"))


@app.route("/status/<int:book_id>", methods=["POST"])
def status(book_id):
    new_status = request.form.get("status")

    if new_status in ["Available", "Issued"]:
        update_status(book_id, new_status)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)