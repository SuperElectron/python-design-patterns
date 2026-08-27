"""Generators: the iterator pattern as a language feature.

A function with ``yield`` returns an object that already implements
``__iter__`` and ``__next__``; the cursor state lives in the paused frame.
An ``__iter__`` written as a generator makes a class iterable in one line.
"""

from __future__ import annotations

from collections.abc import Iterator


def odd_numbers(maximum: int) -> Iterator[int]:
    """The whole of naive.py, as a generator."""
    n = 1
    while n <= maximum:
        yield n
        n += 2


class OddNumbers:
    """An iterable class whose __iter__ is itself a generator."""

    def __init__(self, maximum: int) -> None:
        self.maximum = maximum

    def __iter__(self) -> Iterator[int]:
        n = 1
        while n <= self.maximum:
            yield n
            n += 2


def main() -> None:
    print(list(odd_numbers(7)))
    print(list(OddNumbers(7)))
    print([n * n for n in OddNumbers(9)])  # comprehensions speak the protocol


if __name__ == "__main__":
    main()
