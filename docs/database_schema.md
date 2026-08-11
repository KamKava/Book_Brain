# Book Brain — Database Schema

**Project status:** Initial development
**Version:** 1.0
**Last updated:** August 2026
**Database:** SQLite

---

# 1. Purpose

This document defines the implementation-level database schema for Book Brain.

The schema translates the conceptual database design into the actual SQLite tables, columns, constraints, relationships and indexes required by the MVP.

The database is responsible for storing:

* Bibliographic book information.
* Authors.
* Genres.
* Series.
* User library entries.
* Book formats.
* Reading history.
* Reading sessions.
* Personal notes.

The database is the authoritative source of truth for the user's personal library and reading information.

---

# 2. MVP Tables

The MVP contains 12 tables.

| #  | Table              | Purpose                                     | Priority |
| -- | ------------------ | ------------------------------------------- | -------- |
| 1  | `books`            | Book and bibliographic information          | ⭐ Core   |
| 2  | `authors`          | Author information                          | ⭐ Core   |
| 3  | `genres`           | Genres and categories                       | ⭐ Core   |
| 4  | `book_authors`     | Book ↔ author relationships                 | ⭐ Core   |
| 5  | `book_genres`      | Book ↔ genre relationships                  | ⭐ Core   |
| 6  | `series`           | Series information                          | Core     |
| 7  | `series_books`     | Book ↔ series relationships and order       | Core     |
| 8  | `formats`          | Paperback, hardback, ebook, audiobook, etc. | Core     |
| 9  | `library_entries`  | User's library relationship with a book     | ⭐ Core   |
| 10 | `reading_records`  | Individual instances of reading a book      | ⭐ Core   |
| 11 | `reading_sessions` | Individual periods of reading               | Core     |
| 12 | `notes`            | Personal notes about books                  | Core     |

---

# 3. Schema Design Standards

The following conventions apply throughout the schema.

## 3.1 Primary Keys

All main entities use an integer primary key:

```sql
INTEGER PRIMARY KEY
```

SQLite automatically generates the identifier when a row is inserted without specifying the primary key.

Examples:

```text
book_id
author_id
genre_id
series_id
format_id
library_entry_id
reading_record_id
session_id
note_id
```

Junction tables use composite primary keys where appropriate.

---

# 3.2 Foreign Keys

Foreign keys maintain relationships between tables.

SQLite foreign-key enforcement must be explicitly enabled:

```sql
PRAGMA foreign_keys = ON;
```

Foreign-key behaviour is defined for each relationship.

---

# 3.3 NULL Values

`NOT NULL` is used where a value is essential for the existence or meaning of a record.

`NULL` is allowed where information may legitimately be unknown or unavailable.

For example:

```text
Book title → NOT NULL
Book page count → NULL
Book ISBN → NULL
```

This is important because external book metadata may be incomplete.

---

# 3.4 Timestamps

Timestamp fields use:

```sql
DATETIME
```

SQLite does not have a dedicated datetime storage class. Book Brain will store timestamps using SQLite-compatible datetime text values.

Example:

```text
2026-08-11 14:30:00
```

---

# 3.5 Dates

Date-only fields use:

```sql
DATE
```

Example:

```text
2026-08-11
```

These are appropriate for events where the time of day is not required.

---

# 3.6 Naming Convention

Tables and columns use:

```text
snake_case
```

Examples:

```text
reading_records
library_entry_id
publication_date
created_at
```

---

# 4. Entity Overview

The core relationships are:

```text
                         ┌─────────────┐
                         │   authors   │
                         └──────┬──────┘
                                │
                           book_authors
                                │
                                ▼
┌─────────────┐          ┌─────────────┐          ┌─────────────┐
│   genres    │──────────│    books    │──────────│   series    │
└──────┬──────┘ book_genres └──────┬──────┘ series_books └───────┘
       │                           │
       │              ┌────────────┼─────────────┐
       │              │            │             │
       │              ▼            ▼             ▼
       │       library_entries   notes    reading_records
       │              │                         │
       │              ▼                         ▼
       │           formats              reading_sessions
       │
```

