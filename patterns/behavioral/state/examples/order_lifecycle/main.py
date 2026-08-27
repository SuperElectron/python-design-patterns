"""Demo: one order's happy path, with the machine refusing the wrong turns."""

from __future__ import annotations

from patterns.behavioral.state.examples.order_lifecycle.lifecycle import build_lifecycle
from patterns.behavioral.state.examples.order_lifecycle.models import Order, OrderAction
from patterns.behavioral.state.pattern import IllegalTransitionError


def main() -> None:
    order = Order("O-1", total=59.0, items=["keyboard"])
    lifecycle = build_lifecycle(order)

    lifecycle.trigger(OrderAction.PLACE)
    lifecycle.trigger(OrderAction.PAY)
    order.amount_paid = order.total
    lifecycle.trigger(OrderAction.SHIP)

    try:
        lifecycle.trigger(OrderAction.CANCEL)  # too late: it's on the truck
    except IllegalTransitionError as err:
        print(f"refused: {err}")

    lifecycle.trigger(OrderAction.DELIVER)
    print(f"final status: {lifecycle.state.name}")
    print("audit log:")
    for step in lifecycle.log:
        print(f"  {step.source.name} --{step.event.name}--> {step.target.name}")


if __name__ == "__main__":
    main()
