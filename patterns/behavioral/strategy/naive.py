"""The Gang of Four Strategy: one class per algorithm, a context that holds one.

An order applies whichever promotion strategy it was configured with.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class LineItem:
    product: str
    quantity: int
    price: float

    def total(self) -> float:
        return self.quantity * self.price


class Promotion(ABC):
    """The strategy interface."""

    @abstractmethod
    def discount(self, order: Order) -> float: ...


class Order:
    """The context: holds cart plus one interchangeable strategy."""

    def __init__(self, cart: list[LineItem], promotion: Promotion | None = None) -> None:
        self.cart = cart
        self.promotion = promotion

    def total(self) -> float:
        return sum(item.total() for item in self.cart)

    def due(self) -> float:
        discount = self.promotion.discount(self) if self.promotion else 0.0
        return self.total() - discount


class BulkItemPromo(Promotion):
    """10% off each line item of 20+ units."""

    def discount(self, order: Order) -> float:
        return sum(item.total() * 0.1 for item in order.cart if item.quantity >= 20)


class LargeOrderPromo(Promotion):
    """7% off orders with 10+ distinct products."""

    def discount(self, order: Order) -> float:
        if len({item.product for item in order.cart}) >= 10:
            return order.total() * 0.07
        return 0.0


def main() -> None:
    cart = [LineItem("banana", 30, 0.5), LineItem("apple", 10, 1.5)]
    print(f"bulk promo due:  {Order(cart, BulkItemPromo()).due():.2f}")
    print(f"no promo due:    {Order(cart).due():.2f}")


if __name__ == "__main__":
    main()
