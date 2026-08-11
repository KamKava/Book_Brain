# Book Brain — Database Design

**Project status:** Initial development
**Version:** 0.3
**Last updated:** August 2026

---

# 1. Purpose

This document defines the relational database design for Book Brain.

The database provides the authoritative storage layer for the user's personal library and reading information.

The design supports the current MVP while providing a controlled path toward future functionality including:

* External book metadata APIs.
* ISBN lookup.
* Barcode scanning.
* Reading analytics.
* Power BI.
* Personalised recommendations.
* Context-aware recommendations.
* Series-aware recommendations.
* Semantic search.
* AI librarian functionality.
* Web applications.
* Mobile applications.
* Wearable/device integration.

The initial implementation will use **SQLite**.

A future migration to **PostgreSQL** should be possible without fundamentally redesigning the core data model.

The database is intentionally designed to remain relatively small during the MVP. Future entities will only be introduced when the corresponding functionality is actually implemented.

---

# 2. Database Design Principles

## 2.1 Separate Bibliographic Information from User Information

Information describing a book should be separated from information describing the user's relationship with that book.

For example:

### Book

```text
Title: Dracula
Author: Bram Stoker
Pages: 336
Genre: Horror
ISBN: ...
```

describes the book itself.

Whereas:

### Library Entry

```text
Format: Paperback
Status: TBR
Date added: 2026-08-01
```

describes the user's library relationship with that book.

This separation allows bibliographic information to remain reusable while personal information remains associated with the user's library.

---

## 2.2 Database as the Source of Truth

The database shall be the authoritative source for the user's personal library information.

This includes:

* Books owned.
* Library entries.
* TBR status.
* Current reading status.
* Reading history.
* Ratings.
* Reading dates.
* Reading sessions.
* Notes.
* Formats owned.

The AI system shall not be treated as the authoritative source for this information.

The AI must obtain personal library information through controlled application functionality.

---

## 2.3 Separate Books from Library Entries

A `Book` represents bibliographic information.

A `LibraryEntry` represents the user's relationship with a book.

This distinction allows:

```text
Book
 └── Dracula

Library Entries
 ├── Paperback
 ├── E-book
 └── Audiobook
```

The same book can therefore exist once in the bibliographic database while the user can have multiple library entries representing different formats or copies.

---

## 2.4 Reading History Is Separate from Ownership

A user may read a book without the current library entry representing the exact copy used.

Reading history therefore belongs to the user's reading activity rather than simply being stored as fields on `Book`.

This allows:

* Rereading.
* Multiple reading records.
* Historical ratings.
* Different reading periods.
* Reading sessions.
* Future changes to ownership.

---

## 2.5 Reading Sessions Are Separate from Reading Records

A `ReadingRecord` represents an overall instance of reading a book.

A `ReadingSession` represents an individual period of reading.

For example:

```text
Reading Record
 └── Dracula
      ├── Session — 20 minutes
      ├── Session — 35 minutes
      └── Session — 45 minutes
```

This distinction allows detailed reading-time analytics without duplicating overall reading information.

---

## 2.6 Support Unassigned Reading Sessions

A reading session does not necessarily need to have a book assigned when it is created.

For example:

```text
Reading Session
Started: 14:10
Ended: 14:52
Duration: 42 minutes
Book: NULL
```

The user may assign the session later.

This is particularly important for future mobile and wearable functionality.

---

## 2.7 Avoid Unnecessary Duplication

Reusable information such as authors, genres, series and formats should be stored separately where appropriate.

Junction tables shall be used for many-to-many relationships.

---

## 2.8 Support Incomplete Metadata

External APIs may not provide complete information.

A book should remain valid if information such as:

* ISBN.
* Page count.
* Publisher.
* Description.
* Publication date.
* Cover image.
* Language.

is unavailable.

Missing metadata must not prevent the book from being stored.

---

## 2.9 Design for Analytics

The database shall store structured information that supports future analytics.

Examples include:

* Page count.
* Publication date.
* Reading dates.
* Reading duration.
* Genre.
* Author.
* Rating.
* Reading status.
* Format.

Calculated statistics should generally be generated from underlying data rather than permanently stored.

For example, the database should store:

```text
page_count = 137
```

rather than:

```text
length_category = "Short"
```

The application can calculate the category when required.

---

## 2.10 Design for Recommendations

The database shall provide sufficient information for the future recommendation system to distinguish between:

* Books owned by the user.
* Books on the TBR.
* Books currently being read.
* Books previously completed.
* Books the user has rated highly.
* Books not owned by the user.
* Standalone books.
* Series books.
* Series progress.
* Book length.
* Genres.
* Authors.
* Reading history.

The recommendation engine will use this structured information when generating candidates and ranking them.

---

# 3. MVP Entity Model

The initial database will contain the following core entities.

### Bibliographic entities

1. `Book`
2. `Author`
3. `Genre`
4. `Series`

### Library entities

5. `Format`
6. `LibraryEntry`

### Reading entities

7. `ReadingRecord`
8. `ReadingSession`

### Supporting entities

9. `Note`

### Relationship entities

10. `BookAuthor`
11. `BookGenre`
12. `SeriesBook`

The conceptual structure is:

