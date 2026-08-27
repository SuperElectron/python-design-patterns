"""Behavioral tests for the notification-router mini-project."""

from __future__ import annotations

import json
from collections.abc import Callable

import pytest

from patterns.principle.composition_over_inheritance.examples.notification_router import (
    Alert,
    Dedup,
    FakeWebhook,
    MemorySink,
    Notifier,
    Router,
    as_json,
    console,
    min_severity,
    plain_text,
)
from patterns.principle.composition_over_inheritance.examples.notification_router.__main__ import (
    main,
)
from patterns.principle.composition_over_inheritance.pattern import Filter


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


SAMPLE = Alert("db", 5, "primary down")

#: Expected payload per format for SAMPLE — content, not just counts.
EXPECTED = {
    "plain_text": "[5] db: primary down",
    "as_json": json.dumps({"source": "db", "severity": 5, "message": "primary down"}),
}


class TestEveryCombination:
    """The headline claim, demonstrated: 2 filters x 2 formats x 3 sinks = 12
    behaviors from 7 small pieces and zero subclasses."""

    @pytest.mark.parametrize("filter_name", ["min_severity", "dedup"])
    @pytest.mark.parametrize("format_name", ["plain_text", "as_json"])
    @pytest.mark.parametrize("sink_name", ["memory", "webhook", "console"])
    def test_the_full_cross_product_delivers_the_right_content(
        self,
        filter_name: str,
        format_name: str,
        sink_name: str,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        chosen_filter: Filter[Alert] = min_severity(4) if filter_name == "min_severity" else Dedup()
        transform = {"plain_text": plain_text, "as_json": as_json}[format_name]

        sink: Callable[[str], None]
        delivered: Callable[[], str]
        if sink_name == "memory":
            memory = MemorySink()
            sink, delivered = memory, lambda: memory.lines[0]
        elif sink_name == "webhook":
            webhook = FakeWebhook("https://pager.example/hook")
            sink, delivered = webhook, lambda: webhook.posted[0]
        else:
            sink, delivered = console, lambda: capsys.readouterr().out.rstrip("\n")

        notifier = Notifier(filters=(chosen_filter,), transform=transform, sink=sink)
        assert notifier.process(SAMPLE) is True
        assert delivered() == EXPECTED[format_name]


class TestComposition:
    def test_two_behaviors_one_class_zero_subclasses(self) -> None:
        chatty, pager = MemorySink(), MemorySink()
        router = Router(
            notifiers=(
                Notifier(filters=(min_severity(2),), transform=plain_text, sink=chatty),
                Notifier(filters=(min_severity(4), Dedup()), transform=as_json, sink=pager),
            )
        )
        router.broadcast(alert(2, "latency rising"))
        router.broadcast(alert(5, "primary down", "db"))
        router.broadcast(alert(5, "primary down", "db"))  # duplicate
        assert chatty.lines == [
            "[2] api: latency rising",
            "[5] db: primary down",
            "[5] db: primary down",  # console repeats; that is its policy
        ]
        assert pager.lines == [EXPECTED["as_json"]]  # webhook policy dedups
        assert type(router.notifiers[0]) is type(router.notifiers[1])  # one class

    def test_filter_order_is_policy_dedup_must_not_see_vetoed_alerts(self) -> None:
        # min_severity runs before Dedup, so a sub-threshold alert must not
        # poison the dedup memory: the later legitimate page still goes out.
        pager = MemorySink()
        notifier = Notifier(filters=(min_severity(4), Dedup()), transform=plain_text, sink=pager)
        assert notifier.process(alert(1, "primary down", "db")) is False  # vetoed
        assert notifier.process(alert(5, "primary down", "db")) is True  # delivered
        assert pager.lines == ["[5] db: primary down"]

    def test_process_reports_whether_delivery_happened(self) -> None:
        sink = MemorySink()
        notifier = Notifier(filters=(min_severity(4),), transform=plain_text, sink=sink)
        assert notifier.process(alert(5)) is True
        assert notifier.process(alert(1)) is False
        assert sink.lines == ["[5] api: m"]


class TestDemo:
    def test_main_dedups_the_duplicate_page(self, capsys: pytest.CaptureFixture[str]) -> None:
        main()
        out = capsys.readouterr().out
        assert "webhook received 1 page(s)" in out
        assert "[5] db: primary down" in out  # console saw it (twice, its policy)