The most important application relationship is:

```text
Book
  ↓
LibraryEntry
  ↓
ReadingRecord
  ↓
ReadingSession
```

These represent four different concepts:

```text
Book
What is the book?

LibraryEntry
Is it part of my library, and what is its current status?

ReadingRecord
Have I read it, and when?

ReadingSession
How did I spend my individual reading time?
```

---

# 5. Table: `books`

## Purpose

Stores bibliographic information about books.

A `Book` represents the reusable bibliographic record rather than the user's ownership of the book.

A book may exist without a corresponding `library_entries` record. This allows external catalogue books to exist without being owned by the user.

## Columns

| Column             | Data type | Key    | NULL     | Description                        |
| ------------------ | --------- | ------ | -------- | ---------------------------------- |
| `book_id`          | INTEGER   | PK     | NOT NULL | Internal book identifier           |
| `isbn13`           | TEXT      | UNIQUE | NULL     | ISBN-13 where available            |
| `isbn10`           | TEXT      | UNIQUE | NULL     | ISBN-10 where available            |
| `title`            | TEXT      |        | NOT NULL | Book title                         |
| `subtitle`         | TEXT      |        | NULL     | Optional subtitle                  |
| `publisher`        | TEXT      |        | NULL     | Publisher                          |
| `publication_date` | DATE      |        | NULL     | Publication date                   |
| `page_count`       | INTEGER   |        | NULL     | Number of pages                    |
| `description`      | TEXT      |        | NULL     | Book description                   |
| `language`         | TEXT      |        | NULL     | Book language                      |
| `cover_url`        | TEXT      |        | NULL     | External cover image URL           |
| `external_id`      | TEXT      |        | NULL     | Identifier from an external source |
| `external_source`  | TEXT      |        | NULL     | External source name               |
| `created_at`       | DATETIME  |        | NOT NULL | Creation timestamp                 |
| `updated_at`       | DATETIME  |        | NOT NULL | Last modification timestamp        |

## Constraints

```text
PK:
book_id

UNIQUE:
isbn13
isbn10

CHECK:
page_count IS NULL OR page_count >= 0
```

`isbn13`, `isbn10`, page count and external metadata may legitimately be unavailable.

## Relationships

```text
books → book_authors
books → book_genres
books → series_books
books → library_entries
books → reading_records
books → notes
```

## Cardinality

```text
Book → Authors
1 : many through book_authors

Book → Genres
1 : many through book_genres

Book → Series
1 : many through series_books

Book → Library Entries
1 : many

Book → Reading Records
1 : many

Book → Notes
1 : many
```

## Indexes

```sql
CREATE INDEX idx_books_title
ON books(title);

CREATE INDEX idx_books_isbn13
ON books(isbn13);

CREATE INDEX idx_books_isbn10
ON books(isbn10);

CREATE INDEX idx_books_external_id
ON books(external_id);
```

---

# 6. Table: `authors`

## Purpose

Stores reusable author information.

An author may be associated with multiple books.

## Columns

| Column       | Data type | Key    | NULL     | Description                |
| ------------ | --------- | ------ | -------- | -------------------------- |
| `author_id`  | INTEGER   | PK     | NOT NULL | Internal author identifier |
| `name`       | TEXT      | UNIQUE | NOT NULL | Author name                |
| `created_at` | DATETIME  |        | NOT NULL | Creation timestamp         |

## Constraints

```text
PK:
author_id

UNIQUE:
name
```

## Relationships

```text
authors → book_authors
```

## Cardinality

```text
Author → Books
1 : many through book_authors
```

## Indexes

```sql
CREATE INDEX idx_authors_name
ON authors(name);
```

---

# 7. Table: `genres`

## Purpose

Stores reusable genres or categories.

## Columns

