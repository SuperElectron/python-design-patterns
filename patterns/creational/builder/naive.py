"""The Gang of Four Builder, translated literally.

Abstract builder interface + concrete builders + a Director that walks the
steps. The point of studying it: in Python, every one of these moving parts
except the concrete build steps is ceremony.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class House:
    """The product under construction."""

    def __init__(self) -> None:
        self.parts: list[str] = []

    def describe(self) -> str:
        return " + ".join(self.parts)


class HouseBuilder(ABC):
    """The abstract builder interface the Director programs against."""

    def __init__(self) -> None:
        self.house = House()

    @abstractmethod
    def build_walls(self) -> None: ...

    @abstractmethod
    def build_roof(self) -> None: ...


class StoneHouseBuilder(HouseBuilder):
    def build_walls(self) -> None:
        self.house.parts.append("stone walls")

    def build_roof(self) -> None:
        self.house.parts.append("slate roof")


class WoodHouseBuilder(HouseBuilder):
    def build_walls(self) -> None:
        self.house.parts.append("timber walls")

    def build_roof(self) -> None:
        self.house.parts.append("shingle roof")


class Director:
    """Walks the build steps in order; knows nothing about representations."""

    def construct(self, builder: HouseBuilder) -> House:
        builder.build_walls()
        builder.build_roof()
        return builder.house


def main() -> None:
    director = Director()
    print(director.construct(StoneHouseBuilder()).describe())
    print(director.construct(WoodHouseBuilder()).describe())


if __name__ == "__main__":
    main()
