"""Behavioral tests for the notification-router mini-project."""

from __future__ import annotations

import json

import pytest

from patterns.principle.composition_over_inheritance.examples.notification_router import (
    Alert,
    Dedup,
    FakeWebhook,
    MemorySink,
    Notifier,
    Router,
    as_json,
    min_severity,
    plain_text,
)
from patterns.principle.composition_over_inheritance.examples.notification_router.__main__ import (
    main,
)


def alert(severity: int, message: str = "m", source: str = "api") -> Alert:
    return Alert(source, severity, message)


class TestAxes:
    def test_min_severity_parameterizes_instead_of_subclassing(self) -> None:
        assert min_severity(3)(alert(3)) is True
        assert min_severity(3)(alert(2)) is False

    def test_dedup_passes_each_alert_once(self) -> None:
        dedup = Dedup()
        assert dedup(alert(5, "primary down", "db")) is True
        assert dedup(alert(5, "primary down", "db")) is False
        assert dedup(alert(5, "replica down", "db")) is True  # different message

    def test_formats_reshape_the_same_alert_differently(self) -> None:
        sample = alert(5, "primary down", "db")
        assert plain_text(sample) == "[5] db: primary down"
        assert json.loads(as_json(sample)) == {
            "source": "db",
            "severity": 5,
            "message": "primary down",
        }


class TestComposition:
    def test_two_behaviors_one_class_zero_subclasses(self) -> None:
        chatty, pager = MemorySink(), MemorySink()
        router = Router(
            notifiers=(
                Notifier(filters=(min_severity(2),), format=plain_text, deliver=chatty),
                Notifier(filters=(min_severity(4), Dedup()), format=as_json, deliver=pager),
            )
        )
        router.broadcast(alert(2, "latency rising"))
        router.broadcast(alert(5, "primary down", "db"))
        router.broadcast(alert(5, "primary down", "db"))  # duplicate
        assert len(chatty.lines) == 3  # console repeats; that is its policy
        assert len(pager.lines) == 1  # webhook policy dedups
        assert type(router.notifiers[0]) is type(router.notifiers[1])  # one class

    def test_send_reports_whether_delivery_happened(self) -> None:
        sink = MemorySink()
        notifier = Notifier(filters=(min_severity(4),), format=plain_text, deliver=sink)
        assert notifier.send(alert(5)) is True
        assert notifier.send(alert(1)) is False
        assert len(sink.lines) == 1

    def test_fake_webhook_records_payloads(self) -> None:
        webhook = FakeWebhook("https://pager.example/hook")
        Notifier(filters=(), format=as_json, deliver=webhook).send(alert(5, "down", "db"))
        assert json.loads(webhook.posted[0])["source"] == "db"


class TestDemo:
    def test_main_dedups_the_duplicate_page(self, capsys: pytest.CaptureFixture[str]) -> None:
        main()
        out = capsys.readouterr().out
        assert "webhook received 1 page(s)" in out
        assert "[5] db: primary down" in out  # console saw it (twice, its policy)
