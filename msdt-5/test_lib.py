import pytest
from main import Library, Book
from unittest.mock import Mock


@pytest.fixture
def library():
    """Фикстура для создания экземпляра библиотеки."""
    return Library()


def test_add_book(library):
    """Тестирование добавления книги в библиотеку."""
    book = Book("1984")
    library.add_book(book)

    # Проверяем, что книга была добавлена
    assert len(library.books) == 1
    assert library.books[0].title == "1984"


def test_remove_book(library):
    """Тестирование удаления книги из библиотеки."""
    book = Book("1984")
    library.add_book(book)
    assert len(library.books) == 1
    library.remove_book("1984")
    assert len(library.books) == 0


def test_remove_nonexistent_book(library):
    """Тестирование попытки удаления несуществующей книги."""
    result = library.remove_book("Неизвестная книга")
    assert result is False


def test_get_available_books_calls_get_info(library):
    """Тестирование метода get_available_books в классе Library с проверкой вызовов get_info."""

    # Создаем мок-объекты для книг
    mock_book1 = Mock(spec=Book)
    mock_book1.title = "1984"
    mock_book1.is_available = True
    mock_book1.get_info.return_value = "Книга: 1984, доступна: True"

    mock_book2 = Mock(spec=Book)
    mock_book2.title = "To Kill a Mockingbird"
    mock_book2.is_available = True
    mock_book2.get_info.return_value = "Книга: To Kill a Mockingbird, доступна: True"

    mock_book3 = Mock(spec=Book)
    mock_book3.title = "The Great Gatsby"
    mock_book3.is_available = False
    mock_book3.get_info.return_value = "Книга: The Great Gatsby, доступна: False"

    # Добавляем мок-объекты в библиотеку
    library.books = [mock_book1, mock_book2, mock_book3]

    # Вызываем метод get_available_books
    available_books_info = library.get_available_books()

    # Ожидаемый результат
    expected_result = [
        "Книга: 1984, доступна: True",
        "Книга: To Kill a Mockingbird, доступна: True"
    ]

    # Проверяем, что метод вернул правильный результат
    assert len(available_books_info) == 2  # Две доступные книги
    assert available_books_info == expected_result

    # Проверяем, что метод get_info был вызван только для доступных книг
    assert mock_book1.get_info.call_count == 1
    assert mock_book2.get_info.call_count == 1
    assert mock_book3.get_info.call_count == 0


@pytest.mark.parametrize("user_name, expected_user_count, expected_return_value", [
    ('Иван', 1, True),  # Успешная регистрация нового пользователя
    ('', 0, False),  # Попытка регистрации с пустым именем
    (' ', 0, False)  # Попытка регистрации с пустым именем
])
def test_register_user(library, user_name, expected_user_count, expected_return_value):
    result = library.register_user(user_name)
    assert len(library.users) == expected_user_count
    assert result == expected_return_value


def test_register_user_duplicate(library):
    """Тестирование повторной регистрации уже существующего пользователя."""
    library.register_user('Иван')  # Первая регистрация
    result = library.register_user('Иван')  # Повторная регистрация

    assert len(library.users) == 1
    assert result is False


@pytest.mark.parametrize("book_title, expected_result", [
    ("1984", True),  # Успешная выдача книги
    ("Неизвестная книга", False),  # Попытка выдачи несуществующей книги
])
def test_issue_books(library, book_title, expected_result):
    """Тестирование выдачи книги."""
    if expected_result is True:
        book = Book("1984")
        library.add_book(book)

    result = library.issue_book(book_title, "Иван")  # Выдаем книгу
    assert result is expected_result


def test_issue_book_already_issued(library):
    """Тестирование попытки выдачи уже выданной книги."""
    book = Book('1984')
    library.add_book(book)
    library.issue_book('1984', 'Иван')
    result = library.issue_book('1984', 'Петр')
    assert result is False


@pytest.mark.parametrize("book_title, expected_result", [
    ("1984", True),  # Успешный возврат книги
    ("Неизвестная книга", False),  # Попытка возврата несуществующей книги
])
def test_return_books(library, book_title, expected_result):
    """Тестирование возврата книги."""
    if expected_result is True:
        book = Book("1984")
        library.add_book(book)
        library.issue_book("1984", "Иван")

    result = library.return_book(book_title)
    assert result is expected_result


def test_return_book_not_issued(library):
    """Тестирование попытки возврата книги, которая не была выдана."""
    book = Book('1984')
    library.add_book(book)
    result = library.return_book('1984')
    assert result is False


def test_get_book_info_calls_get_info(library):
    """Тестирование метода get_book_info в классе Library с проверкой вызовов get_info."""

    # Создаем мок-объекты для книг
    mock_book1 = Mock(spec=Book)
    mock_book1.title = "1984"
    mock_book1.is_available = True
    mock_book1.get_info.return_value = "Книга: 1984, доступна: True"

    mock_book2 = Mock(spec=Book)
    mock_book2.title = "To Kill a Mockingbird"
    mock_book2.is_available = True
    mock_book2.get_info.return_value = "Книга: To Kill a Mockingbird, доступна: True"

    mock_book3 = Mock(spec=Book)
    mock_book3.title = "The Great Gatsby"
    mock_book3.is_available = False
    mock_book3.get_info.return_value = "Книга: The Great Gatsby, доступна: False"

    # Добавляем мок-объекты в библиотеку
    library.books = [mock_book1, mock_book2, mock_book3]

    # Вызываем метод get_book_info
    result = library.get_book_info()

    # Ожидаемый результат
    expected_result = [
        "Книга: 1984, доступна: True",
        "Книга: To Kill a Mockingbird, доступна: True",
        "Книга: The Great Gatsby, доступна: False"
    ]

    # Проверяем, что метод вернул правильный результат
    assert result == expected_result

    # Проверяем, что метод get_info был вызван для каждой книги
    assert mock_book1.get_info.call_count == 1
    assert mock_book2.get_info.call_count == 1
    assert mock_book3.get_info.call_count == 1
