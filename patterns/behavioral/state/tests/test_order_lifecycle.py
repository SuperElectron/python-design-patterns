"""Behavioral tests for the order-lifecycle mini-project."""

from __future__ import annotations

import pytest

from patterns.behavioral.state import IllegalTransitionError
from patterns.behavioral.state.examples.order_lifecycle import (
    Order,
    OrderAction,
    OrderStatus,
    build_lifecycle,
)
from patterns.behavioral.state.examples.order_lifecycle.__main__ import main


def order_with_items() -> Order:
    return Order("O-1", total=100.0, items=["book"])


class TestHappyPath:
    def test_place_pay_ship_deliver(self) -> None:
        order = order_with_items()
        lifecycle = build_lifecycle(order)
        lifecycle.trigger(OrderAction.PLACE)
        lifecycle.trigger(OrderAction.PAY)
        order.amount_paid = order.total
        lifecycle.trigger(OrderAction.SHIP)
        assert lifecycle.trigger(OrderAction.DELIVER) is OrderStatus.DELIVERED

    def test_the_audit_log_tells_the_whole_story(self) -> None:
        order = order_with_items()
        lifecycle = build_lifecycle(order)
        lifecycle.trigger(OrderAction.PLACE)
        lifecycle.trigger(OrderAction.CANCEL)
        assert [(s.source, s.event, s.target) for s in lifecycle.log] == [
            (OrderStatus.CART, OrderAction.PLACE, OrderStatus.PLACED),
            (OrderStatus.PLACED, OrderAction.CANCEL, OrderStatus.CANCELLED),
        ]


class TestShapeRules:
    def test_cancel_after_shipment_is_not_a_thing(self) -> None:
        order = order_with_items()
        lifecycle = build_lifecycle(order)
        lifecycle.trigger(OrderAction.PLACE)
        lifecycle.trigger(OrderAction.PAY)
        order.amount_paid = order.total
        lifecycle.trigger(OrderAction.SHIP)
        with pytest.raises(IllegalTransitionError):
            lifecycle.trigger(OrderAction.CANCEL)
        assert lifecycle.state is OrderStatus.SHIPPED

    def test_shipping_an_unpaid_order_is_not_a_thing(self) -> None:
        lifecycle = build_lifecycle(order_with_items())
        lifecycle.trigger(OrderAction.PLACE)
        with pytest.raises(IllegalTransitionError):
            lifecycle.trigger(OrderAction.SHIP)


class TestDataGuards:
    def test_an_empty_cart_cannot_be_placed(self) -> None:
        empty = Order("O-2", total=0.0)
        lifecycle = build_lifecycle(empty)
        with pytest.raises(IllegalTransitionError, match="guard"):
            lifecycle.trigger(OrderAction.PLACE)

    def test_refund_requires_money_actually_taken(self) -> None:
        order = order_with_items()
        lifecycle = build_lifecycle(order)
        lifecycle.trigger(OrderAction.PLACE)
        lifecycle.trigger(OrderAction.PAY)  # status moves, but no money landed
        assert not lifecycle.can(OrderAction.REFUND)
        order.amount_paid = order.total
        assert lifecycle.can(OrderAction.REFUND)
        assert lifecycle.trigger(OrderAction.REFUND) is OrderStatus.REFUNDED


class TestDemo:
    def test_main_shows_refusal_delivery_and_audit(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        main()
        out = capsys.readouterr().out
        assert "refused:" in out
        assert "final status: DELIVERED" in out
        assert "CART --PLACE--> PLACED" in out
