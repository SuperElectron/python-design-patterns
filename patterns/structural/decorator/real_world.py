"""The stdlib decorating itself.

``functools.lru_cache`` wraps a function with memoization -- the Decorator
pattern shipping in the standard library, cache statistics included.
"""

from __future__ import annotations

import functools


@functools.cache
def fib(n: int) -> int:
    """Naively exponential -- linear once decorated."""
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def main() -> None:
    print(f"fib(60) = {fib(60)}")
    info = fib.cache_info()
    print(f"cache hits: {info.hits}, misses: {info.misses}")


if __name__ == "__main__":
    main()
