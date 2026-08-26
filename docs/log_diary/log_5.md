# Development Session 05 — ISBN, Edition, Barcode and Copy Structure

**## Completed**

- Reviewed the distinction between ISBN-10 and ISBN-13.

- Added an `editions` table to separate publication/edition information from the underlying book.

- Added ISBN fields to `editions`:

* `isbn_10`
* `isbn_13`

- Changed the library-item structure from:

```text
Book → LibraryEntry
```

to:

```text
Book → Edition → Copy
```

- Added the `copy` table to represent an individual library item.

- Updated `copy` so it references an `edition` through `edition_id`.

- Kept format, source and price associated with the individual copy.

- Confirmed that ISBN information belongs to an edition rather than an individual copy.

- Updated the relevant CRUD code to account for the new `edition_id` relationship.

- Confirmed that the database can support the two ISBN formats required for the project.

**## Decisions**

- A **Book** represents the underlying bibliographic work.

- An **Edition** represents a specific publication/edition of that book.

- A **Copy** represents an individual copy held in the user's library.

- ISBN-10 and ISBN-13 belong to the edition.

- Format, source and price belong to the copy.

- The intended relationship is:

```text
Book
  │
  └── Edition
        │
        └── Copy
```

- Barcode scanning itself will remain a future feature. The current work is focused on making the database capable of representing the relevant book identification data.

**## Problems encountered**

- Existing CRUD code still expected `copy` to contain `book_id`.

- The new schema replaced this relationship with `edition_id`.

- CRUD functions therefore needed to be updated to match the new database structure.

- The schema change demonstrated again that changing a table definition does not automatically update the Python code that interacts with it.

**## Lessons learned**

- Database schema changes often require corresponding changes in CRUD functions.

- `CREATE TABLE IF NOT EXISTS` does not modify an existing SQLite table.

- ISBN identifies an edition rather than an individual physical copy.

- Separating Book, Edition and Copy allows multiple editions of the same book and multiple copies of an edition to be represented correctly.

- Database relationships should represent the real-world concepts being modelled rather than simply extending an existing table.

- When changing the database structure, related queries and CRUD functions must be checked before continuing with the application UI.

**## Tests**

- Database schema was updated successfully.

- Edition structure was created successfully.

- ISBN-10 and ISBN-13 fields are available at edition level.

- Copy records now use `edition_id`.

- Existing database functionality was kept working while the structure was changed.

- CRUD code was checked against the new Book → Edition → Copy relationship.

**## Files changed**

- `src/database/schema.py`

- `src/database/crud.py`

**## Documentation updates**

- Development log updated with Session 05.

- Database documentation should be reviewed to reflect the new:

```text
Book → Edition → Copy
```

relationship.

**## Git commit**

```text
feat: add edition and copy structure with ISBN support
```

**## Next development task**

Validation.

Next focus:

- Identify where validation is currently missing.

- Determine which fields should be required.

- Determine which fields may legitimately be `NULL`.

- Validate ISBN-10 and ISBN-13 appropriately.

- Determine what validation belongs in Streamlit, Python/CRUD and SQLite.

- Implement the smallest sensible validation improvements.
