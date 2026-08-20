from database.connection import get_connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS formats (
            format_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Create Authors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    # create the books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            book_type_id INTEGER,
            audience_id INTEGER,
            content_type_id INTEGER,
            FOREIGN KEY (audience_id) REFERENCES audiences(audience_id),
            FOREIGN KEY (content_type_id) REFERENCES content_types(content_type_id),
            FOREIGN KEY (book_type_id) REFERENCES book_types(book_type_id)
        )
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

        # Create genres table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS genres (
            genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Create subgenres table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subgenres (
            subgenre_id INTEGER PRIMARY KEY AUTOINCREMENT,
            genre_id INTEGER NOT NULL,
            name TEXT NOT NULL UNIQUE,
            FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
        )
    """)

    # Create audience table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audiences (
            audience_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

        # Create characteristics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS characteristics (
            characteristic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

        # Create book_types table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_types (
            book_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

        # Create content_types table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content_types (
            content_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

        # Create Book_Authors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_authors (
            book_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            PRIMARY KEY (book_id, author_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (author_id) REFERENCES authors(author_id)
        )
    """)

        # Create book_genres table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_genres (
            book_id INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            PRIMARY KEY (book_id, genre_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
        )
    """)

    # Create book_subgenres table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_subgenres (
            book_id INTEGER NOT NULL,
            subgenre_id INTEGER NOT NULL,
            PRIMARY KEY (book_id, subgenre_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (subgenre_id) REFERENCES subgenres(subgenre_id)
        )
    """)


    # Create book_characteristics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_characteristics (
            book_id INTEGER NOT NULL,
            characteristic_id INTEGER NOT NULL,
            PRIMARY KEY (book_id, characteristic_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (characteristic_id) REFERENCES characteristics(characteristic_id)
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

    # Populate book_types table with some initial data
    cursor.execute("""
        INSERT OR IGNORE INTO book_types (name)
        VALUES
            ('Novel'),
            ('Novella'),
            ('Short Story'),
            ('Short Story Collection'),
            ('Anthology'),
            ('Poetry Collection'),
            ('Essay'),
            ('Essay Collection'),
            ('Graphic Novel'),
            ('Biography'),
            ('Autobiography'),
            ('Memoir'),
            ('Academic Book'),
            ('Textbook'),
            ('Monograph'),
            ('Reference Book'),
            ('Encyclopedia'),
            ('Dictionary'),
            ('Atlas'),
            ('Art Book'),
            ('Photography Book'),
            ('Cookbook'),
            ('Travel Guide'),
            ('Journal'),
            ('Workbook'),
            ('Study Guide'),
            ('Children''s Book'),
            ('Activity Book'),
            ('Catalogue')
    """)


    # Populate content_types table with some initial data
    cursor.execute("""
        INSERT OR IGNORE INTO content_types (name)
        VALUES
            ('Fiction'),
            ('Non-fiction'),
            ('Reference'),
            ('Educational')
    """)

        # Populate audiences table with some initial data
    cursor.execute("""
        INSERT OR IGNORE INTO audiences (name)
        VALUES
            ('Academic'),
            ('Adult'),
            ('General'),
            ('Young Adult'),
            ('Children')
    """)


    connection.commit()
    connection.close()