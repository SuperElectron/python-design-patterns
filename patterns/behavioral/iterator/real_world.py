"""``itertools``: the stdlib's iterator toolbox.

Iterators compose: ``count`` is infinite, ``islice`` bounds it, and nothing
is computed until iteration demands it.
"""

from __future__ import annotations

import itertools
from collections.abc import Iterator


def first_n_odd_squares(n: int) -> Iterator[int]:
    """A lazy pipeline over an infinite source."""
    odds = itertools.count(start=1, step=2)  # 1, 3, 5, ... forever
    return itertools.islice((x * x for x in odds), n)


def main() -> None:
    print(list(first_n_odd_squares(5)))
    evens_then_odds = itertools.chain([0, 2, 4], [1, 3, 5])
    print(list(evens_then_odds))


if __name__ == "__main__":
    main()
