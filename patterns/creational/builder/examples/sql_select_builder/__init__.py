"""Order analytics over sqlite, with every query built through SelectBuilder.

Run it: ``uv run python -m patterns.creational.builder.examples.sql_select_builder``
"""

from patterns.creational.builder.examples.sql_select_builder.database import seed_orders
from patterns.creational.builder.examples.sql_select_builder.reports import (
    big_orders,
    orders_in_region,
    top_orders,
)

__all__ = ["big_orders", "orders_in_region", "seed_orders", "top_orders"]
