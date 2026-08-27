"""Mediator as an importable building block: dumb fields, one rule owner.

The pattern's Python lesson is a division of labor: widgets hold a value
and report changes; *every* cross-widget rule lives in one mediator method.
``Field`` is the reusable half — a value holder with no rules, wired to
whatever coordinator its owner passes in.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Field:
    """A dumb widget: holds a value, reports changes. No rules, ever."""

    notify: Callable[[], None]
    value: str = ""

    def set(self, value: str) -> None:
        self.value = value
        self.notify()
