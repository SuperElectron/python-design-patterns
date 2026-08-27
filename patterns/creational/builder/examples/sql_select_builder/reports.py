"""Analytics queries, each staged through the builder and run for real.

The builder assembles a frozen ``Query``; sqlite executes it with the
parameters kept separate from the SQL text — the same discipline as any
production database layer.
"""

from __future__ import annotations

import sqlite3

from patterns.creational.builder.pattern import SelectBuilder


def _run(conn: sqlite3.Connection, builder: SelectBuilder) -> list[tuple[object, ...]]:
    query = builder.build()
    return [tuple(row) for row in conn.execute(query.sql(), query.params)]


def top_orders(conn: sqlite3.Connection, count: int) -> list[tuple[object, ...]]:
    """The biggest orders, largest first."""
    builder = SelectBuilder("orders").columns("id", "amount").order_by("amount DESC").limit(count)
    return _run(conn, builder)


def big_orders(conn: sqlite3.Connection, minimum: int) -> list[tuple[object, ...]]:
    """Orders at or above a spend threshold."""
    builder = (
        SelectBuilder("orders")
        .columns("id", "region", "amount")
        .where("amount >= ?", minimum)
        .order_by("id")
    )
    return _run(conn, builder)


def orders_in_region(
    conn: sqlite3.Connection, region: str, product: str | None = None
) -> list[tuple[object, ...]]:
    """Orders for a region — optionally narrowed to one product.

    The builder's win over a one-shot call: the second condition is added
    only when the caller asked for it.
    """
    builder = SelectBuilder("orders").columns("id", "product", "amount")
    builder.where("region = ?", region)
    if product is not None:
        builder.where("product = ?", product)
    return _run(conn, builder.order_by("id"))
