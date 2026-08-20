# Development Session 03 — Authors and Book-Author Relationships

## Completed

- Added `authors` table.
- Added `book_authors` junction table.
- Added UNIQUE constraint to `authors.name`.
- Added `add_author()` CRUD function.
- Added `get_author_by_name()` CRUD function.
- Added `add_book_author()` CRUD function.
- Added author input to the Streamlit "Add a book" form.
- When adding a book:
  - Existing authors are looked up by name.
  - A new author is created if no matching author exists.
  - The resulting author is linked to the book through `book_authors`.
- Successfully tested adding a book with an author.

## Database changes

New tables:

### authors

- `author_id` — primary key
- `name` — required and unique

### book_authors

- `book_id` — foreign key to `books`
- `author_id` — foreign key to `authors`
- Composite primary key on (`book_id`, `author_id`)

This implements a many-to-many relationship between books and authors.

A book can have multiple authors, and an author can have multiple books.

## Problems encountered

### SQLite schema changes

`CREATE TABLE IF NOT EXISTS` does not modify an existing table.

Adding columns or changing an existing table definition therefore does not automatically update an existing SQLite database.

During early development, controlled database resets may be used when appropriate. Later, proper database migrations should be introduced.

### Duplicate authors

Attempting to insert an author that already existed produced:

`sqlite3.IntegrityError: UNIQUE constraint failed: authors.name`

This was expected behaviour because author names are UNIQUE.

The application now checks whether an author already exists before creating a new one.

### Database locking

A `database is locked` error was encountered during development.

This reinforced the importance of closing SQLite connections and avoiding multiple processes/connections writing to the database unnecessarily during development.

## Lessons learned

- `CREATE TABLE IF NOT EXISTS` only creates missing tables; it does not migrate existing tables.
- Many-to-many relationships are represented using a junction table.
- Foreign keys should reference IDs rather than storing duplicated author names in books.
- UNIQUE constraints can protect database integrity, but application logic should handle expected duplicate cases cleanly.
- Streamlit reruns the application script, so database operations placed directly in the script must be designed carefully.
- CRUD functions should remain responsible for database operations, while Streamlit handles user interaction.

## Tests

Successfully tested:

- Creating an author.
- Looking up an existing author by name.
- Reusing an existing author rather than creating a duplicate.
- Creating a book.
- Creating a `book_authors` relationship between the book and author.
- Adding the book to the library.

## Files changed

- `src/database/schema.py`
- `src/database/crud.py`
- `src/app.py`
- `docs/development-log.md`

## Git commit

Suggested commit:

`feat: add author management and book-author relationships`

## Next development task

Review the current database and application state before continuing with additional functionality.

Potential next steps include improving author handling/display and then continuing with the remaining library-management functionality.