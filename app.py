import streamlit as st
import pickle
import os

class Book:
    def __init__(self, title, author, publish_year, gender, read):
        self.title = title
        self.author = author
        self.publish_year = publish_year
        self.gender = gender
        self.read = read

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publish_year}) - {self.gender} - Read: {'Yes' if self.read else 'No'}"

class Library:
    def __init__(self):
        self.file_name = "books.pkl"
        self.books = self.load_books()

    def load_books(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "rb") as file:
                return pickle.load(file)
        return []

    def save_books(self):
        with open(self.file_name, "wb") as file:
            pickle.dump(self.books, file)

    def add_book(self, title, author, publish_year, gender, read):
        new_book = Book(title, author, publish_year, gender, read)
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, title):
        self.books = [book for book in self.books if book.title.lower() != title.lower()]
        self.save_books()

    def search_book(self, keyword):
        return [book for book in self.books if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]

    def display_books(self):
        return self.books

    def display_statistics(self):
        total_books = len(self.books)
        read_books = sum(1 for book in self.books if book.read)
        unread_books = total_books - read_books
        return total_books, read_books, unread_books

library = Library()
st.title("📚 Book Management System")

menu = st.sidebar.selectbox("Menu", ["Add Book", "Remove Book", "Search Book", "Display All Books", "Display Statistics"])

if menu == "Add Book":
    st.header("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    publish_year = st.text_input("Publish Year")
    gender = st.selectbox("Select Gender", ["Male", "Female"])
    read = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        library.add_book(title, author, publish_year, gender, read)
        st.success("Book added successfully!")

elif menu == "Remove Book":
    st.header("Remove a Book")
    title = st.text_input("Enter book title to remove")
    if st.button("Remove Book"):
        library.remove_book(title)
        st.success("Book removed successfully!")

elif menu == "Search Book":
    st.header("Search a Book")
    keyword = st.text_input("Enter title or author to search")
    if st.button("Search"):
        found_books = library.search_book(keyword)
        if found_books:
            for book in found_books:
                st.write(book)
        else:
            st.warning("No books found.")

elif menu == "Display All Books":
    st.header("All Books")
    books = library.display_books()
    if books:
        for book in books:
            st.write(book)
    else:
        st.info("No books available.")

elif menu == "Display Statistics":
    st.header("Library Statistics")
    total, read, unread = library.display_statistics()
    st.write(f"Total books: {total}")
    st.write(f"Read books: {read}")
    st.write(f"Unread books: {unread}")
