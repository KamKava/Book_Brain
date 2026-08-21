# Book Brain — Database Design

**Version:** 0.1  
**Status:** Early development  
**Last updated:** August 2026

---

## 1. Purpose

The database stores Book Brain's authoritative library and reading data.

It is designed to:

- Separate book information from the user's ownership of a book.
- Support authors, genres and series.
- Support different book formats.
- Track reading history and reading sessions.
- Support rereading.
- Provide structured data for analytics and recommendations.
- Allow future migration from SQLite to PostgreSQL.

The initial implementation uses SQLite.

---

## 2. Core Concepts

The most important distinction in the database is between the book itself and the user's relationship with it.

### Book

Contains information about the book itself.

Examples:

- Title
- ISBN
- Author
- Publisher
- Page count
- Publication information

### LibraryEntry

Represents the user's relationship with a book.

Examples:

- Whether the user owns it
- Format
- How it was obtained
- Library status
- Date added

### ReadingRecord

Represents one period of reading a book.

Examples:

- Start date
- Finish date
- Rating
- Review

A book can have multiple reading records to support rereading.

### ReadingSession

Represents one individual period of reading.

Examples:

- Start time
- End time
- Book
- Session source

A reading session can exist without a book and be assigned later.

---

## 3. Main Tables

### Book

Stores bibliographic information about a book.

| Column | Type | Notes |
|---|---|---|
| `book_id` | INTEGER | Primary key |
| `title` | TEXT | Required |
| `subtitle` | TEXT | Optional |
| `isbn10` | TEXT | Optional |
| `isbn13` | TEXT | Optional |
| `page_count` | INTEGER | Optional |
| `publication_date` | TEXT | Optional |
| `publisher` | TEXT | Optional |
| `description` | TEXT | Optional |
| `cover_url` | TEXT | Optional |

ISBN-10 and ISBN-13 may both identify the same edition.

---

### Author

Stores authors independently from books.

| Column | Type | Notes |
|---|---|---|
| `author_id` | INTEGER | Primary key |
| `name` | TEXT | Required |

Books and authors have a many-to-many relationship through `BookAuthor`.

---

### BookAuthor

Links books to authors.

| Column | Type | Notes |
|---|---|---|
| `book_id` | INTEGER | Foreign key → Book |
| `author_id` | INTEGER | Foreign key → Author |

The combination of `book_id` and `author_id` forms the primary key.

---

### Genre

Stores reusable genre/category values.

| Column | Type | Notes |
|---|---|---|
| `genre_id` | INTEGER | Primary key |
| `name` | TEXT | Required, unique |

Books and genres have a many-to-many relationship through `BookGenre`.

---

### BookGenre

Links books to genres.

| Column | Type | Notes |
|---|---|---|
| `book_id` | INTEGER | Foreign key → Book |
| `genre_id` | INTEGER | Foreign key → Genre |

The combination of `book_id` and `genre_id` forms the primary key.

---

### Series

Stores book series.

| Column | Type | Notes |
|---|---|---|
| `series_id` | INTEGER | Primary key |
| `name` | TEXT | Required |
| `description` | TEXT | Optional |

---

### BookSeries

Links books to series and records their position.

| Column | Type | Notes |
|---|---|---|
| `book_id` | INTEGER | Foreign key → Book |
| `series_id` | INTEGER | Foreign key → Series |
| `series_number` | REAL | Optional |

A book may belong to more than one series.

---

### Format

Stores the formats in which books can exist.

| Column | Type | Notes |
|---|---|---|
| `format_id` | INTEGER | Primary key |
| `name` | TEXT | Required, unique |

Initial values:

- Paperback
- Hardcover
- Ebook
- Audiobook

---

### Source

Stores how a library item was obtained.

| Column | Type | Notes |
|---|---|---|
| `source_id` | INTEGER | Primary key |
| `name` | TEXT | Required, unique |

Initial values may include:

- Library book
- Bought new
- Bought second hand
- Gift
- Friend's book

---

### LibraryEntry

Represents the user's relationship with a book.

| Column | Type | Notes |
|---|---|---|
| `lib_entry_id` | INTEGER | Primary key |
| `book_id` | INTEGER | Foreign key → Book |
| `format_id` | INTEGER | Foreign key → Format |
| `source_id` | INTEGER | Foreign key → Source |
| `status` | TEXT | Required |
| `date_added` | TEXT | Optional |
| `price` | REAL | Optional |

Possible statuses include:

- TBR
- Currently Reading
- Read

`LibraryEntry` is separate from `Book` because ownership, format and library status describe the user's relationship with the book rather than the book itself.

---

## 4. Reading Tables

