"""Console entry point, demonstration and interactive menu."""

import argparse

from book_manager.exceptions import BookValidationError
from book_manager.models import Book
from book_manager.services import (
    add_book,
    average_pages,
    filter_by_year,
    find_by_author,
    find_largest_book,
    sort_by_pages,
)


def create_demo_books() -> list[Book]:
    return [
        Book("Кобзар", "Тарас Шевченко", 1840, 240),
        Book("Захар Беркут", "Іван Франко", 1883, 192),
        Book("Лісова пісня", "Леся Українка", 1911, 160),
    ]


def print_books(books: list[Book]) -> None:
    if not books:
        print("Книг не знайдено.")
    for book in books:
        print(f"{book.title} | {book.author} | {book.year} | {book.pages} стор.")


def run_demo() -> None:
    books = create_demo_books()
    add_book(books, Book("Мойсей", "Іван Франко", 1905, 80))
    print("КАТАЛОГ КНИГ (після додавання Мойсея)")
    print_books(books)
    print("\nПОШУК ЗА АВТОРОМ: Іван Франко")
    print_books(find_by_author(books, "Іван Франко"))
    print("\nКНИГИ ЗА 1840 РІК")
    print_books(filter_by_year(books, 1840))
    print("\nНАЙБІЛЬША КНИГА")
    largest = find_largest_book(books)
    print_books([largest] if largest else [])
    print(f"\nСередня кількість сторінок: {average_pages(books):.2f}")
    print("\nСОРТУВАННЯ ЗА КІЛЬКІСТЮ СТОРІНОК")
    print_books(sort_by_pages(books))


def run_menu() -> None:
    books: list[Book] = []
    while True:
        print("\n1 Каталог | 2 Додати | 3 Автор | 4 Рік")
        print("5 Найбільша | 6 Середня | 7 Сортувати | 0 Вихід")
        try:
            command = input("Команда: ").strip()
            if command == "0":
                return
            if command == "1":
                print_books(books)
            elif command == "2":
                title = input("Назва: ")
                author = input("Автор: ")
                year = int(input("Рік: "))
                pages = int(input("Сторінок: "))
                add_book(books, Book(title, author, year, pages))
                print("Книгу додано.")
            elif command == "3":
                print_books(find_by_author(books, input("Автор: ")))
            elif command == "4":
                print_books(filter_by_year(books, int(input("Рік: "))))
            elif command == "5":
                largest = find_largest_book(books)
                print_books([largest] if largest else [])
            elif command == "6":
                print(f"Середня кількість сторінок: {average_pages(books):.2f}")
            elif command == "7":
                print_books(sort_by_pages(books))
            else:
                print("Невідома команда.")
        except BookValidationError as error:
            print(f"Помилка: {error}")
        except ValueError:
            print("Помилка: введіть ціле число.")
        except (EOFError, KeyboardInterrupt):
            print("\nРоботу завершено.")
            return


def main() -> None:
    parser = argparse.ArgumentParser(description="Система обліку книг")
    parser.add_argument("--interactive", action="store_true", help="Відкрити меню")
    args = parser.parse_args()
    if args.interactive:
        run_menu()
    else:
        run_demo()


if __name__ == "__main__":
    main()
