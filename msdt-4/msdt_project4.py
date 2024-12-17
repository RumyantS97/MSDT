import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')

class Author:
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year
        logging.debug(f"Author created: {self.name} ({self.birth_year})")

    def __str__(self):
        return f"{self.name} ({self.birth_year})"


class Book:
    def __init__(self, title, author, year, isbn):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.is_borrowed = False
        logging.debug(f"Book created: '{self.title}' by {self.author} ({self.year}), ISBN: {self.isbn}")

    def borrow(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            logging.info(f"Book borrowed: '{self.title}' by {self.author}")
            return True
        logging.warning(f"Attempt to borrow already borrowed book: '{self.title}' by {self.author}")
        return False

    def return_book(self):
        if self.is_borrowed:
            self.is_borrowed = False
            logging.info(f"Book returned: '{self.title}' by {self.author}")
            return True
        logging.warning(f"Attempt to return a book that wasn't borrowed: '{self.title}' by {self.author}")
        return False

    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year})"


class Library:
    def __init__(self):
        self.books = []
        self.members = []
        logging.debug("Library created.")

    def add_book(self, book):
        self.books.append(book)
        logging.info(f"Book added to library: '{book.title}' by {book.author}")

    def remove_book(self, isbn):
        book_to_remove = next((book for book in self.books if book.isbn == isbn), None)
        if book_to_remove:
            self.books.remove(book_to_remove)
            logging.info(f"Book removed from library: '{book_to_remove.title}' by {book_to_remove.author}")
            return True
        logging.warning(f"Attempt to remove non-existing book with ISBN: {isbn}")
        return False

    def borrow_book(self, isbn):
        book = next((book for book in self.books if book.isbn == isbn), None)
        if book and book.borrow():
            logging.info(f"Book borrowed from library: '{book.title}' by {book.author}")
            return True
        logging.warning(f"Attempt to borrow non-existing or already borrowed book with ISBN: {isbn}")
        return False

    def return_book(self, isbn):
        book = next((book for book in self.books if book.isbn == isbn), None)
        if book and book.return_book():
            logging.info(f"Book returned to library: '{book.title}' by {book.author}")
            return True
        logging.warning(f"Attempt to return non-existing or unborrowed book with ISBN: {isbn}")
        return False

    def search_books(self, query):
        found_books = [book for book in self.books if query.lower() in book.title.lower()]
        logging.info(f"Search for books with query '{query}': {len(found_books)} result(s) found")
        return found_books

    def display_books(self):
        logging.debug("Displaying all books in the library.")
        for book in self.books:
            print(book)

    def add_member(self, name):
        self.members.append(name)
        logging.info(f"New member added: {name}")

    def remove_member(self, name):
        if name in self.members:
            self.members.remove(name)
            logging.info(f"Member removed: {name}")
            return True
        logging.warning(f"Attempt to remove non-existing member: {name}")
        return False

    def display_members(self):
        logging.debug("Displaying all members of the library.")
        for member in self.members:
            print(member)


def main():
    author1 = Author("J.K. Rowling", 1965)
    author2 = Author("George Orwell", 1903)

    book1 = Book("Harry Potter and the Sorcerer's Stone", author1, 1997, "1234567890")
    book2 = Book("1984", author2, 1949, "0987654321")

    library = Library()

    library.add_book(book1)
    library.add_book(book2)

    print("Books in the library:")
    library.display_books()

    print("\nBorrowing '1984':")
    if library.borrow_book("0987654321"):
        print("Book borrowed successfully.")
    else:
        print("Book is already borrowed.")

    print("\nSearching for 'Harry Potter':")
    found_books = library.search_books("Harry Potter")
    for book in found_books:
        print(book)

    print("\nReturning '1984':")
    if library.return_book("0987654321"):
        print("Book returned successfully.")
    else:
        print("Book wasn't borrowed.")

    library.add_member("Alice")
    library.add_member("Bob")

    print("\nLibrary members:")
    library.display_members()

    print("\nRemoving '1984':")
    if library.remove_book("0987654321"):
        print("Book removed successfully.")
    else:
        print("Book not found.")

    print("\nRemoving member 'Alice':")
    if library.remove_member("Alice"):
        print("Member removed successfully.")
    else:
        print("Member not found.")


if __name__ == "__main__":
    main()
