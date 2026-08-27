"""Sentinel objects, done right -- plus a small Null Object.

``_MISSING = object()`` is unforgeable and out-of-band; identity comparison
makes the miss check exact even when None is stored.
"""

from __future__ import annotations

from collections.abc import Callable

_MISSING = object()


class Cache:
    """A cache where None is an ordinary, cacheable value."""

    def __init__(self) -> None:
        self._data: dict[str, object] = {}

    def put(self, key: str, value: object) -> None:
        self._data[key] = value

    def get_or_compute(self, key: str, compute: Callable[[], object]) -> object:
        value = self._data.get(key, _MISSING)
        if value is _MISSING:  # identity: the only correct sentinel check
            value = compute()
            self._data[key] = value
        return value


def greet(name: str, greeting: object = _MISSING) -> str:
    """Distinguish 'not passed' from 'passed None' in a default argument."""
    if greeting is _MISSING:
        return f"hello {name}"
    return f"{greeting} {name}" if greeting is not None else name


class NullLogger:
    """Fowler's Null Object: a real object that intentionally does nothing,
    so callers never branch on 'is there a logger?'."""

    def log(self, message: str) -> None:
        pass


def main() -> None:
    cache = Cache()
    cache.put("k", None)
    calls: list[str] = []
    cache.get_or_compute("k", lambda: calls.append("computed"))
    print(f"cached None respected (no recompute): {calls == []}")
    print(greet("ada"), "|", greet("ada", None), "|", greet("ada", "yo"))
    NullLogger().log("silently fine")


if __name__ == "__main__":
    main()
