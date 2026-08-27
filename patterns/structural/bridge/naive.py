"""The Gang of Four Bridge, translated literally.

Abstraction hierarchy (Shape) holds a reference to the implementor
hierarchy (Renderer); each side can grow without touching the other.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Renderer(ABC):
    """The implementor interface."""

    @abstractmethod
    def render_circle(self, radius: float) -> str: ...


class VectorRenderer(Renderer):
    def render_circle(self, radius: float) -> str:
        return f"<circle r={radius}/>"


class RasterRenderer(Renderer):
    def render_circle(self, radius: float) -> str:
        return f"pixels for a circle of radius {radius}"


class Shape(ABC):
    """The abstraction: holds the bridge reference."""

    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer

    @abstractmethod
    def draw(self) -> str: ...


class Circle(Shape):
    def __init__(self, renderer: Renderer, radius: float) -> None:
        super().__init__(renderer)
        self.radius = radius

    def draw(self) -> str:
        return self.renderer.render_circle(self.radius)


def main() -> None:
    print(Circle(VectorRenderer(), 2.0).draw())
    print(Circle(RasterRenderer(), 2.0).draw())


if __name__ == "__main__":
    main()
