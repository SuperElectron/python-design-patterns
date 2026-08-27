"""The Gang of Four Prototype, translated literally.

An abstract ``clone()`` interface, concrete prototypes, and a registry of
exemplars that are copied -- never handed out directly -- on request.
"""

from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from typing import Self


class Shape(ABC):
    """The prototype interface."""

    @abstractmethod
    def clone(self) -> Self: ...


class Circle(Shape):
    def __init__(self, radius: int, color: str) -> None:
        self.radius = radius
        self.color = color

    def clone(self) -> Self:
        return copy.deepcopy(self)


class PrototypeRegistry:
    """Menu of pre-configured exemplars; every request gets a private copy."""

    def __init__(self) -> None:
        self._prototypes: dict[str, Shape] = {}

    def register(self, name: str, prototype: Shape) -> None:
        self._prototypes[name] = prototype

    def create(self, name: str) -> Shape:
        return self._prototypes[name].clone()


def main() -> None:
    registry = PrototypeRegistry()
    registry.register("small-red", Circle(radius=1, color="red"))

    a = registry.create("small-red")
    b = registry.create("small-red")
    print(f"independent copies: {a is not b}")


if __name__ == "__main__":
    main()
