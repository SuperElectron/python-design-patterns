"""The mini-project: a storefront whose only checkout path is the facade.

Every order goes through ``place_order`` -- no call site re-implements the
reserve/charge/ship/notify dance, so the payment-declined rollback exists in
exactly one place. Callers needing the full controls still reach the
subsystem directly (see ``Store.restock``, which talks to the warehouse).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from patterns.structural.facade.pattern import (
    Notifier,
    OrderResult,
    PaymentGateway,
    Shipping,
    Warehouse,
    place_order,
)


@dataclass(frozen=True)
class Order:
    sku: str
    quantity: int
    price_cents: int
    card: str
    address: str


@dataclass
class Store:
    """Owns the subsystem; exposes one door for the common case."""

    warehouse: Warehouse = field(default_factory=Warehouse)
    gateway: PaymentGateway = field(default_factory=PaymentGateway)
    shipping: Shipping = field(default_factory=Shipping)
    notifier: Notifier = field(default_factory=Notifier)

    def restock(self, sku: str, quantity: int) -> None:
        # Full-controls path: the subsystem is public, not imprisoned.
        self.warehouse.release(sku, quantity)

    def checkout(self, order: Order) -> OrderResult:
        return place_order(
            self.warehouse,
            self.gateway,
            self.shipping,
            self.notifier,
            sku=order.sku,
            quantity=order.quantity,
            price_cents=order.price_cents,
            card=order.card,
            address=order.address,
        )

    def process(self, orders: list[Order]) -> tuple[list[OrderResult], list[tuple[Order, str]]]:
        """A day's batch: fulfilled results plus (order, reason) failures."""
        fulfilled: list[OrderResult] = []
        failed: list[tuple[Order, str]] = []
        for order in orders:
            try:
                fulfilled.append(self.checkout(order))
            except (LookupError, PermissionError) as exc:
                failed.append((order, str(exc)))
        return fulfilled, failed