| Column     | Data type | Key    | NULL     | Description               |
| ---------- | --------- | ------ | -------- | ------------------------- |
| `genre_id` | INTEGER   | PK     | NOT NULL | Internal genre identifier |
| `name`     | TEXT      | UNIQUE | NOT NULL | Genre name                |

## Constraints

```text
PK:
genre_id

UNIQUE:
name

CHECK:
length(trim(name)) > 0
```

## Relationships

```text
genres → book_genres
```

## Cardinality

```text
Genre → Books
1 : many through book_genres
```

## Indexes

```sql
CREATE INDEX idx_genres_name
ON genres(name);
```

---

# 8. Table: `book_authors`

## Purpose

Junction table representing the many-to-many relationship between books and authors.

A book may have multiple authors, and an author may be associated with multiple books.

## Columns

| Column        | Data type | Key   | NULL     | Description       |
| ------------- | --------- | ----- | -------- | ----------------- |
| `book_id`     | INTEGER   | PK/FK | NOT NULL | Associated book   |
| `author_id`   | INTEGER   | PK/FK | NOT NULL | Associated author |
| `author_role` | TEXT      |       | NULL     | Optional role     |

## Constraints

```text
PRIMARY KEY:
(book_id, author_id)
```

## Foreign Keys

```text
book_id → books.book_id
author_id → authors.author_id
```

## ON DELETE

```text
book_id:
CASCADE

author_id:
RESTRICT
```

Deleting a book removes its junction records.

Deleting an author is prevented while books still reference that author.

## Relationships

```text
Book ←→ Author
```

## Cardinality

```text
Book → Author
many-to-many

Author → Book
many-to-many
```

## Indexes

```sql
CREATE INDEX idx_book_authors_author_id
ON book_authors(author_id);
```

The composite primary key already provides an index beginning with `book_id`.

---

# 9. Table: `book_genres`

## Purpose

Junction table representing the many-to-many relationship between books and genres.

## Columns

| Column     | Data type | Key   | NULL     | Description      |
| ---------- | --------- | ----- | -------- | ---------------- |
| `book_id`  | INTEGER   | PK/FK | NOT NULL | Associated book  |
| `genre_id` | INTEGER   | PK/FK | NOT NULL | Associated genre |

## Constraints

```text
PRIMARY KEY:
(book_id, genre_id)
```

## Foreign Keys

```text
book_id → books.book_id
genre_id → genres.genre_id
```

## ON DELETE

```text
book_id:
CASCADE

genre_id:
RESTRICT
```

## Relationships

```text
Book ←→ Genre
```

## Cardinality

```text
Book → Genre
many-to-many

Genre → Book
many-to-many
```

## Indexes

```sql
CREATE INDEX idx_book_genres_genre_id
ON book_genres(genre_id);
```

---

# 10. Table: `series`

## Purpose

Stores information about book series.

A book does not need to belong to a series.

## Columns

| Column        | Data type | Key    | NULL     | Description                |
| ------------- | --------- | ------ | -------- | -------------------------- |
| `series_id`   | INTEGER   | PK     | NOT NULL | Internal series identifier |
| `name`        | TEXT      | UNIQUE | NOT NULL | Series name                |
| `description` | TEXT      |        | NULL     | Optional description       |
| `created_at`  | DATETIME  |        | NOT NULL | Creation timestamp         |

## Constraints

```text
PK:
series_id

UNIQUE:
name

CHECK:
length(trim(name)) > 0
```

## Relationships

```text
series → series_books
```

## Cardinality

```text
Series → Books
1 : many through series_books
```

## Indexes

```sql
CREATE INDEX idx_series_name
ON series(name);
```

---

# 11. Table: `series_books`

## Purpose

Junction table representing the relationship between books and series and storing the book's position within the series.

The table supports numbering such as:

```text
1
2
2.5
3
```

## Columns

| Column          | Data type | Key   | NULL     | Description                |
| --------------- | --------- | ----- | -------- | -------------------------- |
| `series_id`     | INTEGER   | PK/FK | NOT NULL | Associated series          |
| `book_id`       | INTEGER   | PK/FK | NOT NULL | Associated book            |
| `series_number` | REAL      |       | NULL     | Position within the series |

