"""Behavioral tests for all three repository variants."""

import sqlite3

from patterns.modern.repository import naive, pythonic, real_world
from patterns.modern.repository.pythonic import Invoice


class TestNaive:
    def test_inline_sql_works_but_needs_a_database(self) -> None:
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE invoices (customer TEXT, amount INT)")
        conn.executemany("INSERT INTO invoices VALUES (?, ?)", [("ada", 100), ("ada", 50)])
        assert naive.total_owed(conn, "ada") == 150


class TestPythonic:
    def test_domain_logic_runs_on_the_fake(self) -> None:
        repo = pythonic.InMemoryInvoices()
        repo.add(Invoice("ada", 100))
        repo.add(Invoice("grace", 9))
        assert pythonic.total_owed(repo, "ada") == 100

    def test_unknown_customer_owes_nothing(self) -> None:
        assert pythonic.total_owed(pythonic.InMemoryInvoices(), "nobody") == 0


class TestRealWorld:
    def test_same_domain_function_over_sqlite(self) -> None:
        repo = real_world.SqliteInvoices(sqlite3.connect(":memory:"))
        repo.add(Invoice("ada", 100))
        repo.add(Invoice("ada", 50))
        assert pythonic.total_owed(repo, "ada") == 150

    def test_the_two_repos_are_interchangeable(self) -> None:
        for repo in (
            pythonic.InMemoryInvoices(),
            real_world.SqliteInvoices(sqlite3.connect(":memory:")),
        ):
            repo.add(Invoice("x", 7))
            assert pythonic.total_owed(repo, "x") == 7
