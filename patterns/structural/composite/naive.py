"""The Gang of Four Composite, translated literally.

Abstract component, leaf, and composite -- including the book's contested
choice of declaring child management on the component so the leaf must
refuse it at runtime.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Graphic(ABC):
    """The component interface every node implements."""

    @abstractmethod
    def render(self, indent: int = 0) -> str: ...

    def add(self, child: Graphic) -> None:
        raise TypeError(f"{type(self).__name__} cannot hold children")


class Circle(Graphic):
    """A leaf: no children, and add() raises per the base default."""

    def __init__(self, name: str) -> None:
        self.name = name

    def render(self, indent: int = 0) -> str:
        return " " * indent + f"circle({self.name})"


class Group(Graphic):
    """A composite: renders by recursing over children."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._children: list[Graphic] = []

    def add(self, child: Graphic) -> None:
        self._children.append(child)

    def render(self, indent: int = 0) -> str:
        lines = [" " * indent + f"group({self.name})"]
        lines.extend(child.render(indent + 2) for child in self._children)
        return "\n".join(lines)


def main() -> None:
    scene = Group("scene")
    scene.add(Circle("sun"))
    inner = Group("cluster")
    inner.add(Circle("a"))
    inner.add(Circle("b"))
    scene.add(inner)
    print(scene.render())


if __name__ == "__main__":
    main()
