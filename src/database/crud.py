from database.connection import get_connection


def add_book(title, book_type_id, audience_id, content_type_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO books (
            title,
            book_type_id,
            audience_id,
            content_type_id
        )
        VALUES (?, ?, ?, ?)
    """, (
        title,
        book_type_id,
        audience_id,
        content_type_id
    ))

    connection.commit()

    book_id = cursor.lastrowid

    connection.close()

    return book_id

# Add author to the authors table
def add_author(name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO authors (name)
        VALUES (?)
    """, (name,))

    connection.commit()

    author_id = cursor.lastrowid

    connection.close()

    return author_id

# Find author by name
def get_author_by_name(name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT author_id FROM authors WHERE name = ?
    """, (name,))

    author = cursor.fetchone()

    connection.close()

    return author

# Add entry to the book_authors table
def add_book_author(book_id, author_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO book_authors (book_id, author_id)
        VALUES (?, ?)
    """, (book_id, author_id))

    connection.commit()

    connection.close()


# Helper for add genres
def add_genre(name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO genres (name)
        VALUES (?)
    """, (name,))

    cursor.execute("""
        SELECT genre_id 
        FROM genres 
        WHERE name = ?
    """, (name,))

    genre_id = cursor.fetchone()[0]

    connection.commit()
    connection.close()

    return genre_id

# Add genre to a book
def add_book_genre(book_id, genre_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO book_genres (book_id, genre_id)
        VALUES (?, ?)
    """, (book_id, genre_id))

    connection.commit()
    connection.close()


# Add subgenre to a book
def add_book_subgenre(book_id, subgenre_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO book_subgenres (book_id, subgenre_id)
        VALUES (?, ?)
    """, (book_id, subgenre_id))

    connection.commit()
    connection.close()


# Add characteristic to a book
def add_book_characteristic(book_id, characteristic_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO book_characteristics (book_id, characteristic_id)
        VALUES (?, ?)
    """, (book_id, characteristic_id))

    connection.commit()
    connection.close()

def get_genres():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT genre_id, name
        FROM genres
        ORDER BY name
    """)

    genres = cursor.fetchall()

    connection.close()

    return genres


def get_subgenres_by_genres(genre_ids):
    connection = get_connection()
    cursor = connection.cursor()

    if not genre_ids:
        connection.close()
        return []

    placeholders = ",".join("?" for _ in genre_ids)

    cursor.execute(f"""
        SELECT subgenre_id, name
        FROM subgenres
        WHERE genre_id IN ({placeholders})
        ORDER BY name
    """, genre_ids)

    subgenres = cursor.fetchall()

    connection.close()

    return subgenres


def get_audiences():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT audience_id, name
        FROM audiences
        ORDER BY name
    """)

    audiences = cursor.fetchall()

    connection.close()

    return audiences

def get_characteristics():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT characteristic_id, name
        FROM characteristics
        ORDER BY name
    """)

    characteristics = cursor.fetchall()

    connection.close()

    return characteristics

def get_book_types():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT book_type_id, name
        FROM book_types
        ORDER BY name
    """)

    book_types = cursor.fetchall()

    connection.close()

    return book_types

def get_content_types():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT content_type_id, name
        FROM content_types
        ORDER BY name
    """)

    content_types = cursor.fetchall()

    connection.close()

    return content_types


def add_edition(
    book_id,
    isbn_13=None,
    isbn_10=None,
    barcode=None,
    barcode_type=None,
    publisher=None,
    publication_date=None
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO editions (
            book_id,
            isbn_13,
            isbn_10,
            barcode,
            barcode_type,
            publisher,
            publication_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        book_id,
        isbn_13,
        isbn_10,
        barcode,
        barcode_type,
        publisher,
        publication_date
    ))

    connection.commit()

    edition_id = cursor.lastrowid

    connection.close()

    return edition_id

def get_edition_by_isbn(isbn):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM editions
        WHERE isbn_13 = ?
           OR isbn_10 = ?
    """, (isbn, isbn))

    edition = cursor.fetchone()

    connection.close()

    return edition

def get_edition_by_barcode(barcode):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM editions
        WHERE barcode = ?
    """, (barcode,))

    edition = cursor.fetchone()

    connection.close()

    return edition

def add_copy(edition_id, format_id, source_id, price):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO copy (
            edition_id,
            format_id,
            source_id,
            price
        )
        VALUES (?, ?, ?, ?)
    """, (
        edition_id,
        format_id,
        source_id,
        price
    ))

    connection.commit()

    copy_id = cursor.lastrowid

    connection.close()

    return copy_id
# Get book names and authors for display in the library table
def get_copies():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.lib_entry_id,
            b.title,
            GROUP_CONCAT(a.name, ', ') AS authors,
            f.name AS format,
            s.name AS source,
            c.price
        FROM copy c
        JOIN editions e ON c.edition_id = e.edition_id
        JOIN books b ON e.book_id = b.book_id
        LEFT JOIN book_authors ba ON b.book_id = ba.book_id
        LEFT JOIN authors a ON ba.author_id = a.author_id
        JOIN formats f ON c.format_id = f.format_id
        JOIN sources s ON c.source_id = s.source_id
        GROUP BY
            c.lib_entry_id,
            b.title,
            f.name,
            s.name,
            c.price
    """)

    copies = cursor.fetchall()

    connection.close()

    return copies

# Get books for dropdowns and other displays
def get_books():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    connection.close()

    return books

# Get Authors for dropdowns and other displays
def get_authors():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM authors")

    authors = cursor.fetchall()

    connection.close()

    return authors


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


def add_subgenre(genre_id, name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO subgenres (genre_id, name)
        VALUES (?, ?)
    """, (genre_id, name))

    connection.commit()
    connection.close()


# Add characteristics to the characteristics table
def add_characteristic(name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO characteristics (name)
        VALUES (?)
    """, (name,))

    connection.commit()
    connection.close()

