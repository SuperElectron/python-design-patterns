"""Pricing rules as registered strategies, and the engine that compares them.

Each rule is a plain function ``(Order) -> float`` (the discount it grants).
Adding a rule is defining one — ``best_promo`` and the comparison report
pick it up with no other edit.
"""

from __future__ import annotations

from patterns.behavioral.strategy.examples.promotions.models import Order
from patterns.behavioral.strategy.pattern import StrategyRegistry

promotion: StrategyRegistry[Order, float] = StrategyRegistry()


@promotion.register
def bulk_item(order: Order) -> float:
    """10% off each line item of 20+ units."""
    return sum(item.total() * 0.1 for item in order.cart if item.quantity >= 20)


@promotion.register
def large_order(order: Order) -> float:
    """7% off orders with 10+ distinct products."""
    if len({item.product for item in order.cart}) >= 10:
        return order.total() * 0.07
    return 0.0


@promotion.register
def loyalty(order: Order) -> float:
    """5% off for customers holding 1000+ loyalty points."""
    if order.loyalty_points >= 1000:
        return order.total() * 0.05
    return 0.0


def best_promo(
    order: Order, rules: StrategyRegistry[Order, float] | None = None
) -> tuple[str, float]:
    """Compare every registered rule; return the winner's name and discount.

    Ties go to the earliest-registered rule — ``max`` keeps the first of
    equals, and the registry iterates in registration order.
    """
    results = (rules if rules is not None else promotion).results(order)
    name = max(results, key=lambda n: results[n])
    return name, results[name]


def due(order: Order, rules: StrategyRegistry[Order, float] | None = None) -> float:
    """What the customer pays after the best promotion."""
    _, discount = best_promo(order, rules)
    return order.total() - discount
