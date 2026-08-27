"""The protocol, both ways.

A class with __enter__/__exit__, and the generator form where the yield is
the seam between acquire and release. Note the try/finally around the yield:
without it, an exception in the body skips cleanup.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from types import TracebackType


class Managed:
    def __init__(self, name: str, log: list[str]) -> None:
        self.name = name
        self.log = log

    def __enter__(self) -> Managed:
        self.log.append(f"open {self.name}")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.log.append(f"close {self.name}")  # returning None: never swallow


@contextmanager
def managed(name: str, log: list[str]) -> Iterator[str]:
    log.append(f"open {name}")
    try:
        yield name
    finally:
        log.append(f"close {name}")


def main() -> None:
    log: list[str] = []
    with Managed("a", log):
        log.append("work")
    with managed("b", log):
        log.append("more work")
    print(log)


if __name__ == "__main__":
    main()
