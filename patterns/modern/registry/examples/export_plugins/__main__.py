"""Demo: one dataset through every registered exporter."""

from __future__ import annotations

from patterns.modern.registry.examples.export_plugins import EXPORTERS, export
from patterns.modern.registry.pattern import UnknownKeyError


def main() -> None:
    rows = [
        {"name": "ada", "role": "eng"},
        {"name": "grace", "role": "ops"},
    ]
    for fmt in EXPORTERS.names():
        print(f"--- {fmt} ---")
        print(export(rows, fmt))
    try:
        export(rows, "xml")
    except UnknownKeyError as exc:
        print(f"--- unknown format ---\n{exc}")


if __name__ == "__main__":
    main()
