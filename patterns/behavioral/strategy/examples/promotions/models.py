"""Domain types for the promotions mini-project."""

from __future__ import annotations

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
    """A cart at checkout; loyalty points may unlock extra promotions."""

    cart: tuple[LineItem, ...]
    loyalty_points: int = 0

    def total(self) -> float:
        return sum(item.total() for item in self.cart)
