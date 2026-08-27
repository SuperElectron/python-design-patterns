"""Behavioral tests for the order_checkout mini-project."""

from __future__ import annotations

from patterns.structural.facade.examples.order_checkout import Order, Store
from patterns.structural.facade.pattern import PaymentGateway, Warehouse


def build_store() -> Store:
    return Store(
        warehouse=Warehouse(stock={"mug": 10, "tee": 3}),
        gateway=PaymentGateway(declined_cards={"4000-declined"}),
    )


def test_batch_separates_fulfilled_from_failed() -> None:
    store = build_store()
    fulfilled, failed = store.process(
        [
            Order("mug", 2, 1200, "4242", "12 Grace Ave"),
            Order("tee", 1, 2500, "4000-declined", "9 Hopper St"),
            Order("mug", 1, 1200, "4111", "3 Lovelace Rd"),
        ]
    )
    assert [r.transaction_id for r in fulfilled] == ["txn-1", "txn-2"]
    assert [(o.sku, "declined" in reason) for o, reason in failed] == [("tee", True)]


def test_declined_order_leaves_stock_untouched_for_the_rest_of_the_batch() -> None:
    store = build_store()
    store.process(
        [
            Order("tee", 2, 2500, "4000-declined", "9 Hopper St"),
            Order("tee", 3, 2500, "4242", "12 Grace Ave"),
        ]
    )
    # The rollback restored the 2 tees, so the order for all 3 could succeed.
    assert store.warehouse.stock["tee"] == 0
    assert len(store.gateway.charges) == 1


def test_full_controls_path_bypasses_the_facade() -> None:
    store = build_store()
    store.restock("mug", 5)
    assert store.warehouse.stock["mug"] == 15
