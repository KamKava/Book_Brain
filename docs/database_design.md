# Book Brain — Database Design

**Project status:** Initial development
**Version:** 0.2
**Last updated:** August 2026

---

# 1. Purpose

This document defines the initial relational database design for Book Brain.

The database will provide the authoritative storage layer for:

* Books.
* Authors.
* Genres.
* Series.
* Book formats.
* User library entries.
* Reading status.
* Ratings.
* Reading history.
* Reading sessions.
* Notes.

The design is intended to support the current MVP while allowing future development of:

* External book API integration.
* ISBN lookup.
* Barcode scanning.
* Reading analytics.
* Power BI.
* Personalised recommendations.
* Series-aware recommendations.
* Semantic search.
* AI librarian functionality.
* Web applications.
* Mobile applications.
* Wearable/device integration.

The initial implementation will use **SQLite**.

A future migration to **PostgreSQL** should be possible without fundamentally redesigning the data model.

---

# 2. Database Design Principles

## 2.1 Separate Bibliographic Information from User Information

Information describing a book should be separated from information describing the user's relationship with that book.

For example:

```text
BOOK

Title: Dracula
Author: Bram Stoker
Pages: 336
Genre: Horror
```

is different from:

```text
LIBRARY ENTRY

Owned: Yes
Format: Paperback
Status: TBR
Date added: 2026-08-01
```

This separation is important because bibliographic information describes the book itself, while the library entry describes the user's relationship with it.

---

## 2.2 Database as the Source of Truth

The database shall be the authoritative source for the user's personal library information.

This includes:

* Books owned.
* TBR status.
* Current reading status.
* Reading history.
* Ratings.
* Reading dates.
* Reading sessions.
* Notes.
* Formats owned.

The AI system shall not be treated as the authoritative source for this information.

---

## 2.3 Avoid Unnecessary Duplication

Reusable information such as authors, genres and series should be stored separately and linked through relationships.

This avoids repeatedly storing the same information.

---

## 2.4 Support Many-to-Many Relationships

A book may have:

* Multiple authors.
* Multiple genres.
* Potentially multiple series relationships in unusual publishing situations.

An author may have multiple books.

A genre may contain many books.

Junction tables will therefore be used where appropriate.

---

## 2.5 Support Incomplete Metadata

External APIs may not provide complete information.

A book should remain valid if information such as:

* ISBN.
* Page count.
* Publisher.
* Description.
* Publication date.
* Cover image.

is unavailable.

Missing information must not prevent the book from being stored.

---

## 2.6 Design for Analytics

The database shall store structured information that can support future analytics.

Examples include:

* Page count.
* Publication year.
* Reading dates.
* Reading duration.
* Genre.
* Author.
* Rating.
* Reading status.

This allows Book Brain to calculate meaningful statistics without storing pre-calculated values unnecessarily.

---

## 2.7 Design for Recommendations

The database shall provide sufficient information for the future recommendation system to distinguish between:

* Books the user owns.
* Books the user has read.
* Books currently being read.
* Books on the TBR.
* Books the user has rated highly.
* Books the user does not own.
* Standalone books.
* Books belonging to a series.
* The user's position within a series.
* Book length.

This is particularly important for context-aware recommendations.

---

# 3. Entity Model

The initial database will contain the following core entities:

### Bibliographic entities

1. `Book`
2. `Author`
3. `Genre`
4. `Series`

### Library entities

5. `LibraryEntry`
6. `Format`

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
   BookGenre              ┌────┴────┐             SeriesBook
                           │         │
                           ▼         ▼
                    LibraryEntry    Note
                           │
                           ▼
                       ReadingRecord
                           │
                           ▼
                      ReadingSession

                    LibraryEntry
                           │
                           ▼
                         Format
