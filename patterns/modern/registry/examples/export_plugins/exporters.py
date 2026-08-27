"""The registry, the built-in exporters, and the one dispatch function."""

from __future__ import annotations

import json
from collections.abc import Callable

from patterns.modern.registry.pattern import Registry

Rows = list[dict[str, str]]
Exporter = Callable[[Rows], str]

EXPORTERS: Registry[Exporter] = Registry(kind="format")


@EXPORTERS.register("csv")
def to_csv(rows: Rows) -> str:
    if not rows:
        return ""
    header = ",".join(rows[0])
    body = "\n".join(",".join(row.values()) for row in rows)
    return f"{header}\n{body}"


@EXPORTERS.register("json")
def to_json(rows: Rows) -> str:
    return json.dumps(rows, indent=2)


def export(rows: Rows, fmt: str) -> str:
    """Dispatch is a lookup; the unknown-format policy lives in the registry, once."""
    return EXPORTERS.get(fmt)(rows)