```text
                       ┌─────────────┐
                       │    Author   │
                       └──────┬──────┘
                              │
                         BookAuthor
                              │
                              ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│    Genre    │─────────│    Book     │─────────│   Series    │
└──────┬──────┘         └──────┬──────┘         └──────┬──────┘
       │                       │                       │
   BookGenre                  │                   SeriesBook
                              │
                 ┌────────────┼────────────┐
                 │            │            │
                 ▼            ▼            ▼
          LibraryEntry      Note      Book metadata
                 │
                 │
                 ▼
          ReadingRecord
                 │
                 ▼
          ReadingSession

Format
   │
   ▼
LibraryEntry
```

---

# 4. Book

The `Book` entity represents bibliographic information about a book or identifiable edition.

For the current project, the `Book` record is the reusable bibliographic representation used by Book Brain.

ISBN values may identify a particular edition.

A book does not need to have an ISBN.

## Attributes

| Attribute          | Type      | Key / Constraint | Description                          |
| ------------------ | --------- | ---------------- | ------------------------------------ |
| `book_id`          | INTEGER   | PK               | Internal unique identifier           |
| `isbn13`           | TEXT      | UNIQUE, nullable | ISBN-13 where available              |
| `isbn10`           | TEXT      | UNIQUE, nullable | ISBN-10 where available              |
| `title`            | TEXT      | NOT NULL         | Book title                           |
| `subtitle`         | TEXT      | nullable         | Optional subtitle                    |
| `publisher`        | TEXT      | nullable         | Publisher                            |
| `publication_date` | DATE/TEXT | nullable         | Publication date where known         |
| `page_count`       | INTEGER   | nullable         | Number of pages                      |
| `description`      | TEXT      | nullable         | Book description                     |
| `language`         | TEXT      | nullable         | Book language                        |
| `cover_url`        | TEXT      | nullable         | External cover image URL             |
| `external_id`      | TEXT      | nullable         | Identifier from an external book API |
| `external_source`  | TEXT      | nullable         | Source of external identifier        |
| `created_at`       | DATETIME  | NOT NULL         | Record creation time                 |
| `updated_at`       | DATETIME  | NOT NULL         | Last modification time               |

---

# 5. Book Identification

The internal `book_id` shall be the primary key.

ISBNs shall be treated as external identifiers rather than primary keys.

This is because:

* Some books do not have ISBNs.
* Older books may use other identifiers.
* ISBNs identify particular editions.
* External APIs may provide different identifiers.
* A book may exist in Book Brain without external metadata.

Where available, ISBN values should have unique constraints.

ISBN values should also be indexed to support rapid lookup.

---

# 6. External Metadata

The following fields support future external book API integration:

```text
external_id
external_source
```

For example:

```text
external_id = "OL1234567M"
external_source = "OpenLibrary"
```

The exact external services used by Book Brain will be determined during the external metadata development phase.

External metadata shall not replace user-controlled library information.

Where practical, imported information should be distinguishable from information manually entered or modified by the user.

---

# 7. Page Count

`page_count` is an important bibliographic attribute.

It supports:

* Short-book recommendations.
* Long-book recommendations.
* Average book length.
* Page-count distributions.
* Pages read.
* Reading trends.
* Context-aware recommendations.

For example:

> "I want something short for the beach."

The recommendation engine can use `page_count` when filtering and ranking candidates.

Potential categories include:

```text
Under 100 pages
100–199 pages
200–299 pages
300–399 pages
400–499 pages
500+ pages
```

These categories shall be generated by application logic rather than stored permanently.

This allows recommendation thresholds to change without modifying existing data.

`page_count` shall remain nullable.

---

# 8. Author

The `Author` entity stores reusable author information.

## Attributes

| Attribute    | Type     | Key / Constraint | Description          |
| ------------ | -------- | ---------------- | -------------------- |
| `author_id`  | INTEGER  | PK               | Internal identifier  |
| `name`       | TEXT     | NOT NULL         | Author name          |
| `created_at` | DATETIME | NOT NULL         | Record creation time |

An author may be associated with many books.

---

# 9. BookAuthor

`BookAuthor` represents the many-to-many relationship between books and authors.

## Attributes

| Attribute     | Type    | Key / Constraint | Description       |
| ------------- | ------- | ---------------- | ----------------- |
| `book_id`     | INTEGER | PK/FK            | Associated book   |
| `author_id`   | INTEGER | PK/FK            | Associated author |
| `author_role` | TEXT    | nullable         | Optional role     |

Composite primary key:

```text
(book_id, author_id)
```

Possible future roles include:

* Author.
* Translator.
* Editor.
* Illustrator.

The role field should only be expanded if the application genuinely needs this distinction.

---

# 10. Genre

The `Genre` entity stores reusable genres or categories.

## Attributes

| Attribute  | Type    | Key / Constraint | Description         |
| ---------- | ------- | ---------------- | ------------------- |
| `genre_id` | INTEGER | PK               | Internal identifier |
| `name`     | TEXT    | UNIQUE, NOT NULL | Genre/category name |

Examples include:

```text
Horror
Dark Romance
Fantasy
Science Fiction
Literary Fiction
Mystery
Historical Fiction
```

A book may belong to multiple genres.

---

# 11. BookGenre

`BookGenre` represents the many-to-many relationship between books and genres.

## Attributes

