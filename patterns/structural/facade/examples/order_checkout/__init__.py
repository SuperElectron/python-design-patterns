"""A storefront processing a day's orders through the checkout facade.

Run it: ``uv run python -m patterns.structural.facade.examples.order_checkout``
"""

from patterns.structural.facade.examples.order_checkout.store import (
    Order,
    Store,
)

__all__ = ["Order", "Store"]
