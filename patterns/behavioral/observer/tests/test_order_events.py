"""Behavioral tests for the order-events mini-project."""

from __future__ import annotations

import pytest

from patterns.behavioral.observer.examples.order_events import (
    AuditLog,
    EmailNotifier,
    MetricsCounter,
    OrderPipeline,
    flaky_webhook,
)
from patterns.behavioral.observer.examples.order_events.__main__ import main


def wired_pipeline() -> tuple[OrderPipeline, EmailNotifier, MetricsCounter, AuditLog]:
    pipeline = OrderPipeline()
    email, metrics, audit = EmailNotifier(), MetricsCounter(), AuditLog()
    for subscriber in (email, metrics, audit):
        pipeline.events.subscribe(subscriber)
    return pipeline, email, metrics, audit


class TestIndependentSubscribers:
    def test_every_subscriber_sees_every_event(self) -> None:
        pipeline, _, metrics, audit = wired_pipeline()
        pipeline.advance("A-1", "placed", 10.0)
        pipeline.advance("A-1", "paid", 10.0)
        assert metrics.counts == {"placed": 1, "paid": 1}
        assert len(audit.entries) == 2

    def test_email_reacts_only_to_shipping(self) -> None:
        pipeline, email, _, _ = wired_pipeline()
        pipeline.advance("A-2", "placed", 5.0)
        assert email.outbox == []
        pipeline.advance("A-2", "shipped", 5.0)
        assert email.outbox == ["to customer of A-2: your order shipped!"]

    def test_the_pipeline_needs_no_subscribers_at_all(self) -> None:
        pipeline = OrderPipeline()
        pipeline.advance("A-3", "placed", 1.0)  # nobody listening, no error
        assert pipeline.dead_letters == []


class TestFailureIsolation:
    def test_a_down_webhook_does_not_silence_the_others(self) -> None:
        pipeline, _, metrics, audit = wired_pipeline()
        pipeline.events.subscribe(flaky_webhook)
        pipeline.advance("A-4", "paid", 99.0)
        assert metrics.counts["paid"] == 1
        assert len(audit.entries) == 1

    def test_failures_land_in_the_dead_letter_list_with_a_name(self) -> None:
        pipeline, *_ = wired_pipeline()
        pipeline.events.subscribe(flaky_webhook)
        pipeline.advance("A-5", "shipped", 3.0)
        assert pipeline.dead_letters == ["flaky_webhook: partner endpoint 503"]


class TestDemo:
    def test_main_reports_deliveries_and_the_dead_webhook(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        main()
        out = capsys.readouterr().out
        assert "your order shipped!" in out
        assert "'placed': 1" in out and "'shipped': 1" in out
        assert "dead letters: 3" in out
