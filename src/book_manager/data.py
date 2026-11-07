"""Fresh demonstration data using the validated Book model from lab 1."""

from book_manager.models import Book

BOOK_FIELDS = ("title", "author", "year", "pages")


def create_books() -> list[Book]:
    return [
        Book("Кобзар", "Тарас Шевченко", 1840, 240),
        Book("Захар Беркут", "Іван Франко", 1883, 192),
        Book("Лісова пісня", "Леся Українка", 1911, 160),
        Book("Мойсей", "Іван Франко", 1905, 80),
        Book("Тіні забутих предків", "Михайло Коцюбинський", 1911, 128),
    ]
