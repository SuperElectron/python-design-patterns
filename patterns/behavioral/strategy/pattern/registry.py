"""Strategy in its Python form: functions registered as interchangeable rules.

A strategy is any callable ``(argument) -> result``. ``StrategyRegistry``
collects a family of them — registering is decorating — so callers can pick
one by name, run them all, or compare their results.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Generic, TypeVar

In_ = TypeVar("In_")
Out = TypeVar("Out")


class UnknownStrategyError(LookupError):
    """No strategy with that name is registered."""


class StrategyRegistry(Generic[In_, Out]):
    """A named family of interchangeable algorithms.

    New strategies join by being defined (``@registry.register``) — the code
    that *uses* the family never changes.
    """

    def __init__(self) -> None:
        self._strategies: dict[str, Callable[[In_], Out]] = {}

    def register(
        self, strategy: Callable[[In_], Out], *, replace: bool = False
    ) -> Callable[[In_], Out]:
        """Add a strategy under its function name; usable as a decorator.

        A duplicate name is an error unless ``replace=True`` — the key is
        ``__name__``, so two same-named functions from different modules
        collide by accident, and silently dropping a rule is how a discount
        stops applying with nothing logged.
        """
        name = str(getattr(strategy, "__name__", repr(strategy)))
        if name in self._strategies and not replace:
            raise ValueError(f"strategy {name!r} already registered (pass replace=True)")
        self._strategies[name] = strategy
        return strategy

    def unregister(self, name: str) -> None:
        """Remove a strategy by name; membership, like order, is policy."""
        try:
            del self._strategies[name]
        except KeyError:
            known = ", ".join(sorted(self._strategies)) or "none"
            raise UnknownStrategyError(f"no strategy {name!r} (known: {known})") from None

    def get(self, name: str) -> Callable[[In_], Out]:
        """Look one strategy up by name."""
        try:
            return self._strategies[name]
        except KeyError:
            known = ", ".join(sorted(self._strategies)) or "none"
            raise UnknownStrategyError(f"no strategy {name!r} (known: {known})") from None

    def names(self) -> list[str]:
        return list(self._strategies)

    def results(self, argument: In_) -> dict[str, Out]:
        """Run every registered strategy on one argument, keyed by name."""
        return {name: strategy(argument) for name, strategy in self._strategies.items()}

    def __iter__(self) -> Iterator[Callable[[In_], Out]]:
        return iter(self._strategies.values())

    def __len__(self) -> int:
        return len(self._strategies)
