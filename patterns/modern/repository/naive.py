"""Persistence soaked into domain logic: SQL inline, everywhere."""

from __future__ import annotations

import sqlite3


def total_owed(conn: sqlite3.Connection, customer: str) -> int:
    """Domain question, welded to storage details."""
    conn.execute("CREATE TABLE IF NOT EXISTS invoices (customer TEXT, amount INT)")
    rows = conn.execute("SELECT amount FROM invoices WHERE customer = ?", (customer,)).fetchall()
    return sum(amount for (amount,) in rows)


def main() -> None:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE invoices (customer TEXT, amount INT)")
    conn.executemany("INSERT INTO invoices VALUES (?, ?)", [("ada", 100), ("ada", 50)])
    print(f"ada owes {total_owed(conn, 'ada')}")


if __name__ == "__main__":
    main()
