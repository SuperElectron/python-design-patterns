"""Behavioral tests for the StrategyRegistry building block."""

from __future__ import annotations

import pytest

from patterns.behavioral.strategy import StrategyRegistry, UnknownStrategyError


def make_registry() -> StrategyRegistry[int, int]:
    registry: StrategyRegistry[int, int] = StrategyRegistry()

    @registry.register
    def double(n: int) -> int:
        return n * 2

    @registry.register
    def square(n: int) -> int:
        return n * n

    return registry


class TestRegistration:
    def test_registering_is_decorating_and_keeps_the_function_usable(self) -> None:
        registry: StrategyRegistry[int, int] = StrategyRegistry()

        @registry.register
        def negate(n: int) -> int:
            return -n

        assert negate(3) == -3  # the decorator hands the function back
        assert registry.names() == ["negate"]

    def test_len_and_iteration_expose_the_family(self) -> None:
        registry = make_registry()
        assert len(registry) == 2
        assert [strategy(3) for strategy in registry] == [6, 9]

    def test_duplicate_name_is_refused(self) -> None:
        registry = make_registry()
        with pytest.raises(ValueError, match="already registered"):

            @registry.register
            def double(n: int) -> int:  # same __name__ as an existing rule
                return n + n

        assert registry.get("double")(3) == 6  # the original survives

    def test_accidental_same_name_collision_from_helpers_is_caught(self) -> None:
        # Two factories both produce a function named "promo" — the classic
        # accidental collision the name-keying invites.
        registry: StrategyRegistry[int, int] = StrategyRegistry()

        def make_promo_a() -> None:
            @registry.register
            def promo(n: int) -> int:
                return n - 1

        def make_promo_b() -> None:
            @registry.register
            def promo(n: int) -> int:
                return n + 1

        make_promo_a()
        with pytest.raises(ValueError, match="'promo' already registered"):
            make_promo_b()

    def test_replace_swaps_a_strategy_intentionally(self) -> None:
        registry = make_registry()

        def double(n: int) -> int:
            return n + n + n  # deliberately different behavior

        registry.register(double, replace=True)
        assert registry.get("double")(3) == 9

    def test_unregister_unknown_name_raises(self) -> None:
        registry = make_registry()
        with pytest.raises(UnknownStrategyError, match="no strategy 'cube'"):
            registry.unregister("cube")

    def test_names_keep_registration_order(self) -> None:
        registry: StrategyRegistry[int, int] = StrategyRegistry()

        def zeta(n: int) -> int:
            return n

        def alpha(n: int) -> int:
            return n

        registry.register(zeta)
        registry.register(alpha)
        assert registry.names() == ["zeta", "alpha"]  # insertion, not sorted


class TestLookup:
    def test_get_returns_the_named_strategy(self) -> None:
        registry = make_registry()
        assert registry.get("square")(4) == 16

    def test_unknown_name_raises_with_the_known_names(self) -> None:
        registry = make_registry()
        with pytest.raises(UnknownStrategyError, match="double, square"):
            registry.get("cube")


class TestResults:
    def test_results_runs_every_strategy_keyed_by_name(self) -> None:
        registry = make_registry()
        assert registry.results(3) == {"double": 6, "square": 9}

    def test_independent_registries_do_not_share_strategies(self) -> None:
        first = make_registry()
        second: StrategyRegistry[int, int] = StrategyRegistry()
        assert len(first) == 2
        assert len(second) == 0
