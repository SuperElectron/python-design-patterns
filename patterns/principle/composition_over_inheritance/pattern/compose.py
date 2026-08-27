"""Composition Over Inheritance as importable, typed building blocks.

The principle's vocabulary: each independent axis of variation is a small
callable — something that decides (``Filter``), something that reshapes
(``Transform``), something that acts (``Sink``) — and ``Pipeline`` is the
one composition point that wires a piece per axis together. ``Logger`` is
the guide's own worked shape, built *on* ``Pipeline`` rather than beside
it: M filters + N transforms cover M x N behaviors with M + N pieces.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")
In = TypeVar("In")
Out = TypeVar("Out")

#: One alias per axis kind — the principle's whole type system.
Filter = Callable[[T], bool]
Transform = Callable[[T], U]
Sink = Callable[[T], None]


def identity(message: str) -> str:
    """The do-nothing Transform: a composed axis can opt out explicitly."""
    return message


@dataclass
class Pipeline(Generic[In, Out]):
    """The composition point: one piece per axis, wired once, no subclasses.

    Filters run in declaration order and short-circuit (``all``). That order
    is behavior when a filter keeps state: put cheap vetoes before
    state-recording filters, or the recorder remembers items that were never
    delivered.
    """

    filters: tuple[Filter[In], ...]
    transform: Transform[In, Out]
    sink: Sink[Out]

    def process(self, item: In) -> bool:
        """Deliver if every filter accepts; report whether delivery happened."""
        if not all(accepts(item) for accepts in self.filters):
            return False
        self.sink(self.transform(item))
        return True


@dataclass
class Logger:
    """The guide's worked shape, composed from ``Pipeline``.

    The sink axis here is "append to my lines": ``sink`` stays a plain
    ``list[str]`` so callers and tests read results directly, and the
    ``Sink`` handed to the underlying ``Pipeline`` is ``sink.append``.
    """

    sink: list[str] = field(default_factory=list)
    filters: tuple[Filter[str], ...] = ()
    transform: Transform[str, str] = identity

    def log(self, message: str) -> None:
        Pipeline(self.filters, self.transform, self.sink.append).process(message)
