"""Validation boundaries and whitespace normalization."""

import unittest

from book_manager.exceptions import BookValidationError
from book_manager.models import Book


class ModelTests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(Book(" A ", " B ", 1, 1).title, "A")

    def test_invalid_fields(self):
        for values in [
            ("", "B", 2000, 1),
            ("A", " ", 2000, 1),
            ("A", "B", 0, 1),
            ("A", "B", 2101, 1),
            ("A", "B", True, 1),
            ("A", "B", 2000, 0),
            ("A", "B", 2000, 1.5),
            ("A", "B", 2000, True),
        ]:
            with self.subTest(values=values), self.assertRaises(BookValidationError):
                Book(*values)
