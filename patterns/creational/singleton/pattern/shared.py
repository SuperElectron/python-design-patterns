"""What to write instead of a Singleton class: a shared-instance accessor.

A module is already a singleton — created once, cached in ``sys.modules`` —
so the simplest form is an ordinary object built at module level (the Global
Object pattern). When construction is expensive or needs configuration first,
``Shared`` wraps the remaining bookkeeping: build on first use, hand back the
same instance after, and — the part the classic form always forgets — an
explicit ``reset()`` seam so tests don't leak state into each other.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar

T = TypeVar("T")


class Shared(Generic[T]):
    """One lazily-built instance behind an accessor, with a test-reset seam.

    Not thread-safe: two threads racing the first ``get`` can each build an
    instance (one wins the slot). Harmless for cheap objects; wrap ``get`` in
    a ``threading.Lock`` if construction has side effects.
    """

    def __init__(self, factory: Callable[[], T]) -> None:
        self._factory = factory
        self._instance: T | None = None

    def get(self) -> T:
        """Build the instance on first call, then keep handing it back."""
        if self._instance is None:
            self._instance = self._factory()
        return self._instance

    def reset(self) -> None:
        """Drop the instance so the next ``get`` builds fresh — for tests."""
        self._instance = None

    @property
    def built(self) -> bool:
        """Whether the instance exists yet (laziness is observable)."""
        return self._instance is not None
