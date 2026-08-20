import streamlit as st

from database.schema import create_tables
from database.crud import (
    add_author,
    add_book,
    add_book_author,
    add_book_genre,
    add_book_subgenre,
    add_book_characteristic,
    add_library_entry,
    get_author_by_name,
    get_books,
    get_book,
    get_library_entries,
    get_sources,
    get_formats,
    get_authors,
    get_genres,
    get_subgenres_by_genres,
    get_audiences,
    get_characteristics,
    get_book_types,
    get_content_types,
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

author_names = st.text_input("Author name(s)")
# Get book classifications for dropdowns
content_types = get_content_types()
book_types = get_book_types()
audiences = get_audiences()

selected_content_type = st.selectbox(
    "Content Type",
    content_types,
    format_func=lambda content_type: content_type[1]
)

selected_book_type = st.selectbox(
    "Book Type",
    book_types,
    format_func=lambda book_type: book_type[1]
)

# Get genres
genres = get_genres()

selected_genres = st.multiselect(
    "Genre",
    genres,
    format_func=lambda genre: genre[1]
)

# Get subgenres belonging to selected genres
selected_genre_ids = [genre[0] for genre in selected_genres]

subgenres = get_subgenres_by_genres(selected_genre_ids)

selected_subgenres = st.multiselect(
    "Subgenre",
    subgenres,
    format_func=lambda subgenre: subgenre[1]
)

# Get characteristics
characteristics = get_characteristics()
st.write("DEBUG characteristics:", characteristics)
selected_characteristics = st.multiselect(
    "Characteristics",
    characteristics,
    format_func=lambda characteristic: characteristic[1]
)

selected_audience = st.selectbox(
    "Audience",
    audiences,
    format_func=lambda audience: audience[1]
)

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

        book_id = add_book(title, selected_book_type[0], selected_audience[0], selected_content_type[0])

        if author_names:
            authors = author_names.split(",")

            for author_name in authors:
                author_name = author_name.strip()

                if author_name:
                    author = get_author_by_name(author_name)

                    if author:
                        author_id = author[0]
                    else:
                        author_id = add_author(author_name)

                    add_book_author(book_id, author_id)
            for genre in selected_genres:
                add_book_genre(book_id, genre[0])
            for subgenre in selected_subgenres:
                add_book_subgenre(book_id, subgenre[0])
            for characteristic in selected_characteristics:
                add_book_characteristic(book_id, characteristic[0])


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

library_entries = get_library_entries()

if library_entries:
    for entry in library_entries:
        st.write(f"{entry[1]} — {entry[2]} — {entry[3]}")

        if st.button("Delete book", key=f"delete_{entry[0]}"):
            delete_book(entry[0])
            st.success("Book deleted!")
else:
    st.write("No books in your library yet.")

