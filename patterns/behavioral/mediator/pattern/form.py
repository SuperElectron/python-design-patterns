"""Mediator as an importable building block: dumb fields, one rule owner.

The pattern's Python lesson is a division of labor: widgets hold a value
and report changes; *every* cross-widget rule lives in one mediator method.
``Field`` is the colleague half — a value holder with no rules. ``Form`` is
the mediator half: it creates the fields wired back to itself and owns the
single ``recheck`` hook where all coordination lives.
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


class Form:
    """The mediator base: owns its fields and every cross-field rule.

    Subclasses implement ``recheck`` — the one place rules live. Fields are
    created through ``add_field`` so each one notifies this mediator and
    none can be wired to two coordinators by accident.
    """

    def __init__(self) -> None:
        self._fields: dict[str, Field] = {}

    def add_field(self, name: str) -> Field:
        """Create and register a field wired to this mediator's recheck."""
        if name in self._fields:
            raise ValueError(f"field {name!r} already registered (pass a fresh name)")
        created = Field(self.recheck)
        self._fields[name] = created
        return created

    def field_names(self) -> list[str]:
        """Registration order — the mediator knows its colleagues."""
        return list(self._fields)

    def recheck(self) -> None:
        """Re-derive every dependent value; subclasses own the rules."""
        raise NotImplementedError
