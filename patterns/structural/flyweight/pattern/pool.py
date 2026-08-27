"""Flyweight as an importable building block: a keyed intern pool.

``InternPool`` fronts construction with a pool: identical keys yield the
*identical* object. It is the explicit, inspectable form of what
``functools.lru_cache`` on a factory does implicitly — and the pool only
stays safe if the pooled values are immutable, which ``get`` can enforce.
"""

from __future__ import annotations

from collections.abc import Callable, Hashable
from dataclasses import fields, is_dataclass
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


def _is_frozen(value: object) -> bool:
    # Best-effort immutability check for the guard rail: frozen dataclasses
    # and common immutable builtins pass; everything else is the caller's
    # own risk and rejected under strict=True.
    if is_dataclass(value) and not isinstance(value, type):
        params = getattr(type(value), "__dataclass_params__", None)
        return bool(params and params.frozen) and all(
            _is_frozen(getattr(value, f.name)) for f in fields(value)
        )
    return isinstance(value, (str, bytes, int, float, bool, frozenset, tuple, type(None)))


class InternPool(Generic[K, V]):
    """Share one instance per distinct key.

    ``build`` constructs a value the first time a key appears; every later
    request for that key returns the same object. With ``strict=True`` the
    pool refuses values it cannot verify as immutable — a mutated shared
    instance corrupts every holder at once.
    """

    def __init__(self, build: Callable[[K], V], *, strict: bool = False) -> None:
        self._build = build
        self._strict = strict
        self._pool: dict[K, V] = {}

    def get(self, key: K) -> V:
        """Return the shared instance for ``key``, building it on first use."""
        try:
            return self._pool[key]
        except KeyError:
            value = self._build(key)
            if self._strict and not _is_frozen(value):
                raise TypeError(
                    f"InternPool(strict=True) refuses mutable value {value!r}; "
                    "flyweights must be immutable"
                ) from None
            self._pool[key] = value
            return value

    def __len__(self) -> int:
        """How many distinct instances exist — the number sharing saves you to."""
        return len(self._pool)

    def __contains__(self, key: object) -> bool:
        return key in self._pool
