"""Domain types for the order-events mini-project."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderEvent:
    """One change in an order's life, broadcast to whoever cares."""

    order_id: str
    status: str  # "placed" | "paid" | "shipped"
    total: float
