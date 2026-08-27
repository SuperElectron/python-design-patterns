"""Generators as protocol scanners: frame suspension holds the state.

A scanner for BEGIN/END blocks -- no state flag anywhere; being inside the
``while`` loop IS the "in a block" state.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator


def blocks(lines: Iterable[str]) -> Iterator[list[str]]:
    """Yield the lines between each BEGIN/END pair."""
    it = iter(lines)
    for line in it:
        if line == "BEGIN":
            collected: list[str] = []
            for inner in it:  # <- the machine is now in the "collecting" state
                if inner == "END":
                    break
                collected.append(inner)
            yield collected


def main() -> None:
    text = ["noise", "BEGIN", "a", "b", "END", "more noise", "BEGIN", "c", "END"]
    print(list(blocks(text)))


if __name__ == "__main__":
    main()