## Constraints

```text
PRIMARY KEY:
(series_id, book_id)

CHECK:
series_number IS NULL OR series_number > 0
```

## Foreign Keys

```text
series_id → series.series_id
book_id → books.book_id
```

## ON DELETE

```text
series_id:
CASCADE

book_id:
CASCADE
```

Deleting a series removes its book relationships.

Deleting a book removes its series relationships.

## Relationships

```text
Book ←→ Series
```

## Cardinality

```text
Book → Series
many-to-many

Series → Book
many-to-many
```

The MVP will normally use one series per book, but the junction-table design leaves room for books associated with multiple series where necessary.

## Indexes

```sql
CREATE INDEX idx_series_books_book_id
ON series_books(book_id);
```

---

# 12. Table: `formats`

## Purpose

Stores controlled values describing the format of a library entry.

Initial values include:

```text
Paperback
Hardback
E-book
Audiobook
Other
```

## Columns

| Column      | Data type | Key    | NULL     | Description                |
| ----------- | --------- | ------ | -------- | -------------------------- |
| `format_id` | INTEGER   | PK     | NOT NULL | Internal format identifier |
| `name`      | TEXT      | UNIQUE | NOT NULL | Format name                |

## Constraints

```text
PK:
format_id

UNIQUE:
name

CHECK:
length(trim(name)) > 0
```

## Relationships

```text
formats → library_entries
```

## Cardinality

```text
Format → Library Entries
1 : many
```

## Reference Data

The MVP should populate this table with:

```text
Paperback
Hardback
E-book
Audiobook
Other
```

## Indexes

```sql
CREATE INDEX idx_formats_name
ON formats(name);
```

---

# 13. Table: `library_entries`

## Purpose

Represents the user's relationship with a book.

A `Book` describes the bibliographic object.

A `LibraryEntry` describes the user's personal library relationship.

This is where ownership/library membership, format and current status are represented.

## Columns

| Column             | Data type | Key | NULL     | Description                       |
| ------------------ | --------- | --- | -------- | --------------------------------- |
| `library_entry_id` | INTEGER   | PK  | NOT NULL | Internal library entry identifier |
| `book_id`          | INTEGER   | FK  | NOT NULL | Associated book                   |
| `format_id`        | INTEGER   | FK  | NOT NULL | Owned format                      |
| `status`           | TEXT      |     | NOT NULL | Current library/reading status    |
| `date_added`       | DATE      |     | NOT NULL | Date added to library             |
| `personal_notes`   | TEXT      |     | NULL     | Optional ownership/copy notes     |
| `created_at`       | DATETIME  |     | NOT NULL | Creation timestamp                |
| `updated_at`       | DATETIME  |     | NOT NULL | Last modification timestamp       |

## Constraints

```text
PK:
library_entry_id

UNIQUE:
(book_id, format_id)

CHECK:
status IN (
    'TBR',
    'Currently Reading',
    'Read'
)
```

The uniqueness constraint prevents accidental duplicate entries for the same book and format.

## Foreign Keys

```text
book_id → books.book_id
format_id → formats.format_id
```

## ON DELETE

```text
book_id:
RESTRICT

format_id:
RESTRICT
```

A book should not be deleted while it still has a library entry.

A format should not be deleted while it is being used by library entries.

## Relationships

```text
Book → LibraryEntry
Format → LibraryEntry
```

## Cardinality

```text
Book → LibraryEntry
1 : many

Format → LibraryEntry
1 : many
```

## Indexes

```sql
CREATE INDEX idx_library_entries_book_id
ON library_entries(book_id);

CREATE INDEX idx_library_entries_status
ON library_entries(status);

CREATE INDEX idx_library_entries_format_id
ON library_entries(format_id);
```

---

# 14. Table: `reading_records`

## Purpose

Represents one instance of reading a book.

