"""Pure collection operations; duplicate titles retain all matching books."""

from collections import Counter, defaultdict
from collections.abc import Callable

from book_manager.models import Book


def unique_authors(books: list[Book]) -> set[str]:
    return {book.author for book in books}


def group_by_author(books: list[Book]) -> dict[str, list[Book]]:
    groups: defaultdict[str, list[Book]] = defaultdict(list)
    for book in books:
        groups[book.author].append(book)
    return dict(groups)


def create_title_index(books: list[Book]) -> dict[str, tuple[Book, ...]]:
    """O(n) average build; keys use strip/casefold, values retain duplicates."""
    groups: defaultdict[str, list[Book]] = defaultdict(list)
    for book in books:
        groups[book.title.casefold()].append(book)
    return {title: tuple(matches) for title, matches in groups.items()}


def find_by_title(index: dict[str, tuple[Book, ...]], title: str) -> tuple[Book, ...]:
    """Average O(1) lookup with respect to the number of indexed books."""
    return index.get(title.strip().casefold(), ())


def count_by_author(books: list[Book]) -> Counter[str]:
    return Counter(book.author for book in books)


def filter_items(books: list[Book], predicate: Callable[[Book], bool]) -> list[Book]:
    return [book for book in books if predicate(book)]


def sort_books(
    books: list[Book], key: Callable[[Book], object], *, reverse: bool = False
) -> list[Book]:
    return sorted(books, key=key, reverse=reverse)


def filter_by_year(books: list[Book], year: int) -> list[Book]:
    return filter_items(books, lambda book: book.year == year)


def sort_by_year(books: list[Book], *, reverse: bool = False) -> list[Book]:
    return sort_books(books, key=lambda book: book.year, reverse=reverse)
