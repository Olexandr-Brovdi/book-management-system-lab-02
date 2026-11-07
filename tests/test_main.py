"""Check user-visible output and recovery after invalid input."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from book_manager.legacy_cli import run_demo, run_menu


class ConsoleTests(unittest.TestCase):
    def test_demo(self):
        output = io.StringIO()
        with redirect_stdout(output):
            run_demo()
        self.assertIn("168.00", output.getvalue())
        self.assertIn("Кобзар", output.getvalue())

    def test_menu_operations(self):
        commands = [
            "1",
            "5",
            "6",
            "2",
            "Книга",
            "Автор",
            "2020",
            "100",
            "3",
            "автор",
            "4",
            "2020",
            "5",
            "6",
            "7",
            "0",
        ]
        output = io.StringIO()
        with patch("builtins.input", side_effect=commands), redirect_stdout(output):
            run_menu()
        self.assertIn("Книгу додано.", output.getvalue())
        self.assertIn("100.00", output.getvalue())

    def test_invalid_input(self):
        commands = ["x", "4", "abc", "2", "", "A", "2000", "10", "0"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=commands), redirect_stdout(output):
            run_menu()
        self.assertIn("Невідома команда", output.getvalue())
        self.assertIn("Помилка", output.getvalue())

    def test_eof(self):
        with (
            patch("builtins.input", side_effect=EOFError),
            redirect_stdout(io.StringIO()),
        ):
            run_menu()
