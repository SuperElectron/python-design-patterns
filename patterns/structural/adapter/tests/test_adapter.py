"""Behavioral tests for the DelegatingAdapter building block."""

from __future__ import annotations

import pytest

from patterns.structural.adapter import DelegatingAdapter


class Legacy:
    def speed_mph(self) -> float:
        return 62.0

    def vendor_id(self) -> str:
        return "acme-42"


class MetricAdapter(DelegatingAdapter[Legacy]):
    def speed_kmh(self) -> float:
        return self.adaptee.speed_mph() * 1.609344

    def vendor_id(self) -> str:  # deliberately shadows the adaptee's method
        return "translated"


class TestDelegatingAdapter:
    def test_translated_method_converts(self) -> None:
        assert MetricAdapter(Legacy()).speed_kmh() == pytest.approx(99.78, abs=0.01)

    def test_untranslated_methods_forward_to_the_adaptee(self) -> None:
        adapter = MetricAdapter(Legacy())
        assert adapter.speed_mph() == 62.0

    def test_a_defined_method_always_beats_forwarding(self) -> None:
        assert MetricAdapter(Legacy()).vendor_id() == "translated"

    def test_missing_names_raise_attribute_error_not_silence(self) -> None:
        with pytest.raises(AttributeError):
            MetricAdapter(Legacy()).warp_drive()

    def test_the_adaptee_stays_reachable(self) -> None:
        legacy = Legacy()
        assert MetricAdapter(legacy).adaptee is legacy
