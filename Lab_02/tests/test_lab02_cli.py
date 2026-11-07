"""New demonstration and JSON export use the real CLI entry point."""

import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from book_manager.main import main, run_demo


class Lab02CliTests(unittest.TestCase):
    def test_demo(self):
        output = io.StringIO()
        with redirect_stdout(output):
            run_demo()
        for fragment in ("160.00", "COUNTER", "Іван Франко", "CLOSURE", "1911"):
            self.assertIn(fragment, output.getvalue())

    def test_export(self):
        with TemporaryDirectory() as folder:
            output = Path(folder) / "summary.json"
            with (
                patch("sys.argv", ["book-manager", "--export", str(output)]),
                redirect_stdout(io.StringIO()),
            ):
                main()
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["count"], 5)

    def test_benchmark_output_requires_benchmark(self):
        with (
            patch("sys.argv", ["book-manager", "--benchmark-output", "out.json"]),
            self.assertRaises(SystemExit),
        ):
            main()
