import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from library import Book, Library


# Тесты для класса Book
@pytest.mark.parametrize(
    "title, author",
    [
        ("1984", "George Orwell"),
        ("To Kill a Mockingbird", "Harper Lee"),
        ("The Great Gatsby", "F. Scott Fitzgerald"),
    ],
)
def test_book_initialization(title, author):
    """Тестирует инициализацию объекта Book."""
    book = Book(title, author)
    assert book.title == title
    assert book.author == author
    assert not book.is_checked_out
    assert book.checked_out_date is None


def test_book_check_out():
    """Тестирует выдачу книги."""
    book = Book("1984", "George Orwell")
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 10, 1)
        book.check_out()
        assert book.is_checked_out
        assert book.checked_out_date == datetime(2023, 10, 1)


def test_book_check_out_already_checked_out():
    """Тестирует попытку выдать уже выданную книгу."""
    book = Book("1984", "George Orwell")
    book.check_out()
    with pytest.raises(Exception, match="Книга уже выдана."):
        book.check_out()


def test_book_return_book():
    """Тестирует возврат книги."""
    book = Book("1984", "George Orwell")
    book.check_out()
    book.return_book()
    assert not book.is_checked_out
    assert book.checked_out_date is None


def test_book_return_book_not_checked_out():
    """Тестирует попытку вернуть книгу, которая не была выдана."""
    book = Book("1984", "George Orwell")
    with pytest.raises(Exception, match="Книга не была выдана."):
        book.return_book()


# Тесты для класса Library
def test_library_add_book():
    """Тестирует добавление книги в библиотеку."""
    library = Library()
    book = Book("1984", "George Orwell")
    library.add_book(book)
    assert len(library.books) == 1
    assert library.books[0] == book


def test_library_add_book_invalid_type():
    """Тестирует добавление некорректного объекта в библиотеку."""
    library = Library()
    with pytest.raises(ValueError, match="Неверный тип книги."):
        library.add_book("Not a Book object")


def test_library_check_out_book():
    """Тестирует выдачу книги из библиотеки."""
    library = Library()
    book = Book("1984", "George Orwell")
    library.add_book(book)
    library.check_out_book("1984")
    assert book.is_checked_out


def test_library_check_out_book_not_found():
    """Тестирует попытку выдать книгу, которая не найдена."""
    library = Library()
    with pytest.raises(ValueError, match="Книга не найдена."):
        library.check_out_book("1984")


def test_library_return_book():
    """Тестирует возврат книги в библиотеку."""
    library = Library()
    book = Book("1984", "George Orwell")
    library.add_book(book)
    book.check_out()
    library.return_book("1984")
    assert not book.is_checked_out


def test_library_return_book_not_found():
    """Тестирует попытку вернуть книгу, которая не найдена."""
    library = Library()
    with pytest.raises(ValueError, match="Книга не найдена."):
        library.return_book("1984")


def test_library_find_book():
    """Тестирует поиск книги в библиотеке."""
    library = Library()
    book = Book("1984", "George Orwell")
    library.add_book(book)
    found_book = library.find_book("1984")
    assert found_book == book


def test_library_find_book_not_found():
    """Тестирует поиск книги, которая не найдена."""
    library = Library()
    found_book = library.find_book("1984")
    assert found_book is None


def test_library_list_books():
    """Тестирует вывод списка книг в библиотеке."""
    library = Library()
    book1 = Book("1984", "George Orwell")
    book2 = Book("To Kill a Mockingbird", "Harper Lee")
    library.add_book(book1)
    library.add_book(book2)
    book1.check_out()
    expected_list = [
        ("1984", "George Orwell", True),
        ("To Kill a Mockingbird", "Harper Lee", False),
    ]
    assert library.list_books() == expected_list
