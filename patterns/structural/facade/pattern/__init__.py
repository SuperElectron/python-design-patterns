"""The Facade pattern, importable as library code."""

from patterns.structural.facade.pattern.checkout import (
    Notifier,
    OrderResult,
    PaymentGateway,
    Shipping,
    Warehouse,
    place_order,
)

__all__ = [
    "Notifier",
    "OrderResult",
    "PaymentGateway",
    "Shipping",
    "Warehouse",
    "place_order",
]
