"""The mini-project: one expensive connection, three kinds of mediation.

The stack, outside-in: metering observes everything (including denials),
protection guards by role, laziness defers the expensive connect until a
query actually runs. This composition over one subject is what a single
``cached_property`` cannot express -- and the reason the pattern survives.
"""

from __future__ import annotations

from patterns.structural.proxy.pattern import LazyProxy, MeteringProxy, ProtectionProxy

READ_ONLY_ATTRS = frozenset({"query", "connected"})


class WarehouseConnection:
    """The real subject; pretend ``__init__`` dials a distant warehouse."""

    instances_connected = 0

    def __init__(self, dsn: str) -> None:
        type(self).instances_connected += 1
        self.dsn = dsn
        self.connected = True
        self.queries_run: list[str] = []

    def query(self, sql: str) -> list[str]:
        self.queries_run.append(sql)
        return [f"row for {sql!r}"]

    def drop_table(self, name: str) -> str:
        return f"dropped {name}"


def allow_for_role(role: str) -> frozenset[str]:
    """Analyst sees the read-only surface; admin sees everything."""
    return (
        frozenset({"query", "connected", "drop_table", "dsn", "queries_run"})
        if role == "admin"
        else READ_ONLY_ATTRS
    )


def build_gateway(dsn: str, *, role: str) -> MeteringProxy:
    """Stack the three proxies over one lazily-built connection."""
    allowed = allow_for_role(role)
    lazy = LazyProxy(lambda: WarehouseConnection(dsn))
    guarded = ProtectionProxy(lazy, lambda name: name in allowed or name == "is_built")
    return MeteringProxy(guarded)
