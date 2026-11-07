"""Book operations independent from console input and output."""

from book_manager.models import Book


def add_book(books: list[Book], book: Book) -> None:
    """Append a validated book to the catalogue."""
    books.append(book)


def find_by_author(books: list[Book], author: str) -> list[Book]:
    """Find an exact author name ignoring case and outer whitespace."""
    query = author.strip().casefold()
    return [book for book in books if book.author.casefold() == query]


def filter_by_year(books: list[Book], year: int) -> list[Book]:
    """Return books published in the specified year."""
    return [book for book in books if book.year == year]


def find_largest_book(books: list[Book]) -> Book | None:
    """Return the first book with most pages, or None for an empty list."""
    return max(books, key=lambda book: book.pages, default=None)


def average_pages(books: list[Book]) -> float:
    """Return mean page count; an empty catalogue yields 0.0."""
    return sum(book.pages for book in books) / len(books) if books else 0.0


def sort_by_pages(books: list[Book]) -> list[Book]:
    """Return a new list in descending page-count order."""
    return sorted(books, key=lambda book: book.pages, reverse=True)
