"""The Gang of Four virtual proxy, translated literally.

The proxy shares the subject's interface and defers the expensive
construction until the first real call.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Report(ABC):
    @abstractmethod
    def summary(self) -> str: ...


class ExpensiveReport(Report):
    """The real subject; pretend __init__ crunches a warehouse of data."""

    instances_built = 0

    def __init__(self) -> None:
        type(self).instances_built += 1

    def summary(self) -> str:
        return "42 pages of insight"


class ReportProxy(Report):
    """Same interface; builds the real subject only when first needed."""

    def __init__(self) -> None:
        self._real: ExpensiveReport | None = None

    def summary(self) -> str:
        if self._real is None:
            self._real = ExpensiveReport()
        return self._real.summary()


def main() -> None:
    proxy = ReportProxy()
    print(f"built after construction: {ExpensiveReport.instances_built}")
    print(proxy.summary())
    print(f"built after first use:    {ExpensiveReport.instances_built}")


if __name__ == "__main__":
    main()
