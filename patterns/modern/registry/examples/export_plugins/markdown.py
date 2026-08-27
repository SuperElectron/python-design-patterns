"""A plugin in its own module — the import-time caveat, made concrete.

Nothing imports this module for its names; it is imported (by the package
``__init__``) purely so the ``@EXPORTERS.register`` below runs. Comment out
that import and ``"markdown"`` vanishes from the registry without any other
code changing — which is exactly why real plugin systems pair registries
with entry points or explicit plugin loading.
"""

from __future__ import annotations

from patterns.modern.registry.examples.export_plugins.exporters import EXPORTERS, Rows


@EXPORTERS.register("markdown")
def to_markdown(rows: Rows) -> str:
    if not rows:
        return ""
    headers = list(rows[0])
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines += ["| " + " | ".join(row[h] for h in headers) + " |" for row in rows]
    return "\n".join(lines)
