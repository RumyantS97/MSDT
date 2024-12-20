import logging
import json
import os

from datetime import datetime
from typing import List, Dict, Optional


# Setup logging
def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Setup logger
    logger = logging.getLogger('library_manager')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	
	# Add logger handlers
    file_handler = logging.FileHandler('logs/library.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

class Book:
    def __init__(self, title: str, author: str, isbn: str, year: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.is_available = True
        self.borrowed_by = None
        self.borrow_date = None

    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'year': self.year,
            'is_available': self.is_available,
            'borrowed_by': self.borrowed_by,
            'borrow_date': self.borrow_date.isoformat() if self.borrow_date else None
        }

class LibraryManager:
    def __init__(self, logger):
        self.books: Dict[str, Book] = {}
        self.logger = logger
        self.data_file = 'library_data.json'
        self.load_data()

    def add_book(self, title: str, author: str, isbn: str, year: int) -> bool:
        if isbn in self.books:
            self.logger.warning(f"Trying to add book with existing ISBN: {isbn}")
            return False

        book = Book(title, author, isbn, year)
        self.books[isbn] = book
        self.logger.info(f"Added new book: {title} (ISBN: {isbn})")
        self.save_data()
        return True

    def remove_book(self, isbn: str) -> bool:
        if isbn not in self.books:
            self.logger.error(f"Trying to delete non-existen book with ISBN: {isbn}")
            return False

        book = self.books.pop(isbn)
        self.logger.info(f"Deleted book: {book.title} (ISBN: {isbn})")
        self.save_data()
        return True

    def borrow_book(self, isbn: str, user: str) -> bool:
        if isbn not in self.books:
            self.logger.error(f"Trying to borrow non-existen book with ISBN: {isbn}")
            return False

        book = self.books[isbn]
        if not book.is_available:
            self.logger.warning(f"Trying to borrow unavailable book: {book.title} (ISBN: {isbn})")
            return False

        book.is_available = False
        book.borrowed_by = user
        book.borrow_date = datetime.now()
        self.logger.info(f"Book '{book.title}' is already taken by {user}")
        self.save_data()
        return True

    def return_book(self, isbn: str) -> bool:
        if isbn not in self.books:
            self.logger.error(f"Trying to return non-existen book with ISBN: {isbn}")
            return False

        book = self.books[isbn]
        if book.is_available:
            self.logger.warning(f"Trying to return already returned book: {book.title}")
            return False

        book.is_available = True
        book.borrowed_by = None
        book.borrow_date = None
        self.logger.info(f"Book '{book.title}' borrowed to library")
        self.save_data()
        return True

    def search_books(self, query: str) -> List[Book]:
        self.logger.debug(f"Searching books with query: {query}")
        query = query.lower()
        results = []
        for book in self.books.values():
            if (query in book.title.lower() or 
                query in book.author.lower() or 
                query in book.isbn.lower()):
                results.append(book)
        return results

    def save_data(self):
        try:
            data = {isbn: book.to_dict() for isbn, book in self.books.items()}
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.debug("Library data successfully saved")
        except Exception as e:
            self.logger.error(f"Error while saving library data: {str(e)}")

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for isbn, book_data in data.items():
                    book = Book(
                        book_data['title'],
                        book_data['author'],
                        isbn,
                        book_data['year']
                    )
                    book.is_available = book_data['is_available']
                    book.borrowed_by = book_data['borrowed_by']
                    if book_data['borrow_date']:
                        book.borrow_date = datetime.fromisoformat(book_data['borrow_date'])
                    self.books[isbn] = book
                self.logger.info(f"Loaded {len(self.books)} books from file")
            else:
                self.logger.info("No data file is found, creating new library")
        except Exception as e:
            self.logger.error(f"Error while loading data: {str(e)}")

def main():
    # Logger init
    logger = setup_logging()
    
    # Create library manager
    library = LibraryManager(logger)

    # Usage examples
    try:
        # Adding books
        library.add_book("1984", "George Orwell", "978-0451524935", 1949)
        library.add_book("The Hobbit", "J.R.R. Tolkien", "978-0547928227", 1937)
        library.add_book("Pride and Prejudice", "Jane Austen", "978-0141439518", 1813)

        # Searching books
        search_results = library.search_books("tolkien")
        logger.info(f"Founded books: {len(search_results)}")
		
		# Borrowing book
        if library.borrow_book("978-0547928227", "John Doe"):
            logger.info("Book borrowed successfully")
        
        # Borrowing already borrowed book
        if not library.borrow_book("978-0547928227", "Jane Smith"):
            logger.warning("Cannot borrow book thas already borrowed")

        # Returning book
        if library.return_book("978-0547928227"):
            logger.info("Book returned successfully")

        # Removing book
        if library.remove_book("978-0141439518"):
            logger.info("Book deleted from library successfully")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()