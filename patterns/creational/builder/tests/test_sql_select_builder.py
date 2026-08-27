"""Behavioral tests for the sql_select_builder mini-project — real sqlite rows."""

from __future__ import annotations

from patterns.creational.builder.examples.sql_select_builder import (
    big_orders,
    orders_in_region,
    seed_orders,
    top_orders,
)


class TestReports:
    def test_top_orders_come_largest_first(self) -> None:
        conn = seed_orders()
        assert top_orders(conn, 3) == [("A-4", 3100), ("A-1", 1200), ("A-5", 950)]

    def test_big_orders_filters_by_threshold(self) -> None:
        conn = seed_orders()
        rows = big_orders(conn, 900)
        assert [row[0] for row in rows] == ["A-1", "A-4", "A-5"]
        assert all(isinstance(row[2], int) and row[2] >= 900 for row in rows)

    def test_region_report_narrows_conditionally(self) -> None:
        conn = seed_orders()
        west_all = orders_in_region(conn, "west")
        west_widgets = orders_in_region(conn, "west", "widgets")
        assert [row[0] for row in west_all] == ["A-1", "A-3"]
        assert west_widgets == west_all  # west only has widgets...
        assert orders_in_region(conn, "east", "gears") == [("A-2", "gears", 450)]

    def test_no_rows_is_an_empty_list_not_an_error(self) -> None:
        conn = seed_orders()
        assert orders_in_region(conn, "south") == []
