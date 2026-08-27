"""Demo: laziness, denial, and metering over one connection."""

from __future__ import annotations

from patterns.structural.proxy.examples.db_gateway.gateway import (
    WarehouseConnection,
    build_gateway,
)


def main() -> None:
    analyst = build_gateway("warehouse://prod", role="analyst")
    print(f"connections before any query: {WarehouseConnection.instances_connected}")
    rows = analyst.query("SELECT sku, qty FROM stock")
    print(f"first query connected lazily: {WarehouseConnection.instances_connected} -> {rows}")
    try:
        analyst.drop_table("stock")
    except PermissionError as exc:
        print(f"analyst denied: {exc}")
    print(f"metered access counts: {dict(analyst.access_counts)}")


if __name__ == "__main__":
    main()
