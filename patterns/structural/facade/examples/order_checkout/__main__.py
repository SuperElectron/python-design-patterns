"""Demo: a morning's orders, one declined card among them."""

from __future__ import annotations

from patterns.structural.facade.examples.order_checkout.store import Order, Store
from patterns.structural.facade.pattern import PaymentGateway, Warehouse


def main() -> None:
    store = Store(
        warehouse=Warehouse(stock={"mug": 10, "tee": 3}),
        gateway=PaymentGateway(declined_cards={"4000-declined"}),
    )
    orders = [
        Order("mug", 2, 1200, "4242", "12 Grace Ave"),
        Order("tee", 1, 2500, "4000-declined", "9 Hopper St"),
        Order("mug", 1, 1200, "4111", "3 Lovelace Rd"),
    ]
    fulfilled, failed = store.process(orders)
    for result in fulfilled:
        print(f"fulfilled: {result.transaction_id} -> {result.shipping_label}")
    for order, reason in failed:
        print(f"failed:    {order.sku} x{order.quantity} ({reason})")
    print(f"stock after (tee restored by rollback): {store.warehouse.stock}")


if __name__ == "__main__":
    main()
