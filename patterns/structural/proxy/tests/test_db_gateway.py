"""Behavioral tests for the db_gateway mini-project."""

from __future__ import annotations

import pytest

from patterns.structural.proxy.examples.db_gateway import (
    WarehouseConnection,
    build_gateway,
)


@pytest.fixture(autouse=True)
def reset_connection_counter() -> None:
    WarehouseConnection.instances_connected = 0


def test_no_connection_until_the_first_query() -> None:
    gateway = build_gateway("warehouse://prod", role="analyst")
    assert WarehouseConnection.instances_connected == 0
    rows = gateway.query("SELECT 1")
    assert WarehouseConnection.instances_connected == 1
    assert rows == ["row for 'SELECT 1'"]


def test_denied_role_never_touches_the_subject() -> None:
    gateway = build_gateway("warehouse://prod", role="analyst")
    with pytest.raises(PermissionError):
        gateway.drop_table("stock")
    # The denial fired before the lazy layer: nothing ever connected.
    assert WarehouseConnection.instances_connected == 0


def test_admin_role_reaches_the_full_surface() -> None:
    gateway = build_gateway("warehouse://prod", role="admin")
    assert gateway.drop_table("stock") == "dropped stock"


def test_metering_counts_all_traffic_including_denials() -> None:
    gateway = build_gateway("warehouse://prod", role="analyst")
    gateway.query("SELECT 1")
    gateway.query("SELECT 2")
    with pytest.raises(PermissionError):
        gateway.drop_table("stock")
    assert gateway.access_counts == {"query": 2, "drop_table": 1}


def test_analyst_can_read_connected_but_not_dsn() -> None:
    gateway = build_gateway("warehouse://prod", role="analyst")
    gateway.query("SELECT 1")  # force the connection into existence
    assert gateway.connected is True
    with pytest.raises(PermissionError):
        gateway.dsn  # noqa: B018 — the access itself is the assertion


def test_admin_reads_dsn_and_query_log() -> None:
    gateway = build_gateway("warehouse://prod", role="admin")
    gateway.query("SELECT 1")
    assert gateway.dsn == "warehouse://prod"
    assert gateway.queries_run == ["SELECT 1"]


def test_is_built_passes_through_the_stack() -> None:
    gateway = build_gateway("warehouse://prod", role="analyst")
    assert gateway.is_built is False
    gateway.query("SELECT 1")
    assert gateway.is_built is True
