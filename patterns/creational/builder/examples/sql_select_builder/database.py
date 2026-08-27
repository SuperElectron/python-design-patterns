"""An in-memory orders table for the mini-project to query."""

from __future__ import annotations

import sqlite3

ORDERS = [
    ("A-1", "west", "widgets", 1200),
    ("A-2", "east", "gears", 450),
    ("A-3", "west", "widgets", 80),
    ("A-4", "north", "sprockets", 3100),
    ("A-5", "east", "widgets", 950),
]


def seed_orders() -> sqlite3.Connection:
    """A fresh in-memory database with the sample orders."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE orders (id TEXT, region TEXT, product TEXT, amount INTEGER)")
    conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", ORDERS)
    return conn
