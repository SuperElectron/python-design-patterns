"""Behavioral tests for the SelectBuilder / Query building block."""

from __future__ import annotations

import dataclasses

import pytest

from patterns.creational.builder import Query, SelectBuilder


class TestAssembly:
    def test_minimal_query_defaults_to_star(self) -> None:
        query = SelectBuilder("orders").build()
        assert query.sql() == "SELECT * FROM orders"
        assert query.params == ()

    def test_full_query_renders_clauses_in_sql_order(self) -> None:
        query = (
            SelectBuilder("orders")
            .columns("id", "amount")
            .where("region = ?", "west")
            .where("amount >= ?", 100)
            .order_by("amount DESC")
            .limit(5)
            .build()
        )
        assert query.sql() == (
            "SELECT id, amount FROM orders "
            "WHERE region = ? AND amount >= ? "
            "ORDER BY amount DESC LIMIT 5"
        )
        assert query.params == ("west", 100)

    def test_steps_work_as_statements_for_conditional_assembly(self) -> None:
        builder = SelectBuilder("orders")
        builder.where("region = ?", "east")
        query = builder.build()
        assert "WHERE region = ?" in query.sql()


class TestStagedValidation:
    def test_empty_table_rejected_at_start(self) -> None:
        with pytest.raises(ValueError, match="needs a table"):
            SelectBuilder("")

    def test_placeholder_count_mismatch_fails_at_the_faulty_step(self) -> None:
        with pytest.raises(ValueError, match="1 placeholder"):
            SelectBuilder("orders").where("region = ?")

    def test_non_positive_limit_rejected(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            SelectBuilder("orders").limit(0)


class TestProductImmutability:
    def test_product_is_frozen(self) -> None:
        query = SelectBuilder("orders").build()
        with pytest.raises(dataclasses.FrozenInstanceError):
            query.table = "other"  # type: ignore[misc]

    def test_mutating_the_builder_after_build_leaves_products_alone(self) -> None:
        builder = SelectBuilder("orders").columns("id")
        first = builder.build()
        builder.where("amount >= ?", 100).limit(1)
        second = builder.build()
        assert first.sql() == "SELECT id FROM orders"  # untouched
        assert first != second
        assert isinstance(second, Query)
