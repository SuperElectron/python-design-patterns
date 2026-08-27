"""What to write instead: a registry of callables.

Classes are first-class values in Python, and ``functools.partial`` turns
"this class plus these arguments" into a zero-argument factory. The registry
stores factories; asking for a fresh instance is just calling one.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from functools import partial


@dataclass
class Circle:
    radius: int
    color: str


#: The whole pattern: names mapped to zero-argument factories.
MENU: dict[str, Callable[[], Circle]] = {
    "small-red": partial(Circle, radius=1, color="red"),
    "big-blue": partial(Circle, radius=10, color="blue"),
}


def create(name: str) -> Circle:
    return MENU[name]()


def main() -> None:
    a = create("small-red")
    b = create("small-red")
    print(f"fresh instances: {a is not b}, equal config: {a == b}")
    print(create("big-blue"))


if __name__ == "__main__":
    main()
