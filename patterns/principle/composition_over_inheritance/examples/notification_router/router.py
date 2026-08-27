"""The composition point, instantiated for the notification domain."""

from __future__ import annotations

from dataclasses import dataclass

from patterns.principle.composition_over_inheritance.examples.notification_router.models import (
    Alert,
)
from patterns.principle.composition_over_inheritance.pattern import Pipeline

#: One class, ever — the pattern's ``Pipeline`` bound to the alert domain.
#: A new behavior combination is a constructor call, not a subclass.
Notifier = Pipeline[Alert, str]


@dataclass
class Router:
    """Fan-out: every notifier sees every alert, each applies its own policy."""

    notifiers: tuple[Notifier, ...]

    def broadcast(self, alert: Alert) -> int:
        return sum(1 for notifier in self.notifiers if notifier.process(alert))
