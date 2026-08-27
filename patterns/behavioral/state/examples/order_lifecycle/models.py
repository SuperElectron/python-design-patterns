"""Domain types for the order-lifecycle mini-project."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class OrderStatus(Enum):
    CART = auto()
    PLACED = auto()
    PAID = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()
    REFUNDED = auto()


class OrderAction(Enum):
    PLACE = auto()
    PAY = auto()
    SHIP = auto()
    DELIVER = auto()
    CANCEL = auto()
    REFUND = auto()


@dataclass
class Order:
    """The domain object whose behavior depends on where it is in its life."""

    order_id: str
    total: float
    amount_paid: float = 0.0
    items: list[str] = field(default_factory=list)
