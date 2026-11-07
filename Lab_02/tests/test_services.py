"""Requirements of variant 2 and empty-catalogue behavior."""

import unittest

from book_manager.models import Book
from book_manager.services import (
    add_book,
    average_pages,
    filter_by_year,
    find_by_author,
    find_largest_book,
    sort_by_pages,
)


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.books = [
            Book("A", "Іван Франко", 2000, 100),
            Book("B", "Іван Франко", 2001, 200),
            Book("C", "Інший", 2000, 300),
        ]

    def test_add(self):
        book = Book("D", "Автор", 2020, 50)
        add_book(self.books, book)
        self.assertIs(self.books[-1], book)

    def test_author(self):
        self.assertEqual(find_by_author(self.books, " ІВАН ФРАНКО "), self.books[:2])
        self.assertEqual(find_by_author(self.books, "немає"), [])

    def test_year(self):
        self.assertEqual(filter_by_year(self.books, 2000), self.books[::2])
        self.assertEqual(filter_by_year(self.books, 1), [])

    def test_largest_and_average(self):
        self.assertIs(find_largest_book(self.books), self.books[2])
        self.assertEqual(average_pages(self.books), 200.0)

    def test_empty(self):
        self.assertIsNone(find_largest_book([]))
        self.assertEqual(average_pages([]), 0.0)
        self.assertEqual(filter_by_year([], 2000), [])

    def test_sort_and_ties(self):
        before = self.books.copy()
        self.assertEqual(sort_by_pages(self.books), self.books[::-1])
        self.assertEqual(self.books, before)
        self.assertIs(find_largest_book([before[0], before[0]]), before[0])
