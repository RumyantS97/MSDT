class Reader:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []
        self.history = []

    def borrow_book(self, book):
        if book.available:
            self.borrowed_books.append(book)
            book.available = False
            self.history.append(book)
            print(f"{self.name} borrowed '{book.title}'.")
        else:
            print(f"Sorry, '{book.title}' is not available.")

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.available = True
            print(f"{self.name} returned '{book.title}'.")
        else:
            print(f"{self.name} did not borrow '{book.title}'.")
