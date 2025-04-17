import streamlit as st
import json

# Global book list
library = []

# ---------- Utility Functions ----------
def save_library():
    with open("library.txt", "w") as file:
        json.dump(library, file)
    st.success("💾 Library saved to file.")

def load_library():
    try:
        with open("library.txt", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def footer():
    st.markdown(
        """
        <hr style="margin-top: 50px;" />
        <div style="text-align: center; color: gray;">
            © 2025 <strong>Owais Khan</strong>. All Rights Reserved.
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- Features ----------
def add_book():
    st.subheader("✨ Add a New Book")
    with st.form(key="add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1)
        genre = st.text_input("Genre")
        read_status = st.radio("Have you read this book?", ["Yes", "No"]) == "Yes"
        submit = st.form_submit_button("Add Book")
        if submit:
            book = {
                'title': title,
                'author': author,
                'year': year,
                'genre': genre,
                'read_status': read_status
            }
            library.append(book)
            st.success(f"✅ Book '{title}' added to your library!")

def remove_book():
    st.subheader("🗑️ Remove a Book")
    title = st.text_input("Enter the title to remove")
    if st.button("Remove"):
        global library
        original_count = len(library)
        library = [book for book in library if book['title'].lower() != title.lower()]
        if len(library) < original_count:
            st.success(f"✅ '{title}' removed.")
        else:
            st.warning("❌ Book not found.")

def search_book():
    st.subheader("🔍 Search Books")
    choice = st.radio("Search by:", ["Title", "Author"])
    query = st.text_input(f"Enter {choice}")
    if query:
        results = []
        for book in library:
            if query.lower() in book[choice.lower()].lower():
                results.append(book)

        if results:
            st.write("### Results:")
            for i, book in enumerate(results, 1):
                st.write(f"**{i}. {book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'Read' if book['read_status'] else 'Unread'}")
        else:
            st.warning("❌ No matching books found.")

def display_books():
    st.subheader("📚 Your Library")
    if not library:
        st.warning("No books added yet.")
        return
    for i, book in enumerate(library, 1):
        st.markdown(f"""
        **{i}. {book['title']}**  
        - Author: *{book['author']}*  
        - Year: {book['year']}  
        - Genre: {book['genre']}  
        - Status: {"✅ Read" if book['read_status'] else "📖 Unread"}  
        ---
        """)

def display_statistics():
    st.subheader("📊 Library Stats")
    total = len(library)
    if total == 0:
        st.info("No books to calculate stats.")
        return
    read = sum(1 for b in library if b['read_status'])
    percent = (read / total) * 100
    st.metric("Total Books", total)
    st.metric("Books Read", f"{read} ({percent:.2f}%)")
    st.progress(int(percent))

# ---------- Main App ----------
def main():
    global library
    library = load_library()

    # Main Title
    st.markdown("<h1 style='text-align: center;'>📚 Personal Library Manager</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar Menu
    menu = st.sidebar.selectbox(
        "Navigate",
        ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics", "Exit"]
    )

    # Page Routing
    if menu == "Add a Book":
        add_book()
    elif menu == "Remove a Book":
        remove_book()
    elif menu == "Search for a Book":
        search_book()
    elif menu == "Display All Books":
        display_books()
    elif menu == "Display Statistics":
        display_statistics()
    elif menu == "Exit":
        save_library()
        footer()
        st.balloons()
        st.stop()

    # Footer always visible
    footer()

# ---------- Run ----------
if __name__ == "__main__":
    main()
