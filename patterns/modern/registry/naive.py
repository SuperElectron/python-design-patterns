"""Dispatch as an if/elif ladder: every new format edits this function."""

from __future__ import annotations


def export(rows: list[dict[str, str]], fmt: str) -> str:
    if fmt == "csv":
        if not rows:
            return ""
        header = ",".join(rows[0])
        body = "\n".join(",".join(row.values()) for row in rows)
        return f"{header}\n{body}"
    elif fmt == "keyvalue":
        return "\n".join(f"{k}={v}" for row in rows for k, v in row.items())
    else:
        raise ValueError(f"unknown format: {fmt}")


def main() -> None:
    rows = [{"name": "ada", "role": "eng"}]
    print(export(rows, "csv"))
    print(export(rows, "keyvalue"))


if __name__ == "__main__":
    main()
