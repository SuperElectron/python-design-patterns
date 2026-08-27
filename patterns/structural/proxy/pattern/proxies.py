"""Three composable proxies: lazy, protection, metering.

Each forwards attribute access to a subject via ``__getattr__`` -- no shared
interface required -- and each adds exactly one kind of mediation. Because
every proxy is also a plain object, they stack:
``MeteringProxy(ProtectionProxy(LazyProxy(build), allow))``.

The disguise is skin-deep (this unit's standing caveat): ``isinstance``,
identity, and dunder lookups all see the proxy, not the subject.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from typing import Any

# Not-yet-built marker: ``None`` won't do, because a factory may legitimately
# return ``None`` and that result must still be cached exactly once.
_MISSING = object()


class LazyProxy:
    """Defer construction: the subject is built on first attribute access."""

    def __init__(self, factory: Callable[[], object]) -> None:
        # object.__setattr__-free here: plain attributes are fine because
        # __getattr__ only fires for names *not* found on the proxy itself.
        self._factory = factory
        self._subject: object = _MISSING

    @property
    def is_built(self) -> bool:
        """Whether the expensive subject exists yet."""
        return self._subject is not _MISSING

    def __getattr__(self, name: str) -> Any:
        if self._subject is _MISSING:
            self._subject = self._factory()
        return getattr(self._subject, name)


class ProtectionProxy:
    """Guard access: every attribute name passes ``allow`` or raises."""

    def __init__(self, subject: object, allow: Callable[[str], bool]) -> None:
        self._subject = subject
        self._allow = allow

    def __getattr__(self, name: str) -> Any:
        if not self._allow(name):
            raise PermissionError(f"access to {name!r} denied")
        return getattr(self._subject, name)


class MeteringProxy:
    """Observe access: count every attribute lookup by name, then forward."""

    def __init__(self, subject: object) -> None:
        self._subject = subject
        self.access_counts: Counter[str] = Counter()

    def __getattr__(self, name: str) -> Any:
        self.access_counts[name] += 1
        return getattr(self._subject, name)
