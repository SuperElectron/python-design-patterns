"""One small piece per axis of variation: filter x format x deliver.

Three axes, a few pieces each. Composed, they cover every combination the
inheritance route would need a class for — no ``DedupJsonWebhookNotifier``
anywhere.
"""

from __future__ import annotations

import json

from patterns.principle.composition_over_inheritance.examples.notification_router.models import (
    Alert,
)
from patterns.principle.composition_over_inheritance.pattern import Filter

# --- axis 1: filters (decide) ------------------------------------------------


def min_severity(threshold: int) -> Filter[Alert]:
    """Parameterization instead of a subclass per threshold."""

    def accepts(alert: Alert) -> bool:
        return alert.severity >= threshold

    return accepts


class Dedup:
    """A stateful filter: each (source, message) passes once."""

    def __init__(self) -> None:
        self._seen: set[tuple[str, str]] = set()

    def __call__(self, alert: Alert) -> bool:
        key = (alert.source, alert.message)
        if key in self._seen:
            return False
        self._seen.add(key)
        return True


# --- axis 2: formats (reshape) -----------------------------------------------


def plain_text(alert: Alert) -> str:
    return f"[{alert.severity}] {alert.source}: {alert.message}"


def as_json(alert: Alert) -> str:
    return json.dumps(
        {"source": alert.source, "severity": alert.severity, "message": alert.message}
    )


# --- axis 3: deliveries (act) ------------------------------------------------


def console(line: str) -> None:
    print(line)


class MemorySink:
    """Delivery for tests and demos: keeps what it was handed."""

    def __init__(self) -> None:
        self.lines: list[str] = []

    def __call__(self, line: str) -> None:
        self.lines.append(line)


class FakeWebhook:
    """Stands in for an HTTP POST; records payloads instead of sending."""

    def __init__(self, url: str) -> None:
        self.url = url
        self.posted: list[str] = []

    def __call__(self, payload: str) -> None:
        self.posted.append(payload)
