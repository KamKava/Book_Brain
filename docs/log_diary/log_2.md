# Development Session 02 — Library Entry Foundation

## Completed

- Added initial/reference data for book formats:
  - Paperback
  - Hardcover
  - Ebook
  - Audiobook
- Added initial/reference data for book sources:
  - Library book
  - Bought new
  - Bought second hand
  - Gift
  - Friend's book
- Added format selection to the Streamlit book form.
- Added source selection to the Streamlit book form.
- Added optional price input.
- Added `add_library_entry()` CRUD function.
- Connected book creation with library entry creation.
- Books can now be added to the personal library with format, source and optional price.

## Decisions

- `Book` and `LibraryEntry` remain separate concepts.
- Format and source are stored using foreign keys rather than duplicated names.
- Price is nullable because some library sources do not involve a purchase.
- `add_book()` remains responsible only for creating a book.
- `add_library_entry()` is responsible for creating the relationship between a book and its library information.
- Initial/reference data is populated by the database initialisation process.

## Problems encountered

- Initially attempted to pass format, source and price directly to `add_book()`.
- This produced a `TypeError` because `add_book()` accepts only the book title.
- Resolved by creating a separate `add_library_entry()` function.
- SQLite schema was recreated after changing `price` from `NOT NULL` to nullable.
- Streamlit dropdown data initially appeared duplicated because reference data was being inserted repeatedly. `UNIQUE` constraints and `INSERT OR IGNORE` were used to prevent duplicate reference data.

## Lessons learned

- Separate database operations should reflect separate database entities.
- A foreign key relationship should be created using IDs rather than duplicating descriptive values.
- `NULL` is preferable to fake values such as `0` when information is genuinely not applicable.
- SQLite `CREATE TABLE IF NOT EXISTS` does not modify an existing table when the schema definition changes.

## Tests

- Confirmed format dropdown displays existing formats.
- Confirmed source dropdown displays existing sources.
- Confirmed a book can be created through Streamlit.
- Confirmed a corresponding library entry is created.
- Confirmed format, source and price are stored with the library entry.

## Files changed

- `src/database/schema.py`
- `src/database/crud.py`
- `src/app.py`

## Documentation updates

- Library management implementation progressed.
- Database schema now includes formats, sources and library entries.

## Git commit

Add library entry creation

## Next development task

Continue expanding library management, beginning with the remaining library-entry functionality rather than introducing new external technologies.