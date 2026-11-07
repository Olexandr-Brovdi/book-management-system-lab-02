"""Validated immutable data model."""

from dataclasses import dataclass

from book_manager.config import MAX_YEAR, MIN_PAGES, MIN_YEAR
from book_manager.exceptions import BookValidationError


@dataclass(frozen=True)
class Book:
    title: str
    author: str
    year: int
    pages: int

    def __post_init__(self) -> None:
        for field in ("title", "author"):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip():
                raise BookValidationError("Назва й автор не можуть бути порожніми.")
            object.__setattr__(self, field, value.strip())
        if type(self.year) is not int or not MIN_YEAR <= self.year <= MAX_YEAR:
            raise BookValidationError(f"Рік має бути цілим: {MIN_YEAR}–{MAX_YEAR}.")
        if type(self.pages) is not int or self.pages < MIN_PAGES:
            raise BookValidationError("Кількість сторінок має бути додатним цілим.")
