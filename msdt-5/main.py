class Book:
    def __init__(self, title):
        self.title = title
        self.is_available = True  # По умолчанию книга доступна

    def get_info(self):
        """Возвращает информацию о книге."""
        return f"Книга: {self.title}, доступна: {self.is_available}"


class Library:
    def __init__(self):
        self.users = []
        self.books = []

    def register_user(self, name):
        if not name.strip():  # Проверка на пустое значение имени
            print("Ошибка: имя пользователя не может быть пустым.")
            return False

        if name not in self.users:
            self.users.append(name)
            print(f"Пользователь '{name}' зарегистрирован.")
            return True
        else:
            print(f"Пользователь '{name}' уже зарегистрирован.")
            return False

    def issue_book(self, title, user):
        for book in self.books:
            if book.title == title:
                if book.is_available:
                    book.is_available = False
                    print(f"Книга '{title}' выдана пользователю '{user}'.")
                    return True
                else:
                    print(f"Книга '{title}' недоступна.")
                    return False
        print(f"Книга '{title}' не найдена.")
        return False

    def return_book(self, title):
        for book in self.books:
            if book.title == title:
                if not book.is_available:
                    book.is_available = True
                    print(f"Книга '{title}' возвращена.")
                    return True
                else:
                    print(f"Книга '{title}' не была выдана.")
                    return False
        print(f"Книга '{title}' не найдена.")
        return False

    def add_book(self, book):
        """Добавляет книгу в библиотеку."""
        self.books.append(book)
        print(f'Книга "{book.title}" добавлена в библиотеку.')

    def remove_book(self, title):
        """Удаляет книгу из библиотеки по названию."""
        for book in self.books:
            if book.title == title:
                self.books.remove(book)
                print(f'Книга "{title}" удалена из библиотеки.')
                return True
        print(f'Книга "{title}" не найдена в библиотеке.')
        return False

    def get_book_info(self):
        """Возвращает информацию о всех книгах в библиотеке."""
        return [book.get_info() for book in self.books]

    def get_available_books(self):
        """Возвращает список доступных книг."""
        return [book.get_info() for book in self.books if book.is_available]


if __name__ == "__main__":
    # Пример использования
    library = Library()

    # Добавляем книги
    library.add_book(Book('1984'))
    library.add_book(Book('Война и мир'))

    library.register_user('Иван')

    # Выдаем книгу
    library.issue_book('1984', 'Иван')

    # Возвращаем книгу
    library.return_book('1984')

    # Получаем доступные книги
    available_books = library.get_available_books()
    print(f"Доступные книги: {available_books}")

    # Удаляем книгу
    library.remove_book('1984')

    # Проверяем доступные книги после удаления
    available_books = library.get_available_books()
    print(f"Доступные книги после удаления: {available_books}")
