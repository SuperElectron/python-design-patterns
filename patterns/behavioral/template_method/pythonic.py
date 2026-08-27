"""The skeleton as a function, the steps as callable parameters."""

from __future__ import annotations

from collections.abc import Callable


def plain_rows(data: dict[str, int]) -> str:
    return "\n".join(f"{key}: {value}" for key, value in data.items())


def csv_rows(data: dict[str, int]) -> str:
    return "\n".join(f"{key},{value}" for key, value in data.items())


def render(
    data: dict[str, int],
    *,
    header: str = "REPORT",
    format_rows: Callable[[dict[str, int]], str] = plain_rows,
) -> str:
    """The whole template method: skeleton fixed, steps injected."""
    return f"{header}\n{format_rows(data)}"


def main() -> None:
    data = {"apples": 3, "pears": 5}
    print(render(data))
    print(render(data, header="key,value", format_rows=csv_rows))


if __name__ == "__main__":
    main()
