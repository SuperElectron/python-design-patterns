"""The Global Object pattern's one reusable tool: deferred construction.

Constants and cheap prebuilt objects need no machinery — assign them at
module level and stop. What the pattern *does* need code for is the expensive
global: ``Lazy`` defers construction to first use, keeps ``import`` free of
I/O, and gives tests a reset seam.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar, cast

T = TypeVar("T")

_UNSET = object()  # a sentinel (see python/sentinel_object): None may be a value


class Lazy(Generic[T]):
    """A module-global built on first ``get()``, not at import time.

    Why not ``functools.cache`` on the factory? Two reasons this class earns
    its ~15 lines: the ``_UNSET`` sentinel means a factory that legitimately
    returns ``None`` is still cached exactly once (an ``is None`` check would
    rebuild it forever), and ``reset()``/``initialized`` give tests the seam
    and the proof that the import stayed cheap.

    Not thread-safe: two threads racing the first ``get()`` may both run the
    factory. Fine for the import-time-globals use this pattern serves; wrap
    ``get()`` in a lock if a threaded first touch is real for you.

    >>> table = Lazy(load_expensive_table)   # import: nothing happens
    >>> table.get()                          # first use: built once
    >>> table.reset()                        # tests: order-independence back
    """

    def __init__(self, factory: Callable[[], T]) -> None:
        self._factory = factory
        self._value: object = _UNSET

    @property
    def initialized(self) -> bool:
        """Whether the factory has run — importable proof of a cheap import."""
        return self._value is not _UNSET

    def get(self) -> T:
        """Return the value, constructing it on the first call only."""
        if self._value is _UNSET:
            self._value = self._factory()
        return cast("T", self._value)

    def reset(self) -> None:
        """Discard the value so the next ``get()`` rebuilds — the test seam."""
        self._value = _UNSET
