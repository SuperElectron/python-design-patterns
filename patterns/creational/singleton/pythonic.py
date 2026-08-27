"""What to write instead: the Global Object pattern.

A module is itself a singleton -- created once, cached in ``sys.modules``.
So the pythonic "Singleton" is a perfectly ordinary class instantiated once
at module level. Callers ``import`` the instance instead of constructing it.

For construction that is expensive or needs configuration first, hide the
instance behind a small accessor function instead (shown below).
"""

from __future__ import annotations


class Logger:
    """An ordinary class -- nothing about it knows it will be shared."""

    def __init__(self) -> None:
        self.lines: list[str] = []

    def log(self, message: str) -> None:
        self.lines.append(message)


#: The Global Object: built once, at import time. This is the whole pattern.
logger = Logger()


# Lazy variant, for when construction must wait until first use:
_lazy_instance: Logger | None = None


def get_logger() -> Logger:
    """Build the shared instance on first call, then keep handing it back.

    Not thread-safe: two threads racing the first call can each build a
    Logger (one wins the slot). Harmless for a cheap object; guard with a
    threading.Lock if construction has side effects.
    """
    global _lazy_instance
    if _lazy_instance is None:
        _lazy_instance = Logger()
    return _lazy_instance


def main() -> None:
    logger.log("hello")
    print(f"module global is shared: {logger.lines}")
    print(f"lazy accessor is stable: {get_logger() is get_logger()}")


if __name__ == "__main__":
    main()
