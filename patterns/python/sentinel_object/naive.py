"""The failure modes sentinels fix.

1. The in-band sentinel value: str.find's -1 is a legal integer, so forgetting
   the check produces a *plausible* wrong answer instead of an error.
2. None-as-missing: a cache that stores None cannot tell a hit from a miss.
"""

from __future__ import annotations


def last_char_before(text: str, needle: str) -> str:
    """BUG (deliberate): when needle is absent, find() returns -1 and the
    index silently becomes text[-2] -- plausible garbage, no exception."""
    position = text.find(needle)
    return text[position - 1]


class NoneCache:
    """A cache where storing None is indistinguishable from a miss."""

    def __init__(self) -> None:
        self._data: dict[str, object | None] = {}

    def put(self, key: str, value: object | None) -> None:
        self._data[key] = value

    def get_or_compute(self, key: str, compute_calls: list[str]) -> object | None:
        value = self._data.get(key)
        if value is None:  # ... but None might BE the cached value!
            compute_calls.append(key)
            value = None  # pretend we recomputed
            self._data[key] = value
        return value


def main() -> None:
    print(f"present: {last_char_before('hello', 'e')!r}")
    print(f"absent -- plausible garbage: {last_char_before('hello', 'z')!r}")
    cache = NoneCache()
    calls: list[str] = []
    cache.put("k", None)
    cache.get_or_compute("k", calls)
    cache.get_or_compute("k", calls)
    print(f"cached None recomputed every time: {calls}")


if __name__ == "__main__":
    main()
