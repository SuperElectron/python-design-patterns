"""State as an importable, typed building block.

The machine is data: a transition table mapping ``(state, event)`` to the
next state, optional guards that can veto a listed transition, and a log of
every step taken. States and events are any hashable values — ``Enum``
members read best.
"""

from __future__ import annotations

from collections.abc import Callable, Hashable, Mapping
from dataclasses import dataclass
from typing import Generic, TypeVar

State = TypeVar("State", bound=Hashable)
Event = TypeVar("Event", bound=Hashable)

Guard = Callable[[], bool]


class IllegalTransitionError(Exception):
    """The event is not allowed from the current state."""


@dataclass(frozen=True)
class Step(Generic[State, Event]):
    """One recorded transition: where the machine was, what moved it, where it went."""

    source: State
    event: Event
    target: State


class StateMachine(Generic[State, Event]):
    """An explicit-table state machine with guards and a transition log."""

    def __init__(
        self,
        initial: State,
        table: Mapping[tuple[State, Event], State],
        guards: Mapping[tuple[State, Event], Guard] | None = None,
    ) -> None:
        self._state = initial
        self._table = dict(table)
        self._guards = dict(guards or {})
        self.log: list[Step[State, Event]] = []

    @property
    def state(self) -> State:
        return self._state

    def can(self, event: Event) -> bool:
        """True if the event is in the table AND its guard (if any) passes."""
        key = (self._state, event)
        if key not in self._table:
            return False
        guard = self._guards.get(key)
        return guard() if guard is not None else True

    def trigger(self, event: Event) -> State:
        """Fire an event: move to the target state or raise, never half-move."""
        key = (self._state, event)
        if key not in self._table:
            allowed = sorted(str(e) for s, e in self._table if s == self._state)
            raise IllegalTransitionError(
                f"{event} is not allowed from {self._state} (allowed: {allowed or 'none'})"
            )
        guard = self._guards.get(key)
        if guard is not None and not guard():
            raise IllegalTransitionError(f"{event} from {self._state} rejected by its guard")
        target = self._table[key]
        self.log.append(Step(self._state, event, target))
        self._state = target
        return target
