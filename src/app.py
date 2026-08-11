from database.schema import create_tables
from database.crud import (
    add_book,
    get_books,
    get_book,
    update_book,
    delete_book
)


def main():
    # Make sure the database tables exist
    create_tables()

    # Add a book
    book_id = add_book("Earthlings")
    print("Added book:", book_id)

    # Get all books
    print("\nAll books:")
    print(get_books())

    # Get one book
    print("\nSpecific book:")
    print(get_book(book_id))

    # Update the book
    update_book(book_id, "Earthlings - Updated")

    print("\nAfter update:")
    print(get_book(book_id))

    # Delete the book
    #delete_book(book_id)

    #print("\nAfter deletion:")
    print(get_books())


if __name__ == "__main__":
    main()