```

---

# 4. Book

The `Book` entity represents the bibliographic identity of a book.

It contains information about the work/edition that is useful regardless of whether the user owns it.

## Attributes

| Attribute          | Type     | Key    | Description                     |
| ------------------ | -------- | ------ | ------------------------------- |
| `book_id`          | INTEGER  | PK     | Internal unique identifier      |
| `isbn13`           | TEXT     | Unique | ISBN-13 where available         |
| `isbn10`           | TEXT     | Unique | ISBN-10 where available         |
| `title`            | TEXT     |        | Book title                      |
| `subtitle`         | TEXT     |        | Optional subtitle               |
| `publisher`        | TEXT     |        | Publisher                       |
| `publication_date` | TEXT     |        | Publication date where known    |
| `page_count`       | INTEGER  |        | Number of pages                 |
| `description`      | TEXT     |        | Book description                |
| `language`         | TEXT     |        | Book language                   |
| `cover_url`        | TEXT     |        | External cover image URL        |
| `external_id`      | TEXT     |        | Identifier from an external API |
| `created_at`       | DATETIME |        | Record creation time            |
| `updated_at`       | DATETIME |        | Last modification time          |

---

# 5. Page Count

`page_count` is a core book attribute.

It is required for future functionality including:

* Short-read recommendations.
* Long-read recommendations.
* Reading statistics.
* Average book length.
* Page-count distributions.
* Pages read.
* Book-length trends.

For example, a future recommendation request might be:

> "I want something short for the beach."

The recommendation engine can use `page_count` when filtering and ranking candidates.

Potential categories may eventually include:

```text
Under 100 pages
100–199 pages
200–299 pages
300–399 pages
400–499 pages
500+ pages
```

These categories should be generated by application logic rather than permanently stored in the database.

This allows thresholds to change without modifying existing data.

`page_count` should be nullable because external metadata may not provide it.

---

# 6. ISBN

ISBN-10 and ISBN-13 will be stored as optional external identifiers.

ISBN should not be the primary key because:

* Some books do not have an ISBN.
* Older books may use other identifiers.
* ISBNs can represent specific editions.
* External metadata may not provide an ISBN.

The internal `book_id` will therefore remain the primary key.

ISBN values should be indexed for efficient lookup.

---

# 7. Author

The `Author` entity stores author information independently from books.

## Attributes

| Attribute    | Type     | Key | Description                |
| ------------ | -------- | --- | -------------------------- |
| `author_id`  | INTEGER  | PK  | Internal unique identifier |
| `name`       | TEXT     |     | Author name                |
| `created_at` | DATETIME |     | Record creation time       |

An author may be associated with many books.

---

# 8. BookAuthor

`BookAuthor` represents the many-to-many relationship between books and authors.

## Attributes

| Attribute     | Type    | Key   | Description       |
| ------------- | ------- | ----- | ----------------- |
| `book_id`     | INTEGER | PK/FK | Associated book   |
| `author_id`   | INTEGER | PK/FK | Associated author |
| `author_role` | TEXT    |       | Optional role     |

The composite primary key is:

```text
(book_id, author_id)
```

The optional `author_role` can later support roles such as:

* Author.
* Translator.
* Editor.
* Illustrator.

---

# 9. Genre

The `Genre` entity stores reusable genres or categories.

## Attributes

| Attribute  | Type    | Key    | Description         |
| ---------- | ------- | ------ | ------------------- |
| `genre_id` | INTEGER | PK     | Internal identifier |
| `name`     | TEXT    | Unique | Genre/category name |

Examples:

```text
Horror
Dark Romance
Fantasy
Science Fiction
Literary Fiction
Mystery
Historical Fiction
```

A book may have multiple genres.

---

# 10. BookGenre

`BookGenre` represents the many-to-many relationship between books and genres.

## Attributes

| Attribute  | Type    | Key   | Description      |
| ---------- | ------- | ----- | ---------------- |
| `book_id`  | INTEGER | PK/FK | Associated book  |
| `genre_id` | INTEGER | PK/FK | Associated genre |

Composite primary key:

```text
(book_id, genre_id)
```

This supports queries such as:

> "Show me horror books I own."

and:

> "Which genres do I read most?"

---

# 11. Series

The `Series` entity represents a collection of books belonging to a named series.

## Attributes

| Attribute     | Type     | Key    | Description                 |
| ------------- | -------- | ------ | --------------------------- |
| `series_id`   | INTEGER  | PK     | Internal identifier         |
| `name`        | TEXT     | Unique | Series name                 |
| `description` | TEXT     |        | Optional series description |
| `created_at`  | DATETIME |        | Creation time               |

Examples:

```text
The Lord of the Rings
Harry Potter
The Witcher
Discworld
```

A book does not have to belong to a series.

A missing series relationship therefore represents a standalone book unless additional metadata indicates otherwise.

---

# 12. SeriesBook

`SeriesBook` represents the relationship between books and series.

## Attributes

| Attribute       | Type    | Key   | Description                |
| --------------- | ------- | ----- | -------------------------- |
| `series_id`     | INTEGER | PK/FK | Associated series          |
| `book_id`       | INTEGER | PK/FK | Associated book            |
| `series_number` | REAL    |       | Position within the series |

Composite primary key:

```text
(series_id, book_id)
```

`series_number` uses `REAL` rather than `INTEGER` to allow values such as:

```text
1
2
2.5
3
```

This can represent novellas, intermediate stories or other numbering systems.

---

# 13. Series-Aware Recommendations

Series information is considered important to the recommendation system.

The application should eventually be able to distinguish between:

### Standalone

```text
Book
 └── No series relationship
