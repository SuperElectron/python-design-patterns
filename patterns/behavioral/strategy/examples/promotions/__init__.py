"""A promotions engine built on the Strategy pattern.

Run it: ``uv run python -m patterns.behavioral.strategy.examples.promotions``
"""

from patterns.behavioral.strategy.examples.promotions.models import LineItem, Order
from patterns.behavioral.strategy.examples.promotions.rules import (
    best_promo,
    due,
    promotion,
)

__all__ = ["LineItem", "Order", "best_promo", "due", "promotion"]
