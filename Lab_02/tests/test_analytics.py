"""Closures, decorators, aggregation and variadic arguments."""

import unittest

from book_manager.analytics import (
    average_pages,
    average_values,
    create_page_filter,
    create_record,
    summarize,
)
from book_manager.data import create_books
from book_manager.decorators import measure_time


class AnalyticsTests(unittest.TestCase):
    def test_average(self):
        self.assertEqual(average_pages(create_books()), 160.0)
        self.assertEqual(average_pages([]), 0.0)
        self.assertEqual(average_values(240, 192, 160, 80, 128), 160.0)
        self.assertEqual(average_values(), 0.0)

    def test_closures_are_independent(self):
        small, large = create_page_filter(100), create_page_filter(240)
        book = create_books()[1]
        self.assertTrue(small(book))
        self.assertFalse(large(book))
        self.assertTrue(create_page_filter(192)(book))
        for invalid in (-1, True, 1.5):
            with self.assertRaises(ValueError):
                create_page_filter(invalid)

    def test_kwargs_and_summary(self):
        self.assertEqual(create_record(a=1, name="книга"), {"a": 1, "name": "книга"})
        self.assertEqual(create_record(), {})
        self.assertEqual(summarize(create_books())["total_pages"], 800)
        self.assertIsNone(summarize([])["largest_title"])

    def test_decorator_returns_value_and_keeps_metadata(self):
        @measure_time("test")
        def add(value: int, *, delta: int = 1) -> int:
            """Original function."""
            return value + delta

        with self.assertLogs("book_manager.decorators", level="INFO") as logs:
            self.assertEqual(add(2, delta=3), 5)
        self.assertEqual(add.__name__, "add")
        self.assertEqual(add.__doc__, "Original function.")
        self.assertIn("test add", logs.output[0])

    def test_decorator_preserves_exception(self):
        @measure_time()
        def fail():
            raise ValueError("expected")

        with self.assertRaisesRegex(ValueError, "expected"):
            fail()