```

### Series book

```text
Series
 ├── Book 1
 ├── Book 2
 └── Book 3
```

This allows future recommendations to consider context.

For example:

> "I want a self-contained beach read."

The recommendation engine should be able to prefer standalone books.

Alternatively:

> "I'm happy to start a series."

Series books can then be considered.

---

# 14. Series Completion

The database design should allow Book Brain to determine whether the user owns multiple books in a series.

For example:

```text
Series: Example Trilogy

Book 1
Owned: Yes
Read: Yes

Book 2
Owned: Yes
Read: No

Book 3
Owned: No
```

This information can support future questions such as:

> "Which series do I own completely?"

> "I've finished book 1. Do I own book 2?"

> "What should I buy to complete my series?"

The system should not assume that a series is complete based only on the highest numbered book the user owns, because series may contain novellas, companion books and changing publication plans.

---

# 15. Format

The `Format` entity represents the format of a library entry.

## Attributes

| Attribute   | Type    | Key    | Description         |
| ----------- | ------- | ------ | ------------------- |
| `format_id` | INTEGER | PK     | Internal identifier |
| `name`      | TEXT    | Unique | Format name         |

Initial values may include:

```text
Paperback
Hardback
E-book
Audiobook
Other
```

---

# 16. LibraryEntry

`LibraryEntry` represents the user's relationship with a book.

This is distinct from the `Book` entity.

## Attributes

| Attribute          | Type     | Key | Description                        |
| ------------------ | -------- | --- | ---------------------------------- |
| `library_entry_id` | INTEGER  | PK  | Internal identifier                |
| `book_id`          | INTEGER  | FK  | Associated book                    |
| `format_id`        | INTEGER  | FK  | Format owned                       |
| `status`           | TEXT     |     | Current library/reading status     |
| `date_added`       | DATE     |     | Date added                         |
| `is_owned`         | BOOLEAN  |     | Whether the user currently owns it |
| `personal_notes`   | TEXT     |     | Optional personal notes            |
| `created_at`       | DATETIME |     | Creation time                      |
| `updated_at`       | DATETIME |     | Last modification                  |

Initial statuses:

```text
TBR
Currently Reading
Read
```

Additional statuses may be added later.

---

# 17. Multiple Copies and Formats

The separation between `Book` and `LibraryEntry` allows a user to own multiple representations of the same book.

For example:

```text
Book
 └── Dracula

LibraryEntry
 ├── Paperback
 ├── E-book
 └── Audiobook
```

This allows Book Brain to distinguish the underlying book from the user's physical/digital copies.

The exact rules governing duplicate library entries will be determined during implementation.

---

# 18. ReadingRecord

`ReadingRecord` represents an instance of the user reading a book.

A separate record is required because the user may reread a book.

## Attributes

| Attribute           | Type     | Key | Description              |
| ------------------- | -------- | --- | ------------------------ |
| `reading_record_id` | INTEGER  | PK  | Internal identifier      |
| `library_entry_id`  | INTEGER  | FK  | Associated library entry |
| `date_started`      | DATE     |     | Reading start date       |
| `date_finished`     | DATE     |     | Reading finish date      |
| `rating`            | REAL     |     | User rating              |
| `review`            | TEXT     |     | Optional review          |
| `created_at`        | DATETIME |     | Creation time            |

The rating will initially use a 0–5 scale.

Ratings may be stored in increments such as:

```text
1
2
3
4
5
```

or:

```text
0.5
1.0
1.5
...
5.0
```

The final scale will be confirmed during implementation.

---

# 19. Reading History

Reading history is represented by `ReadingRecord`.

This allows multiple reading events for the same book.

Example:

```text
Dracula

Reading Record 1
Started: 2024-10-01
Finished: 2024-10-07
Rating: 4

Reading Record 2
Started: 2026-08-01
Finished: 2026-08-04
Rating: 5
```

This allows future analytics such as:

* Books reread.
* Rereading frequency.
* Rating changes.
* Reading duration changes.
* Reading habits over time.

---

# 20. ReadingSession

`ReadingSession` records an individual period of reading.

This is separate from the overall reading record.

## Attributes

| Attribute           | Type     | Key          | Description               |
| ------------------- | -------- | ------------ | ------------------------- |
| `session_id`        | INTEGER  | PK           | Internal identifier       |
| `reading_record_id` | INTEGER  | FK, nullable | Associated reading record |
| `started_at`        | DATETIME |              | Session start             |
| `ended_at`          | DATETIME |              | Session end               |
| `duration_seconds`  | INTEGER  |              | Session duration          |
| `source`            | TEXT     |              | How session was recorded  |
| `created_at`        | DATETIME |              | Creation time             |

Potential source values:

```text
Manual
Mobile
Fitbit
Other
```

---

# 21. Unassigned Reading Sessions

A reading session may initially have no associated book.

For example:

```text
Reading Session