Multiple reading records may exist for the same book, allowing rereading to be represented.

For example:

```text
Dracula
│
├── Reading Record — 2024
└── Reading Record — 2026
```

## Columns

| Column              | Data type | Key | NULL     | Description                        |
| ------------------- | --------- | --- | -------- | ---------------------------------- |
| `reading_record_id` | INTEGER   | PK  | NOT NULL | Internal reading record identifier |
| `book_id`           | INTEGER   | FK  | NOT NULL | Book being read                    |
| `library_entry_id`  | INTEGER   | FK  | NULL     | Relevant library entry, if known   |
| `date_started`      | DATE      |     | NULL     | Date reading began                 |
| `date_finished`     | DATE      |     | NULL     | Date reading finished              |
| `rating`            | REAL      |     | NULL     | Rating from 0.0 to 5.0             |
| `review`            | TEXT      |     | NULL     | Optional review                    |
| `created_at`        | DATETIME  |     | NOT NULL | Creation timestamp                 |

## Constraints

```text
PK:
reading_record_id

CHECK:
rating IS NULL OR (
    rating >= 0.0
    AND rating <= 5.0
)

CHECK:
date_finished IS NULL
OR date_started IS NULL
OR date_finished >= date_started
```

## Foreign Keys

```text
book_id → books.book_id
library_entry_id → library_entries.library_entry_id
```

## ON DELETE

```text
book_id:
RESTRICT

library_entry_id:
SET NULL
```

Reading history should be protected when a book is removed.

If a specific library entry is removed, the historical reading record should remain valid, but its optional library-entry reference should become `NULL`.

## Relationships

```text
Book → ReadingRecord
LibraryEntry → ReadingRecord
```

## Cardinality

```text
Book → ReadingRecord
1 : many

LibraryEntry → ReadingRecord
1 : many, optional
```

## Indexes

```sql
CREATE INDEX idx_reading_records_book_id
ON reading_records(book_id);

CREATE INDEX idx_reading_records_library_entry_id
ON reading_records(library_entry_id);

CREATE INDEX idx_reading_records_date_finished
ON reading_records(date_finished);
```

---

# 15. Table: `reading_sessions`

## Purpose

Stores individual periods of reading.

A reading session represents a specific period during which the user was reading.

Example:

```text
Reading Record
└── Dracula
     ├── Session — 20 minutes
     ├── Session — 35 minutes
     └── Session — 45 minutes
```

A session may initially exist without an associated reading record.

This supports future mobile and wearable functionality.

## Columns

| Column              | Data type | Key | NULL     | Description                  |
| ------------------- | --------- | --- | -------- | ---------------------------- |
| `session_id`        | INTEGER   | PK  | NOT NULL | Internal session identifier  |
| `reading_record_id` | INTEGER   | FK  | NULL     | Associated reading record    |
| `started_at`        | DATETIME  |     | NOT NULL | Session start                |
| `ended_at`          | DATETIME  |     | NULL     | Session end                  |
| `duration_seconds`  | INTEGER   |     | NULL     | Session duration             |
| `source`            | TEXT      |     | NOT NULL | How the session was recorded |
| `created_at`        | DATETIME  |     | NOT NULL | Creation timestamp           |

## Constraints

```text
PK:
session_id

CHECK:
ended_at IS NULL
OR ended_at >= started_at

CHECK:
duration_seconds IS NULL
OR duration_seconds >= 0

CHECK:
source IN (
    'Manual',
    'Mobile',
    'Web',
    'Fitbit',
    'WearOS',
    'Other'
)
```

## Foreign Keys

```text
reading_record_id → reading_records.reading_record_id
```

## ON DELETE

```text
reading_record_id:
SET NULL
```

Deleting a reading record should not destroy the historical record of time spent reading.

The session can remain in the database as an unassigned session.

## Active Sessions

An active reading session is represented by:

```text
ended_at = NULL
```

Once stopped, the application records:

```text
ended_at
duration_seconds
```

