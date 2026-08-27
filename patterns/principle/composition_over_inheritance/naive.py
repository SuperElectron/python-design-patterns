"""The subclass explosion, reproduced faithfully.

Two independent axes (filtering, destination) already cost four classes;
each new filter or destination multiplies, not adds.
"""

from __future__ import annotations


class Logger:
    def __init__(self, sink: list[str]) -> None:
        self.sink = sink

    def log(self, message: str) -> None:
        self.sink.append(message)


class FilteredLogger(Logger):
    """Axis 1 bolted on by subclassing."""

    def __init__(self, pattern: str, sink: list[str]) -> None:
        super().__init__(sink)
        self.pattern = pattern

    def log(self, message: str) -> None:
        if self.pattern in message:
            super().log(message)


class UppercaseLogger(Logger):
    """Axis 2 bolted on by subclassing."""

    def log(self, message: str) -> None:
        super().log(message.upper())


class FilteredUppercaseLogger(FilteredLogger):
    """And here is the explosion: one class PER COMBINATION."""

    def log(self, message: str) -> None:
        if self.pattern in message:
            self.sink.append(message.upper())


def main() -> None:
    sink: list[str] = []
    FilteredUppercaseLogger("error", sink).log("error: disk full")
    FilteredUppercaseLogger("error", sink).log("all fine")
    print(sink)


if __name__ == "__main__":
    main()
