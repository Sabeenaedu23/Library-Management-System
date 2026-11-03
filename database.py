import sqlite3

DATABASE = "library.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                category TEXT,
                status TEXT DEFAULT 'Available'
            )
        """)


def get_all_books():
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM books ORDER BY id DESC"
        ).fetchall()


def add_book(title, author, isbn, category):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO books (title, author, isbn, category)
            VALUES (?, ?, ?, ?)
        """, (title, author, isbn or None, category))


def delete_book(book_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM books WHERE id = ?", (book_id,)
        )


def update_status(book_id, status):
    with get_connection() as connection:
        connection.execute(
            "UPDATE books SET status = ? WHERE id = ?",
            (status, book_id)
        )


def get_statistics():
    with get_connection() as connection:
        total = connection.execute(
            "SELECT COUNT(*) FROM books"
        ).fetchone()[0]

        available = connection.execute(
            "SELECT COUNT(*) FROM books WHERE status = 'Available'"
        ).fetchone()[0]

        issued = connection.execute(
            "SELECT COUNT(*) FROM books WHERE status = 'Issued'"
        ).fetchone()[0]

    return {
        "total": total,
        "available": available,
        "issued": issued
    }