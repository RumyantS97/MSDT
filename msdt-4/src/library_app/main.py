from library import Library
from loguru import logger


def main():
    moscow_library = Library()
    moscow_library.add_book("1984", "George Orwell", "123456789", "Fiction")
    moscow_library.add_book("To Kill a Mockingbird", "Harper Lee", "987654321", "Fiction")
    moscow_library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "111222333", "Fiction")
    moscow_library.register_reader("Alice")
    moscow_library.register_reader("Bob")

    search_results = moscow_library.search_books(author="George Orwell")
    print("Search Results:")
    for book in search_results:
        print(book)

    moscow_library.borrow_book("Alice", "123456789")
    moscow_library.borrow_book("Bob", "987654321")

    moscow_library.return_book("Alice", "123456789")

    moscow_library.remove_book("111222333")  # Удаляем книгу
    moscow_library.remove_reader("Bob")  # Удаляем читателя

    moscow_library.report_popular_books()


if __name__ == "__main__":
    logger.add(
        'logs/log.txt',
        rotation='15KB',
        retention='30 days',
        level='INFO',
        format = "{time} {level} {message}"
    )
    main()