The application should ensure that an active session is handled correctly and that invalid timestamps cannot be created.

## Relationships

```text
ReadingRecord → ReadingSession
```

## Cardinality

```text
ReadingRecord → ReadingSession
1 : many, optional
```

A reading session may exist without a reading record.

## Indexes

```sql
CREATE INDEX idx_reading_sessions_reading_record_id
ON reading_sessions(reading_record_id);

CREATE INDEX idx_reading_sessions_started_at
ON reading_sessions(started_at);
```

---

# 16. Table: `notes`

## Purpose

Stores personal notes associated with books.

Notes belong to the book rather than a specific library entry or reading record.

This allows notes to remain associated with the book even if ownership changes.

## Columns

| Column       | Data type | Key | NULL     | Description                 |
| ------------ | --------- | --- | -------- | --------------------------- |
| `note_id`    | INTEGER   | PK  | NOT NULL | Internal note identifier    |
| `book_id`    | INTEGER   | FK  | NOT NULL | Associated book             |
| `content`    | TEXT      |     | NOT NULL | Note content                |
| `created_at` | DATETIME  |     | NOT NULL | Creation timestamp          |
| `updated_at` | DATETIME  |     | NOT NULL | Last modification timestamp |

## Constraints

```text
PK:
note_id

CHECK:
length(trim(content)) > 0
```

## Foreign Keys

```text
book_id → books.book_id
```

## ON DELETE

```text
book_id:
RESTRICT
```

Deleting a book should not silently destroy personal notes.

The application should explicitly handle associated notes before deleting a book.

## Relationships

```text
Book → Note
```

## Cardinality

```text
Book → Note
1 : many
```

## Indexes

```sql
CREATE INDEX idx_notes_book_id
ON notes(book_id);
```

---

# 17. Relationship Summary

| Parent            | Child              | Relationship                   | Cardinality | Delete behaviour |
| ----------------- | ------------------ | ------------------------------ | ----------- | ---------------- |
| `books`           | `book_authors`     | Book has authors               | 1 : many    | CASCADE          |
| `authors`         | `book_authors`     | Author has books               | 1 : many    | RESTRICT         |
| `books`           | `book_genres`      | Book has genres                | 1 : many    | CASCADE          |
| `genres`          | `book_genres`      | Genre has books                | 1 : many    | RESTRICT         |
| `series`          | `series_books`     | Series contains books          | 1 : many    | CASCADE          |
| `books`           | `series_books`     | Book belongs to series         | 1 : many    | CASCADE          |
| `books`           | `library_entries`  | Book has library entries       | 1 : many    | RESTRICT         |
| `formats`         | `library_entries`  | Format used by entries         | 1 : many    | RESTRICT         |
| `books`           | `reading_records`  | Book has reading records       | 1 : many    | RESTRICT         |
| `library_entries` | `reading_records`  | Entry may have reading records | 1 : many    | SET NULL         |
| `reading_records` | `reading_sessions` | Record has sessions            | 1 : many    | SET NULL         |
| `books`           | `notes`            | Book has notes                 | 1 : many    | RESTRICT         |

---

# 18. Many-to-Many Relationships

The MVP contains three many-to-many relationships.

## Books ↔ Authors

Implemented using:

```text
book_authors
```

```text
Book ←→ Author
```

---

## Books ↔ Genres

Implemented using:

```text
book_genres
```

```text
Book ←→ Genre
```

---

## Books ↔ Series

Implemented using:

```text
series_books
```

```text
Book ←→ Series
```

Although most books will probably belong to zero or one series, the junction table provides flexibility for books associated with multiple series.

---

# 19. Index Summary

The initial index set is:

