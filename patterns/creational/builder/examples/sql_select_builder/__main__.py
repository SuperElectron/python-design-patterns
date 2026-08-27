"""Demo: order analytics with builder-assembled queries."""

from __future__ import annotations

from patterns.creational.builder.examples.sql_select_builder.database import seed_orders
from patterns.creational.builder.examples.sql_select_builder.reports import (
    big_orders,
    orders_in_region,
    top_orders,
)


def main() -> None:
    conn = seed_orders()
    print("top 3 orders:", top_orders(conn, 3))
    print("orders >= $900:", big_orders(conn, 900))
    print("west widgets:", orders_in_region(conn, "west", "widgets"))


if __name__ == "__main__":
    main()
