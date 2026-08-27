"""The decorator-filled registry: defining a handler registers it.

New formats are new functions -- possibly in other modules -- and the
dispatcher never changes again.
"""

from __future__ import annotations

from collections.abc import Callable

Exporter = Callable[[list[dict[str, str]]], str]

EXPORTERS: dict[str, Exporter] = {}


def register(name: str) -> Callable[[Exporter], Exporter]:
    def decorator(func: Exporter) -> Exporter:
        EXPORTERS[name] = func
        return func

    return decorator


@register("csv")
def to_csv(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    header = ",".join(rows[0])
    body = "\n".join(",".join(row.values()) for row in rows)
    return f"{header}\n{body}"


@register("keyvalue")
def to_keyvalue(rows: list[dict[str, str]]) -> str:
    return "\n".join(f"{k}={v}" for row in rows for k, v in row.items())


def export(rows: list[dict[str, str]], fmt: str) -> str:
    """Dispatch is a lookup; the unknown-key policy lives here, once."""
    try:
        exporter = EXPORTERS[fmt]
    except KeyError:
        known = ", ".join(sorted(EXPORTERS))
        raise ValueError(f"unknown format {fmt!r} (known: {known})") from None
    return exporter(rows)


def main() -> None:
    rows = [{"name": "ada", "role": "eng"}]
    print(export(rows, "csv"))
    print(export(rows, "keyvalue"))


if __name__ == "__main__":
    main()
