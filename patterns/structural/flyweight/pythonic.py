"""Two pythonic flyweights.

1. ``functools.lru_cache`` on a factory function: the cache *is* the pool.
2. The guide's ``__new__`` variant: the class hides the pool, so plain
   construction syntax returns shared instances.
"""

from __future__ import annotations

import functools
from typing import ClassVar


@functools.cache
def get_card(rank: str, suit: str) -> tuple[str, str]:
    """The factory form: identical arguments yield the identical object."""
    return (rank, suit)


class Card:
    """The __new__ form: ``Card('9', '♥') is Card('9', '♥')``.

    The pool is unbounded and unsynchronized: fine for a fixed domain like
    52 cards, wrong for unbounded user-supplied keys or racing threads.
    """

    _pool: ClassVar[dict[tuple[str, str], Card]] = {}

    rank: str
    suit: str

    def __new__(cls, rank: str, suit: str) -> Card:
        key = (rank, suit)
        card = cls._pool.get(key)
        if card is None:
            card = super().__new__(cls)
            card.rank = rank
            card.suit = suit
            cls._pool[key] = card
        return card

    def __repr__(self) -> str:
        return f"<Card {self.rank}{self.suit}>"


def main() -> None:
    print(f"factory form shares:  {get_card('9', '♥') is get_card('9', '♥')}")
    print(f"__new__ form shares:  {Card('9', '♥') is Card('9', '♥')}")
    print(f"distinct stays distinct: {Card('9', '♥') is not Card('A', '♠')}")


if __name__ == "__main__":
    main()
