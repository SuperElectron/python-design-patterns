"""Composition Over Inheritance as importable, typed building blocks.

The principle's vocabulary: each independent axis of variation is a small
callable — something that decides (``Filter``), something that reshapes
(``Transform``), something that acts (``Sink``) — and behavior is assembled
by *composing* them, not by subclassing per combination. ``Logger`` is the
guide's own worked shape: M filters + N transforms cover M x N behaviors
with M + N pieces.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TypeVar

T = TypeVar("T")
U = TypeVar("U")

#: One alias per axis kind — the principle's whole type system.
Filter = Callable[[T], bool]
Transform = Callable[[T], U]
Sink = Callable[[T], None]


def identity(message: str) -> str:
    return message


@dataclass
class Logger:
    """One logger class, ever. Behavior comes from what you compose into it."""

    sink: list[str] = field(default_factory=list)
    filters: tuple[Filter[str], ...] = ()
    transform: Transform[str, str] = identity

    def log(self, message: str) -> None:
        if all(accepts(message) for accepts in self.filters):
            self.sink.append(self.transform(message))