Started: 14:10
Finished: 14:52
Duration: 42 minutes
Book: NULL
```

The user may assign the session to a book later.

This design supports future wearable functionality without requiring the wearable to identify the book automatically.

---

# 22. Future Fitbit Integration

A future wearable integration may allow the user to start and stop a reading session from a supported device.

Potential workflow:

```text
Fitbit
   ↓
Start Reading
   ↓
Reading session
   ↓
Stop Reading
   ↓
Synchronise
   ↓
Book Brain
```

If the user has a currently selected book:

```text
Currently Reading:
Dracula
```

the session may automatically be associated with the relevant reading record.

Otherwise, the session may remain unassigned until the user chooses a book.

The technical feasibility of direct Fitbit integration must be investigated before implementation.

---

# 23. Note

The `Note` entity stores personal notes associated with books.

## Attributes

| Attribute    | Type     | Key | Description         |
| ------------ | -------- | --- | ------------------- |
| `note_id`    | INTEGER  | PK  | Internal identifier |
| `book_id`    | INTEGER  | FK  | Associated book     |
| `content`    | TEXT     |     | Note content        |
| `created_at` | DATETIME |     | Creation time       |
| `updated_at` | DATETIME |     | Last modification   |

Potential uses include:

* Personal thoughts.
* Favourite quotes.
* Reading observations.
* Content warnings.
* Personal tags.

The note model may be expanded later if notes need to be associated with specific reading sessions.

---

# 24. Entity Relationships

The primary relationships are:

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
   └──── one-to-many ───── Note

LibraryEntry
   │
   ├──── many-to-one ───── Format
   │
   └──── one-to-many ───── ReadingRecord
                                │
                                └──── one-to-many ─── ReadingSession
```

---

# 25. Relationship Summary

| Relationship                   | Type         |
| ------------------------------ | ------------ |
| Book → Author                  | Many-to-many |
| Book → Genre                   | Many-to-many |
| Book → Series                  | Many-to-many |
| Book → LibraryEntry            | One-to-many  |
| Book → Note                    | One-to-many  |
| Format → LibraryEntry          | One-to-many  |
| LibraryEntry → ReadingRecord   | One-to-many  |
| ReadingRecord → ReadingSession | One-to-many  |

---

# 26. Referential Integrity

Foreign keys shall be used to maintain valid relationships.

SQLite foreign key enforcement should be explicitly enabled:

```sql
PRAGMA foreign_keys = ON;
```

Deletion behaviour must be defined carefully.

For example, deleting a book should not unintentionally destroy historical reading information.

Appropriate behaviours may include:

* `CASCADE`
* `RESTRICT`
* `SET NULL`

The final behaviour will be defined when the SQL schema is implemented.

---

# 27. Indexing

Indexes should be created for fields that will frequently be searched or joined.

Likely indexes include:

```text
books.isbn13
books.isbn10
books.title
authors.name
genres.name
series.name
library_entries.book_id
library_entries.status
reading_records.date_finished
reading_sessions.started_at
```

The final indexes will be determined during implementation based on actual query requirements.

---

# 28. Data Validation

Important values should be validated at both application and database level where practical.

Examples:

### Page count

Must not normally be negative.

### Rating

Must remain within the defined rating scale.

### Dates

A finish date should not normally occur before the start date.

### Reading session

`ended_at` should not occur before `started_at`.

### Duration

Duration should not be negative.

### Series number

Should normally be greater than zero.

### ISBN

ISBN-10 and ISBN-13 should be validated where possible.

---

# 29. Analytics Support

The relational structure intentionally stores data required for future analytics.

## Reading volume

`ReadingRecord.date_finished`

Can support:

* Books per month.
* Books per year.
* Reading trends.

## Book length

`Book.page_count`

Can support:

* Average pages.
* Median pages.
* Pages read.
* Short/medium/long book analysis.
* Page-count distributions.

## Genre

`Book → BookGenre → Genre`

Can support:

* Books read by genre.
* Books owned by genre.
* Pages read by genre.
* Average rating by genre.
* Genre trends.

## Author

`Book → BookAuthor → Author`

Can support:

* Most-read authors.
* Pages read by author.
* Average author rating.

