"""Visitor in its Python form: ``singledispatch`` families, no ``accept()``.

An operation over a node structure is a family of small functions dispatched
on node type. ``Operation`` wraps ``functools.singledispatch`` with the two
things a visitor needs and the stdlib leaves open: a *strict* default (an
unregistered node type is an error, not a silent pass) and an inspectable
set of handled types.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import singledispatch
from typing import Any, Generic, TypeVar

R = TypeVar("R")
N = TypeVar("N")


class UnhandledNodeError(TypeError):
    """The operation has no case registered for this node type."""


class Operation(Generic[R]):
    """One operation over a node structure, as a type-dispatched family.

    Registering a case is decorating a function whose argument annotation
    names the node type — node classes are never edited.
    """

    def __init__(self, name: str) -> None:
        self.name = name

        @singledispatch
        def dispatch(node: object) -> R:
            handled = ", ".join(sorted(t.__name__ for t in self.registered_types())) or "none"
            raise UnhandledNodeError(
                f"operation {self.name!r} has no case for {type(node).__name__} "
                f"(handles: {handled})"
            )

        self._dispatch = dispatch

    def register(self, case: Callable[[N], R]) -> Callable[[N], R]:
        """Add the case for one node type (read from the annotation)."""
        self._dispatch.register(case)
        return case

    def __call__(self, node: object) -> R:
        return self._dispatch(node)

    def registered_types(self) -> frozenset[type[Any]]:
        return frozenset(t for t in self._dispatch.registry if t is not object)
