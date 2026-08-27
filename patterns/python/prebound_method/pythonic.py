"""The Prebound Method pattern.

One hidden instance built at import time; its bound methods become the
module's public functions. The class stays public for isolated state.
"""

from __future__ import annotations


class Counter:
    """An ordinary class; instantiable by anyone needing isolation."""

    def __init__(self) -> None:
        self.count = 0

    def increment(self) -> int:
        self.count += 1
        return self.count

    def peek(self) -> int:
        return self.count


_instance = Counter()

#: The pattern: module-level names bound to one instance's methods.
increment = _instance.increment
peek = _instance.peek


def main() -> None:
    print(f"module API: {increment()}, {increment()}, peek={peek()}")
    isolated = Counter()
    print(f"isolated instance unaffected: {isolated.peek()}")


if __name__ == "__main__":
    main()
