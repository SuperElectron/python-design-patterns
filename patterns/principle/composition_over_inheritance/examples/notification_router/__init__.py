"""An alert router built on Composition Over Inheritance.

Run it: ``uv run python -m patterns.principle.composition_over_inheritance\
.examples.notification_router``
"""

from patterns.principle.composition_over_inheritance.examples.notification_router.axes import (
    Dedup,
    FakeWebhook,
    MemorySink,
    as_json,
    console,
    min_severity,
    plain_text,
)
from patterns.principle.composition_over_inheritance.examples.notification_router.models import (
    Alert,
)
from patterns.principle.composition_over_inheritance.examples.notification_router.router import (
    Notifier,
    Router,
)

__all__ = [
    "Alert",
    "Dedup",
    "FakeWebhook",
    "MemorySink",
    "Notifier",
    "Router",
    "as_json",
    "console",
    "min_severity",
    "plain_text",
]