## Reading time

`ReadingSession.duration_seconds`

Can support:

* Total reading time.
* Average session duration.
* Reading time per book.
* Reading time by genre.
* Reading time over time.

## Series

`Book → SeriesBook → Series`

Can support:

* Series progress.
* Series completion.
* Books owned within each series.
* Missing books.
* Series-related recommendations.

---

# 30. Power BI Considerations

The operational database will remain the source of truth.

Power BI will consume structured data rather than becoming responsible for application data storage.

Future analytical views may include:

```text
vw_reading_statistics
vw_genre_statistics
vw_author_statistics
vw_monthly_reading
vw_book_statistics
vw_series_progress
```

These views may simplify Power BI integration.

The core application will remain functional without Power BI.

---

# 31. Recommendation System Requirements

The database is designed to support a future recommendation engine.

Potential inputs include:

```text
Book
 ├── Genres
 ├── Authors
 ├── Page count
 ├── Description
 ├── Publication information
 └── Series

LibraryEntry
 ├── Ownership
 ├── Status
 └── Format

ReadingRecord
 ├── Rating
 ├── Dates
 └── Reading history

ReadingSession
 └── Reading behaviour
```

This allows the recommendation engine to distinguish between:

```text
Owned books
TBR books
Currently reading
Completed books
Highly rated books
Unread books
Standalone books
Series books
Books within completed/incomplete series
Books of different lengths
```

---

# 32. Context-Aware Recommendation Example

A request such as:

> "I'm going to the beach. What should I read?"

could eventually produce constraints such as:

```text
Available:
    Books owned by user

Preferred:
    Unread/TBR
    User's preferred genres
    Shorter books
    Good historical ratings

Potentially preferred:
    Standalone books
    Books already physically owned

Avoid:
    Books already read
    Currently reading
    Very long books
```

The database provides the structured information required to apply these constraints.

---

# 33. Bookshop Recommendation Example

A different request:

> "I'm going to the bookshop. What should I buy?"

may use:

```text
User reading history
        +
User ratings
        +
Genres
        +
Authors
        +
Series
        +
Books already owned
        ↓
Recommendation engine
        ↓
External book catalogue
```

The system can then identify books that match the user's preferences while excluding books already present in the user's library.

---

# 34. AI Librarian Considerations

The AI librarian should access database information through controlled application services rather than directly manipulating the database.

Conceptually:

```text
User
 ↓
LLM
 ↓
Application tools/services
 ↓
Database
 ↓
Results
 ↓
LLM
 ↓
User
```

Example tool operations may eventually include:

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

# 35. Future Multi-User Support

The initial design is intended primarily for a single-user application.

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

This allows multiple users to maintain separate libraries while avoiding unnecessary duplication of book metadata.

---

# 36. Future Semantic Search

If semantic search is introduced, books may eventually have associated embeddings.

A future structure could be:

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
* Other suitable vector databases.

Vector storage is **not required for the MVP**.

---

# 37. Future Entities

Potential future entities include:

```text
User
Embedding
ExternalBookSource
Recommendation
RecommendationFeedback
ReadingGoal
ReadingChallenge
AIConversation
AIMessage
```

These should not be added to the MVP database until the corresponding functionality is actually developed.

---

# 38. Initial MVP Tables

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

These tables provide the foundation for the core Book Brain functionality.

---

# 39. Future Schema Expansion

The database can later be expanded with functionality such as:

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

Additional tables should be introduced only when justified by an actual feature.

---

# 40. Initial Database Design Decision

Book Brain will use a **normalised relational database design** centred around the `Book` and `LibraryEntry` entities.

The design deliberately separates:

* Bibliographic information.
* Authors.
* Genres.
* Series.
* Ownership.
* Formats.
* Reading history.
* Reading sessions.
* Notes.

This structure provides a foundation for:

* Core library management.
* Reading analytics.
* Power BI.
* Recommendation algorithms.
* Series-aware recommendations.
* Semantic search.
* AI librarian functionality.
* Mobile applications.
* Future wearable integration.

The initial implementation will use SQLite.

PostgreSQL remains the planned future migration target if the application's requirements justify a server-based database.

---

# 41. Next Step

The next stage is to convert this conceptual database design into an actual SQLite schema.

Implementation should include:

1. Create the SQL `CREATE TABLE` statements.
2. Define primary keys.
3. Define foreign keys.
4. Define constraints.
5. Define indexes.
6. Enable SQLite foreign-key enforcement.
7. Create the initial database.
8. Insert required reference data such as formats.
9. Test the schema.
10. Update this document if implementation decisions differ from the design.
