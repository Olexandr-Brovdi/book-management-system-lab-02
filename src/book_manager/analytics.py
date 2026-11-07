"""Aggregations, closures and functions with variadic arguments."""

from collections.abc import Callable

from book_manager.decorators import measure_time
from book_manager.models import Book
from book_manager.services import find_largest_book


@measure_time("Середня кількість сторінок")
def average_pages(books: list[Book]) -> float:
    return sum(book.pages for book in books) / len(books) if books else 0.0


def average_values(*values: int) -> float:
    """Mean of page counts passed as positional arguments."""
    return sum(values) / len(values) if values else 0.0


def create_record(**fields: object) -> dict[str, object]:
    """Return metadata supplied as keyword arguments without hidden defaults."""
    return dict(fields)


def create_page_filter(minimum: int) -> Callable[[Book], bool]:
    """Return a predicate retaining its own minimum page count."""
    if type(minimum) is not int or minimum < 0:
        raise ValueError("Мінімум сторінок має бути невід'ємним цілим.")

    def predicate(book: Book) -> bool:
        return book.pages >= minimum

    return predicate


def summarize(books: list[Book]) -> dict[str, object]:
    largest = find_largest_book(books)
    return create_record(
        count=len(books),
        total_pages=sum(b.pages for b in books),
        average_pages=average_pages(books),
        largest_title=largest.title if largest else None,
    )
