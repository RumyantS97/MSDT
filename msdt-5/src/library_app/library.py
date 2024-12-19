from loguru import logger
from book import Book
from reader import Reader

class Library:
    def __init__(self):
        self.books = []
        self.readers = []

    def add_book(self, title, author, isbn, category=None):
        try:
            new_book = Book(title, author, isbn, category)
            self.books.append(new_book)
            print(f"Book '{title}' added to the library.")
            logger.info(f"Книга isbn: {isbn} успешно добавлена!")
        except Exception as e:
            logger.error(f"Произошла непредвиденная ошибка при добавлении книги: {e}")
            print("Произошла внезапная ошибка при добавлении книги")

    def register_reader(self, name):
        try:
            new_reader = Reader(name)
            self.readers.append(new_reader)
            print(f"Reader '{name}' registered.")
            logger.info(f"Читатель {name} успешно зарегистрирован!")
        except Exception as e:
            logger.error(f"Внезапная ошибка ({e})")
            print("Произошла внезапная ошибка при добавлении. Мы уже работаем над этим")

    def borrow_book(self, reader_name, isbn):
        try:
            reader = next((r for r in self.readers if r.name == reader_name), None)
            book = next((b for b in self.books if b.isbn == isbn and b.available), None)

            if reader is None:
                raise ValueError("Reader not found.")
            if book is None:
                raise ValueError("Book not found or not available.")

            reader.borrow_book(book)
            logger.info(f"Читатель '{reader_name}' взял книгу '{book.title}' (ISBN: {isbn}).")
        except Exception as e:
            logger.error(f"Ошибка при заимствовании книги: {e}")
            print(f"Error borrowing book: {e}")

    def return_book(self, reader_name, isbn):
        try:
            reader = next((r for r in self.readers if r.name == reader_name), None)
            book = next((b for b in self.books if b.isbn == isbn), None)

            if reader is None:
                raise ValueError("Reader not found.")
            if book is None:
                raise ValueError("Book not found.")

            reader.return_book(book)
            logger.info(f"Читатель '{reader_name}' вернул книгу '{book.title}' (ISBN: {isbn}).")
        except Exception as e:
            logger.error(f"Ошибка при возврате книги: {e}")
            print(f"Error returning book: {e}")

    def search_books(self, title=None, author=None, category=None):
        results = [book for book in self.books if
                   (title.lower() in book.title.lower() if title else True) and
                   (author.lower() in book.author.lower() if author else True) and
                   (book.category == category if category else True)]
        return results

    def remove_book(self, isbn):
        try:
            book_to_remove = next((b for b in self.books if b.isbn == isbn), None)
            if book_to_remove:
                self.books.remove(book_to_remove)
                logger.info(f"Книга '{book_to_remove.title}' (ISBN: {isbn}) удалена из библиотеки.")
                print(f"Book '{book_to_remove.title}' removed from the library.")
            else:
                logger.warning(f"Книга с ISBN: {isbn} не найдена.")
                print("Book not found.")
        except Exception as e:
            logger.error(f"Ошибка при удалении книги: {e}")
            print(f"Error removing book: {e}")

    def remove_reader(self, name):
        try:
            reader_to_remove = next((r for r in self.readers if r.name == name), None)
            if reader_to_remove:
                self.readers.remove(reader_to_remove)
                logger.info(f"Читатель '{name}' удален из библиотеки.")
                print(f"Reader '{name}' removed from the library.")
            else:
                print("Reader not found.")
        except Exception as e:
            logger.error(f"Ошибка при удалении читателя: {e}")
            print("Error removing reader")


    def list_books(self):
        print("Books in the library:")
        for book in self.books:
            print(book)

    def list_readers(self):
        print("Registered readers:")
        for reader in self.readers:
            print(reader.name)

    def report_popular_books(self):
        popular_books = {}
        for reader in self.readers:
            for book in reader.history:
                popular_books[book.title] = popular_books.get(book.title, 0) + 1

        sorted_books = sorted(popular_books.items(), key=lambda x: x[1], reverse=True)
        print("Most popular books:")
        for title, count in sorted_books:
            print(f"{title}: borrowed {count} times")
