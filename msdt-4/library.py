import json
import os

from datetime import datetime
from typing import List, Dict, Optional


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
    def __init__(self):
        self.books: Dict[str, Book] = {}
        self.data_file = 'library_data.json'
        self.load_data()

    def add_book(self, title: str, author: str, isbn: str, year: int) -> bool:
        if isbn in self.books:
            return False

        book = Book(title, author, isbn, year)
        self.books[isbn] = book
        self.save_data()
        return True

    def remove_book(self, isbn: str) -> bool:
        if isbn not in self.books:
            return False

        book = self.books.pop(isbn)
        self.save_data()
        return True

    def borrow_book(self, isbn: str, user: str) -> bool:
        if isbn not in self.books:
            return False

        book = self.books[isbn]
        if not book.is_available:
            return False

        book.is_available = False
        book.borrowed_by = user
        book.borrow_date = datetime.now()
        self.save_data()
        return True

    def return_book(self, isbn: str) -> bool:
        if isbn not in self.books:
            return False

        book = self.books[isbn]
        if book.is_available:
            return False

        book.is_available = True
        book.borrowed_by = None
        book.borrow_date = None
        self.save_data()
        return True

    def search_books(self, query: str) -> List[Book]:
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
        except Exception as e:
            pass

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
        except Exception as e:
            pass

def main():
    # Create library manager
    library = LibraryManager()

    # Usage examples
    try:
        # Adding books
        library.add_book("1984", "George Orwell", "978-0451524935", 1949)
        library.add_book("The Hobbit", "J.R.R. Tolkien", "978-0547928227", 1937)
        library.add_book("Pride and Prejudice", "Jane Austen", "978-0141439518", 1813)

        # Searching books
        search_results = library.search_books("tolkien")
		
		# Borrowing book
        borrow = library.borrow_book("978-0547928227", "John Doe")
        
        # Borrowing already borrowed book
        borrow = library.borrow_book("978-0547928227", "Jane Smith")

        # Returning book
        returning = library.return_book("978-0547928227")

        # Removing book
        removing = library.remove_book("978-0141439518")

    except Exception as e:
        pass

if __name__ == "__main__":
    main()