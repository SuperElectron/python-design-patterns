"""Demo: one order's life, four independent listeners, one of them down."""

from __future__ import annotations

from patterns.behavioral.observer.examples.order_events.subscribers import (
    AuditLog,
    EmailNotifier,
    MetricsCounter,
    OrderPipeline,
    flaky_webhook,
)


def main() -> None:
    pipeline = OrderPipeline()
    email, metrics, audit = EmailNotifier(), MetricsCounter(), AuditLog()
    for subscriber in (email, metrics, audit, flaky_webhook):
        pipeline.events.subscribe(subscriber)

    pipeline.advance("A-100", "placed", 42.50)
    pipeline.advance("A-100", "paid", 42.50)
    pipeline.advance("A-100", "shipped", 42.50)

    print(f"email outbox: {email.outbox}")
    print(f"metrics:      {dict(metrics.counts)}")
    print(f"audit trail:  {len(audit.entries)} entries")
    print(f"dead letters: {len(pipeline.dead_letters)} (webhook was down, nobody else noticed)")


if __name__ == "__main__":
    main()
