"""Behavioral tests for all three abstract-factory variants."""

from decimal import Decimal

from patterns.creational.abstract_factory import naive, pythonic, real_world


class TestNaive:
    def test_client_builds_through_the_interface(self) -> None:
        floats = naive.parse_numbers(["1.5"], naive.FloatFactory())
        exacts = naive.parse_numbers(["1.5"], naive.DecimalFactory())
        assert floats == [1.5] and isinstance(floats[0], float)
        assert exacts == [Decimal("1.5")] and isinstance(exacts[0], Decimal)


class TestPythonic:
    def test_callable_is_the_factory(self) -> None:
        assert pythonic.parse_numbers(["2.5"], Decimal) == [Decimal("2.5")]

    def test_default_factory(self) -> None:
        assert pythonic.parse_numbers(["2.5"]) == [2.5]

    def test_family_bundle_swaps_every_member(self) -> None:
        result = pythonic.parse(["1.1"], pythonic.EXACT_FAMILY)
        assert result == (Decimal("1.1"),)
        assert pythonic.parse(["1.1"]) == [1.1]


class TestRealWorld:
    def test_parse_float_hook_changes_the_family(self) -> None:
        doc = real_world.load_exact('{"x": 0.1}')
        assert isinstance(doc, dict)
        assert doc["x"] == Decimal("0.1")
        assert isinstance(doc["x"], Decimal)
