"""The Gang of Four Flyweight: a factory in front of an instance pool.

Cards are immutable; the factory returns the pooled instance when the same
card is requested again.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Card:
    """The flyweight: intrinsic state only, and frozen."""

    rank: str
    suit: str


class CardFactory:
    """Checks the pool before constructing -- the book's central mechanism."""

    def __init__(self) -> None:
        self._pool: dict[tuple[str, str], Card] = {}

    def get(self, rank: str, suit: str) -> Card:
        key = (rank, suit)
        if key not in self._pool:
            self._pool[key] = Card(rank, suit)
        return self._pool[key]

    @property
    def distinct_cards(self) -> int:
        return len(self._pool)


def main() -> None:
    factory = CardFactory()
    hand = [factory.get("9", "♥"), factory.get("A", "♠"), factory.get("9", "♥")]
    print(f"hand: {hand}")
    print(f"shared: {hand[0] is hand[2]}")
    print(f"distinct objects created: {factory.distinct_cards}")


if __name__ == "__main__":
    main()