| Attribute  | Type    | Key / Constraint | Description      |
| ---------- | ------- | ---------------- | ---------------- |
| `book_id`  | INTEGER | PK/FK            | Associated book  |
| `genre_id` | INTEGER | PK/FK            | Associated genre |

Composite primary key:

```text
(book_id, genre_id)
```

This supports queries such as:

> "Show me horror books I own."

and:

> "Which genres do I read most?"

---

# 12. Series

The `Series` entity represents a collection of books belonging to a named series.

## Attributes

| Attribute     | Type     | Key / Constraint | Description          |
| ------------- | -------- | ---------------- | -------------------- |
| `series_id`   | INTEGER  | PK               | Internal identifier  |
| `name`        | TEXT     | UNIQUE, NOT NULL | Series name          |
| `description` | TEXT     | nullable         | Optional description |
| `created_at`  | DATETIME | NOT NULL         | Creation time        |

A book does not have to belong to a series.

A missing series relationship therefore represents a standalone book unless additional metadata indicates otherwise.

---

# 13. SeriesBook

`SeriesBook` represents the relationship between books and series.

## Attributes

| Attribute       | Type    | Key / Constraint | Description                |
| --------------- | ------- | ---------------- | -------------------------- |
| `series_id`     | INTEGER | PK/FK            | Associated series          |
| `book_id`       | INTEGER | PK/FK            | Associated book            |
| `series_number` | REAL    | nullable         | Position within the series |

Composite primary key:

```text
(series_id, book_id)
```

`series_number` uses `REAL` to support values such as:

```text
1
2
2.5
3
```

This can represent novellas, intermediate stories or other numbering schemes.

---

# 14. Format

The `Format` entity stores the format of a user's library entry.

## Attributes

| Attribute   | Type    | Key / Constraint | Description         |
| ----------- | ------- | ---------------- | ------------------- |
| `format_id` | INTEGER | PK               | Internal identifier |
| `name`      | TEXT    | UNIQUE, NOT NULL | Format name         |

Initial values may include:

```text
Paperback
Hardback
E-book
Audiobook
Other
```

Formats should be reference data rather than repeated free-text values.

---

# 15. LibraryEntry

`LibraryEntry` represents the user's relationship with a book.

This is one of the most important distinctions in the database.

A `Book` answers:

> What book is this?

A `LibraryEntry` answers:

> What relationship does the user currently have with this book?

## Attributes

| Attribute          | Type     | Key / Constraint | Description                    |
| ------------------ | -------- | ---------------- | ------------------------------ |
| `library_entry_id` | INTEGER  | PK               | Internal identifier            |
| `book_id`          | INTEGER  | FK, NOT NULL     | Associated book                |
| `format_id`        | INTEGER  | FK, NOT NULL     | Format of the user's copy      |
| `status`           | TEXT     | NOT NULL         | Current reading/library status |
| `date_added`       | DATE     | NOT NULL         | Date added to library          |
| `personal_notes`   | TEXT     | nullable         | Notes about ownership/copy     |
| `created_at`       | DATETIME | NOT NULL         | Creation time                  |
| `updated_at`       | DATETIME | NOT NULL         | Last modification time         |

Initial statuses:

```text
TBR
Currently Reading
Read
```

Additional statuses may be introduced later.

---

# 16. Why `is_owned` Is Not Required

The previous design contained:

```text
is_owned
```

This is no longer necessary.

A `LibraryEntry` already represents the user's library relationship with a book.

Therefore:

```text
Book
```

may exist because it was imported from an external catalogue.

But:

```text
LibraryEntry
```

exists when the book is part of the user's personal library.

This avoids contradictory states such as:

```text
LibraryEntry exists
is_owned = false
```

Instead:

```text
Book
   │
   ├── no LibraryEntry → not currently owned
   │
   └── LibraryEntry → present in user's library
```

This is cleaner and better supports future bookshop recommendations.

---

# 17. Multiple Formats and Copies

The design allows the same book to have multiple library entries.

For example:

```text
Book
└── Dracula

LibraryEntry
├── Paperback
├── E-book
└── Audiobook
```

This means the user can own multiple representations of the same book.

A suitable uniqueness rule should normally prevent accidental duplicate entries of the exact same format.

For example:

```text
UNIQUE(book_id, format_id)
```

may be used initially.

If the application later needs to distinguish multiple physical copies of the same format, this constraint can be reconsidered and a dedicated copy identifier can be introduced.

The MVP will avoid modelling individual physical copies unless there is a demonstrated need.

---

# 18. Library Status

`LibraryEntry.status` represents the user's current state in relation to the book.

Initial values:

```text
TBR
Currently Reading
Read
```

The application shall validate status values.

The status is intentionally stored on `LibraryEntry` because it represents the user's current relationship with the book.

Historical reading events are stored separately in `ReadingRecord`.

---

# 19. ReadingRecord

`ReadingRecord` represents one instance of the user reading a book.

This is separate from the current library status because the user may reread a book.

## Attributes

| Attribute           | Type     | Key / Constraint | Description                      |
| ------------------- | -------- | ---------------- | -------------------------------- |
| `reading_record_id` | INTEGER  | PK               | Internal identifier              |
| `book_id`           | INTEGER  | FK, NOT NULL     | Book being read                  |
| `library_entry_id`  | INTEGER  | FK, nullable     | Relevant library entry, if known |
| `date_started`      | DATE     | nullable         | Reading start date               |
| `date_finished`     | DATE     | nullable         | Reading finish date              |
| `rating`            | REAL     | nullable         | Rating for this reading          |
| `review`            | TEXT     | nullable         | Optional review                  |
| `created_at`        | DATETIME | NOT NULL         | Record creation time             |

