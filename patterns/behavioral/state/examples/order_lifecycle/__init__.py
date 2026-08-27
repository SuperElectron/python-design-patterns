"""An order lifecycle FSM, built on the State pattern.

Run it: ``uv run python -m patterns.behavioral.state.examples.order_lifecycle``
"""

from patterns.behavioral.state.examples.order_lifecycle.lifecycle import (
    LIFECYCLE,
    build_lifecycle,
)
from patterns.behavioral.state.examples.order_lifecycle.models import (
    Order,
    OrderAction,
    OrderStatus,
)

__all__ = ["LIFECYCLE", "Order", "OrderAction", "OrderStatus", "build_lifecycle"]
