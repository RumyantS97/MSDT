import pytest
from library_app.library import Library
from unittest.mock import patch, MagicMock

@pytest.fixture
def library():
    library = Library()
    return library

@pytest.fixture
def library_with_books():
    lib = Library()
    lib.add_book("1984", "George Orwell", "1234567890")
    lib.add_book("To Kill a Mockingbird", "Harper Lee", "0987654321")
    lib.register_reader("Alice")
    lib.register_reader("Bob")
    return lib

def test_add_book(library):
    library.add_book("1984", "George Orwell", "1234567890")
    assert len(library.books) == 1
    assert library.books[0].title == "1984"
    assert library.books[0].author == "George Orwell"
    assert library.books[0].isbn == "1234567890"

def test_register_reader(library):
    library.register_reader("Alice")
    assert len(library.readers) == 1
    assert library.readers[0].name == "Alice"

def test_borrow_book(library):
    library.add_book("1984", "George Orwell", "1234567890")
    library.register_reader("Alice")
    
    library.borrow_book("Alice", "1234567890")
    assert len(library.readers[0].borrowed_books) == 1
    assert library.readers[0].borrowed_books[0].title == "1984"

def test_return_book(library):
    library.add_book("1984", "George Orwell", "1234567890")
    library.register_reader("Alice")
    
    library.borrow_book("Alice", "1234567890")
    library.return_book("Alice", "1234567890")
    
    assert len(library.readers[0].borrowed_books) == 0
    assert library.books[0].available is True

def test_remove_book(library):
    library.add_book("1984", "George Orwell", "1234567890")
    assert len(library.books) == 1
    
    library.remove_book("1234567890")
    assert len(library.books) == 0

def test_remove_reader(library):
    library.register_reader("Alice")
    assert len(library.readers) == 1
    
    library.remove_reader("Alice")
    assert len(library.readers) == 0

def test_borrow_nonexistent_book(library):
    library.register_reader("Alice")
    
    with pytest.raises(ValueError, match="Book not found or not available."):
        library.borrow_book("Alice", "nonexistent_isbn")

def test_return_nonexistent_book(library):
    library.add_book("1984", "George Orwell", "1234567890")
    library.register_reader("Alice")
    
    with pytest.raises(ValueError, match="Book not found."):
        library.return_book("Alice", "nonexistent_isbn")

def test_remove_nonexistent_book(library):
    with pytest.raises(ValueError, match="Book not found."):
        library.remove_book("nonexistent_isbn")

def test_remove_nonexistent_reader(library):
    with pytest.raises(ValueError, match="Reader not found."):
        library.remove_reader("Nonexistent Reader")


@pytest.mark.parametrize("title, author, isbn, category, expected_exception", [
    ("1984", "George Orwell", "1234567890", "Dystopian", None),
    ("To Kill a Mockingbird", "Harper Lee", "0987654321", "Fiction", None),
    ("", "Unknown Author", "1111111111", "Fiction", ValueError),
    ("Invalid Book", "", "2222222222", ValueError, None)
])
def test_add_book(library, title, author, isbn, category, expected_exception):
    if expected_exception is None:
        library.add_book(title, author, isbn, category)
        assert any(book.isbn == isbn for book in library.books)
    else:
        with pytest.raises(expected_exception):
            library.add_book(title, author, isbn, category)


@patch('library_app.library.Reader')
@patch('library_app.library.logger')
def test_register_reader(mock_logger, mock_reader, library):
    mock_reader.return_value = MagicMock(name='ReaderInstance')
    name = "Alice"
    library.register_reader(name)
    mock_reader.assert_called_once_with(name)
    assert len(library.readers) == 1
    assert library.readers[0] == mock_reader.return_value
    mock_logger.info.assert_called_once_with(f"Читатель {name} успешно зарегистрирован!")

@patch('library_app.library.Reader')
@patch('library_app.library.logger')
def test_register_reader_exception(mock_logger, mock_reader, library):
    mock_reader.side_effect = Exception("Ошибка создания читателя")
    name = "Bob"
    library.register_reader(name)
    mock_logger.error.assert_called_once_with("Внезапная ошибка (Ошибка создания читателя)")