"""Cleanup by hand: try/finally on every exit path.

Correct -- and it must be re-written correctly at every call site.
The nested version shows why the discipline doesn't scale.
"""

from __future__ import annotations


class Resource:
    def __init__(self, name: str, log: list[str]) -> None:
        self.name = name
        self.log = log
        self.log.append(f"open {name}")

    def close(self) -> None:
        self.log.append(f"close {self.name}")


def use_one(log: list[str], *, explode: bool = False) -> None:
    resource = Resource("a", log)
    try:
        log.append("work")
        if explode:
            raise RuntimeError("boom")
    finally:
        resource.close()


def use_two(log: list[str]) -> None:
    first = Resource("a", log)
    try:
        second = Resource("b", log)  # every extra resource nests another level
        try:
            log.append("work")
        finally:
            second.close()
    finally:
        first.close()


def main() -> None:
    import contextlib

    log: list[str] = []
    with contextlib.suppress(RuntimeError):  # itself a context manager!
        use_one(log, explode=True)
    print(f"cleanup survived the exception: {log}")
    log.clear()
    use_two(log)
    print(f"nested by hand: {log}")


if __name__ == "__main__":
    main()