The `book_id` is the fundamental relationship.

`library_entry_id` is optional because the user may read a book without the specific library copy being known or still existing.

---

# 20. Why ReadingRecord Uses `book_id`

Reading history should remain meaningful even if the user's ownership changes.

For example:

```text
2024
User owns Dracula
↓
Reads Dracula
↓
Sells Dracula
↓
2026
User buys another copy
↓
Reads Dracula again
```

The reading history still belongs to:

```text
Book → Dracula
```

rather than depending entirely on one particular library entry.

This makes rereading and changes in ownership easier to model.

---

# 21. Rereading

Multiple `ReadingRecord` rows may refer to the same book.

Example:

```text
Dracula

ReadingRecord 1
Started: 2024-10-01
Finished: 2024-10-07
Rating: 4

ReadingRecord 2
Started: 2026-08-01
Finished: 2026-08-04
Rating: 5
```

This supports future analytics such as:

* Number of rereads.
* Rereading frequency.
* Rating changes.
* Reading duration changes.
* Reading behaviour over time.

---

# 22. ReadingSession

`ReadingSession` records an individual period of reading.

A session may optionally be associated with a `ReadingRecord`.

## Attributes

| Attribute           | Type     | Key / Constraint | Description               |
| ------------------- | -------- | ---------------- | ------------------------- |
| `session_id`        | INTEGER  | PK               | Internal identifier       |
| `reading_record_id` | INTEGER  | FK, nullable     | Associated reading record |
| `started_at`        | DATETIME | NOT NULL         | Session start             |
| `ended_at`          | DATETIME | nullable         | Session end               |
| `duration_seconds`  | INTEGER  | nullable         | Calculated duration       |
| `source`            | TEXT     | NOT NULL         | How session was recorded  |
| `created_at`        | DATETIME | NOT NULL         | Creation time             |

Potential source values:

```text
Manual
Mobile
Fitbit
Other
```

The source should describe how the session entered Book Brain, not necessarily which physical device produced it.

---

# 23. Active Reading Sessions

An active reading session may temporarily have:

```text
ended_at = NULL
```

For example:

```text
Session
Started: 2026-08-11 14:10
Ended: NULL
```

Once the session is stopped, the application should record:

```text
ended_at
duration_seconds
```

The application should prevent invalid states such as an end time earlier than the start time.

Only appropriate active sessions should be allowed according to application rules.

---

# 24. Unassigned Reading Sessions

A reading session may initially have no associated book.

Example:

```text
ReadingSession

Started: 14:10
Finished: 14:52
Duration: 42 minutes
ReadingRecord: NULL
```

The user may later assign the session to the relevant reading record.

This is particularly important for future wearable functionality.

---

# 25. Reading Session and Current Book

The application may maintain a current reading book through `LibraryEntry.status = 'Currently Reading'`.

A future application service can use this information when associating sessions.

For example:

```text
LibraryEntry
Book: Dracula
Status: Currently Reading
```

then:

```text
Start Reading
      ↓
ReadingSession created
      ↓
Current reading record identified
      ↓
Session associated where appropriate
```

The database itself should not blindly assume that every session belongs to the current book. The application should make that decision and allow the user to correct it.

---

# 26. Reading Session Source

The `source` field supports future integrations.

Potential values include:

```text
Manual
Mobile
Web
Fitbit
WearOS
Other
```

The exact reference values can be expanded when integrations are implemented.

The MVP will primarily use:

```text
Manual
```

---

# 27. Note

The `Note` entity stores personal notes associated with books.

## Attributes

| Attribute    | Type     | Key / Constraint | Description            |
| ------------ | -------- | ---------------- | ---------------------- |
| `note_id`    | INTEGER  | PK               | Internal identifier    |
| `book_id`    | INTEGER  | FK, NOT NULL     | Associated book        |
| `content`    | TEXT     | NOT NULL         | Note content           |
| `created_at` | DATETIME | NOT NULL         | Creation time          |
| `updated_at` | DATETIME | NOT NULL         | Last modification time |

Potential uses include:

* Personal thoughts.
* Favourite quotes.
* Reading observations.
* Content warnings.
* Personal tags.

---

# 28. Future Note Expansion

The initial note model associates notes with a book.

If later requirements show that notes need to be attached to specific reading events or sessions, the model can be expanded.

For example:

```text
Note
 ├── book_id
 ├── reading_record_id
 └── reading_session_id
```

This should not be introduced until the functionality requires it.

---

# 29. Entity Relationships

The core relationships are:

```text
Author
   │
   │ many-to-many
   ▼
Book
   │
   ├──── many-to-many ──── Genre
   │
   ├──── many-to-many ──── Series
   │
   ├──── one-to-many ───── LibraryEntry
   │
   ├──── one-to-many ───── ReadingRecord
   │
   └──── one-to-many ───── Note

LibraryEntry
   │
   └──── many-to-one ───── Format

ReadingRecord
   │
   └──── one-to-many ───── ReadingSession
```

