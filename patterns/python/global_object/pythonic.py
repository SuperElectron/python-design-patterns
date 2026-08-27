"""The Global Object pattern done well.

Constants, cheap deterministic import-time computation, and lazy
initialization for anything expensive. Importing this module does no I/O
and mutates nothing observable.
"""

from __future__ import annotations

import re

#: The Constant Pattern: immutable, named, computed once.
MONTHS_PER_YEAR = 12
VOWELS = frozenset("aeiou")

#: Import-time computation is fine when it is cheap and pure:
#: a compiled regex is the guide's own example of a good global object.
IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def count_vowels(text: str) -> int:
    return sum(1 for ch in text if ch in VOWELS)


# Lazy initialization: pay for expensive construction on first use, not import.
_big_table: dict[int, int] | None = None


def big_table() -> dict[int, int]:
    global _big_table
    if _big_table is None:
        _big_table = {n: n * n for n in range(10_000)}
    return _big_table


def main() -> None:
    print(f"constant:        {MONTHS_PER_YEAR}")
    print(f"regex global:    {bool(IDENTIFIER.fullmatch('valid_name'))}")
    print(f"vowels in text:  {count_vowels('global object')}")
    print(f"lazy table size: {len(big_table())}")


if __name__ == "__main__":
    main()
