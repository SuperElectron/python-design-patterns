"""Behavioral tests for the checkout facade."""

from __future__ import annotations

import pytest

from patterns.structural.facade.pattern import (
    Notifier,
    PaymentGateway,
    Shipping,
    Warehouse,
    place_order,
)


def build_subsystem(
    stock: int = 10, declined: set[str] | None = None
) -> tuple[Warehouse, PaymentGateway, Shipping, Notifier]:
    return (
        Warehouse(stock={"mug": stock}),
        PaymentGateway(declined_cards=declined or set()),
        Shipping(),
        Notifier(),
    )


def test_happy_path_runs_the_whole_dance_in_order() -> None:
    warehouse, gateway, shipping, notifier = build_subsystem()
    result = place_order(
        warehouse,
        gateway,
        shipping,
        notifier,
        sku="mug",
        quantity=2,
        price_cents=1200,
        card="4242",
        address="12 Grace Ave",
    )
    assert warehouse.stock["mug"] == 8
    assert gateway.charges == [("4242", 2400)]
    assert result.shipping_label in shipping.labels
    assert notifier.sent and result.transaction_id in notifier.sent[0]


def test_declined_payment_rolls_back_the_reservation() -> None:
    warehouse, gateway, shipping, notifier = build_subsystem(declined={"4000"})
    with pytest.raises(PermissionError):
        place_order(
            warehouse,
            gateway,
            shipping,
            notifier,
            sku="mug",
            quantity=3,
            price_cents=1000,
            card="4000",
            address="9 Hopper St",
        )
    assert warehouse.stock["mug"] == 10  # released, not leaked
    assert shipping.labels == []
    assert notifier.sent == []


def test_gateway_blowup_also_releases_the_reservation() -> None:
    # Rollback must cover ANY charge failure, not just the declined path.
    class ExplodingGateway(PaymentGateway):
        def charge(self, card: str, amount_cents: int) -> str:
            raise ConnectionError("gateway unreachable")

    warehouse, _, shipping, notifier = build_subsystem()
    with pytest.raises(ConnectionError):
        place_order(
            warehouse,
            ExplodingGateway(),
            shipping,
            notifier,
            sku="mug",
            quantity=3,
            price_cents=1000,
            card="4242",
            address="9 Hopper St",
        )
    assert warehouse.stock["mug"] == 10  # released, not leaked
    assert shipping.labels == []


def test_insufficient_stock_stops_before_any_charge() -> None:
    warehouse, gateway, shipping, notifier = build_subsystem(stock=1)
    with pytest.raises(LookupError):
        place_order(
            warehouse,
            gateway,
            shipping,
            notifier,
            sku="mug",
            quantity=5,
            price_cents=1000,
            card="4242",
            address="3 Lovelace Rd",
        )
    assert gateway.charges == []


def test_subsystem_stays_usable_without_the_facade() -> None:
    warehouse, gateway, _, _ = build_subsystem()
    warehouse.reserve("mug", 1)  # full-controls path: no facade required
    assert gateway.charge("4242", 100) == "txn-1"
    assert warehouse.stock["mug"] == 9
