"""Behavioral tests for the pattern's domain logic, run against the fake."""

from __future__ import annotations

from datetime import date

from patterns.modern.repository import InMemoryInvoices, Invoice, overdue, total_owed

TODAY = date(2026, 8, 27)


def invoice(number: str, customer: str = "ada", cents: int = 100_00, due: date = TODAY) -> Invoice:
    return Invoice(number, customer, cents, due)


class TestDomainLogic:
    def test_total_owed_sums_one_customer_only(self) -> None:
        repo = InMemoryInvoices()
        repo.add(invoice("INV-1", "ada", 100_00))
        repo.add(invoice("INV-2", "ada", 50_00))
        repo.add(invoice("INV-3", "grace", 9_00))
        assert total_owed(repo, "ada") == 150_00

    def test_total_owed_for_an_unknown_customer_is_zero(self) -> None:
        assert total_owed(InMemoryInvoices(), "nobody") == 0

    def test_overdue_respects_grace_and_sorts_oldest_first(self) -> None:
        repo = InMemoryInvoices()
        repo.add(invoice("INV-1", due=date(2026, 8, 1)))
        repo.add(invoice("INV-2", due=date(2026, 7, 1)))
        repo.add(invoice("INV-3", due=date(2026, 8, 26)))  # 1 day late
        late = overdue(repo, TODAY, grace_days=5)
        assert [i.number for i in late] == ["INV-2", "INV-1"]

    def test_due_today_is_not_overdue(self) -> None:
        repo = InMemoryInvoices()
        repo.add(invoice("INV-1", due=TODAY))
        assert overdue(repo, TODAY) == []
