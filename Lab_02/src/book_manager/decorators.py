"""Typed parameterized timing decorator, enabled through standard logging."""

import logging
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
LOGGER = logging.getLogger(__name__)


def measure_time(
    label: str = "operation",
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorate(function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = perf_counter()
            try:
                return function(*args, **kwargs)
            finally:
                LOGGER.info(
                    "%s %s: %.8f s", label, function.__name__, perf_counter() - start
                )

        return wrapper

    return decorate
