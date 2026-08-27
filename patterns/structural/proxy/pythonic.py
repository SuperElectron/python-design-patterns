"""Lazy access, two pythonic sizes.

A generic ``__getattr__`` proxy defers construction of *any* object; and
when the goal is one expensive attribute, ``functools.cached_property``
is the whole pattern.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import cached_property
from typing import Any


class LazyProxy:
    """Builds the real object on first attribute access, then forwards."""

    def __init__(self, factory: Callable[[], object]) -> None:
        # Avoid __setattr__/__getattr__ recursion via object.__setattr__.
        object.__setattr__(self, "_factory", factory)
        object.__setattr__(self, "_real", None)

    def __getattr__(self, name: str) -> Any:
        real = object.__getattribute__(self, "_real")
        if real is None:
            real = object.__getattribute__(self, "_factory")()
            object.__setattr__(self, "_real", real)
        return getattr(real, name)


class Dataset:
    """cached_property: the one-attribute proxy, built into functools."""

    def __init__(self, raw: list[int]) -> None:
        self.raw = raw
        self.computations = 0

    @cached_property
    def stats(self) -> tuple[int, int]:
        self.computations += 1
        return (min(self.raw), max(self.raw))


def main() -> None:
    built: list[str] = []

    def factory() -> object:
        built.append("now")
        return "the real string"

    proxy = LazyProxy(factory)
    print(f"built before use: {built}")
    print(f"forwarded upper(): {proxy.upper()}, built: {built}")

    data = Dataset([3, 1, 4])
    print(f"stats {data.stats} computed {data.computations} time(s) over 2 reads: {data.stats}")


if __name__ == "__main__":
    main()
