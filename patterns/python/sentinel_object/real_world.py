"""Sentinels in the stdlib.

``dataclasses.MISSING`` separates "no default" from "default is None";
two-argument ``iter(callable, sentinel)`` stops when the sentinel appears.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field, fields


@dataclass
class Config:
    name: str
    retries: int | None = None
    tags: list[str] = field(default_factory=list)


def has_default(field_name: str) -> bool:
    """MISSING lets introspection distinguish no-default from None-default."""
    for f in fields(Config):
        if f.name == field_name:
            return (
                f.default is not dataclasses.MISSING or f.default_factory is not dataclasses.MISSING
            )
    raise KeyError(field_name)


def read_until_blank(chunks: list[str]) -> list[str]:
    """iter(callable, sentinel): the empty string terminates the stream."""
    supply = iter(chunks).__next__
    return list(iter(supply, ""))


def main() -> None:
    print(f"'name' has default:    {has_default('name')}")
    print(f"'retries' has default: {has_default('retries')}")
    print(f"read until blank:      {read_until_blank(['a', 'b', '', 'c'])}")


if __name__ == "__main__":
    main()
