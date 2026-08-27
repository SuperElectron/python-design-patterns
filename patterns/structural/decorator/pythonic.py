"""Python's native form: the function decorator.

Two shapes you need: the plain decorator (two layers) and the parameterized
decorator (three layers). Both use ``functools.wraps`` so the wrapped
function keeps its identity under introspection.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import TypeVar

R = TypeVar("R")


def count_calls(func: Callable[..., R]) -> Callable[..., R]:
    """Plain decorator: adds a call counter to any function."""

    @functools.wraps(func)
    def wrapper(*args: object, **kwargs: object) -> R:
        wrapper.calls += 1  # type: ignore[attr-defined]
        return func(*args, **kwargs)

    wrapper.calls = 0  # type: ignore[attr-defined]
    return wrapper


def repeat(times: int) -> Callable[[Callable[..., R]], Callable[..., list[R]]]:
    """Parameterized decorator: the outer layer takes the arguments."""

    def decorator(func: Callable[..., R]) -> Callable[..., list[R]]:
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> list[R]:
            return [func(*args, **kwargs) for _ in range(times)]

        return wrapper

    return decorator


@count_calls
def greet(name: str) -> str:
    """Say hello."""
    return f"hello {name}"


@repeat(times=3)
def beep() -> str:
    return "beep"


def main() -> None:
    print(greet("ada"), greet("grace"))
    print(f"calls: {greet.calls}")  # type: ignore[attr-defined]
    print(f"wraps preserved identity: {greet.__name__!r}, {greet.__doc__!r}")
    print(beep())


if __name__ == "__main__":
    main()
