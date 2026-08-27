"""A sqlite3-backed repository satisfying the same protocol.

Same domain function, durable storage -- the swap the pattern promises.
"""

from __future__ import annotations

import sqlite3

from patterns.modern.repository.pythonic import Invoice, total_owed


class SqliteInvoices:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._conn.execute("CREATE TABLE IF NOT EXISTS invoices (customer TEXT, amount INT)")

    def add(self, invoice: Invoice) -> None:
        self._conn.execute("INSERT INTO invoices VALUES (?, ?)", (invoice.customer, invoice.amount))

    def for_customer(self, customer: str) -> list[Invoice]:
        rows = self._conn.execute(
            "SELECT customer, amount FROM invoices WHERE customer = ?", (customer,)
        ).fetchall()
        return [Invoice(c, a) for c, a in rows]


def main() -> None:
    repo = SqliteInvoices(sqlite3.connect(":memory:"))
    repo.add(Invoice("ada", 100))
    repo.add(Invoice("ada", 50))
    print(f"ada owes {total_owed(repo, 'ada')} (from sqlite)")


if __name__ == "__main__":
    main()
