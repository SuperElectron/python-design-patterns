"""Demo: two very different notifiers from one class and a handful of pieces."""

from __future__ import annotations

from patterns.principle.composition_over_inheritance.examples.notification_router.axes import (
    Dedup,
    FakeWebhook,
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


def main() -> None:
    webhook = FakeWebhook("https://pager.example/hook")
    router = Router(
        notifiers=(
            Notifier(filters=(min_severity(2),), format=plain_text, deliver=console),
            Notifier(filters=(min_severity(4), Dedup()), format=as_json, deliver=webhook),
        )
    )
    alerts = [
        Alert("api", 2, "latency rising"),
        Alert("db", 5, "primary down"),
        Alert("db", 5, "primary down"),  # duplicate: webhook dedups, console repeats
        Alert("cron", 1, "nightly job finished"),
    ]
    for alert in alerts:
        router.broadcast(alert)
    print(f"webhook received {len(webhook.posted)} page(s): {webhook.posted[0]}")


if __name__ == "__main__":
    main()
