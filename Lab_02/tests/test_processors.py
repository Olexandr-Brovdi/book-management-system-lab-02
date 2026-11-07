"""Lab 2 operations including duplicate-title index behavior."""

import unittest
from collections import Counter

from book_manager.data import create_books
from book_manager.models import Book
from book_manager.processors import (
    count_by_author,
    create_title_index,
    filter_by_year,
    filter_items,
    find_by_title,
    group_by_author,
    sort_books,
    sort_by_year,
    unique_authors,
)


class ProcessorTests(unittest.TestCase):
    def setUp(self):
        self.books = create_books()

    def test_unique_and_counter(self):
        self.assertEqual(len(unique_authors(self.books)), 4)
        self.assertIsInstance(count_by_author(self.books), Counter)
        self.assertEqual(count_by_author(self.books)["Іван Франко"], 2)

    def test_grouping(self):
        groups = group_by_author(self.books)
        self.assertEqual(sum(map(len, groups.values())), 5)
        self.assertEqual(groups["Іван Франко"], [self.books[1], self.books[3]])

    def test_title_index_duplicate(self):
        duplicate = Book("КОБЗАР", "Тарас Шевченко", 2000, 300)
        index = create_title_index(self.books + [duplicate])
        self.assertEqual(find_by_title(index, " Кобзар "), (self.books[0], duplicate))
        self.assertEqual(find_by_title(index, "відсутня"), ())

    def test_year_and_sort(self):
        original = self.books.copy()
        self.assertEqual(len(filter_by_year(self.books, 1911)), 2)
        self.assertEqual(filter_by_year(self.books, 2000), [])
        ordered = sort_by_year(self.books)
        self.assertEqual([b.year for b in ordered], [1840, 1883, 1905, 1911, 1911])
        self.assertEqual(sort_by_year(self.books, reverse=True)[0].year, 1911)
        self.assertEqual(sort_books(self.books, lambda b: b.pages)[0].pages, 80)
        self.assertEqual(original, self.books)

    def test_empty(self):
        self.assertEqual(unique_authors([]), set())
        self.assertEqual(group_by_author([]), {})
        self.assertEqual(create_title_index([]), {})
        self.assertEqual(sort_by_year([]), [])
        self.assertEqual(filter_items([], lambda b: True), [])

    def test_universal_filter(self):
        self.assertEqual(len(filter_items(self.books, lambda b: b.pages >= 180)), 2)