---

# 30. Relationship Summary

| Relationship                   | Cardinality                       |
| ------------------------------ | --------------------------------- |
| Book → Author                  | Many-to-many                      |
| Book → Genre                   | Many-to-many                      |
| Book → Series                  | Many-to-many                      |
| Book → LibraryEntry            | One-to-many                       |
| Book → ReadingRecord           | One-to-many                       |
| Book → Note                    | One-to-many                       |
| Format → LibraryEntry          | One-to-many                       |
| LibraryEntry → ReadingRecord   | One-to-many, optional association |
| ReadingRecord → ReadingSession | One-to-many                       |

The `ReadingRecord → LibraryEntry` relationship is optional because reading history should remain valid even when a specific library entry is unavailable.

---

# 31. Series-Aware Recommendations

Series information supports future recommendation functionality.

The database can distinguish between:

### Standalone book

```text
Book
└── No SeriesBook relationship
```

### Series book

```text
Series
├── Book 1
├── Book 2
└── Book 3
```

This allows future recommendations to consider whether the user:

* Wants a standalone book.
* Wants to start a series.
* Is already partway through a series.
* Owns the next book in a series.
* Needs to acquire the next book.
* Has completed a series.

---

# 32. Series Progress

Series progress can be calculated by joining:

```text
Series
   ↓
SeriesBook
   ↓
Book
   ↓
LibraryEntry
   ↓
ReadingRecord
```

For example:

```text
Example Trilogy

Book 1
Owned: Yes
Read: Yes

Book 2
Owned: Yes
Read: No

Book 3
Owned: No
```

This can support future questions such as:

> "Which series do I own completely?"

> "I've finished book 1. Do I own book 2?"

> "Which books do I need to buy to complete my series?"

The application should not assume that the highest numbered book represents the entire series.

---

# 33. Ownership and External Books

The database should distinguish between:

### Personal library

Represented through:

```text
LibraryEntry
```

and:

### External catalogue books

Represented by bibliographic information obtained from external sources.

A book can therefore exist in `Book` without being owned by the user.

For example:

```text
Book
└── Book X

LibraryEntry
└── None
```

means:

```text
Book X exists in the catalogue
but is not currently in the user's library.
```

This is important for bookshop recommendations.

The recommendation engine can compare external candidates against the user's existing `LibraryEntry` records.

---

# 34. External Book Recommendations

For a request such as:

> "I'm going to the bookshop. What should I buy?"

the system can use:

```text
User's books
       ↓
Reading history
       ↓
Ratings
       ↓
Genres
       ↓
Authors
       ↓
Recommendation engine
       ↓
External book catalogue
```

External candidate books do not need to be inserted into the user's library simply because they were considered as recommendations.

A future recommendation system may temporarily represent external candidates in application memory or through a dedicated recommendation entity.

A permanent `Recommendation` table is not required for the MVP.

---

# 35. Context-Aware Recommendation Data

The database provides structured data for recommendation contexts such as:

### Immediate reading

```text
LibraryEntry
 ├── Book
 ├── Format
 └── Status
```

### Short reading

```text
Book.page_count
```

### Genre preference

```text
Book
 └── BookGenre
      └── Genre
```

### Author preference

```text
Book
 └── BookAuthor
      └── Author
```

### Historical preference

```text
ReadingRecord
 └── rating
```

### Reading behaviour

```text
ReadingSession
 └── duration_seconds
```

---

# 36. Recommendation Filtering

The database should support application-level filtering such as:

```text
Owned
TBR
Unread
Currently Reading
Previously Read
Under 150 pages
Specific genres
Specific authors
Specific series
Not previously completed
```

These filters should be implemented by the application/recommendation layer rather than embedded into the database as hard-coded recommendation rules.

---

# 37. Recommendation Ranking

The database stores the information required for the recommendation engine to calculate scores.

For example:

```text
Book
 ├── page_count
 ├── genres
 ├── authors
 └── series

LibraryEntry
 ├── format
 └── status

ReadingRecord
 ├── rating
 ├── date_started
 └── date_finished

ReadingSession
 └── duration
```

The actual weighting algorithm belongs to the recommendation service.

The database should remain responsible for storing facts rather than recommendation decisions.

---

# 38. AI Librarian Architecture

The AI librarian should not access the SQLite database directly.

The intended architecture is:

```text
User
 ↓
LLM
 ↓
Application tools/services
 ↓
Repositories
 ↓
Database
 ↓
Results
 ↓
LLM
 ↓
User
```

Potential application tools may include:

```text
search_library()
get_book()
get_tbr()
get_current_book()
get_reading_statistics()
find_books_by_genre()
find_books_under_pages()
get_series_progress()
get_recommendations()
start_reading_session()
stop_reading_session()
search_external_books()
```

The exact tool architecture will be defined during AI development.

---

# 39. Database and AI Safety

The AI system should not directly modify database records.

For example, the AI should not be given unrestricted SQL access.

Instead:

```text
AI
 ↓
Controlled tool
 ↓
Validation
 ↓
Service
 ↓
Repository
 ↓
Database
```

This allows the application to:

* Validate inputs.
* Enforce business rules.
* Prevent accidental destructive operations.
* Maintain data integrity.
* Log actions where appropriate.

---

# 40. Referential Integrity

