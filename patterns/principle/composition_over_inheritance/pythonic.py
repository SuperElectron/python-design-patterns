"""Composition: one small object per axis, combined at runtime.

M filters + N transforms cover M x N behaviors with M + N classes; a new
combination is a constructor call, not a new class.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

Filter = Callable[[str], bool]
Transform = Callable[[str], str]


def contains(pattern: str) -> Filter:
    return lambda message: pattern in message


def identity(message: str) -> str:
    return message


@dataclass
class Logger:
    """One logger class, ever. Behavior comes from what you compose into it."""

    sink: list[str] = field(default_factory=list)
    filters: tuple[Filter, ...] = ()
    transform: Transform = identity

    def log(self, message: str) -> None:
        if all(f(message) for f in self.filters):
            self.sink.append(self.transform(message))


def main() -> None:
    loud_errors = Logger(filters=(contains("error"),), transform=str.upper)
    loud_errors.log("error: disk full")
    loud_errors.log("all fine")
    print(loud_errors.sink)


if __name__ == "__main__":
    main()
