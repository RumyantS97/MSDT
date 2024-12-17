class Author:
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year

    def __str__(self):
        return f"{self.name} ({self.birth_year})"


class Book:
    def __init__(self, title, author, year, isbn):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.is_borrowed = False

    def borrow(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            return True
        return False

    def return_book(self):
        if self.is_borrowed:
            self.is_borrowed = False
            return True
        return False

    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year})"


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, isbn):
        book_to_remove = next((book for book in self.books if book.isbn == isbn), None)
        if book_to_remove:
            self.books.remove(book_to_remove)
            return True
        return False

    def borrow_book(self, isbn):
        book = next((book for book in self.books if book.isbn == isbn), None)
        if book and book.borrow():
            return True
        return False

    def return_book(self, isbn):
        book = next((book for book in self.books if book.isbn == isbn), None)
        if book and book.return_book():
            return True
        return False

    def search_books(self, query):
        return [book for book in self.books if query.lower() in book.title.lower()]

    def display_books(self):
        for book in self.books:
            print(book)

    def add_member(self, name):
        self.members.append(name)

    def remove_member(self, name):
        if name in self.members:
            self.members.remove(name)
            return True
        return False

    def display_members(self):
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
