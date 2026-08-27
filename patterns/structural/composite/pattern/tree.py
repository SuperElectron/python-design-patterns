"""Composite as an importable, typed building block — with honest interfaces.

A tree node is anything with ``total() -> V``; leaves are your own frozen
domain objects. ``Composite`` is the one container: it manages children
(that's where ``add``/``remove`` honestly belong — never on leaves) and rolls
totals up by combining its children's. Any value that can be summed works as
``V`` — an ``int``, or a metrics dataclass with ``__add__``.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Generic, Protocol, TypeVar

V = TypeVar("V")
V_co = TypeVar("V_co", covariant=True)


class HasTotal(Protocol[V_co]):
    """What every node — leaf or subtree — must offer: one rollup value."""

    def total(self) -> V_co: ...


class Composite(Generic[V]):
    """A container node: holds children, rolls their totals up."""

    def __init__(
        self,
        combine: Callable[[Iterable[V]], V],
        children: Iterable[HasTotal[V]] = (),
    ) -> None:
        self._combine = combine
        self._children: list[HasTotal[V]] = list(children)

    def add(self, child: HasTotal[V]) -> None:
        """Child management lives here, on the container — not on leaves."""
        self._children.append(child)

    def remove(self, child: HasTotal[V]) -> None:
        """Remove a direct child; ``ValueError`` if it is not one."""
        self._children.remove(child)

    def total(self) -> V:
        """Same interface as a leaf: callers never ask which kind they hold."""
        return self._combine(child.total() for child in self._children)

    def __iter__(self) -> Iterator[HasTotal[V]]:
        return iter(self._children)

    def __len__(self) -> int:
        return len(self._children)
