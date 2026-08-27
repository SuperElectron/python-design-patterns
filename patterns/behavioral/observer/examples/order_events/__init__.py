"""Order events with independent subscribers, built on the Observer pattern.

Run it: ``uv run python -m patterns.behavioral.observer.examples.order_events``
"""

from patterns.behavioral.observer.examples.order_events.models import OrderEvent
from patterns.behavioral.observer.examples.order_events.subscribers import (
    AuditLog,
    EmailNotifier,
    MetricsCounter,
    OrderPipeline,
    flaky_webhook,
)

__all__ = [
    "AuditLog",
    "EmailNotifier",
    "MetricsCounter",
    "OrderEvent",
    "OrderPipeline",
    "flaky_webhook",
]
