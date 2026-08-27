"""The Gang of Four Singleton, translated literally.

The class intercepts construction in ``__new__`` and caches the sole instance.
Note the wart this forces in Python: ``__init__`` runs on *every* call, so it
must guard against re-initialization itself.
"""

from __future__ import annotations

from typing import ClassVar, Self


class Logger:
    """A classic GoF singleton: every construction returns the same instance."""

    _instance: ClassVar[Self | None] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Without this guard, a second Logger() call would wipe the log.
        if not hasattr(self, "lines"):
            self.lines: list[str] = []

    def log(self, message: str) -> None:
        self.lines.append(message)


def main() -> None:
    a = Logger()
    b = Logger()
    a.log("first")
    b.log("second")
    print(f"a is b: {a is b}")
    print(f"log seen by both: {a.lines}")


if __name__ == "__main__":
    main()
