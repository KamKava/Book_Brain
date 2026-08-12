import streamlit as st

from database.schema import create_tables
from database.crud import (
    add_book,
    get_books,
    get_book,
    update_book,
    delete_book
)


# Make sure the database and tables exist
create_tables()


st.title("Book Brain")

# --------------------
# Add a book
# --------------------

st.subheader("Add a book")

title = st.text_input("Book title")

if st.button("Add book"):
    if title:
        book_id = add_book(title)
        st.success(f"Book added! ID: {book_id}")
    else:
        st.warning("Please enter a book title.")


# --------------------
# Display books
# --------------------

st.subheader("My books")

books = get_books()

if books:
    for book in books:
        st.write(f"{book[0]} — {book[1]}")
        if st.button("Delete book", key=f"delete_{book[0]}"):
            delete_book(book[0])
            st.success("Book deleted!")
else:
    st.write("No books in your library yet.")
