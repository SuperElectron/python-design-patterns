"""Behavioral tests for the promotions mini-project."""

from __future__ import annotations

import pytest

from patterns.behavioral.strategy.examples.promotions import (
    LineItem,
    Order,
    best_promo,
    due,
    promotion,
)
from patterns.behavioral.strategy.examples.promotions.__main__ import main
from patterns.behavioral.strategy.pattern import StrategyRegistry


def bulk_cart() -> Order:
    return Order((LineItem("banana", 30, 0.5), LineItem("apple", 10, 1.5)))


class TestIndividualRules:
    def test_bulk_item_discounts_only_the_bulky_lines(self) -> None:
        order = bulk_cart()  # 30 bananas qualify (15.00), 10 apples do not
        assert promotion.get("bulk_item")(order) == 1.5

    def test_large_order_needs_ten_distinct_products(self) -> None:
        nine = Order(tuple(LineItem(f"p{n}", 1, 1.0) for n in range(9)))
        ten = Order(tuple(LineItem(f"p{n}", 1, 1.0) for n in range(10)))
        assert promotion.get("large_order")(nine) == 0.0
        assert promotion.get("large_order")(ten) == pytest.approx(0.7)

    def test_loyalty_needs_a_thousand_points(self) -> None:
        casual = Order((LineItem("coffee", 2, 9.0),), loyalty_points=999)
        regular = Order((LineItem("coffee", 2, 9.0),), loyalty_points=1000)
        assert promotion.get("loyalty")(casual) == 0.0
        assert promotion.get("loyalty")(regular) == 0.9


class TestSelectionPolicy:
    def test_best_promo_names_the_winning_rule(self) -> None:
        name, discount = best_promo(bulk_cart())
        assert name == "bulk_item"
        assert discount == 1.5

    def test_due_charges_total_minus_best_discount(self) -> None:
        order = bulk_cart()  # total 30.00, best discount 1.50
        assert due(order) == 28.5

    def test_a_rule_added_at_runtime_joins_the_comparison(self) -> None:
        # A local registry: the module-global one stays untouched by tests.
        local: StrategyRegistry[Order, float] = StrategyRegistry()
        for rule in promotion:
            local.register(rule)

        @local.register
        def everything_free(order: Order) -> float:
            return order.total()

        name, _ = best_promo(bulk_cart(), local)
        assert name == "everything_free"
        assert "everything_free" not in promotion.names()

    def test_ties_go_to_the_earliest_registered_rule(self) -> None:
        local: StrategyRegistry[Order, float] = StrategyRegistry()

        def first(order: Order) -> float:
            return 1.0

        def second(order: Order) -> float:
            return 1.0

        local.register(first)
        local.register(second)
        name, discount = best_promo(bulk_cart(), local)
        assert (name, discount) == ("first", 1.0)


class TestDemo:
    def test_demo_reports_every_cart_with_its_winner(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        main()
        out = capsys.readouterr().out
        assert "bulk banana buyer" in out
        assert "-> bulk_item" in out
        assert "-> large_order" in out
        assert "-> loyalty" in out
