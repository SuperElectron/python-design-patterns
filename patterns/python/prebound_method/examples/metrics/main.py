"""Demo: modules that never met, reporting into one hidden collector."""

from __future__ import annotations

from patterns.python.prebound_method.examples.metrics import api
from patterns.python.prebound_method.pattern import shares_instance


def take_order(order_id: str) -> None:
    api.increment("orders")
    api.timing("checkout_ms", 12.5 if order_id.endswith("2") else 8.0)


def failed_payment() -> None:
    api.increment("payment_errors")


def main() -> None:
    api.reset()
    for order_id in ("o-1", "o-2", "o-3"):
        take_order(order_id)
    failed_payment()
    print(f"one hidden instance: {shares_instance(api.increment, api.timing, api.snapshot)}")
    print(f"snapshot: {api.snapshot()}")


if __name__ == "__main__":
    main()
