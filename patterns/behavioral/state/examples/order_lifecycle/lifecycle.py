"""The order lifecycle: one table, two guards, an audit log for free.

The whole business policy is readable in ``LIFECYCLE`` — which motions
exist — plus two guards for the rules that depend on data, not shape:
you can't pay for an empty cart, and you can't refund money never taken.
"""

from __future__ import annotations

from patterns.behavioral.state.examples.order_lifecycle.models import (
    Order,
    OrderAction,
    OrderStatus,
)
from patterns.behavioral.state.pattern import StateMachine

#: (current status, action) -> next status. Absent pairs are illegal:
#: cancelling after shipment and refunding before payment simply don't exist.
LIFECYCLE: dict[tuple[OrderStatus, OrderAction], OrderStatus] = {
    (OrderStatus.CART, OrderAction.PLACE): OrderStatus.PLACED,
    (OrderStatus.PLACED, OrderAction.PAY): OrderStatus.PAID,
    (OrderStatus.PLACED, OrderAction.CANCEL): OrderStatus.CANCELLED,
    (OrderStatus.PAID, OrderAction.SHIP): OrderStatus.SHIPPED,
    (OrderStatus.PAID, OrderAction.CANCEL): OrderStatus.CANCELLED,
    (OrderStatus.PAID, OrderAction.REFUND): OrderStatus.REFUNDED,
    (OrderStatus.SHIPPED, OrderAction.DELIVER): OrderStatus.DELIVERED,
    (OrderStatus.DELIVERED, OrderAction.REFUND): OrderStatus.REFUNDED,
}


def build_lifecycle(order: Order) -> StateMachine[OrderStatus, OrderAction]:
    """A fresh machine for one order; guards close over the order's data."""
    return StateMachine(
        initial=OrderStatus.CART,
        table=LIFECYCLE,
        guards={
            (OrderStatus.CART, OrderAction.PLACE): lambda: bool(order.items),
            (OrderStatus.PAID, OrderAction.REFUND): lambda: order.amount_paid > 0,
            (OrderStatus.DELIVERED, OrderAction.REFUND): lambda: order.amount_paid > 0,
        },
    )
