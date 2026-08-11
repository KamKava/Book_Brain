# Development Log

## August 2026 — SQLite Database and Book CRUD

### Database implementation

Began implementation of the SQLite database for Book Brain.

The original database schema contains 12 MVP tables. Rather than implementing the complete schema in one step, development was scaled down to a minimal working database first.

The initial implementation contains:

* SQLite database creation
* Database connection module
* `books` table
* Automatic integer primary key
* Book title field
* Basic CRUD operations

### Database structure

The initial `books` table contains:

```text
books
├── book_id
└── title
```

SQLite foreign-key enforcement is enabled through the database connection:

```sql
PRAGMA foreign_keys = ON;
```

The database connection is separated into `connection.py`, while book database operations are handled separately in `crud.py`.

### Book CRUD functionality

Implemented the following operations:

* Add a book
* Retrieve all books
* Retrieve an individual book by ID
* Update a book title
* Delete a book

The database automatically creates the SQLite database file when a connection is established if it does not already exist.

### Application structure

The database code was separated into distinct responsibilities:

```text
src/
└── database/
    ├── connection.py
    ├── schema.py
    ├── crud.py
    └── app.py
```

`connection.py` handles database connections.

`schema.py` handles database/table creation.

`crud.py` contains database operations.

`app.py` acts as the application entry point and will eventually provide the user-facing application flow.

### Development decisions

The complete ERD and database schema will be implemented incrementally rather than creating all 12 tables immediately.

The first goal is to establish a reliable working database and application flow:

```text
Create database
      ↓
Create books table
      ↓
Add books
      ↓
View books
      ↓
Edit books
      ↓
Delete books
```

Once this basic functionality is working reliably, additional entities and relationships will be introduced incrementally.

### Issues encountered

Several Python import and project-structure issues were encountered while separating the database modules.

The main issue was attempting to execute individual modules directly, which caused Python to resolve imports differently depending on the current execution context.

This led to restructuring the database code and establishing a clearer separation between the connection, schema, CRUD and application layers.

A further issue occurred when attempting to insert books before the `books` table had been created. This reinforced the need for database initialisation to occur before CRUD operations.

### Current status

The SQLite database is successfully created and the initial `books` table is operational.

Book CRUD operations have been tested successfully.

The next step is to create a simple application interface that calls the CRUD functions, allowing books to be added, viewed, edited and deleted through the application rather than directly through test code.