Foreign keys shall be used to maintain valid relationships.

SQLite foreign-key enforcement must be explicitly enabled:

```sql
PRAGMA foreign_keys = ON;
```

Foreign-key behaviour must be deliberately defined for each relationship.

Possible behaviours include:

```text
CASCADE
RESTRICT
SET NULL
```

The default behaviour should favour protecting historical user data.

For example, deleting a `Book` should not casually destroy valuable reading history.

The exact `ON DELETE` behaviour will be specified in the implementation schema.

---

# 41. Deletion Strategy

Deletion requires particular care because Book Brain contains historical information.

Potentially destructive operations should generally follow these principles:

### Deleting a library entry

Should not automatically delete:

* The book.
* Reading history.
* Reading sessions.

### Deleting a book

Should normally be restricted if historical reading information still depends on it.

### Deleting an author or genre

Should only be permitted when relationships have been handled appropriately.

The application should normally use explicit confirmation before destructive operations.

---

# 42. Data Validation

Important values should be validated at both application and database level where practical.

## Page count

Must not normally be negative.

```text
page_count >= 0
```

## Rating

Must remain within the defined rating scale.

The initial implementation will use:

```text
0.0–5.0
```

with the final allowed increments determined during implementation.

## Dates

A finish date should not occur before a start date.

## Reading sessions

```text
ended_at >= started_at
```

where `ended_at` exists.

## Duration

```text
duration_seconds >= 0
```

## Series number

Should normally be greater than zero.

## ISBN

ISBN-10 and ISBN-13 should be validated where practical.

---

# 43. Rating Design

Ratings belong to `ReadingRecord` rather than `Book`.

This is intentional.

The same book may receive different ratings during different rereads.

For example:

```text
ReadingRecord 1
Rating: 3.5

ReadingRecord 2
Rating: 5.0
```

This preserves historical information.

If the application later wants to display a "current overall rating", that can be calculated from reading records.

---

# 44. Reading Status Versus Reading History

`LibraryEntry.status` and `ReadingRecord` serve different purposes.

### LibraryEntry.status

Represents the current state:

```text
TBR
Currently Reading
Read
```

### ReadingRecord

Represents historical reading activity:

```text
Started
Finished
Rating
Review
```

For example:

```text
LibraryEntry
Status: Read

ReadingRecord 1
2024
Rating: 4

ReadingRecord 2
2026
Rating: 5
```

This allows the current state and historical activity to coexist without overwriting one another.

---

# 45. Analytics Support

The relational structure intentionally stores data required for future analytics.

## Reading volume

```text
ReadingRecord.date_finished
```

Supports:

* Books per month.
* Books per year.
* Reading trends.
* Completion patterns.

## Book length

```text
Book.page_count
```

Supports:

* Average pages.
* Median pages.
* Page-count distributions.
* Short/medium/long book analysis.
* Pages read.

## Genre

```text
Book
 ↓
BookGenre
 ↓
Genre
```

Supports:

* Books read by genre.
* Books owned by genre.
* Pages read by genre.
* Average rating by genre.
* Genre trends.

## Author

```text
Book
 ↓
BookAuthor
 ↓
Author
```

Supports:

* Most-read authors.
* Pages read by author.
* Average rating by author.

## Reading time

```text
ReadingSession.duration_seconds
```

Supports:

* Total reading time.
* Average session duration.
* Reading time per book.
* Reading time by genre.
* Reading time over time.

## Series

```text
Book
 ↓
SeriesBook
 ↓
Series
```

Supports:

* Series progress.
* Series completion.
* Books owned within series.
* Missing books.
* Series recommendations.

---

# 46. Calculated Analytics

The database should store underlying measurements rather than unnecessary calculated statistics.

For example:

The database stores:

```text
started_at
ended_at
duration_seconds
```

The application can calculate:

```text
Average session duration
Total reading time
Reading time per month
Reading time per genre
```

Similarly, the database stores:

```text
page_count
```

rather than:

```text
short_book = true
```

This prevents calculated categories from becoming stale when business rules change.

---

# 47. Power BI Considerations

The operational SQLite database remains the source of truth.

Power BI should consume structured application data rather than becoming responsible for storing application information.

Potential future analytical views include:

```text
vw_reading_statistics
vw_genre_statistics
vw_author_statistics
vw_monthly_reading
vw_book_statistics
vw_series_progress
vw_reading_sessions
```

These views are optional.

They should only be created if they simplify analytics or Power BI integration.

The core application must remain functional without Power BI.

---

# 48. Indexing

Indexes should be created for fields frequently searched, filtered or joined.

Likely indexes include:

```text
books.isbn13
books.isbn10
books.title
books.external_id
authors.name
genres.name
series.name

library_entries.book_id
library_entries.status
library_entries.format_id

reading_records.book_id
reading_records.date_finished

reading_sessions.reading_record_id
reading_sessions.started_at
```

Foreign-key columns should be indexed where appropriate for expected query patterns.

The final index set will be determined during implementation and adjusted based on actual query requirements.

Indexes should not be added indiscriminately.

---

# 49. Search Requirements

The database should support efficient searching by:

* Book title.
* Author.
* ISBN.
* Genre.
* Series.

Basic title and author searches can initially use ordinary indexed fields.

More advanced search, including semantic search, is a future concern.

