"""Composite with duck typing: no abstract base, honest interfaces.

The leaf and the container simply share a method. A ``Protocol`` gives the
type checker the same guarantee the ABC gave, without forcing leaves to
inherit -- or to carry child management they cannot honor.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class Sized(Protocol):
    def total_bytes(self) -> int: ...


@dataclass(frozen=True)
class File:
    """A leaf. It has no add() -- files honestly cannot hold children."""

    name: str
    size: int

    def total_bytes(self) -> int:
        return self.size


@dataclass
class Directory:
    """A composite. Child management lives here, where it belongs."""

    name: str
    entries: list[Sized] = field(default_factory=list)

    def add(self, entry: Sized) -> None:
        self.entries.append(entry)

    def total_bytes(self) -> int:
        return sum(entry.total_bytes() for entry in self.entries)


def main() -> None:
    root = Directory("root")
    root.add(File("a.txt", 100))
    sub = Directory("sub")
    sub.add(File("b.bin", 400))
    root.add(sub)
    print(f"total: {root.total_bytes()} bytes")


if __name__ == "__main__":
    main()
