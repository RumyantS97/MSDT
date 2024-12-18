import datetime

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_checked_out = False
        self.checked_out_date = None

    def check_out(self):
        if self.is_checked_out:
            raise Exception("Книга уже выдана.")
        self.is_checked_out = True
        self.checked_out_date = datetime.datetime.now()

    def return_book(self):
        if not self.is_checked_out:
            raise Exception("Книга не была выдана.")
        self.is_checked_out = False
        self.checked_out_date = None


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        if not isinstance(book, Book):
            raise ValueError("Неверный тип книги.")
        self.books.append(book)

    def check_out_book(self, title):
        book = self.find_book(title)
        if book is None:
            raise ValueError("Книга не найдена.")
        book.check_out()

    def return_book(self, title):
        book = self.find_book(title)
        if book is None:
            raise ValueError("Книга не найдена.")
        book.return_book()

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def list_books(self):
        return [(book.title, book.author, book.is_checked_out) for book in self.books]