The MVP does not require a vector database or embedding storage.

---

# 50. Future Semantic Search

If semantic search is introduced, books may eventually have associated embeddings.

A possible future structure could be:

```text
Book
 │
 └── Embedding
       ├── model
       ├── vector
       └── created_at
```

The exact implementation will depend on the selected technology.

Potential technologies include:

* PostgreSQL + pgvector.
* Chroma.
* Qdrant.
* Other suitable vector technologies.

Vector storage is **not required for the MVP**.

The embedding system should remain separate from the core relational model wherever practical.

---

# 51. Future Multi-User Support

The initial application is designed primarily as a single-user application.

If Book Brain becomes multi-user, a future `User` entity can be introduced.

The likely structure would become:

```text
User
 │
 └── LibraryEntry
       │
       ├── ReadingRecord
       └── ReadingSession
```

Bibliographic entities such as:

```text
Book
Author
Genre
Series
```

could potentially remain shared.

This would allow multiple users to maintain separate libraries while avoiding unnecessary duplication of bibliographic information.

User-specific notes and other personal data would then also require appropriate user relationships.

The MVP shall not introduce `User`.

---

# 52. Future Recommendation Entities

The recommendation engine does not initially require its own database tables.

Recommendations can initially be calculated dynamically:

```text
User request
 ↓
Recommendation service
 ↓
Database query
 ↓
Candidates
 ↓
Ranking
 ↓
Recommendation
```

If later versions require persistent recommendation history, the database may introduce entities such as:

```text
Recommendation
RecommendationFeedback
```

These should only be introduced when there is a demonstrated requirement, such as:

* Tracking recommendation performance.
* Recording user feedback.
* Measuring recommendation quality.
* Training/improving ranking algorithms.

---

# 53. Future AI Entities

The AI librarian does not initially require permanent conversation storage.

If conversation history becomes a required feature, future entities may include:

```text
AIConversation
AIMessage
```

These are deliberately excluded from the MVP.

The AI should initially operate using current application data and controlled tools.

---

# 54. Future External Book Source Entity

If Book Brain eventually integrates multiple external book services, a future entity could represent external identifiers more formally.

For example:

```text
ExternalBookSource
 ├── external_book_id
 ├── source
 └── book_id
```

This may become preferable to keeping all external identifiers directly on `Book`.

For the MVP, the simpler:

```text
external_id
external_source
```

approach is sufficient.

The schema can be normalised further when multiple external providers are actually required.

---

# 55. Future Wearable Integration

Wearable integration does not require a separate wearable database table in the MVP.

The important data is already represented by:

```text
ReadingSession
```

A wearable integration can create reading sessions with:

```text
source = Fitbit
```

and populate:

```text
started_at
ended_at
duration_seconds
```

The session can optionally be associated with a `ReadingRecord`.

This means wearable support can be added without redesigning the core reading-session model.

---

# 56. Data Provenance

Where practical, Book Brain should distinguish between different sources of information.

Potential sources include:

```text
User
External API
Application
Wearable
AI
```

For example, an external API may provide:

```text
Title
Publisher
Page count
Cover
```

while the user may later correct the page count.

The database should not allow AI-generated information to silently overwrite authoritative user data.

More detailed field-level provenance may be introduced later if required.

---

# 57. Data Ownership

The user's personal information includes:

* Library entries.
* Reading history.
* Ratings.
* Reviews.
* Notes.
* Reading sessions.
* Personal preferences.

These should remain under the user's control.

Bibliographic information may originate from external sources, but the user's personal library data must remain distinct.

---

# 58. Export Requirements

The database design should support future export of the user's personal data.

At minimum, the application should eventually be able to export:

```text
Books
Library entries
Reading records
Reading sessions
Notes
```

Suitable export formats may include:

* CSV.
* JSON.
* SQLite database backup.

Export functionality is part of the MVP acceptance criteria, although the exact export implementation will be determined during development.

---

# 59. Initial MVP Tables

The initial database is expected to contain:

```text
books
authors
genres
book_authors
book_genres
series
series_books
formats
library_entries
reading_records
reading_sessions
notes
```

These tables provide the foundation for the current MVP.

No AI, recommendation, user-account, vector, wearable-specific or conversation tables are required initially.

---

# 60. Future Schema Expansion

Potential future entities include:

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
```

Additional entities should only be introduced when the corresponding feature is being implemented.

The project should avoid adding speculative tables simply because the long-term architecture mentions a feature.

---

# 61. Normalisation

The database will use a normalised relational design.

The design separates:

* Books.
* Authors.
* Genres.
* Series.
* Formats.
* Library relationships.
* Reading history.
* Reading sessions.
* Notes.

Many-to-many relationships are represented through junction tables.

This reduces unnecessary duplication and makes the database easier to maintain.

The design should generally target at least third normal form for the core transactional data, while allowing later analytical views or derived datasets where they provide practical benefits.

---

# 62. Current Database Architecture

The current operational data flow is:

```text
Python application
       │
       ▼
Repositories / database layer
       │
       ▼
SQLite
       │
       ├── Books
       ├── Library
       ├── Reading history
       ├── Reading sessions
       └── Notes
