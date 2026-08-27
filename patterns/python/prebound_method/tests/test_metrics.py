"""Behavioral tests for the metrics mini-project."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from patterns.python.prebound_method.examples.metrics import api
from patterns.python.prebound_method.examples.metrics.__main__ import main
from patterns.python.prebound_method.examples.metrics.collector import MetricsCollector
from patterns.python.prebound_method.pattern import shares_instance


@pytest.fixture(autouse=True)
def clean_shared_collector() -> Iterator[None]:
    api.reset()
    yield
    api.reset()


class TestModuleApi:
    def test_all_prebound_names_share_the_hidden_collector(self) -> None:
        assert shares_instance(api.increment, api.timing, api.snapshot, api.reset)

    def test_modules_that_never_met_report_into_one_place(self) -> None:
        api.increment("orders")
        api.increment("orders", by=2)
        api.timing("checkout_ms", 10.0)
        api.timing("checkout_ms", 20.0)
        snap = api.snapshot()
        assert snap["counts"] == {"orders": 3}
        assert snap["timing_avg_ms"] == {"checkout_ms": 15.0}

    def test_reset_is_the_test_seam(self) -> None:
        api.increment("orders")
        api.reset()
        assert api.snapshot() == {"counts": {}, "timing_avg_ms": {}}


class TestIsolation:
    def test_an_isolated_collector_leaves_the_shared_one_alone(self) -> None:
        own = MetricsCollector()
        own.increment("private")
        assert api.snapshot() == {"counts": {}, "timing_avg_ms": {}}
        assert own.snapshot()["counts"] == {"private": 1}


class TestDemo:
    def test_main_reports_orders_and_the_shared_instance(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        main()
        out = capsys.readouterr().out
        assert "one hidden instance: True" in out
        assert "'orders': 3" in out
        assert "'payment_errors': 1" in out
