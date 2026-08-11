import sqlite3


# Opens the SQLite database.
# SQLite creates the database file if it does not exist.
# Enables foreign-key enforcement.
# Returns the connection.

def get_connection():
    connection = sqlite3.connect("bookbrain.db")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

