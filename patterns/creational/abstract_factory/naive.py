"""The Gang of Four Abstract Factory, translated literally.

An abstract factory interface, one concrete factory per "family", and a
client that never names a concrete class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal


class NumberFactory(ABC):
    """The abstract factory: builds the number family."""

    @abstractmethod
    def build_number(self, text: str) -> object: ...


class FloatFactory(NumberFactory):
    def build_number(self, text: str) -> object:
        return float(text)


class DecimalFactory(NumberFactory):
    def build_number(self, text: str) -> object:
        return Decimal(text)


def parse_numbers(texts: list[str], factory: NumberFactory) -> list[object]:
    """The client: programmed against the interface only."""
    return [factory.build_number(t) for t in texts]


def main() -> None:
    texts = ["1.1", "2.2"]
    print(parse_numbers(texts, FloatFactory()))
    print(parse_numbers(texts, DecimalFactory()))


if __name__ == "__main__":
    main()
