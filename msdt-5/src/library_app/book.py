from loguru import logger

class Book:
    def __init__(self, title, author, isbn, category=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.category = category
        logger.info(f"Кгига {self.title} успешно создана (isbn: {self.isbn})")

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}, Category: {self.category}) - {'Available' if self.available else 'Not Available'}"