```

The database does not currently depend on:

* FastAPI.
* React.
* AI.
* Power BI.
* External book APIs.
* Mobile applications.
* Wearables.
* Vector databases.

Those systems may consume or interact with the database in later development phases.

---

# 63. Future Application Architecture

As Book Brain develops, the database will sit underneath the application services:

```text
Frontend / Mobile / AI
          │
          ▼
       FastAPI
          │
          ▼
      Services
          │
          ▼
     Repositories
          │
          ▼
       Database
```

The database remains responsible for persistence and integrity.

Business rules should remain in application services rather than being unnecessarily embedded in SQL.

---

# 64. PostgreSQL Migration

SQLite is the initial database technology.

A future migration to PostgreSQL may become appropriate when requirements include:

* Multiple users.
* Remote access.
* Cloud deployment.
* Higher concurrency.
* Server-based operation.
* Vector search through `pgvector`.

The relational structure should be designed so that migration is primarily a database implementation task rather than requiring a complete application redesign.

SQLite-specific behaviour should therefore be kept isolated where practical.

---

# 65. Initial Database Design Decisions

Book Brain will use a **normalised relational database design** centred around:

```text
Book
LibraryEntry
ReadingRecord
ReadingSession
```

These represent four distinct concepts:

### Book

What the book is.

### LibraryEntry

The user's relationship with the book.

### ReadingRecord

A particular instance of reading the book.

### ReadingSession

An individual period of reading.

This separation is fundamental to the design.

The database also separates reusable bibliographic information:

```text
Author
Genre
Series
```

and library reference information:

```text
Format
```

---

# 66. Design Decisions Summary

The current database design intentionally follows these rules:

1. `Book` stores bibliographic information.
2. `LibraryEntry` represents the user's library relationship.
3. `is_owned` is not required because a library entry represents ownership/library membership.
4. Multiple formats of the same book are supported.
5. Exact duplicate format entries should normally be prevented.
6. `ReadingRecord` stores individual reading events.
7. Multiple reading records allow rereading.
8. Ratings belong to reading records rather than permanently to books.
9. `ReadingSession` stores individual periods of reading.
10. Reading sessions may initially be unassigned.
11. Reading sessions can later be associated with reading records.
12. External catalogue books can exist without library entries.
13. Recommendations for books not owned can therefore use external catalogue data.
14. Recommendation rules belong to the application layer.
15. AI does not directly control the database.
16. AI accesses library information through controlled application functionality.
17. Calculated statistics should normally be generated rather than permanently stored.
18. Vector storage is not required for the MVP.
19. User accounts are not required for the MVP.
20. Wearable-specific tables are not required for the MVP.
21. Recommendation and AI conversation tables are not required for the MVP.
22. SQLite is the initial database.
23. PostgreSQL is the planned future migration target if requirements justify it.

---

# 67. MVP Database Scope

The MVP database shall support:

* Book creation.
* Book retrieval.
* Book updating.
* Book deletion.
* Author relationships.
* Genre relationships.
* Series relationships.
* Library entries.
* Formats.
* Reading statuses.
* Ratings.
* Reading dates.
* Reviews/notes.
* Reading sessions.
* Manual reading-session tracking.
* Basic statistics.
* Data export.
* Automated testing.

The MVP database shall **not** require:

* User accounts.
* External API-specific tables.
* Embeddings.
* Vector databases.
* Recommendation history.
* Recommendation feedback.
* AI conversations.
* AI messages.
* Wearable-specific entities.
* Cloud infrastructure.

---

# 68. Next Step

The next stage is to convert this conceptual design into the actual SQLite schema.

Implementation should include:

1. Create the SQL `CREATE TABLE` statements.
2. Define primary keys.
3. Define foreign keys.
4. Define `NOT NULL` constraints.
5. Define `UNIQUE` constraints.
6. Define appropriate `CHECK` constraints.
7. Define `ON DELETE` behaviour.
8. Define indexes.
9. Enable SQLite foreign-key enforcement.
10. Insert required reference data such as formats.
11. Create the initial database.
12. Test the schema with representative data.
13. Test relationships and deletion behaviour.
14. Test multiple formats for the same book.
15. Test rereading.
16. Test unassigned reading sessions.
17. Test basic analytics queries.
18. Test data export.
19. Update this document if implementation decisions differ from the conceptual design.

---

# 69. Final Conceptual Model

The core Book Brain data model can be summarised as:

```text
                    ┌─────────────┐
                    │    Author   │
                    └──────┬──────┘
                           │
                      BookAuthor
                           │
                           ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│    Genre    │──────│    Book     │──────│   Series    │
└─────────────┘      └──────┬──────┘      └─────────────┘
                             │
                ┌────────────┼─────────────┐
                │            │             │
                ▼            ▼             ▼
         LibraryEntry      Note      ReadingRecord
                │                         │
                │                         ▼
                │                  ReadingSession
                │
                ▼
             Format
```

The most important conceptual chain is:

```text
Book
  ↓
LibraryEntry
  ↓
ReadingRecord
  ↓
ReadingSession
```

This allows Book Brain to answer four different questions:

```text
What is this book?
        ↓
Book

Do I have it?
        ↓
LibraryEntry

Have I read it?
        ↓
ReadingRecord

How did I spend my reading time?
        ↓
ReadingSession
```

This model provides the foundation for the current MVP while leaving a clear path toward analytics, recommendations, external book discovery, AI, web/mobile interfaces and wearable integration.
