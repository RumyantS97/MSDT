from loguru import logger

class Reader:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []
        self.history = []
        logger.info(f"Пользователь {self.name} успешно создан!")

    def borrow_book(self, book):
        if book.available:
            self.borrowed_books.append(book)
            logger.info(f"Была взята книга {self.book}")
            book.available = False
            self.history.append(book)
            logger.info(f"В историю была добавлена книга {self.book}")
            print(f"{self.name} borrowed '{book.title}'.")
        else:
            logger.error(f"Произошла непредвиденная ошибка при попытке взять книгу ({getattr(self.book, 'isbn')})")
            print(f"Sorry, '{book.title}' is not available.")

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            logger.info(f"Книга {self.book} была возвращена")
            book.available = True
            print(f"{self.name} returned '{book.title}'.")
        else:
            print(f"{self.name} did not borrow '{book.title}'.")
