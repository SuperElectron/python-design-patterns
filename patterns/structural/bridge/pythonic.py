"""The Bridge without ceremony: composition plus an injected dependency.

A Protocol types the implementor side; shapes are dataclasses holding one.
Nothing here is special -- and that is the point.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Renderer(Protocol):
    def circle(self, radius: float) -> str: ...


class Vector:
    def circle(self, radius: float) -> str:
        return f"<circle r={radius}/>"


class Raster:
    def circle(self, radius: float) -> str:
        return f"pixels for a circle of radius {radius}"


@dataclass(frozen=True)
class Circle:
    radius: float
    renderer: Renderer

    def draw(self) -> str:
        return self.renderer.circle(self.radius)


def main() -> None:
    print(Circle(2.0, Vector()).draw())
    print(Circle(2.0, Raster()).draw())


if __name__ == "__main__":
    main()
