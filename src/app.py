import streamlit as st

from database.schema import create_tables
from database.crud import (
    add_author,
    add_book,
    add_book_author,
    add_library_entry,
    get_author_by_name,
    get_books,
    get_book,
    get_sources,
    get_formats,
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

author_name = st.text_input("Author name")

formats = get_formats()

selected_format = st.selectbox(
    "Format",
    formats,
    format_func=lambda format: format[1]
)

# Get sources for dropdown
sources = get_sources()

selected_source = st.selectbox(
    "Source",
    sources,
    format_func=lambda source: source[1]
)
#st.write(sources)
#st.write(selected_source)

has_price = st.checkbox("I paid for this book")

if has_price:
    price = st.number_input(
        "Price (£)",
        min_value=0.0,
        step=0.01,
        format="%.2f"
    )
else:
    price = None

if st.button("Add book"):

    if title:

        book_id = add_book(title)

        if author_name:
            author = get_author_by_name(author_name)

            if author:
                author_id = author[0]
            else:
                author_id = add_author(author_name)

            add_book_author(book_id, author_id)

        add_library_entry(
            book_id,
            selected_format[0],
            selected_source[0],
            price
        )

        st.success(f"Book added! ID: {book_id}")

    else:
        st.warning("Please enter a book title.")

# Get formats and sources for dropdowns
formats = get_formats()
sources = get_sources()

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

