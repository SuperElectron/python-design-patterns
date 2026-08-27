"""The subscribers, and the wired-up signal they listen to.

Each subscriber is independent: the order pipeline emits events without
knowing that email, metrics, and audit exist. The signal's error policy is
the deliberate decision here — a failing subscriber is quarantined and
logged, never allowed to silence the others.
"""

from __future__ import annotations

from collections import Counter

from patterns.behavioral.observer.examples.order_events.models import OrderEvent
from patterns.behavioral.observer.pattern import Signal, Subscriber


class EmailNotifier:
    """Pretends to send mail; records what it would have sent."""

    def __init__(self) -> None:
        self.outbox: list[str] = []

    def __call__(self, event: OrderEvent) -> None:
        if event.status == "shipped":
            self.outbox.append(f"to customer of {event.order_id}: your order shipped!")


class MetricsCounter:
    """Counts events by status, the way a stats client would."""

    def __init__(self) -> None:
        self.counts: Counter[str] = Counter()

    def __call__(self, event: OrderEvent) -> None:
        self.counts[event.status] += 1


class AuditLog:
    """Append-only trail of everything that happened."""

    def __init__(self) -> None:
        self.entries: list[str] = []

    def __call__(self, event: OrderEvent) -> None:
        self.entries.append(f"{event.order_id} -> {event.status} (${event.total:.2f})")


def flaky_webhook(event: OrderEvent) -> None:
    """A partner integration that is down today."""
    raise ConnectionError("partner endpoint 503")


class OrderPipeline:
    """The subject: emits an event per status change, knows no subscriber."""

    def __init__(self) -> None:
        self.dead_letters: list[str] = []
        self.events: Signal[OrderEvent] = Signal(on_error=self._quarantine)

    def _quarantine(self, err: Exception, subscriber: Subscriber[OrderEvent]) -> None:
        name = getattr(subscriber, "__name__", type(subscriber).__name__)
        self.dead_letters.append(f"{name}: {err}")

    def advance(self, order_id: str, status: str, total: float) -> None:
        self.events.emit(OrderEvent(order_id, status, total))