```sql
-- Books
CREATE INDEX idx_books_title
ON books(title);

CREATE INDEX idx_books_isbn13
ON books(isbn13);

CREATE INDEX idx_books_isbn10
ON books(isbn10);

CREATE INDEX idx_books_external_id
ON books(external_id);

-- Authors
CREATE INDEX idx_authors_name
ON authors(name);

-- Genres
CREATE INDEX idx_genres_name
ON genres(name);

-- Book authors
CREATE INDEX idx_book_authors_author_id
ON book_authors(author_id);

-- Book genres
CREATE INDEX idx_book_genres_genre_id
ON book_genres(genre_id);

-- Series
CREATE INDEX idx_series_name
ON series(name);

-- Series books
CREATE INDEX idx_series_books_book_id
ON series_books(book_id);

-- Formats
CREATE INDEX idx_formats_name
ON formats(name);

-- Library entries
CREATE INDEX idx_library_entries_book_id
ON library_entries(book_id);

CREATE INDEX idx_library_entries_status
ON library_entries(status);

CREATE INDEX idx_library_entries_format_id
ON library_entries(format_id);

-- Reading records
CREATE INDEX idx_reading_records_book_id
ON reading_records(book_id);

CREATE INDEX idx_reading_records_library_entry_id
ON reading_records(library_entry_id);

CREATE INDEX idx_reading_records_date_finished
ON reading_records(date_finished);

-- Reading sessions
CREATE INDEX idx_reading_sessions_reading_record_id
ON reading_sessions(reading_record_id);

CREATE INDEX idx_reading_sessions_started_at
ON reading_sessions(started_at);

-- Notes
CREATE INDEX idx_notes_book_id
ON notes(book_id);
```

Primary keys and UNIQUE constraints automatically create indexes where appropriate, so additional indexes should not be created unnecessarily.

---

# 20. Constraint Summary

The database uses constraints to protect data integrity.

## Required relationships

Foreign keys ensure that referenced records exist.

## Unique values

Unique constraints are used for:

```text
books.isbn13
books.isbn10
authors.name
genres.name
series.name
formats.name
```

and:

```text
library_entries(book_id, format_id)
```

## Numeric validation

```text
page_count >= 0
rating between 0.0 and 5.0
duration_seconds >= 0
series_number > 0
```

## Date validation

```text
date_finished >= date_started
```

where both dates exist.

## Session validation

```text
ended_at >= started_at
```

where an end time exists.

---

# 21. ON DELETE Strategy

Deletion behaviour is deliberately conservative because Book Brain stores personal historical information.

## CASCADE

Used for relationship/junction records where the child has no meaningful existence without the parent.

Examples:

```text
Book → book_authors
Book → book_genres
Book → series_books
Series → series_books
```

Deleting the parent removes the relationship record.

---

## RESTRICT

Used where deleting the parent could destroy meaningful user or bibliographic information.

Examples:

```text
Book → library_entries
Book → reading_records
Book → notes
Author → book_authors
Genre → book_genres
Format → library_entries
```

The application must explicitly deal with dependent records first.

---

## SET NULL

Used where historical information should remain but its optional relationship may no longer exist.

Examples:

```text
LibraryEntry → ReadingRecord
ReadingRecord → ReadingSession
```

This allows historical reading information to survive changes to the user's library.

---

# 22. Reference Data

The MVP requires initial reference data for formats.

The following values should be inserted when the database is created:

```text
Paperback
Hardback
E-book
Audiobook
Other
```

Example:

```sql
INSERT INTO formats (name)
VALUES
    ('Paperback'),
    ('Hardback'),
    ('E-book'),
    ('Audiobook'),
    ('Other');
```

The exact IDs should not be hard-coded in application code.

The application should look up the relevant `format_id`.

---

# 23. SQLite Configuration

Foreign-key enforcement must be enabled for each SQLite connection:

```sql
PRAGMA foreign_keys = ON;
```

The application/database connection layer should ensure this is always enabled.

The schema should not rely on SQLite's default foreign-key behaviour.

---

# 24. Database Creation Order

Because tables reference one another, the schema should be created in dependency order.

Recommended order:

```text
1. books
2. authors
3. genres
4. series
5. formats
6. book_authors
7. book_genres
8. series_books
9. library_entries
10. reading_records
11. reading_sessions
12. notes
```

