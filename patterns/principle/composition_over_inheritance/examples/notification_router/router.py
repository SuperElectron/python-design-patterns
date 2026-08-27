"""The composition point: one Notifier class, any behavior combination."""

from __future__ import annotations

from dataclasses import dataclass

from patterns.principle.composition_over_inheritance.examples.notification_router.models import (
    Alert,
)
from patterns.principle.composition_over_inheritance.pattern import Filter, Sink, Transform


@dataclass
class Notifier:
    """One class, ever. A new combination is a constructor call, not a subclass."""

    filters: tuple[Filter[Alert], ...]
    format: Transform[Alert, str]
    deliver: Sink[str]

    def send(self, alert: Alert) -> bool:
        """Deliver if every filter accepts; report whether delivery happened."""
        if not all(accepts(alert) for accepts in self.filters):
            return False
        self.deliver(self.format(alert))
        return True


@dataclass
class Router:
    """Fan-out: every notifier sees every alert, each applies its own policy."""

    notifiers: tuple[Notifier, ...]

    def broadcast(self, alert: Alert) -> int:
        return sum(1 for notifier in self.notifiers if notifier.send(alert))
