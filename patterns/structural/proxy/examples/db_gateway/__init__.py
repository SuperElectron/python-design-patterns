"""An expensive warehouse connection behind stacked proxies.

Run it: ``uv run python -m patterns.structural.proxy.examples.db_gateway``
"""

from patterns.structural.proxy.examples.db_gateway.gateway import (
    WarehouseConnection,
    build_gateway,
)

__all__ = ["WarehouseConnection", "build_gateway"]
