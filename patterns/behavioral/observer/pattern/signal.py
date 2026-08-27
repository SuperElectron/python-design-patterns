"""Observer as an importable, typed building block.

A subscriber is any callable taking the event. ``Signal`` broadcasts to its
subscribers in subscription order, with the failure policy stated up front:
by default a raising subscriber propagates (fail fast); pass ``on_error`` to
isolate subscribers from each other instead.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Generic, TypeVar

Event = TypeVar("Event")

Subscriber = Callable[[Event], None]
ErrorPolicy = Callable[[Exception, "Subscriber[Event]"], None]


class Signal(Generic[Event]):
    """A broadcast list of callables with an explicit failure policy."""

    def __init__(self, on_error: ErrorPolicy[Event] | None = None) -> None:
        self._subscribers: list[Subscriber[Event]] = []
        self._on_error = on_error

    def subscribe(self, subscriber: Subscriber[Event]) -> Subscriber[Event]:
        """Add a subscriber (appending = subscribing); usable as a decorator."""
        self._subscribers.append(subscriber)
        return subscriber

    def unsubscribe(self, subscriber: Subscriber[Event]) -> None:
        """Remove a subscriber; ``ValueError`` if it never subscribed."""
        self._subscribers.remove(subscriber)

    def emit(self, event: Event) -> None:
        """Notify every subscriber in order.

        Iterates over a copy, so subscribers may unsubscribe (even
        themselves) mid-broadcast. A subscriber's exception propagates unless
        an ``on_error`` policy was given, in which case the policy is called
        and the remaining subscribers still run.
        """
        for subscriber in list(self._subscribers):
            try:
                subscriber(event)
            except Exception as err:
                if self._on_error is None:
                    raise
                self._on_error(err, subscriber)

    def __iter__(self) -> Iterator[Subscriber[Event]]:
        return iter(self._subscribers)

    def __len__(self) -> int:
        return len(self._subscribers)
