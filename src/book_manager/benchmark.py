"""Reproducible worst-position and missing-ID lookup benchmark.

Use identical immutable records in both containers. Time index construction
separately; report median batch time per lookup, not a single timer tick.
"""

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass
from functools import partial
from pathlib import Path
from statistics import median
from timeit import repeat

Record = tuple[int, str]
SIZES = (1_000, 10_000, 100_000)


@dataclass(frozen=True)
class BenchmarkResult:
    records: int
    case: str
    list_seconds: float
    dict_seconds: float
    build_seconds: float
    queries_per_batch: int
    repeats: int


def find_linear(records: list[Record], record_id: int) -> Record | None:
    for record in records:
        if record[0] == record_id:
            return record
    return None


def build_index(records: list[Record]) -> dict[int, Record]:
    return {record[0]: record for record in records}


def seconds_per_call(action: Callable[[], object], number: int, repeats: int) -> float:
    return median(repeat(action, number=number, repeat=repeats)) / number


def run_benchmark(
    sizes: tuple[int, ...] = SIZES, *, queries: int = 200, repeats: int = 5
) -> list[BenchmarkResult]:
    if queries < 1 or repeats < 1 or any(size < 1 for size in sizes):
        raise ValueError("Розміри, кількість пошуків і повторів мають бути додатними.")
    results = []
    for size in sizes:
        records = [(i, f"Книга {i}") for i in range(size)]
        index = build_index(records)
        build_time = seconds_per_call(partial(build_index, records), 3, repeats)
        for case, target in (("last", size - 1), ("missing", size)):
            expected = find_linear(records, target)
            assert expected == index.get(target)
            list_time = seconds_per_call(
                partial(find_linear, records, target), queries, repeats
            )
            dict_time = seconds_per_call(partial(index.get, target), queries, repeats)
            results.append(
                BenchmarkResult(
                    size, case, list_time, dict_time, build_time, queries, repeats
                )
            )
    return results


def save_results(results: list[BenchmarkResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([asdict(row) for row in results], ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )


def print_results(results: list[BenchmarkResult]) -> None:
    print("records case    list us   dict us   build ms")
    for row in results:
        print(
            f"{row.records:7} {row.case:7} {row.list_seconds * 1e6:9.3f} "
            f"{row.dict_seconds * 1e6:9.3f} {row.build_seconds * 1e3:9.3f}"
        )
