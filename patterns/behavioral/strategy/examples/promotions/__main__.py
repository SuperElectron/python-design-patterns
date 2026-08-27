"""Demo: three carts compared under every registered pricing rule."""

from __future__ import annotations

from patterns.behavioral.strategy.examples.promotions.models import LineItem, Order
from patterns.behavioral.strategy.examples.promotions.rules import best_promo, due, promotion


def main() -> None:
    carts = {
        "bulk banana buyer": Order((LineItem("banana", 30, 0.5), LineItem("apple", 10, 1.5))),
        "variety shopper": Order(tuple(LineItem(f"item-{n}", 1, 1.0) for n in range(10))),
        "loyal regular": Order((LineItem("coffee", 2, 9.0),), loyalty_points=1500),
    }
    for label, order in carts.items():
        results = promotion.results(order)
        winner, _ = best_promo(order)
        columns = "  ".join(f"{name}: {value:5.2f}" for name, value in results.items())
        print(
            f"{label:18} total {order.total():6.2f}  {columns}  -> {winner}, pay {due(order):.2f}"
        )


if __name__ == "__main__":
    main()
