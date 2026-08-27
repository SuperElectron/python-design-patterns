"""The repository seam: a domain type, a ``Protocol`` port, and the fake.

``Invoices`` names the collection-like operations the domain needs — three
methods, no more. ``InMemoryInvoices`` lives here rather than in a test
helper because the fake *is* the pattern's payoff: domain tests run against
it instantly, and any real adapter (see the mini-project's sqlite one) must
behave identically or the shared contract tests say so.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol


@dataclass(frozen=True)
class Invoice:
    """One invoice, as the domain sees it — no storage details."""

    number: str
    customer: str
    amount_cents: int
    due: date


class Invoices(Protocol):
    """The port: what the domain may ask of invoice storage.

    Contract (held by the shared tests): ``add`` refuses a duplicate invoice
    number with ``ValueError``; ``list_all`` returns insertion order.
    """

    def add(self, invoice: Invoice) -> None: ...

    def for_customer(self, customer: str) -> list[Invoice]: ...

    def list_all(self) -> list[Invoice]: ...


class InMemoryInvoices:
    """The fake that makes domain tests instant."""

    def __init__(self) -> None:
        self._items: list[Invoice] = []

    def add(self, invoice: Invoice) -> None:
        if any(existing.number == invoice.number for existing in self._items):
            raise ValueError(f"invoice {invoice.number!r} already exists")
        self._items.append(invoice)

    def for_customer(self, customer: str) -> list[Invoice]:
        return [i for i in self._items if i.customer == customer]

    def list_all(self) -> list[Invoice]:
        return list(self._items)


def total_owed(repo: Invoices, customer: str) -> int:
    """Pure domain logic: no storage details anywhere in sight."""
    return sum(invoice.amount_cents for invoice in repo.for_customer(customer))


def overdue(repo: Invoices, today: date, grace_days: int = 0) -> list[Invoice]:
    """Every invoice more than ``grace_days`` past due, oldest first."""
    late = [i for i in repo.list_all() if (today - i.due).days > grace_days]
    return sorted(late, key=lambda i: i.due)
