"""The two classic misuses of module globals.

1. Hidden mutable state: every caller of ``tally`` is coupled to every other.
2. Import-time I/O (simulated): importing becomes slow, order-dependent, and
   untestable. Real code that does ``open()``/network at module level fails
   in exactly the ways this pretends to.
"""

from __future__ import annotations

# Misuse 1: a mutable global that functions quietly share.
_counts: dict[str, int] = {}


def tally(word: str) -> int:
    """Two callers who have never met now share state through _counts."""
    _counts[word] = _counts.get(word, 0) + 1
    return _counts[word]


# Misuse 2: work at import time. Here it is only a computation standing in
# for the real sin (reading files, opening sockets) -- but note that it runs
# before any caller has asked for anything.
IMPORT_TIME_WORK: list[int] = [n * n for n in range(1000)]


def main() -> None:
    print(f"tally('a') twice: {tally('a')}, {tally('a')}")
    print(f"import already paid for {len(IMPORT_TIME_WORK)} squares nobody asked for")


if __name__ == "__main__":
    main()
