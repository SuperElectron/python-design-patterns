"""A typed plugin registry: a dict, a decorator, and one lookup policy.

``Registry`` maps names to implementations. Defining a handler registers it
(``@registry.register("csv")``); dispatch is ``registry.get(name)``. The two
policies the folk pattern leaves implicit are explicit here: duplicate names
are an error unless ``replace=True``, and unknown names raise
``UnknownKeyError`` naming what *is* registered.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar

T = TypeVar("T")


class UnknownKeyError(LookupError):
    """The name is not registered; the message lists the names that are."""


class Registry(Generic[T]):
    """A name-to-implementation mapping filled by decorator."""

    def __init__(self, kind: str = "entry") -> None:
        self._kind = kind  # names the registry's contents in error messages
        self._entries: dict[str, T] = {}

    def register(self, name: str, *, replace: bool = False) -> Callable[[T], T]:
        """Return a decorator that registers its target under ``name``.

        Duplicate names raise ``ValueError`` — a silent overwrite is how two
        plugins fight over a name without anyone noticing — unless the caller
        says ``replace=True``.
        """

        def decorator(entry: T) -> T:
            if name in self._entries and not replace:
                raise ValueError(f"{self._kind} {name!r} is already registered (pass replace=True)")
            self._entries[name] = entry
            return entry

        return decorator

    def get(self, name: str) -> T:
        """Look up one entry; unknown names fail loudly, listing known ones."""
        try:
            return self._entries[name]
        except KeyError:
            known = ", ".join(sorted(self._entries)) or "<none>"
            raise UnknownKeyError(f"unknown {self._kind} {name!r} (known: {known})") from None

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._entries))

    def __contains__(self, name: object) -> bool:
        return name in self._entries

    def __len__(self) -> int:
        return len(self._entries)