Reference data should then be inserted into:

```text
formats
```

---

# 25. MVP Database Scope

The following functionality is supported by the schema:

### Books

* Create books.
* Retrieve books.
* Update books.
* Delete books subject to relationship constraints.
* Search by title.
* Search by ISBN.
* Store external metadata identifiers.

### Authors

* Store authors.
* Associate authors with books.
* Support multiple authors per book.

### Genres

* Store genres.
* Associate multiple genres with books.

### Series

* Store series.
* Associate books with series.
* Store series order.

### Library

* Store books belonging to the user's library.
* Store format.
* Store current status.
* Store date added.
* Support multiple formats of the same book.

### Reading

* Store reading history.
* Support rereading.
* Store reading dates.
* Store ratings.
* Store reviews.
* Store individual reading sessions.
* Support active sessions.
* Support unassigned sessions.

### Notes

* Store personal book notes.
* Update and delete notes.

### Analytics

The underlying data supports calculation of:

* Books read.
* Books read per month/year.
* Reading time.
* Average session length.
* Page-count statistics.
* Genre statistics.
* Author statistics.
* Series progress.
* Ratings.

---

# 26. Deliberately Excluded from MVP

The following are **not tables in the MVP schema**:

```text
users
embeddings
external_book_sources
recommendations
recommendation_feedback
reading_goals
reading_challenges
ai_conversations
ai_messages
wearables
fitbit_data
```

These may be introduced in later development phases if actual requirements justify them.

External book APIs can initially use the existing fields:

```text
external_id
external_source
```

within `books`.

---

# 27. Schema Implementation Checklist

Before considering the database schema complete, the implementation should verify:

* [ ] All 12 tables are created.
* [ ] All primary keys are correctly defined.
* [ ] All foreign keys are correctly defined.
* [ ] SQLite foreign-key enforcement is enabled.
* [ ] Required fields use `NOT NULL`.
* [ ] Optional metadata permits `NULL`.
* [ ] ISBN uniqueness is enforced.
* [ ] Author names are unique.
* [ ] Genre names are unique.
* [ ] Series names are unique.
* [ ] Format names are unique.
* [ ] Library-entry format duplicates are prevented.
* [ ] Page-count validation works.
* [ ] Rating validation works.
* [ ] Date validation works.
* [ ] Reading-session validation works.
* [ ] Series-number validation works.
* [ ] `ON DELETE` behaviour has been tested.
* [ ] Required indexes are created.
* [ ] Format reference data is inserted.
* [ ] Representative test data can be inserted.
* [ ] Multiple authors per book work.
* [ ] Multiple genres per book work.
* [ ] Series ordering works.
* [ ] Multiple formats for one book work.
* [ ] Rereading works.
* [ ] Unassigned reading sessions work.
* [ ] Reading history survives library-entry deletion.
* [ ] Data export can retrieve the required personal data.

---

# 28. Final MVP Schema

The complete MVP schema is:

```text
books
│
├── book_authors ─── authors
│
├── book_genres ──── genres
│
├── series_books ──── series
│
├── library_entries ─── formats
│       │
│       └── reading_records
│               │
│               └── reading_sessions
│
└── notes
```

Or, conceptually:

```text
                    ┌───────────┐
                    │  Authors  │
                    └─────┬─────┘
                          │
                    BookAuthors
                          │
                          ▼
┌───────────┐       ┌───────────┐       ┌───────────┐
│  Genres   │───────│   Books   │───────│  Series   │
└─────┬─────┘       └─────┬─────┘       └─────┬─────┘
      │                    │                   │
 BookGenres       ┌────────┼────────┐    SeriesBooks
                   │        │        │
                   ▼        ▼        ▼
             LibraryEntry  Notes  ReadingRecord
                   │                 │
                   ▼                 ▼
                Format        ReadingSession
```

The database therefore has a deliberately small core.

The MVP does **not** attempt to implement the entire future Book Brain architecture. It provides the relational foundation required for the first working version of the application.

