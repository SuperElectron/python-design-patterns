"""The iterator protocol implemented by hand.

The guide's three rules:
1. the iterable's ``__iter__`` returns a new iterator;
2. the iterator's ``__next__`` returns items and raises ``StopIteration``;
3. the iterator's ``__iter__`` returns itself.
"""

from __future__ import annotations


class OddNumbers:
    """An iterable: knows its contents, delegates traversal."""

    def __init__(self, maximum: int) -> None:
        self.maximum = maximum

    def __iter__(self) -> OddIterator:
        return OddIterator(self)


class OddIterator:
    """An iterator: owns the cursor state."""

    def __init__(self, container: OddNumbers) -> None:
        self.container = container
        self.n = -1

    def __next__(self) -> int:
        self.n += 2
        if self.n > self.container.maximum:
            raise StopIteration
        return self.n

    def __iter__(self) -> OddIterator:
        return self


def main() -> None:
    numbers = OddNumbers(7)
    print(list(numbers))
    print(list(numbers))  # a fresh iterator each time -- iteration restarts


if __name__ == "__main__":
    main()
