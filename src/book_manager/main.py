"""Lab 2 demonstration, benchmark, JSON export and the original lab 1 menu."""

import argparse
import json
import logging
from pathlib import Path

from book_manager.analytics import (
    average_pages,
    average_values,
    create_page_filter,
    create_record,
    summarize,
)
from book_manager.benchmark import print_results, run_benchmark, save_results
from book_manager.data import BOOK_FIELDS, create_books
from book_manager.legacy_cli import print_books, run_menu
from book_manager.processors import (
    count_by_author,
    create_title_index,
    filter_by_year,
    filter_items,
    find_by_title,
    group_by_author,
    sort_by_year,
    unique_authors,
)
from book_manager.services import find_largest_book


def show_section(title: str, books: list) -> None:
    print(f"\n{title}")
    print_books(books)


def run_demo() -> None:
    books = create_books()
    show_section("КАТАЛОГ КНИГ", books)
    print("Поля запису (tuple):", BOOK_FIELDS)
    print("Унікальні автори:", "; ".join(sorted(unique_authors(books))))
    print("\nГРУПУВАННЯ ТА COUNTER")
    counts = count_by_author(books)
    for author, members in group_by_author(books).items():
        print(f"{author}: {counts[author]} — {', '.join(b.title for b in members)}")
    index = create_title_index(books)
    show_section("ПОШУК ЗА НАЗВОЮ: кобзар", list(find_by_title(index, " кобзар ")))
    show_section("РІК ВИДАННЯ 1911", filter_by_year(books, 1911))
    largest = find_largest_book(books)
    show_section("НАЙБІЛЬША КНИГА", [largest] if largest else [])
    print(f"Середня кількість сторінок: {average_pages(books):.2f}")
    show_section("СОРТУВАННЯ ЗА РОКОМ", sort_by_year(books))
    show_section(
        "CLOSURE: СТОРІНОК >= 180", filter_items(books, create_page_filter(180))
    )
    print("Середнє через *args:", average_values(*(b.pages for b in books)))
    print("Метадані через **kwargs:", create_record(variant=2, books=len(books)))
    print("ПІДСУМОК:", summarize(books))


def main() -> None:
    parser = argparse.ArgumentParser(description="Аналіз системи обліку книг")
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--benchmark", action="store_true")
    parser.add_argument("--export", type=Path, help="JSON-підсумок каталогу")
    parser.add_argument("--benchmark-output", type=Path, help="JSON вимірювань")
    args = parser.parse_args()
    if args.benchmark_output and not args.benchmark:
        parser.error("--benchmark-output потребує --benchmark")
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if args.interactive:
        run_menu()
    elif args.benchmark:
        results = run_benchmark()
        print_results(results)
        if args.benchmark_output:
            save_results(results, args.benchmark_output)
    else:
        run_demo()
    if args.export:
        args.export.parent.mkdir(parents=True, exist_ok=True)
        args.export.write_text(
            json.dumps(summarize(create_books()), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