### ReadingRecord

Represents one period of reading a book.

| Column | Type | Notes |
|---|---|---|
| `reading_id` | INTEGER | Primary key |
| `book_id` | INTEGER | Foreign key → Book |
| `lib_entry_id` | INTEGER | Optional foreign key → LibraryEntry |
| `start_date` | TEXT | Optional |
| `finish_date` | TEXT | Optional |
| `rating` | REAL | Optional |
| `review` | TEXT | Optional |

Multiple reading records can exist for the same book, allowing rereading to be tracked.

---

### ReadingSession

Represents one individual reading session.

| Column | Type | Notes |
|---|---|---|
| `session_id` | INTEGER | Primary key |
| `book_id` | INTEGER | Optional foreign key → Book |
| `reading_id` | INTEGER | Optional foreign key → ReadingRecord |
| `start_time` | TEXT | Required |
| `end_time` | TEXT | Optional |
| `source` | TEXT | Required |

Possible sources include:

- Manual
- Web
- Mobile
- Wearable
- Imported

A session may initially have no associated book.

Session duration should be calculated from the timestamps rather than stored as the source of truth.

---

## 5. Notes

### Note

Stores notes associated with books.

| Column | Type | Notes |
|---|---|---|
| `note_id` | INTEGER | Primary key |
| `book_id` | INTEGER | Foreign key → Book |
| `content` | TEXT | Required |
| `created_at` | TEXT | Required |
| `updated_at` | TEXT | Optional |

---

## 6. Relationships

The main relationships are:

- A **Book** can have many Authors.
- An **Author** can have many Books.
- A **Book** can have many Genres.
- A **Genre** can apply to many Books.
- A **Book** can belong to one or more Series.
- A **Book** can have multiple LibraryEntries.
- A **Book** can have multiple ReadingRecords.
- A **ReadingRecord** can have multiple ReadingSessions.
- A **ReadingSession** may exist without a Book.
- A **Book** can have multiple Notes.

Many-to-many relationships are implemented using junction tables.

---

## 7. Important Data Rules

### Books

- Every book must have a title.
- ISBN-10 and ISBN-13 are optional.
- Supplied ISBNs should be validated.
- External metadata must not silently overwrite user data.

### Library Entries

- Every LibraryEntry must reference a Book.
- Every LibraryEntry must have a Format.
- Library status belongs to LibraryEntry rather than Book.
- Multiple entries may eventually allow multiple copies or formats of the same book.

### Reading Records

- A book can have multiple ReadingRecords.
- This allows rereading.
- Ratings and reading dates belong to the ReadingRecord.

### Reading Sessions

- A session may exist without a Book.
- A session may be associated with a Book later.
- Sessions represent individual reading periods.
- Duration is derived from timestamps.

### Foreign Keys

Foreign keys should be enabled and enforced by SQLite.

Deletion rules should protect important historical reading data.

---

## 8. Indexes

Indexes will be added where they provide useful lookup performance.

Likely indexes include:

- `Book.title`
- `Book.isbn10`
- `Book.isbn13`
- `LibraryEntry.book_id`
- `LibraryEntry.status`
- `ReadingRecord.book_id`
- `ReadingRecord.start_date`
- `ReadingSession.book_id`
- `ReadingSession.start_time`

The final indexes will be confirmed during implementation and testing.

---

## 9. Reference Data

### Formats

- Paperback
- Hardcover
- Ebook
- Audiobook

### Sources

- Library book
- Bought new
- Bought second hand
- Gift
- Friend's book

Reference values should be stored in the database rather than unnecessarily duplicated throughout application code.

---

## 10. Database Principles

The database follows these principles:

1. The database is the source of truth for the user's personal library data.
2. Bibliographic information is separated from the user's ownership of a book.
3. Reading history is separated from individual reading sessions.
4. Rereading is supported.
5. Many-to-many relationships use junction tables.
6. Reading sessions are independent of the device or application that records them.
7. Derived statistics should normally be calculated from underlying data.
8. External APIs provide information but do not own or control user data.
9. The schema should remain reasonably portable for a future PostgreSQL migration.

---

## 11. Future Extensions

The database may later be extended to support:

- More detailed edition information.
- Additional book identifiers.
- More detailed ownership and copy tracking.
- Metadata provenance.
- Recommendation-related data.
- AI/tool activity logging.
- External recommendation candidates.
- Embeddings and semantic search.

These should only be introduced when required by the relevant development phase.

---

## 12. Current Status

This document describes the intended database design for the initial SQLite implementation.

The actual SQL schema is the implementation of this design.

If implementation or testing reveals that the design should change, the change should be recorded in the development log and this document updated where necessary.