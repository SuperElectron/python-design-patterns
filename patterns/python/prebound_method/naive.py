"""The alternatives the guide rejects.

Option A: bare functions over a loose module global -- state and the
functions that guard it are separated, and moving to two independent
counters later means rewriting every caller.

Option B: no module-level API at all -- every caller instantiates.
"""

from __future__ import annotations

# Option A: the state is just ... lying there.
_count = 0


def increment() -> int:
    global _count
    _count += 1
    return _count


# Option B: callers must build and thread their own instance.
class Counter:
    def __init__(self) -> None:
        self.count = 0

    def increment(self) -> int:
        self.count += 1
        return self.count


def main() -> None:
    print(f"loose global: {increment()}, {increment()}")
    counter = Counter()  # every caller, everywhere, forever
    print(f"DIY instance: {counter.increment()}")


if __name__ == "__main__":
    main()
