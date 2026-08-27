"""``contextlib.ExitStack``: a dynamic pile of context managers.

Open N resources decided at runtime; the stack unwinds them all, in
reverse, on any exit.
"""

from __future__ import annotations

import tempfile
from contextlib import ExitStack
from pathlib import Path


def concatenate(paths: list[Path]) -> str:
    """Open however many files there are; every handle closes on exit."""
    with ExitStack() as stack:
        handles = [stack.enter_context(p.open()) for p in paths]
        return "".join(h.read() for h in handles)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:  # itself a context manager
        paths = []
        for i, text in enumerate(["one ", "two ", "three"]):
            path = Path(tmp) / f"{i}.txt"
            path.write_text(text)
            paths.append(path)
        print(concatenate(paths))


if __name__ == "__main__":
    main()
