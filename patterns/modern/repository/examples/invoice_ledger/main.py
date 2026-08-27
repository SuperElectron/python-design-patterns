"""Demo: identical domain answers from the fake and the sqlite adapter."""

from __future__ import annotations

import sqlite3
from datetime import date

from patterns.modern.repository.examples.invoice_ledger.sqlite_repo import SqliteInvoices
from patterns.modern.repository.pattern import (
    InMemoryInvoices,
    Invoice,
    Invoices,
    overdue,
    total_owed,
)

LEDGER = [
    Invoice("INV-1", "ada", 120_00, date(2026, 8, 1)),
    Invoice("INV-2", "ada", 80_00, date(2026, 9, 15)),
    Invoice("INV-3", "grace", 45_50, date(2026, 7, 15)),
]
TODAY = date(2026, 8, 27)


def report(label: str, repo: Invoices) -> None:
    for invoice in LEDGER:
        repo.add(invoice)
    late = ", ".join(i.number for i in overdue(repo, TODAY)) or "none"
    print(f"[{label}] ada owes {total_owed(repo, 'ada') / 100:.2f}; overdue: {late}")


def main() -> None:
    report("memory", InMemoryInvoices())
    report("sqlite", SqliteInvoices(sqlite3.connect(":memory:")))


if __name__ == "__main__":
    main()
