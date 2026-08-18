from database.connection import get_connection


def add_book(title):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO books (title)
        VALUES (?)
    """, (title,))

    connection.commit()

    book_id = cursor.lastrowid

    connection.close()

    return book_id

def add_library_entry(book_id, format_id, source_id, price):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO library_entries (book_id, format_id, source_id, price)
        VALUES (?, ?, ?, ?)
    """, (book_id, format_id, source_id, price))

    connection.commit()

    lib_entry_id = cursor.lastrowid

    connection.close()

    return lib_entry_id

def get_books():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    connection.close()

    return books


def get_book(book_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM books WHERE book_id = ?",
        (book_id,)
    )

    book = cursor.fetchone()

    connection.close()

    return book


def update_book(book_id, title):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE books
        SET title = ?
        WHERE book_id = ?
    """, (title, book_id))

    connection.commit()
    connection.close()


def delete_book(book_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM books WHERE book_id = ?",
        (book_id,)
    )

    connection.commit()
    connection.close()

# Get formats and sources for dropdowns
def get_formats():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT format_id, name FROM formats")

    formats = cursor.fetchall()

    connection.close()

    return formats

def get_sources():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT source_id, name FROM sources")

    sources = cursor.fetchall()

    connection.close()

    return sources