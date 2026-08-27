"""Facade — public API.

>>> from patterns.structural.facade import place_order
"""

from patterns.structural.facade.pattern import (
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
