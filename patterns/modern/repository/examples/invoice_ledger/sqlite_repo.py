"""The real adapter: the same three methods over durable storage.

The domain functions cannot tell this from ``InMemoryInvoices`` — the shared
contract tests in ``tests/test_invoice_ledger.py`` hold both to it.
"""

from __future__ import annotations

import sqlite3
from datetime import date

from patterns.modern.repository.pattern import Invoice


class SqliteInvoices:
    """An ``Invoices`` adapter over sqlite3 (stdlib, durable when given a path).

    This demo commits per write so the durability claim is true of the code;
    production designs often lift commit into a unit-of-work seam instead
    (see the pitfalls in ``docs/implementation.md``).
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS invoices"
            " (number TEXT PRIMARY KEY, customer TEXT, amount_cents INT, due TEXT)"
        )
        self._conn.commit()

    def add(self, invoice: Invoice) -> None:
        try:
            self._conn.execute(
                "INSERT INTO invoices VALUES (?, ?, ?, ?)",
                (invoice.number, invoice.customer, invoice.amount_cents, invoice.due.isoformat()),
            )
        except sqlite3.IntegrityError:
            raise ValueError(f"invoice {invoice.number!r} already exists") from None
        self._conn.commit()

    def for_customer(self, customer: str) -> list[Invoice]:
        rows = self._conn.execute(
            "SELECT number, customer, amount_cents, due FROM invoices WHERE customer = ?",
            (customer,),
        ).fetchall()
        return [self._to_invoice(row) for row in rows]

    def list_all(self) -> list[Invoice]:
        rows = self._conn.execute(
            "SELECT number, customer, amount_cents, due FROM invoices"
        ).fetchall()
        return [self._to_invoice(row) for row in rows]

    @staticmethod
    def _to_invoice(row: tuple[str, str, int, str]) -> Invoice:
        number, customer, amount_cents, due = row
        return Invoice(number, customer, amount_cents, date.fromisoformat(due))
