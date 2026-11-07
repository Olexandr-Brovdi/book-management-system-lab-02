"""Benchmark correctness without asserting machine-dependent speed ratios."""

import unittest

from book_manager.benchmark import build_index, find_linear, run_benchmark


class BenchmarkTests(unittest.TestCase):
    def test_search_correctness(self):
        records = [(1, "A"), (2, "B")]
        self.assertEqual(find_linear(records, 2), build_index(records).get(2))
        self.assertIsNone(find_linear(records, 3))

    def test_measurement_shape(self):
        rows = run_benchmark((10,), queries=2, repeats=1)
        self.assertEqual([r.case for r in rows], ["last", "missing"])
        self.assertTrue(all(r.list_seconds >= 0 and r.dict_seconds >= 0 for r in rows))
        with self.assertRaises(ValueError):
            run_benchmark((0,))
