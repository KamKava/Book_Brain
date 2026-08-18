from database.connection import get_connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # create the books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS formats (
            format_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # create sources table
    # pk source_id, name
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            source_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Populate formats and sources tables with some initial data
    cursor.execute("""
        INSERT OR IGNORE INTO formats (name)
        VALUES
            ('Paperback'),
            ('Hardcover'),
            ('Ebook'),
            ('Audiobook')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO sources (name)
        VALUES
            ('Library book'),
            ('Bought new'),
            ('Bought second hand'),
            ('Gift'),
            ('Friend''s book')
    """)

# create library_entries table
    # pk lib_entry_id, book_id, format_id, source_id, price
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS library_entries (
            lib_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            format_id INTEGER NOT NULL,
            source_id INTEGER NOT NULL,
            price REAL,
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (format_id) REFERENCES formats(format_id),
            FOREIGN KEY (source_id) REFERENCES sources(source_id)
        )
    """)



    connection.commit()
    connection.close()