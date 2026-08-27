"""The mini-project's point, as tests: ONE contract suite, BOTH adapters.

Every test here runs against the in-memory fake and the sqlite adapter via
the parametrized fixture — the fake stays honest because the same
assertions hold production storage to the same behavior.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from datetime import date

import pytest

from patterns.modern.repository.examples.invoice_ledger import SqliteInvoices
from patterns.modern.repository.examples.invoice_ledger.__main__ import main
from patterns.modern.repository.pattern import (
    InMemoryInvoices,
    Invoice,
    Invoices,
    overdue,
    total_owed,
)

TODAY = date(2026, 8, 27)


@pytest.fixture(params=["memory", "sqlite"])
def repo(request: pytest.FixtureRequest) -> Iterator[Invoices]:
    if request.param == "memory":
        yield InMemoryInvoices()
    else:
        conn = sqlite3.connect(":memory:")
        yield SqliteInvoices(conn)
        conn.close()


class TestRepositoryContract:
    """The port's behavior, pinned identically for fake and real adapter."""

    def test_added_invoices_come_back_whole(self, repo: Invoices) -> None:
        inv = Invoice("INV-1", "ada", 120_00, date(2026, 8, 1))
        repo.add(inv)
        assert repo.for_customer("ada") == [inv]  # round-trip preserves types

    def test_for_customer_filters(self, repo: Invoices) -> None:
        repo.add(Invoice("INV-1", "ada", 100, TODAY))
        repo.add(Invoice("INV-2", "grace", 200, TODAY))
        assert [i.number for i in repo.for_customer("grace")] == ["INV-2"]

    def test_list_all_returns_everything(self, repo: Invoices) -> None:
        repo.add(Invoice("INV-1", "ada", 100, TODAY))
        repo.add(Invoice("INV-2", "grace", 200, TODAY))
        assert {i.number for i in repo.list_all()} == {"INV-1", "INV-2"}

    def test_domain_logic_cannot_tell_the_adapters_apart(self, repo: Invoices) -> None:
        repo.add(Invoice("INV-1", "ada", 120_00, date(2026, 8, 1)))
        repo.add(Invoice("INV-2", "ada", 80_00, date(2026, 9, 15)))
        assert total_owed(repo, "ada") == 200_00
        assert [i.number for i in overdue(repo, TODAY)] == ["INV-1"]


class TestDemo:
    def test_main_reports_identical_answers_from_both_backends(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        main()
        lines = capsys.readouterr().out.strip().splitlines()
        assert lines[0].replace("[memory]", "") == lines[1].replace("[sqlite]", "")
        assert "ada owes 200.00" in lines[0]
        assert "overdue: INV-3, INV-1" in lines[0]
