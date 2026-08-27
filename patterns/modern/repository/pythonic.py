"""The repository seam: a Protocol, a fake, and domain logic that can't tell.

Tests use InMemoryInvoices; production wires something durable. The domain
function is identical either way.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Invoice:
    customer: str
    amount: int


class Invoices(Protocol):
    """The collection-like operations the domain actually needs."""

    def add(self, invoice: Invoice) -> None: ...

    def for_customer(self, customer: str) -> list[Invoice]: ...


class InMemoryInvoices:
    """The fake that makes domain tests instant."""

    def __init__(self) -> None:
        self._items: list[Invoice] = []

    def add(self, invoice: Invoice) -> None:
        self._items.append(invoice)

    def for_customer(self, customer: str) -> list[Invoice]:
        return [i for i in self._items if i.customer == customer]


def total_owed(repo: Invoices, customer: str) -> int:
    """Pure domain logic: no storage details anywhere in sight."""
    return sum(invoice.amount for invoice in repo.for_customer(customer))


def main() -> None:
    repo = InMemoryInvoices()
    repo.add(Invoice("ada", 100))
    repo.add(Invoice("ada", 50))
    repo.add(Invoice("grace", 9))
    print(f"ada owes {total_owed(repo, 'ada')}")


if __name__ == "__main__":
    main()
