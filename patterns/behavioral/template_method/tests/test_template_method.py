"""Behavioral tests for all three template-method variants."""

import json
from datetime import date

import pytest

from patterns.behavioral.template_method import naive, pythonic, real_world


class TestNaive:
    def test_subclasses_vary_steps_not_skeleton(self) -> None:
        data = {"apples": 3}
        assert naive.TextReport().render(data) == "REPORT\napples: 3"
        assert naive.CsvReport().render(data) == "key,value\napples,3"


class TestPythonic:
    def test_default_steps(self) -> None:
        assert pythonic.render({"apples": 3}) == "REPORT\napples: 3"

    def test_injected_steps(self) -> None:
        out = pythonic.render({"apples": 3}, header="key,value", format_rows=pythonic.csv_rows)
        assert out == "key,value\napples,3"

    def test_steps_compose_at_call_time(self) -> None:
        loud = pythonic.render({"a": 1}, format_rows=lambda d: pythonic.plain_rows(d).upper())
        assert loud == "REPORT\nA: 1"


class TestRealWorld:
    def test_hook_handles_dates_inside_the_inherited_skeleton(self) -> None:
        out = real_world.dump_event({"name": "launch", "when": date(2026, 8, 26)})
        assert json.loads(out) == {"name": "launch", "when": "2026-08-26"}

    def test_unknown_types_still_raise_via_super(self) -> None:
        with pytest.raises(TypeError):
            real_world.dump_event({"bad": object()})
