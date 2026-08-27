"""Strategies as plain functions, plus the decorator registry.

``@promotion`` appends each rule to a module-level list, so ``best_promo``
always considers every registered rule -- adding a strategy is just defining
one.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class LineItem:
    product: str
    quantity: int
    price: float

    def total(self) -> float:
        return self.quantity * self.price


@dataclass(frozen=True)
class Order:
    cart: tuple[LineItem, ...]

    def total(self) -> float:
        return sum(item.total() for item in self.cart)


PromoFunc = Callable[[Order], float]

promos: list[PromoFunc] = []


def promotion(func: PromoFunc) -> PromoFunc:
    """Register a promotion strategy by decorating it."""
    promos.append(func)
    return func


@promotion
def bulk_item(order: Order) -> float:
    """10% off each line item of 20+ units."""
    return sum(item.total() * 0.1 for item in order.cart if item.quantity >= 20)


@promotion
def large_order(order: Order) -> float:
    """7% off orders with 10+ distinct products."""
    if len({item.product for item in order.cart}) >= 10:
        return order.total() * 0.07
    return 0.0


def best_promo(order: Order) -> float:
    """Try every registered strategy; keep the best discount."""
    return max(promo(order) for promo in promos)


def due(order: Order, promo: PromoFunc | None = None) -> float:
    """A strategy is just an argument."""
    return order.total() - (promo(order) if promo else 0.0)


def main() -> None:
    order = Order((LineItem("banana", 30, 0.5), LineItem("apple", 10, 1.5)))
    print(f"bulk_item due: {due(order, bulk_item):.2f}")
    print(f"best promo:    {best_promo(order):.2f}")


if __name__ == "__main__":
    main()
